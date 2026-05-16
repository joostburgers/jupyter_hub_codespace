#!/usr/bin/env python
"""
Location Review · Progress Report
==================================
Run from the repo root at any time to see your current grade estimate:

    python tests/progress.py

Shows coverage by mention frequency, which tests pass, your current score,
and exactly what to do next to earn more points.
"""

import sys
import os
from pathlib import Path

# Always run relative to repo root
os.chdir(Path(__file__).parent.parent)
sys.path.insert(0, str(Path(__file__).parent))

import pandas as pd
from helpers import (
    detect_school, near, coverage_stats,
    REVIEW_COLS, JMU_CHECKS, JMU_SPECIFIC_PTS, UNIVERSAL_PTS,
)

W = 62   # display width


def _bar(n: int, total: int, width: int = 20) -> str:
    if total == 0:
        return '░' * width
    filled = round(width * n / total)
    return '█' * filled + '░' * (width - filled)


def _hdr(text: str = '') -> str:
    return f"  ── {text} {'─' * max(0, W - 6 - len(text))}"


def _reviewer_stats(df: pd.DataFrame) -> dict:
    """Return {reviewer: unique_location_count} for actioned rows only."""
    actioned = df[df['action'].isin(['KEEP', 'CORRECT', 'REMOVE'])].copy()
    if actioned.empty or 'reviewer' not in actioned.columns:
        return {}
    # One row per unique (place, lat, lon) group; pick first non-empty reviewer
    groups = (
        actioned
        .groupby(['place', 'latitude', 'longitude'], sort=False)['reviewer']
        .apply(lambda s: next((v for v in s if str(v).strip()), ''))
        .reset_index()
    )
    counts = groups['reviewer'].value_counts()
    return counts.to_dict()


def main() -> None:
    print()
    print('╔' + '═' * W + '╗')
    school = detect_school()
    if not school:
        print(f"║  {'⚠️  No school data found in data/{SCHOOL}/':<{W-2}}║")
        print(f"║  {'Make sure data/{SCHOOL}/{SCHOOL}_geoparsed_long.csv exists.':<{W-2}}║")
        print('╚' + '═' * W + '╝')
        return

    title = f"  {school}  ·  Location Review Progress Report"
    print(f"║{title:<{W}}║")
    print('╚' + '═' * W + '╝')
    print()

    long_path  = Path(f"data/{school}/{school}_geoparsed_long.csv")
    clean_path = Path(f"data/{school}/{school}_geoparsed_cleaned.csv")

    if not long_path.exists():
        print(f"  ⚠️  {long_path} not found.")
        return

    df_long  = pd.read_csv(long_path,  dtype=str).fillna('')
    df_clean = pd.read_csv(clean_path, dtype=str).fillna('') if clean_path.exists() else None

    n_rows   = len(df_long)
    n_groups = df_long.groupby(['place', 'latitude', 'longitude'], sort=False).ngroups
    print(f"  School: {school}   ·   {n_rows:,} rows   ·   {n_groups:,} unique locations")
    print()

    # ── Coverage tiers ────────────────────────────────────────────────────────
    print(_hdr('Coverage by mention frequency'))
    tiers = [
        ('cnt ≥ 10', 10, True),
        ('cnt ≥  5',  5, True),
        ('cnt ≥  3',  3, True),
        ('cnt ≥  2',  2, False),
        ('All rows',  1, False),
    ]
    for label, min_cnt, graded in tiers:
        if min_cnt == 1:
            n_act = df_long['action'].isin(['KEEP', 'CORRECT', 'REMOVE']).sum()
            n_tot = n_rows
        else:
            n_act, n_tot = coverage_stats(df_long, min_cnt)
        if n_tot == 0:
            continue
        pct = n_act / n_tot * 100
        b   = _bar(n_act, n_tot)
        if not graded:
            flag = '(optional)'
        elif n_act == n_tot:
            flag = '✅ done'
        else:
            flag = f'⚠️  {n_tot - n_act} left'
        print(f"  {label}  {n_act:>4} /{n_tot:>4}   {b}  {pct:>5.0f}%  {flag}")
    print()

    # ── Reviewer contributions ──────────────────────────────────────────────────
    rev_counts = _reviewer_stats(df_long)
    if rev_counts:
        print(_hdr('Team contributions  (unique locations per reviewer)'))
        total_reviewed = sum(rev_counts.values())
        for reviewer, cnt in sorted(rev_counts.items(), key=lambda x: -x[1]):
            pct = cnt / total_reviewed * 100 if total_reviewed else 0
            b   = _bar(cnt, total_reviewed)
            label = reviewer if reviewer else '(no name entered)'
            print(f"  {label:<20}  {cnt:>4} locations  {b}  {pct:.0f}%")
        print()

    # ── Grade simulation ──────────────────────────────────────────────────────
    print(_hdr('Estimated grade  [AUTOGRADED — see note below]'))
    score     = 0
    max_score = UNIVERSAL_PTS
    tips      = []

    # T1a — cleaned file exists
    if clean_path.exists():
        score += 2
        print(f"  ✅  T1a · Cleaned file exists              2 / 2 pts")
    else:
        print(f"  ❌  T1a · Cleaned file exists              0 / 2 pts")
        tips.append(f"+2 pts  Run Part D and push {school}_geoparsed_cleaned.csv")

    # T1b — no review columns
    if df_clean is not None:
        leftover = REVIEW_COLS & set(df_clean.columns)
        if not leftover:
            score += 1
            print(f"  ✅  T1b · No review columns                1 / 1 pts")
        else:
            print(f"  ❌  T1b · No review columns                0 / 1 pts  "
                  f"({sorted(leftover)} still present)")
            tips.append("+1 pt   Re-run Part D to strip review columns from the cleaned file")
    else:
        print(f"  ❓  T1b · No review columns                ? / 1 pts  (run Part D first)")

    # T1c — numeric coordinates
    if df_clean is not None:
        lat = pd.to_numeric(df_clean['latitude'],  errors='coerce')
        lon = pd.to_numeric(df_clean['longitude'], errors='coerce')
        bad = df_clean[lat.isna() | lon.isna()]
        if bad.empty:
            score += 1
            print(f"  ✅  T1c · Coordinates numeric              1 / 1 pts")
        else:
            print(f"  ❌  T1c · Coordinates numeric              0 / 1 pts  "
                  f"({len(bad)} non-numeric row(s))")
            tips.append(f"+1 pt   Fix {len(bad)} coordinate(s) in the sheet "
                        "(missing comma in corrected_latlon?)")
    else:
        print(f"  ❓  T1c · Coordinates numeric              ? / 1 pts  (run Part D first)")

    # T2 — all cnt>=5 actioned
    act5, tot5 = coverage_stats(df_long, 5)
    if act5 == tot5:
        score += 3
        print(f"  ✅  T2  · All cnt≥5 groups actioned        3 / 3 pts  ({tot5}/{tot5})")
    else:
        rem5 = tot5 - act5
        print(f"  ❌  T2  · All cnt≥5 groups actioned        0 / 3 pts  ({act5}/{tot5})")
        tips.append(f"+3 pts  Review {rem5} remaining high-frequency group(s) (cnt≥5) "
                    "in the sheet, then re-run Part D + push")

    # T3 — 75% of cnt>=3 actioned
    act3, tot3 = coverage_stats(df_long, 3)
    pct3  = act3 / tot3 * 100 if tot3 else 100.0
    need3 = max(0, round(tot3 * 0.75) - act3)
    if pct3 >= 75.0:
        score += 2
        print(f"  ✅  T3  · 75% of cnt≥3 groups actioned    2 / 2 pts  "
              f"({act3}/{tot3} = {pct3:.0f}%)")
    else:
        print(f"  ❌  T3  · 75% of cnt≥3 groups actioned    0 / 2 pts  "
              f"({act3}/{tot3} = {pct3:.0f}%, need {need3} more)")
        tips.append(f"+2 pts  Review {need3} more cnt≥3 group(s) to reach 75%, "
                    "then re-run Part D + push")

    # JMU-specific checks
    if school == 'JMU':
        max_score += JMU_SPECIFIC_PTS
        print()
        print(_hdr('JMU-specific checks'))
        for chk in JMU_CHECKS:
            if df_clean is None:
                print(f"  ❓  {chk['id']} · {chk['name']:<42} ? /{chk['pts']} pts  "
                      "(run Part D first)")
            else:
                remaining = near(df_clean, chk['ref_lat'], chk['ref_lon'], chk['tol'])
                if remaining.empty:
                    score += chk['pts']
                    print(f"  ✅  {chk['id']} · {chk['name']:<42} "
                          f"{chk['pts']} /{chk['pts']} pts")
                else:
                    n_rem = len(remaining)
                    print(f"  ❌  {chk['id']} · {chk['name']:<42} "
                          f"0 /{chk['pts']} pts  ({n_rem} row(s) still at wrong coords)")
                    hint_short = chk['hint'].split('\n')[0]
                    tips.append(f"+{chk['pts']} pt{'s' if chk['pts']>1 else ''}  "
                                 f"{hint_short}")

    pct_score = score / max_score * 100 if max_score else 0
    print()
    print(f"  {'─' * (W - 2)}")
    print(f"  Autograded estimate:  {score:>3} / {max_score} pts  ({pct_score:.0f}%)")
    print(f"  ⚠️  This score is provisional. All submissions are reviewed")
    print(f"      manually and final grades may differ.")
    print()

    if tips:
        print(_hdr('Next steps to earn more points'))
        for tip in tips:
            print(f"  {tip}")
        print()
        print(f"  After updating the sheet:")
        print(f"    1. Re-run Part C + D in lesson_4_4_preparing_review_sheet.ipynb")
        print(f"    2. git add data/{school}/{school}_geoparsed_long.csv \\")
        print(f"               data/{school}/{school}_geoparsed_cleaned.csv")
        print(f"    3. git commit -m 'review: update {school} location data'")
        print(f"    4. git push")
    else:
        print(f"  🎉  All tests passing — full marks!")

    print()
    print('╔' + '═' * W + '╗')
    print(f"║{'  Run  pytest tests/ -v  to see the full autograder output':<{W}}║")
    print(f"║{'  Note: all work is also reviewed manually by the instructor':<{W}}║")
    print('╚' + '═' * W + '╝')
    print()


if __name__ == '__main__':
    main()
