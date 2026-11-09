#!/usr/bin/env python3
"""
roi_model.py -- every number in Deliverable D comes from here. Change an assumption, rerun, paste into the deck.
All rupee figures are fully loaded hourly costs (salary + tools + overhead), NOT salary alone. These are my assumptions,
not Bambinos data; the first job in the 30-day plan is to replace them with a measured baseline.
"""
A = dict(
  classes_per_week      = 500,
  class_minutes         = 50,
  # ---- today (manual) ----
  manual_review_min     = 45,     # scrub at ~1.5x + notes per class, incl. context switching
  manual_hit_rate       = 0.15,   # share of classes that yield >=1 usable clip (brief says 85-90% of review time is wasted)
  manual_clips_per_hit  = 1.8,    # brief says "1-3 usable clips" per good class
  manual_edit_min       = 45,     # editor finds exact in/out, captions, crop, per clip
  reviewer_rate         = 400,    # INR/hr loaded, junior marketing exec
  editor_rate           = 500,    # INR/hr loaded, video editor
  # ---- AI-assisted ----
  llm_cost_per_class    = 12,     # INR: ~10-14k input tokens x 2 passes (miner + verifier on candidates) on a mid-tier model
  asr_second_pass_per_cand = 3,   # INR: Whisper/Gemini audio on a 40-60s slice
  video_triage_per_cand = 8,      # INR: Gemini video on a 30s clip
  shortlist_rate        = 0.60,   # candidates per class that clear the 7.0 bar (sample: 3 PASS + 1 RESERVE over 4 classes ~ 0.75-1.0; I shade down)
  human_triage_min      = 4,      # read brief, watch 25s, tick visual checklist
  precision_d30         = 0.45,   # share of AI shortlist editors accept, month 1
  precision_d90         = 0.60,   # after prompt iterations
  spot_check_classes    = 50,     # random sample of AI-rejected classes per week to measure what we miss
  spot_check_min        = 5,
  ops_hours_per_week    = 3,      # keeping the Sheet / n8n alive, weekly prompt review
  edit_min_with_brief   = 30,     # exact timestamps + crop + caption notes shave time
  fixed_tools_per_week  = 6000,   # INR: n8n/Make, Airtable/Sheets add-ons, storage, ~25k/month
)

def run(precision):
    a = A
    out = {}
    # manual
    out["manual_review_h"] = a["classes_per_week"] * a["manual_review_min"] / 60
    out["manual_clips"]    = a["classes_per_week"] * a["manual_hit_rate"] * a["manual_clips_per_hit"]
    out["manual_edit_h"]   = out["manual_clips"] * a["manual_edit_min"] / 60
    out["manual_cost"]     = out["manual_review_h"] * a["reviewer_rate"] + out["manual_edit_h"] * a["editor_rate"]
    out["manual_cost_per_clip"] = out["manual_cost"] / out["manual_clips"]
    # AI
    cands = a["classes_per_week"] * a["shortlist_rate"]
    out["ai_candidates"]   = cands
    out["ai_clips"]        = cands * precision
    triage_h = cands * a["human_triage_min"] / 60
    spot_h   = a["spot_check_classes"] * a["spot_check_min"] / 60
    out["ai_review_h"]     = triage_h + spot_h + a["ops_hours_per_week"]
    out["ai_edit_h"]       = out["ai_clips"] * a["edit_min_with_brief"] / 60
    machine = a["classes_per_week"]*a["llm_cost_per_class"] + cands*(a["asr_second_pass_per_cand"]+a["video_triage_per_cand"]) + a["fixed_tools_per_week"]
    out["ai_machine_cost"] = machine
    out["ai_cost"]         = out["ai_review_h"]*a["reviewer_rate"] + out["ai_edit_h"]*a["editor_rate"] + machine
    out["ai_cost_per_clip"]= out["ai_cost"] / out["ai_clips"]
    out["review_hours_saved_pct"] = 100*(1 - out["ai_review_h"]/out["manual_review_h"])
    return out

if __name__ == "__main__":
    m, d30, d90 = run(A["precision_d30"]), run(A["precision_d30"]), run(A["precision_d90"])
    rows = [("Review hours / week", f'{m["manual_review_h"]:.0f}', f'{d30["ai_review_h"]:.0f}', f'{d90["ai_review_h"]:.0f}'),
            ("Editor-accepted clips / week", f'{m["manual_clips"]:.0f}', f'{d30["ai_clips"]:.0f}', f'{d90["ai_clips"]:.0f}'),
            ("Editing hours / week", f'{m["manual_edit_h"]:.0f}', f'{d30["ai_edit_h"]:.0f}', f'{d90["ai_edit_h"]:.0f}'),
            ("Total weekly cost (INR)", f'{m["manual_cost"]:,.0f}', f'{d30["ai_cost"]:,.0f}', f'{d90["ai_cost"]:,.0f}'),
            ("Cost per usable clip (INR)", f'{m["manual_cost_per_clip"]:,.0f}', f'{d30["ai_cost_per_clip"]:,.0f}', f'{d90["ai_cost_per_clip"]:,.0f}')]
    print("| Metric | Manual today | AI-assisted, month 1 (45% precision) | AI-assisted, day 90 (60% precision) |\n|---|---|---|---|")
    for r in rows: print("| " + " | ".join(r) + " |")
    print(f'\nReview time saved: {d30["review_hours_saved_pct"]:.0f}%  |  machine cost / week: INR {d30["ai_machine_cost"]:,.0f}  |  AI candidates / week: {d30["ai_candidates"]:.0f}')
    # sensitivity: what if the manual baseline is much better than assumed?
    print("\nSensitivity (day-90 cost per clip, INR)")
    for hit in (0.10, 0.15, 0.25):
        A["manual_hit_rate"] = hit; mm = run(0.6)
        print(f"  manual hit-rate {hit:.0%}: manual {mm['manual_cost_per_clip']:,.0f}  vs  AI {mm['ai_cost_per_clip']:,.0f}")
    A["manual_hit_rate"] = 0.15
    for p in (0.30, 0.45, 0.60, 0.75):
        r = run(p); print(f"  editor precision {p:.0%}: AI cost/clip {r['ai_cost_per_clip']:,.0f}, clips/week {r['ai_clips']:.0f}")
