#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Deploy jimiknightley.com (The First Spell promo site).

The site is served by GitHub Pages straight from the `main` branch, so a
deploy is: stage everything -> commit -> push. Pages rebuilds on its own,
usually within a minute.

Usage:
  python deploy.py                    # stage all, commit, push, wait for Pages
  python deploy.py -m "Fix hero copy" # same, with your own commit message
  python deploy.py --no-wait          # push and return immediately
  python deploy.py --status           # just report Pages build status, deploy nothing
"""

import argparse
import json
import os
import subprocess
import sys
import time
import urllib.request

REPO = "thejimmo/The-first-spell"
SITE_URL = "https://jimiknightley.com/"
BRANCH = "main"
LOCAL_ROOT = os.path.dirname(os.path.abspath(__file__))

GH = os.path.join(os.environ.get("ProgramFiles", r"C:\Program Files"), "GitHub CLI", "gh.exe")


def git(*args, check=True):
    r = subprocess.run(["git"] + list(args), cwd=LOCAL_ROOT,
                       capture_output=True, text=True, encoding="utf-8")
    if check and r.returncode != 0:
        sys.exit(f"git {' '.join(args)} failed:\n{r.stderr.strip()}")
    return r.stdout.strip()


def gh_api(path):
    """Query the GitHub API through the gh CLI (reuses its stored auth)."""
    exe = GH if os.path.exists(GH) else "gh"
    r = subprocess.run([exe, "api", path], capture_output=True, text=True, encoding="utf-8")
    if r.returncode != 0:
        return None
    return json.loads(r.stdout)


def pages_status():
    data = gh_api(f"repos/{REPO}/pages")
    return data.get("status") if data else None


def latest_build_sha():
    data = gh_api(f"repos/{REPO}/pages/builds/latest")
    return (data or {}).get("commit")


def site_http_code():
    req = urllib.request.Request(SITE_URL, method="HEAD",
                                 headers={"User-Agent": "deploy.py"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.status
    except Exception as e:
        return getattr(e, "code", None) or str(e)


def wait_for_pages(sha, timeout=240):
    """Poll until the Pages build for `sha` finishes, or we run out of patience."""
    print("Waiting for the GitHub Pages build...")
    deadline = time.time() + timeout
    while time.time() < deadline:
        time.sleep(10)
        status = pages_status()
        built_sha = latest_build_sha()
        if built_sha == sha and status == "built":
            print(f"Pages built {sha[:7]}.")
            print(f"{SITE_URL} -> {site_http_code()}")
            return True
        if status == "errored":
            print("Pages build ERRORED. See https://github.com/"
                  f"{REPO}/deployments", file=sys.stderr)
            return False
    print(f"Still building after {timeout}s — check "
          f"https://github.com/{REPO}/deployments")
    return False


def main():
    ap = argparse.ArgumentParser(description="Deploy the site to GitHub Pages.")
    ap.add_argument("-m", "--message", help="commit message")
    ap.add_argument("--no-wait", action="store_true",
                    help="don't wait for the Pages build to finish")
    ap.add_argument("--status", action="store_true",
                    help="report Pages status and exit without deploying")
    args = ap.parse_args()

    if args.status:
        print(f"Pages status: {pages_status()}")
        print(f"Last built commit: {(latest_build_sha() or '?')[:7]}")
        print(f"{SITE_URL} -> {site_http_code()}")
        return

    branch = git("rev-parse", "--abbrev-ref", "HEAD")
    if branch != BRANCH:
        sys.exit(f"On branch '{branch}', not '{BRANCH}'. "
                 f"GitHub Pages only serves '{BRANCH}' — merge or switch first.")

    dirty = git("status", "--porcelain")
    unpushed = git("log", "--oneline", f"origin/{BRANCH}..{BRANCH}")

    if not dirty and not unpushed:
        print("Nothing to deploy — working tree clean and up to date with origin.")
        return

    if dirty:
        print("Changes to deploy:")
        for line in dirty.splitlines():
            print(f"  {line}")
        git("add", "-A")
        message = args.message or "Update site"
        git("commit", "-m", message)
        print(f"Committed: {message}")
    else:
        print("Working tree clean; pushing existing local commits:")
        for line in unpushed.splitlines():
            print(f"  {line}")

    git("push", "origin", BRANCH)
    sha = git("rev-parse", "HEAD")
    print(f"Pushed {sha[:7]} to origin/{BRANCH}.")

    if args.no_wait:
        print(f"Pages will rebuild shortly: {SITE_URL}")
        return
    wait_for_pages(sha)


if __name__ == "__main__":
    main()
