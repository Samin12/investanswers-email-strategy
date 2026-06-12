#!/usr/bin/env python3
"""Build and deploy the portfolio dashboard to here.now.

This wrapper keeps the dashboard update one-command for scheduled portfolio checks.
It intentionally delegates the actual here.now publish/auth flow to the Hermes skill
helper, so API keys stay outside this repository.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
LATEST_URL = ROOT / "state" / "portfolio_manager" / "dashboard_latest_url.txt"
BUILD_SCRIPT = ROOT / "scripts" / "build_portfolio_dashboard.py"
PUBLISH_SCRIPT = Path.home() / ".hermes" / "skills" / "devops" / "here-now-deploy" / "scripts" / "publish_here_now.py"


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=str(ROOT), text=True, capture_output=True, timeout=300)


def last_json(stdout: str) -> dict:
    # Helper scripts print one JSON object. Keep this tolerant in case logs appear.
    starts = [i for i, ch in enumerate(stdout) if ch == "{"]
    for i in reversed(starts):
        try:
            return json.loads(stdout[i:])
        except json.JSONDecodeError:
            continue
    raise RuntimeError(f"Could not parse JSON from publish output: {stdout[:500]}")


def main() -> int:
    if not PUBLISH_SCRIPT.exists():
        raise SystemExit(f"Missing here.now publish helper: {PUBLISH_SCRIPT}")
    build = run([sys.executable, str(BUILD_SCRIPT)])
    if build.returncode != 0:
        print(build.stdout, end="")
        print(build.stderr, file=sys.stderr, end="")
        return build.returncode
    publish = run([
        sys.executable,
        str(PUBLISH_SCRIPT),
        str(PUBLIC),
        "InvestAnswers Portfolio PM Dashboard",
        "Real Alpaca paper positions, performance, watch levels, and trade log",
    ])
    if publish.returncode != 0:
        print(build.stdout, end="")
        print(publish.stdout, end="")
        print(publish.stderr, file=sys.stderr, end="")
        return publish.returncode
    result = last_json(publish.stdout)
    site_url = result.get("siteUrl")
    if not site_url:
        raise SystemExit(f"Publish succeeded but no siteUrl returned: {result}")
    LATEST_URL.parent.mkdir(parents=True, exist_ok=True)
    LATEST_URL.write_text(site_url.rstrip("/") + "/\n")
    summary = {
        "ok": True,
        "siteUrl": site_url.rstrip("/") + "/",
        "verified": result.get("verified"),
        "files": result.get("files"),
        "latest_url_file": str(LATEST_URL),
        "build": last_json(build.stdout),
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
