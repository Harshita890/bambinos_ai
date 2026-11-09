import json, csv
b = json.load(open("output/ad_briefs.json"))
cols = ["Brief ID","Session","Subject","Start","End","Cut ranges","Final length (s)","Bucket","3-sec on-screen hook","Why it stops a parent",
        "Verbatim dialogue (copied from VTT)","Score (Miner)","Sub-scores H/A/P/M/F/W","Score (Verifier)","Status",
        "Geo: India","Geo: GCC","Geo: US/UK/CA/AU","Compliance flags","Visual check (editor must confirm)","Visual status","Editor instructions","Kill switch",
        "Editor decision (Accept/Reject)","Reject reason code","Editor minutes spent"]
with open("sheets/google_sheet_template_with_sample_rows.csv","w",newline="") as f:
    w = csv.writer(f); w.writerow(cols)
    for x in b:
        s = x["scores"]
        w.writerow([x["id"],x["session"],x["subject"],x["start"],x["end"],"; ".join(x["cut_ranges"]),x["duration_s"] or "n/a",x["bucket"],x["hook_3s"],x["why"],
            " | ".join(f'[{v["t"]}] {v["role"]}: {v["text"]}' for v in x["verbatim"]),x["total"],
            "/".join(str(s[k]) for k in ["hook","authenticity","parent_value","mute_legible","feasibility","warmth"]),x["verifier_total"],x["status_final"],
            x["geo"]["india"],x["geo"]["gcc"],x["geo"]["us"]," || ".join(x["flags"])," || ".join(x["visual_check"]),x["visual_status"],x["editor"],x["kill"],"","",""])
# readable markdown
L = ["# Extracted ad briefs (4 real classes -> 5 candidates -> 3 editor-ready)\n",
     "Source: `marketing/transcripts/*.vtt` in the assessment repo, run through `scripts/preprocess_vtt.py`, `prompts/01`, then a second-look pass with the `prompts/02` checklist.",
     "All quotes are machine-checked against the raw VTT by `scripts/verify_quotes.py` (25/25 lines match, same cue, same speaker role).\n",
     "**Important:** the class MP4s were Git-LFS pointers I could not download, so nothing below has been visually verified. Every brief carries a `visual_check` list and a `kill_switch` for the editor.\n",
     "| Rank | ID | Window (final cut) | Bucket | Hook (first 3s, on-screen) | Miner / Verifier | Status |","|---|---|---|---|---|---|---|"]
for i,x in enumerate(sorted(b,key=lambda z:-z["verifier_total"]),1):
    L.append(f'| {i} | {x["id"]} | {x["start"]}-{x["end"]} ({x["duration_s"] or "n/a"}s) | {x["bucket"]} | {x["hook_3s"]} | {x["total"]} / {x["verifier_total"]} | {x["status_final"]} |')
L.append("")
for x in sorted(b,key=lambda z:-z["verifier_total"]):
    s=x["scores"]
    L += [f'## {x["id"]} - {x["subject"]} - {x["bucket"]}', f'**Status:** {x["status_final"]}  ', f'**Cut:** {", ".join(x["cut_ranges"])} (final {x["duration_s"] or "n/a"}s)  ',
          f'**3-second hook (on-screen text):** {x["hook_3s"]}  ', f'**Alt hook:** {x["hook_alt"]}  ', f'**Why it stops a parent:** {x["why"]}\n', "**Verbatim (from VTT, ASR errors left in on purpose):**"]
    L += [f'- `[{v["t"]}]` **{v["role"]}:** {v["text"]}' for v in x["verbatim"]]
    L += ["", f'**Score:** {x["total"]} (hook {s["hook"]} / authenticity {s["authenticity"]} / parent value {s["parent_value"]} / mute-legible {s["mute_legible"]} / feasibility {s["feasibility"]} / warmth {s["warmth"]}). Verifier re-score: {x["verifier_total"]}.\n',
          f'**Geography fit:** India - {x["geo"]["india"]}. GCC - {x["geo"]["gcc"]}. US/UK/CA/AU - {x["geo"]["us"]}.\n', "**Compliance flags:**"]
    L += [f"- {f}" for f in x["flags"]]
    L += ["", "**Editor must confirm on video:**"] + [f"- [ ] {f}" for f in x["visual_check"]]
    L += ["", f'**Editor instructions:** {x["editor"]}\n', f'**Kill switch:** {x["kill"]}\n', "---\n"]
open("output/ad_briefs.md","w").write("\n".join(L))
print("ok")
