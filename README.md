# Bambinos.live: live class to scroll-stopping ad (AI PM, Marketing take-home)

A clip-mining pipeline: raw class transcript in, editor-ready ad briefs out (or an honest "nothing here").

**Start here:** `docs/Case_Report.pdf` (Deliverables A, B, D). Then `output/ad_briefs.md` (Deliverable C) and `prompts/`.

## Run it on the sample data
```bash
git clone https://github.com/bambinoslive/AI-PM-hiring-take-home-assignments
T=AI-PM-hiring-take-home-assignments/marketing/transcripts
python3 scripts/preprocess_vtt.py $T/Gita_2125422751.vtt data/processed --alias Anaya,Anna
# paste data/processed/Gita_2125422751.clean.txt into prompts/01 (user-message template) in Claude / Gemini / a Custom GPT
python3 scripts/verify_quotes.py output/ad_briefs.json $T      # 25/25 quote checks pass
python3 scripts/roi_model.py                                    # every number in the ROI section
sh scripts/build_pdf.sh                                         # needs pandoc + wkhtmltopdf
```

## Honest status
- The five briefs were produced by applying `prompts/01` to the pseudonymised transcripts and a second-look pass using the `prompts/02` checklist. The second pass was not an independent model call.
- The class MP4s were Git-LFS pointers I could not download, so **nothing is visually verified**. Each brief says `UNVERIFIED` and lists what the editor must check.
- Meta Ad Library was not accessible, so the competitor scan is partial (see `docs/competitor_scan_template.md`).
- ROI figures are assumptions in `scripts/roi_model.py`, to be replaced by a measured baseline in the first 30 days.

| Folder | Contents |
|---|---|
| `prompts/` | Miner, Verifier, Visual Triage prompts, changelog |
| `scripts/` | Preprocessing, quote verification, ROI model, output builder, PDF build |
| `data/processed/` | Pseudonymised transcripts and per-minute risk flags |
| `output/` | Briefs (md/json), rejected-moments log |
| `sheets/` | Google Sheet template with the sample rows (File > Import) |
