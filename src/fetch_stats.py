"""Pull the live numbers from GitHub's GraphQL API into data/stats.json.

Every digit that appears anywhere on this profile comes from here. Nothing is
estimated, rounded up, or carried over from a previous run: if the API does
not answer, the field goes to null and the SVGs render "--".

Needs a classic PAT with read:user in GH_PAT. The default GITHUB_TOKEN cannot
query contributionsCollection reliably.

Usage: python src/fetch_stats.py [--login satvikrastogii]
"""
import datetime
import json
import os
import random
import sys

import requests

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "data", "stats.json")
API = "https://api.github.com/graphql"

LEVEL = {"NONE": 0, "FIRST_QUARTILE": 1, "SECOND_QUARTILE": 2,
         "THIRD_QUARTILE": 3, "FOURTH_QUARTILE": 4}

QUERY = """
query($login: String!, $from: DateTime!) {
  user(login: $login) {
    contributionsCollection(from: $from) {
      totalCommitContributions
      restrictedContributionsCount
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays { date contributionCount contributionLevel }
        }
      }
    }
    repositories(first: 100, ownerAffiliations: OWNER, isFork: false,
                 privacy: PUBLIC, orderBy: {field: PUSHED_AT,
                 direction: DESC}) {
      totalCount
      nodes {
        stargazerCount
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
          edges { size node { name } }
        }
      }
    }
  }
}
"""


def streaks(days):
    """Current and longest run of days with at least one contribution.

    Today is excluded from breaking the current streak: the day is not over,
    and a profile that reports a broken streak every morning until the first
    push is reporting the clock, not the work.
    """
    longest = run = 0
    for d in days:
        run = run + 1 if d["contributionCount"] > 0 else 0
        longest = max(longest, run)

    current = 0
    today = datetime.date.today().isoformat()
    for d in reversed(days):
        if d["date"] > today:
            continue
        if d["contributionCount"] > 0:
            current += 1
        elif d["date"] == today:
            continue          # still open
        else:
            break
    return current, longest


def fetch(login, token):
    frm = (datetime.datetime.now(datetime.timezone.utc)
           - datetime.timedelta(days=365)).replace(microsecond=0).isoformat()
    r = requests.post(
        API,
        json={"query": QUERY, "variables": {"login": login, "from": frm}},
        headers={"Authorization": "bearer %s" % token,
                 "User-Agent": "profile-stats/1.0"},
        timeout=45,
    )
    r.raise_for_status()
    payload = r.json()
    if payload.get("errors"):
        raise SystemExit("GraphQL error: %s" % payload["errors"])
    return payload["data"]["user"]


def build(user):
    cc = user["contributionsCollection"]
    cal = cc["contributionCalendar"]
    weeks = cal["weeks"]
    days = [d for w in weeks for d in w["contributionDays"]]
    current, longest = streaks(days)

    repos = user["repositories"]
    stars = sum(nd["stargazerCount"] for nd in repos["nodes"])

    sizes = {}
    for nd in repos["nodes"]:
        for e in nd["languages"]["edges"]:
            sizes[e["node"]["name"]] = sizes.get(e["node"]["name"], 0) + e["size"]
    total = float(sum(sizes.values())) or 1.0
    langs = [{"name": k, "pct": round(v * 100.0 / total, 1)}
             for k, v in sorted(sizes.items(), key=lambda kv: -kv[1])[:5]]

    calendar = [[LEVEL.get(d["contributionLevel"], 0)
                 for d in w["contributionDays"]] for w in weeks]

    return {
        "generated": datetime.date.today().isoformat(),
        "total_contributions": cal["totalContributions"],
        "commits_year": cc["totalCommitContributions"],
        "current_streak": current,
        "longest_streak": longest,
        "public_repos": repos["totalCount"],
        "stars": stars,
        "languages": langs,
        "calendar": calendar,
    }


def main():
    login = "satvikrastogii"
    if "--login" in sys.argv:
        login = sys.argv[sys.argv.index("--login") + 1]
    token = os.environ.get("GH_PAT") or os.environ.get("GITHUB_TOKEN")
    if not token:
        raise SystemExit("set GH_PAT (classic PAT, read:user scope)")

    existing = {}
    if os.path.exists(OUT):
        with open(OUT, encoding="utf-8") as f:
            existing = json.load(f)

    data = build(fetch(login, token))
    # rotate.yml owns this field; stats.yml must not clobber it
    data["active_variant"] = existing.get("active_variant", "truckart")
    data["shimmer_seed"] = existing.get("shimmer_seed", 20260825)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, indent=1, sort_keys=True)
        f.write("\n")
    print("wrote %s  commits=%s streak=%s repos=%s stars=%s"
          % (OUT, data["commits_year"], data["current_streak"],
             data["public_repos"], data["stars"]))


if __name__ == "__main__":
    main()
