#!/usr/bin/env python3
"""Export InvestAnswers Patreon/Gmail emails into this local git repo.

Requires: `gws` authenticated with Gmail scope.
Does not store credentials. It shells out to gws and saves only message corpus data.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import html
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from email import policy
from email.header import decode_header, make_header
from email.parser import BytesParser
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

REPO = Path(__file__).resolve().parents[1]
RAW_DIR = REPO / "emails" / "raw_eml"
TEXT_DIR = REPO / "emails" / "text_md"
META_DIR = REPO / "emails" / "metadata"
STATE_DIR = REPO / "state"
DEFAULT_QUERY = "from:investanswers@creator.patreon.com"


def run_gws(resource: str, action: str, params: Dict[str, Any], *, retries: int = 3) -> Dict[str, Any]:
    cmd = [
        "gws",
        "gmail",
        *resource.split(),
        action,
        "--params",
        json.dumps(params, separators=(",", ":")),
        "--format",
        "json",
    ]
    last = None
    for attempt in range(1, retries + 1):
        proc = subprocess.run(cmd, text=True, capture_output=True)
        if proc.returncode == 0:
            try:
                return json.loads(proc.stdout)
            except json.JSONDecodeError as exc:
                raise RuntimeError(f"gws returned non-json output for {resource} {action}: {proc.stdout[:500]}") from exc
        last = (proc.returncode, proc.stdout, proc.stderr)
        time.sleep(min(2 * attempt, 8))
    code, out, err = last or (999, "", "unknown")
    raise RuntimeError(f"gws failed after {retries} attempts: exit={code}\nSTDOUT={out[:1000]}\nSTDERR={err[:1000]}")


def list_message_ids(query: str, max_results: int = 500, include_spam_trash: bool = False) -> List[Dict[str, str]]:
    messages: List[Dict[str, str]] = []
    page_token: Optional[str] = None
    seen = set()
    while True:
        params: Dict[str, Any] = {
            "userId": "me",
            "q": query,
            "maxResults": min(max_results, 500),
            "includeSpamTrash": include_spam_trash,
        }
        if page_token:
            params["pageToken"] = page_token
        data = run_gws("users messages", "list", params)
        for item in data.get("messages", []) or []:
            mid = item.get("id")
            if mid and mid not in seen:
                seen.add(mid)
                messages.append({"messageId": mid, "threadId": item.get("threadId", "")})
        page_token = data.get("nextPageToken")
        if not page_token:
            break
    return messages


def b64url_decode(raw: str) -> bytes:
    raw = raw.replace("-", "+").replace("_", "/")
    raw += "=" * ((4 - len(raw) % 4) % 4)
    return base64.b64decode(raw)


def safe_header(value: Optional[str]) -> str:
    if not value:
        return ""
    try:
        return str(make_header(decode_header(value)))
    except Exception:
        return str(value)


def strip_html(raw_html: str) -> str:
    text = re.sub(r"(?is)<(script|style).*?</\1>", " ", raw_html or "")
    text = re.sub(r"(?i)<br\s*/?>", "\n", text)
    text = re.sub(r"(?i)</p\s*>", "\n\n", text)
    text = re.sub(r"(?s)<[^>]+>", " ", text)
    text = html.unescape(text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_text(msg) -> str:
    text_parts: List[str] = []
    html_parts: List[str] = []
    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            disp = (part.get("Content-Disposition") or "").lower()
            if "attachment" in disp:
                continue
            try:
                content = part.get_content()
            except Exception:
                payload = part.get_payload(decode=True) or b""
                content = payload.decode(part.get_content_charset() or "utf-8", "replace")
            if ctype == "text/plain":
                text_parts.append(content)
            elif ctype == "text/html":
                html_parts.append(content)
    else:
        ctype = msg.get_content_type()
        try:
            content = msg.get_content()
        except Exception:
            payload = msg.get_payload(decode=True) or b""
            content = payload.decode(msg.get_content_charset() or "utf-8", "replace")
        if ctype == "text/html":
            html_parts.append(content)
        else:
            text_parts.append(content)

    text = "\n\n".join(p.strip() for p in text_parts if p and p.strip())
    if not text and html_parts:
        text = "\n\n".join(strip_html(p) for p in html_parts if p)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def slugify(value: str, max_len: int = 70) -> str:
    value = re.sub(r"[^a-zA-Z0-9._ -]+", "", value or "").strip().replace(" ", "-")
    value = re.sub(r"-+", "-", value)
    return (value[:max_len] or "email").strip("-._")


def header_map(msg) -> Dict[str, str]:
    out: Dict[str, str] = {}
    for key in ["Subject", "From", "To", "Cc", "Date", "Message-ID", "List-Unsubscribe"]:
        out[key] = safe_header(msg.get(key))
    return out


def parse_date(date_header: str) -> tuple[str, str]:
    try:
        dt = parsedate_to_datetime(date_header)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.isoformat(), dt.strftime("%Y-%m-%d_%H%M%S")
    except Exception:
        return "", "unknown-date"


def attachment_summaries(msg) -> List[Dict[str, Any]]:
    items = []
    for part in msg.walk() if msg.is_multipart() else []:
        disp = (part.get("Content-Disposition") or "").lower()
        filename = part.get_filename()
        if "attachment" not in disp and not filename:
            continue
        payload = part.get_payload(decode=True) or b""
        items.append({
            "filename": safe_header(filename),
            "content_type": part.get_content_type(),
            "bytes": len(payload),
            "sha1": hashlib.sha1(payload).hexdigest() if payload else "",
        })
    return items


def export_one(item: Dict[str, str], *, overwrite: bool = False) -> Dict[str, Any]:
    mid = item["messageId"]
    short_hash = hashlib.sha1(mid.encode()).hexdigest()[:8]
    existing = list(META_DIR.glob(f"*_{mid}_{short_hash}.json"))
    if existing and not overwrite:
        meta = json.loads(existing[0].read_text())
        return {"ok": True, "skipped": True, "messageId": mid, "subject": meta.get("subject", "")}

    data = run_gws("users messages", "get", {"userId": "me", "id": mid, "format": "raw"})
    raw_encoded = data.get("raw")
    if not raw_encoded:
        raise RuntimeError(f"raw payload missing for {mid}")
    raw = b64url_decode(raw_encoded)
    msg = BytesParser(policy=policy.default).parsebytes(raw)
    headers = header_map(msg)
    subject = headers.get("Subject", "")
    date_iso, date_slug = parse_date(headers.get("Date", ""))
    text = extract_text(msg)
    base = f"{date_slug}_{slugify(subject)}_{mid}_{short_hash}"

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    TEXT_DIR.mkdir(parents=True, exist_ok=True)
    META_DIR.mkdir(parents=True, exist_ok=True)

    raw_path = RAW_DIR / f"{base}.eml"
    text_path = TEXT_DIR / f"{base}.md"
    meta_path = META_DIR / f"{base}.json"

    raw_path.write_bytes(raw)
    meta = {
        "messageId": mid,
        "threadId": item.get("threadId") or data.get("threadId", ""),
        "display_url": f"https://mail.google.com/mail/u/0/#inbox/{mid}",
        "subject": subject,
        "from": headers.get("From", ""),
        "to": headers.get("To", ""),
        "cc": headers.get("Cc", ""),
        "date_header": headers.get("Date", ""),
        "date_iso": date_iso,
        "message_id_header": headers.get("Message-ID", ""),
        "labelIds": data.get("labelIds", []),
        "snippet": data.get("snippet", ""),
        "filename_base": base,
        "raw_path": str(raw_path.relative_to(REPO)),
        "text_path": str(text_path.relative_to(REPO)),
        "meta_path": str(meta_path.relative_to(REPO)),
        "text_chars": len(text),
        "raw_bytes": len(raw),
        "sizeEstimate": data.get("sizeEstimate"),
        "attachments": attachment_summaries(msg),
    }
    meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n")
    text_path.write_text(
        f"# {subject}\n\n"
        f"- messageId: `{mid}`\n"
        f"- threadId: `{meta['threadId']}`\n"
        f"- date: {headers.get('Date', '')}\n"
        f"- from: {headers.get('From', '')}\n"
        f"- to: {headers.get('To', '')}\n"
        f"- gmail: {meta['display_url']}\n"
        f"- raw: `{meta['raw_path']}`\n"
        f"- metadata: `{meta['meta_path']}`\n\n"
        f"---\n\n{text or '[no text body extracted]'}\n",
        encoding="utf-8",
    )
    return {"ok": True, "skipped": False, "messageId": mid, "subject": subject, "date_iso": date_iso, "text_chars": len(text)}


def load_metadata() -> List[Dict[str, Any]]:
    metas = []
    for path in META_DIR.glob("*.json"):
        try:
            metas.append(json.loads(path.read_text()))
        except Exception as exc:
            print(f"WARN failed to read metadata {path}: {exc}", file=sys.stderr)
    metas.sort(key=lambda m: m.get("date_iso") or "")
    return metas


def write_manifests(query: str, ids: List[Dict[str, str]]) -> None:
    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    (REPO / "message_ids.json").write_text(json.dumps({
        "source": "investanswers@creator.patreon.com",
        "query": query,
        "count": len(ids),
        "generated_at": generated_at,
        "messages": ids,
    }, indent=2, ensure_ascii=False) + "\n")
    metas = load_metadata()
    (REPO / "manifest.json").write_text(json.dumps({
        "source": "investanswers@creator.patreon.com",
        "query": query,
        "count": len(metas),
        "message_id_count": len(ids),
        "generated_at": generated_at,
        "emails": metas,
    }, indent=2, ensure_ascii=False) + "\n")
    subjects = [m.get("subject", "") for m in metas]
    by_year: Dict[str, int] = {}
    for m in metas:
        year = (m.get("date_iso") or "unknown")[:4]
        by_year[year] = by_year.get(year, 0) + 1
    (REPO / "analysis" / "corpus_summary.md").write_text(
        "# Corpus Summary\n\n"
        f"Generated: {generated_at}\n\n"
        f"- Query: `{query}`\n"
        f"- Message IDs found: {len(ids)}\n"
        f"- Emails exported: {len(metas)}\n"
        f"- Years: {json.dumps(by_year, sort_keys=True)}\n\n"
        "## Latest 20 subjects\n\n"
        + "\n".join(f"- {s}" for s in list(reversed(subjects))[:20])
        + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", default=DEFAULT_QUERY)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--limit", type=int, default=0, help="Optional max emails to export for testing")
    args = parser.parse_args()

    for d in [RAW_DIR, TEXT_DIR, META_DIR, STATE_DIR, REPO / "analysis", REPO / "cron"]:
        d.mkdir(parents=True, exist_ok=True)

    ids = list_message_ids(args.query)
    if args.limit:
        ids = ids[: args.limit]
    write_manifests(args.query, ids)

    progress_path = STATE_DIR / "export_progress.json"
    progress = {"done": [], "failed": {}}
    if progress_path.exists():
        try:
            progress = json.loads(progress_path.read_text())
        except Exception:
            pass
    done = set(progress.get("done", []))
    failed: Dict[str, str] = progress.get("failed", {}) or {}

    ok = skipped = errors = 0
    start = time.time()
    for i, item in enumerate(ids, 1):
        mid = item["messageId"]
        try:
            result = export_one(item, overwrite=args.overwrite)
            ok += 1
            skipped += 1 if result.get("skipped") else 0
            done.add(mid)
            failed.pop(mid, None)
            if i % 25 == 0 or i == len(ids):
                print(json.dumps({"progress": i, "total": len(ids), "ok": ok, "skipped": skipped, "errors": errors, "last_subject": result.get("subject", "")}, ensure_ascii=False), flush=True)
        except Exception as exc:
            errors += 1
            failed[mid] = str(exc)
            print(json.dumps({"error_message_id": mid, "error": str(exc)[:500]}, ensure_ascii=False), file=sys.stderr, flush=True)
        progress_path.write_text(json.dumps({"done": sorted(done), "failed": failed, "updated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat()}, indent=2, ensure_ascii=False) + "\n")

    write_manifests(args.query, ids)
    summary = {"ids_found": len(ids), "exported_metadata": len(load_metadata()), "ok_or_existing": ok, "skipped_existing": skipped, "errors": errors, "seconds": round(time.time() - start, 2)}
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0 if errors == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
