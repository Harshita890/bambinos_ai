#!/usr/bin/env python3
"""
verify_quotes.py -- the anti-hallucination gate.
For every brief in ad_briefs.json, checks that each 'verbatim' line:
  (a) exists as a substring of a real cue in the original .vtt, and
  (b) that cue starts at the stated timestamp (+/- 1s), and
  (c) the speaker role matches (teacher = speaker with most words).
Exit code 1 if anything fails, so n8n/Make can stop the run before a brief reaches an editor.

Usage: python verify_quotes.py ad_briefs.json /path/to/marketing/transcripts
"""
import sys, json, re, os
sys.path.insert(0, os.path.dirname(__file__))
from preprocess_vtt import load_vtt, roles

def norm(s): return re.sub(r"\s+", " ", s.lower()).strip()
def sec(t): m, s = t.split(":"); return int(m) * 60 + int(s)

briefs = json.load(open(sys.argv[1]))
tdir = sys.argv[2]
cache, bad, total = {}, 0, 0
for b in briefs:
    f = os.path.join(tdir, b["session"] + ".vtt")
    if f not in cache:
        cues = load_vtt(f); teacher, _ = roles(cues); cache[f] = (cues, teacher)
    cues, teacher = cache[f]
    for v in b["verbatim"]:
        total += 1
        ok = False
        for c in cues:
            role = "TEACHER" if c["speaker"] == teacher else "CHILD"
            if abs(c["start"] - sec(v["t"])) <= 1 and role == v["role"] and norm(v["text"]) in norm(c["text"]):
                ok = True; break
        if not ok:
            bad += 1
            print(f"FAIL  {b['id']} @{v['t']} {v['role']}: {v['text'][:70]}")
    # duration sanity: cut ranges must sum to duration_s (unless on hold)
    if b["duration_s"]:
        s = sum(sec(r.split("-")[1]) - sec(r.split("-")[0]) for r in b["cut_ranges"])
        if abs(s - b["duration_s"]) > 2:
            bad += 1; print(f"FAIL  {b['id']} duration {b['duration_s']} != cut ranges {s}")
print(f"{total - bad if bad < total else 0}/{total} quote checks passed" if bad == 0 else f"{bad} problem(s) found")
sys.exit(1 if bad else 0)
