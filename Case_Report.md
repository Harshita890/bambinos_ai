---
title: "From live class to scroll-stopping ad"
subtitle: "A clip-mining pipeline for Bambinos.live — AI Program Manager (Marketing) take-home"
---

**Candidate:** [Your name] &nbsp;|&nbsp; **Date:** 8 November 2026 &nbsp;|&nbsp; **Repo:** [add your GitHub link] &nbsp;|&nbsp; **Covers:** Deliverables A, B, D (C lives in the repo: prompts, outputs, scripts)

## The short version

I treated this as a filtering problem, not a content-generation problem. Bambinos doesn't lack footage; it lacks a cheap way to say "nothing here" for the 85–90% of classes that have nothing here, and a trustworthy way to say "here, 40:55 to 41:19" for the rest.

- **What I built:** a 7-step pipeline (transcript → pseudonymise → mine → verify → visual check → human gate → editor brief). Two prompts, one preprocessing script, one quote-checker, one ROI model, a Sheet template. All in the repo.
- **What it found on the four real classes:** 5 candidate moments, 3 editor-ready, 1 reserve, 1 on hold for bad ASR. The Maths class returned **zero**, on purpose, and I'd route it to Academics, not marketing.
- **One finding I didn't expect:** the child's share of words is a free pre-filter. English 51%, Gita 19%, Science 11%, Maths 4%. A class where the child barely speaks is almost never an ad.
- **What I could not do, so you know up front:** the four MP4s in the repo are Git-LFS pointers I couldn't download in my environment, so **no clip has been visually verified**. Every brief says so and carries a checklist. I also couldn't open Meta Ad Library live; the competitor section below says exactly what I did and didn't see.
- **Money:** under my assumptions, review time drops from roughly 375 to 27 hours a week (about 93%) and cost per usable clip from about ₹1,486 to about ₹395–444. Those are assumptions, and Day 1–30 of the plan is about replacing them with measured numbers.

## A. Research and creative taxonomy

### A1. What parents are actually shown, and what I could and couldn't verify

**Bambinos' own positioning.** The pricing page leans on three ideas: small batches ("Max 6 kids per batch. Not 40, not 50"), a child who actually gets a turn ("Most kids never get a turn to speak"), and a teacher who knows the child by name. That is the brand promise, so my buckets are built to *prove* those three things on video instead of repeating them in a voiceover.

**Competitor pattern (PlanetSpark), from an ad-library aggregator.** hawky.ai's summary of PlanetSpark's public Meta ads (updated 12 Aug 2026) lists about 1,989 ads, 708 still live, mostly public-speaking. Its most repeated openers are slogan-style: "PUBLIC SPEAKING FOR KIDS" (53 creatives), "PUBLIC SPEAKING = POWER" (52), "Are you even a leader if you can't speak properly?" (40). Almost every ad ends on "Book now". Reading that: the category leader mostly sells the *promise* (fear and aspiration) in the first line.

**What I take from it:** Bambinos can't win a slogan fight with a bigger spender, but it has something slogans don't: footage of a real child doing the thing. The opening line should be a *moment*, not a claim.

**Not verified (please read this as a gap, not a finding).** I could not open Meta Ad Library or Instagram from my working environment, so I have *no first-hand observations* of Bhanzu, BrightChamps or Vedantu creatives. I'm not going to invent them. The repo has `docs/competitor_scan_template.md`, a 20-minute checklist (hook type, real-class vs studio, on-screen language, CTA, run length) to complete with screenshots on day 1.

### A2. The four sample classes, in one table

| Class | Minutes | Child's share of words | Tone flags (windows) | Admin/PII flags (windows) | Verdict |
|---|---|---|---|---|---|
| English | 50 | **51%** | 3 | 1 | 2 PASS |
| Gita | 50 | 19% | 0 | 0 | 1 PASS, 3 RESERVE |
| Science | 52 | 11% | 0 | 4 | 0 PASS, 1 HOLD |
| Maths | 42 | **4%** | **6** | 0 | **0 — escalate** |

Child-talk share is cheap to compute and ranked the four classes in the same order as my manual read of them. The tone and admin columns are regex *review flags*; my first draft flagged "very angry" about a god in a story, so I tightened it to teacher-to-child shaming and still treat it as a prompt to look, not a verdict. I'd use it as a pre-filter (below 8%: skip mining, run the tone check only).

### A3. Six moment buckets

Each bucket is a *proof* a parent can't get from a school class of 40.

| Bucket | What the parent thinks | What it looks like in a transcript | Real example from the data |
|---|---|---|---|
| **B1 Unscripted Delight** | "My child actually enjoys this." | Child volunteers a feeling nobody asked for | Gita 41:01, "I feel like it wasn't that long." (about meditation) |
| **B2 Visible Learning** | "I can see it working." | Wrong → right within ~20s, after one nudge | English 12:26, "I see turtles, I saw a crab, I saw a fish" |
| **B3 Child Speaks Up** | "He's finally talking." | Child holds the floor, reasons aloud, argues politely | Science 48:56 (parked; ASR unreadable) |
| **B4 Teacher Knows My Child** | "Someone is paying attention to her." | Teacher notices, remembers, adapts | Gita 22:29, teacher notices the room is too dark (reserve) |
| **B5 Curiosity Spark** | "They're hooked on the story." | Suspense, imagination, a funny confident wrong answer | English 10:45, octopus on the sand; Gita 19:48, "You want Shiva to help this boy?" |
| **B6 Values & Culture** | "This builds character, not just marks." | Courage, kindness, prayer, festivals, in a child's words | Gita 27:15, "Because he is brave" (reserve) |

Not a bucket: teacher explaining, reading slides, giving instructions, homework, or admin. If the teacher is talking for more than ~10 seconds without the child, it usually isn't a moment.

### A4. Scoring rubric (out of 10)

| Criterion | Max | What earns the points |
|---|---|---|
| Hook (first 3s, works on mute) | 2.0 | Surprise, question, contrast, or a genuinely funny line |
| Authenticity | 2.0 | Child-led, unscripted, imperfect in a charming way |
| Parent value | 2.0 | Shows personal attention, a turn to speak, visible progress, or values |
| Mute-legibility | 1.5 | One clear beat, 12–25s, understood with captions only |
| Production feasibility | 1.5 | Clean ASR, clear speakers, tidy cut, nothing depends on an unseen visual |
| Warmth / brand fit | 1.0 | Kind, encouraging teacher tone |

**≥ 7.0 PASS, 6.0–6.9 RESERVE (library, not this week), < 6.0 HOLD/DROP.** Any hard exclusion sets the score to 0.
A 9 should be rare. On the sample, the best clip scored 8.2 and the other two passing clips 7.5 and 7.7. If a prompt starts handing out 8s to everything, it has drifted.

**How I'd calibrate it:** two editors independently score the same 20 clips from past ads. If they differ by more than 1.0 on average, the rubric wording is the problem, not the model. Then compare the AI's scores to those, and later to real ad performance.

### A5. Hard exclusions and compliance red flags

Any one of these is an automatic drop. The "how it's caught" column matters: most can't be caught by the LLM alone.

| # | Exclusion | How it's caught |
|---|---|---|
| X1 | Child PII: name, surname, school, city, birthday, **travel plans**, phone, handles | Names pseudonymised before any LLM sees the text; Miner and Verifier both screen the rest. (Dropped in sample: a child describing a trip abroad; a birthday date.) |
| X2 | Price, payment, schedule, renewal, sales talk | Regex flags in preprocessing + LLM. (Sample: "they paid $100"; ~6 minutes of scheduling chat in Science.) |
| X3 | Child embarrassed, corrected harshly, put on the spot | Verifier reads the teacher's *next* lines; video triage describes expression. |
| X4 | Teacher shaming, sarcasm, guilt-trips, threats to stop teaching | Regex + LLM, also at class level. (Maths: 6 flagged windows. English: "I'll cry now because your beings are naughty" at 21:02.) |
| X5 | Unverified outcome claims ("topper", "fluent in a week") | Hook-writing rule: describe the moment, never the result |
| X6 | Medical or therapeutic claims (eyesight, anxiety, focus) | Verifier. (Gita 22:48, "not good to watch your screen in a dark room", drifts here.) |
| X7 | Siblings, parents, home interiors, door knocks, background voices | Regex + video triage. (English door knocks; Gita "my baby brothers... disturbing".) |
| X8 | Third-party content on screen (shared cartoon video), competitor/brand names | Video triage; crop to the child's tile. |
| X9 | Religious content that pressures or compares | Verifier; Gita clips get per-region review. |
| X10 | Key line depends on garbled ASR | Second-ASR check on the clip window. |
| X11 | Tech trouble, long silences, "can you hear me" | Regex + LLM. |
| X12 | **No parental marketing consent on file** | Hard gate in the Sheet: no `consent_ok = TRUE`, no handoff. |

Also: **sound-off legibility** is a scoring criterion, not an exclusion. Every brief must make sense with captions alone.

### A6. India vs GCC vs US/UK/CA/AU

| Region | What lands | What to watch |
|---|---|---|
| India | Spoken-English confidence, "my child finally talks", school-vs-live contrast, regional festivals and values | Parent-pressure tone; avoid anything that sounds like shaming |
| GCC (Indian diaspora) | English confidence, Maths, discipline-with-warmth | Religion-specific content needs local review; I default Gita clips to "hold" for GCC |
| US / UK / CA / AU | Culture and values without a lecture; confidence and curiosity; screen-time guilt ("she asked for *more* meditation") | "English fluency" is a weaker angle; children's-data rules are stricter |

Every brief carries a High/Medium/Low rating for each region with a one-line reason, so the same clip can be cut differently per geography instead of being re-found.

## B. Workflow and SOP

### B1. Architecture

<div class="flow">
<svg viewBox="0 0 980 190" xmlns="http://www.w3.org/2000/svg" font-family="DejaVu Sans, Arial, sans-serif">
<defs><marker id="ar" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#555"/></marker></defs>
<g font-size="11" text-anchor="middle">
<rect x="5" y="20" width="110" height="64" rx="8" fill="#eef3ff" stroke="#6b86d6"/><text x="60" y="44" font-weight="bold">0 Class ends</text><text x="60" y="60">recording + VTT</text><text x="60" y="74">land in storage</text>
<rect x="135" y="20" width="110" height="64" rx="8" fill="#eef3ff" stroke="#6b86d6"/><text x="190" y="44" font-weight="bold">1 Pre-process</text><text x="190" y="60">pseudonymise,</text><text x="190" y="74">flag, child-talk %</text>
<rect x="265" y="20" width="110" height="64" rx="8" fill="#e9f7ee" stroke="#4aa36c"/><text x="320" y="44" font-weight="bold">2 Mine (LLM)</text><text x="320" y="60">Miner prompt</text><text x="320" y="74">JSON, can be []</text>
<rect x="395" y="20" width="110" height="64" rx="8" fill="#e9f7ee" stroke="#4aa36c"/><text x="450" y="44" font-weight="bold">3 Verify</text><text x="450" y="60">quote match +</text><text x="450" y="74">red-team + 2nd ASR</text>
<rect x="525" y="20" width="110" height="64" rx="8" fill="#fff4e0" stroke="#e0a030"/><text x="580" y="44" font-weight="bold">4 Visual triage</text><text x="580" y="60">30s clip only,</text><text x="580" y="74">GO / FIX / NO-GO</text>
<rect x="655" y="20" width="110" height="64" rx="8" fill="#fdecec" stroke="#d65a5a"/><text x="710" y="44" font-weight="bold">5 Human gate</text><text x="710" y="60">marketer, ~4 min</text><text x="710" y="74">accept / reject+code</text>
<rect x="785" y="20" width="110" height="64" rx="8" fill="#fdecec" stroke="#d65a5a"/><text x="840" y="44" font-weight="bold">6 Editor brief</text><text x="840" y="60">rough-cut proxy</text><text x="840" y="74">+ card + checklist</text>
</g>
<g stroke="#555" stroke-width="1.5" marker-end="url(#ar)"><line x1="116" y1="52" x2="133" y2="52"/><line x1="246" y1="52" x2="263" y2="52"/><line x1="376" y1="52" x2="393" y2="52"/><line x1="506" y1="52" x2="523" y2="52"/><line x1="636" y1="52" x2="653" y2="52"/><line x1="766" y1="52" x2="783" y2="52"/></g>
<g font-size="10.5" fill="#444"><text x="5" y="122">Gate 1: child-talk &lt; 8% or tone flags: skip mining, send to teacher-tone review.</text>
<text x="5" y="138">Gate 2: any quote not found in the VTT: run stops. Verifier REJECT on tone / comfort / PII: row dies.</text>
<text x="5" y="154">Gate 3: no visual status, no assignment. Kill-switch true: row dies.</text>
<text x="5" y="170">Feedback loop (step 7, not shown): accept/reject codes + Meta hook-rate and hold-rate flow back to the Sheet by Brief ID and re-tune the rubric monthly.</text></g>
</svg>
</div>

### B2. Stage by stage, with tools

| # | Stage | Tool(s) | Input → output | Quality gate |
|---|---|---|---|---|
| 0 | Trigger | Storage event (the sample transcripts already live in a GCS bucket) → **n8n** webhook (Make/Zapier work too) | New VTT + MP4 → job | File exists, duration > 20 min |
| 1 | Pre-process | n8n Code node running `preprocess_vtt.py` | VTT → pseudonymised text + 60s window flags | Child-talk < 8% or tone flags → skip to tone review. No raw names leave this step. |
| 2 | Mine | **Claude** (Sonnet-class) with `prompts/01`; Gemini or GPT as alternates | Clean transcript → JSON array of candidates (may be empty) | Schema validation; every timestamp must exist |
| 3 | Verify | n8n Code node `verify_quotes.py`; **second model** with `prompts/02A`; Whisper/Gemini audio re-run on the clip slice only | Candidates → verdict + re-score | Quote mismatch stops the run; REJECT on tone/comfort/PII; ASR disagreement → re-caption or drop |
| 4 | Visual triage | `ffmpeg` trim (±5s) → **Gemini** video with `prompts/02B` | 30s clip → camera state, layout, crop box, blur boxes, GO/FIX/NO-GO | NO-GO or kill-switch = dies. Unverified = can't move on. |
| 5 | Human gate | **Google Sheets / Airtable** view per marketer | Candidate rows → Accept / Reject + reason code | Marketer must tick the visual checklist. 4 minutes per row. |
| 6 | Editor handoff | n8n → Drive/Frame.io folder, `ffmpeg` rough-cut with 3s handles, Asana/Trello card | Accepted row → proxy clip + brief + checklist | Editor sees a 25s clip, not a 50-minute file |
| 7 | Edit and launch | **CapCut** or Premiere; **OpusClip** only for auto-captions/reframing as a starting point; **ElevenLabs** voice-isolator for noisy audio (never voice-cloning children) | Rough cut → final 9:16 | Compliance checklist (below), then upload |
| 8 | Learn | Meta Ads API → Sheet (join on Brief ID) | Hook rate, hold rate, CPL by bucket | Monthly rubric re-weighting |

One cost control that matters: **the video model never sees a full class**, only a ~30-second slice of a shortlisted candidate. That keeps both cost and child-data exposure tiny.

### B3. Solving the audio-vs-visual gap

A transcript tells me what was said. It doesn't tell me whether the child's camera was on. I handle this in four layers instead of pretending the LLM can see.

**Layer 1, mine the transcript for visual clues.** The preprocessing script flags 60-second windows containing phrases that imply something visual or environmental. The real classes are full of them:

| Where | What the transcript gives away | What it means for the editor |
|---|---|---|
| English 8:55 | Child: "why don't you fake teacher image… you put a picture of you"; teacher: "That's my picture" | Teacher's camera is a still photo. No "teacher face" layout. |
| English 7:44, 23:13 | "somebody is at the door" | Someone else is audible or in frame |
| Gita 8:51–10:13 | "I will play the video now" | Screen is third-party animation; crop to the child's tile |
| Gita 22:29 | "It's too dark in your room" | Dark footage until about 22:36 |
| Gita 29:46, 32:59 | "You're a mute", "my light turned blue" | Mic/lighting glitches |
| Science 16:25 | "two snails… one is an actual snail and the other one is a toy" | Is it a physical prop on camera or a slide? Can't tell. Check video. |
| Science 21:09 | "I can't see the screen" | Screen-share trouble |

**Layer 2, the LLM must say what it can't know.** Every brief has a `visual_check` list and a `kill_switch`: one condition that, if true on video, kills the clip. The prompt forbids describing what's on screen.

**Layer 3, a video model checks the clip, not the class.** The visual-triage prompt reports child camera state, teacher camera (live vs still), layout, a suggested 9:16 crop, blur boxes, other people, lighting, screen-share content and the child's visible expression, then GO / FIX / NO-GO.

**Layer 4, a status the system respects.** Each row has a `visual_status`. Anything not "VERIFIED" can't be assigned to an editor. In my sample all five rows read UNVERIFIED because I didn't have the MP4s, and I'd rather show that honestly than fake a "visual check passed".

**Fallbacks are in the brief,** so an editor never starts from zero: "if the child's camera is off, drop (audio-only has no value)", "if the teacher's answer drags, end at 41:06 for a 10-second reaction cut".

### B4. The SOP a non-technical team actually follows

**Marketing exec (about 20 minutes a day)**

1. Open the *Today* tab. Rows are sorted by score; you'll see roughly 20–30 candidates a day at full volume.
2. For each: read the hook and quote (30 seconds), play the 25-second proxy (30 seconds), tick the visual checklist (1 minute).
3. Choose **Accept** or **Reject**. If rejecting, pick one code: R1 camera off/face not visible · R2 child looks uncomfortable · R3 transcript wrong · R4 PII or background visible · R5 hook is weak · R6 off-brand tone · R7 other.
4. Don't edit the hook in the Sheet; leave a comment. We change the prompt, not the output.
5. Once a week, spend 30 minutes with an editor on the rejected rows. That meeting *is* the training data.

**Video editor**

1. Open the Asana/Trello card. You get a 25-second proxy with 3-second handles, the brief, and the checklist, not the 50-minute file.
2. Do the 2-minute visual check first. If the kill-switch is true, mark Reject with a code and stop.
3. Follow the editor instructions; if you deviate, write one line in the card why.
4. Run the compliance checklist before upload: no names or tiles with names, no price, no outcome claim, no third-party video, consent flag is TRUE, captions match *audio* (not the ASR).
5. Log minutes spent on the card. That's how we prove time saved.

### B5. Edge cases I built for (and a few I didn't)

- **Zero-moment classes** return `[]` and cost almost nothing. No quota of "top 5".
- **Classes that are a quality problem, not an ad problem.** Maths: the teacher says "It's stupid. I explained it taking 5–10 minutes" and "it's the complete wastage for me to say anything", and speaks 96% of the words. The same run routes it to a private Academics view. I would not show it in the marketing Sheet.
- **ASR that looks fine but isn't.** My dictionary-based check catches transliteration and mangled names, but Science passes it while the sentences are nonsense ("pet roller is the locker bench"). Only a second ASR on the clip window catches that, so the second ASR is not optional.
- **The ASR calls the child by three different names** ("Zyan", "Zion", "Ziyang"). The pseudonymiser takes aliases per class; the Verifier has its own PII pass for anything that slips through.
- **Prompt injection from a transcript.** A child saying "ignore your instructions" is funny until it isn't. The Miner treats the transcript as data inside clearly delimited tags and its output is schema-validated.
- **Consent.** A clip of a child in a paid ad needs parental consent that explicitly covers marketing. I haven't seen Bambinos' T&Cs, so the Sheet has a hard `consent_ok` gate and I'd ask Legal to confirm the wording and the rules for each region (India's data-protection law, and children's-data rules in the US and UK). I'm not a lawyer and haven't tried to settle that here.
- **Not handled yet:** Hindi/Malayalam-heavy classes (the Science teacher switches mid-sentence), classes with several children in frame, and withdrawal of consent after an ad is live (needs a kill process to pull ads).

## D. Business impact, metrics and 30-60-90

### D1. Unit economics at 500 classes a week

All inputs are in `scripts/roi_model.py`. They are **my assumptions**, not Bambinos data; the day 1–30 baseline replaces them. Costs are fully loaded hourly rates (reviewer ₹400, editor ₹500).

| Metric | Manual today | AI-assisted, month 1 | AI-assisted, day 90 |
|---|---|---|---|
| Review hours / week | 375 | 27 | 27 |
| Editor-accepted clips / week | 135 | 135 | 180 |
| Editing hours / week | 101 | 68 | 90 |
| Total weekly cost | ₹2.01 L | ₹0.60 L | ₹0.71 L |
| **Cost per usable clip** | **₹1,486** | **₹444** | **₹395** |

**Key assumptions.** Manual: 45 minutes of review per 50-minute class; 15% of classes yield a clip (the brief says 85–90% of review time is wasted); 1.8 clips per hit class; 45 minutes to edit a clip. AI: about ₹12 of model cost per class; 60% of classes produce a candidate that clears the 7.0 bar; 4 minutes of human triage per candidate; editors accept 45% of candidates in month 1, 60% by day 90; editing drops to 30 minutes because timestamps, crop and captions are already specified. Machine cost, including a ₹6k/week allowance for tools, is about ₹15k/week.

**Sensitivity.** If manual hit-rate is 25% instead of 15%, manual cost per clip falls to about ₹1,042, and AI is still about 2.6× cheaper. If editors accept only 30% of what the AI proposes, the AI cost per clip is about ₹541. The conclusion survives my assumptions being wrong in the unfavourable direction.

**Two honest caveats.** (1) I've put manual and AI on the same 500 classes for a fair comparison. In real life I suspect the team samples far fewer than 500, so the bigger win may be *coverage*: 100% of classes screened instead of whatever fits in a day. (2) The model assumes the visual step doesn't add much human time. If editors reject a lot at the video check, precision falls and cost per clip rises, which is exactly what the 30-day shadow period measures.

### D2. Getting a skeptical team to use it

**Principles.** Editors have veto power with one click, and no one has to explain a rejection beyond a code. I show the AI's misses in public, not just its wins. Nothing changes for anyone in the first two weeks: the AI runs in *shadow mode* beside the manual process.

**Training.** One 45-minute session built around the Maths class (why it returns nothing) and the English octopus clip (why one clip is borderline), then a daily 15-minute reject review for two weeks. I'd name one editor and one marketer as champions who get first say on prompt changes.

**What I'd track**

| KPI | Definition | Target by day 90 |
|---|---|---|
| Review hours per 100 classes | Human minutes spent finding candidates | ≤ 6 h (from ~75 h) |
| **Precision** (false-positive rate = 1 − precision) | Share of AI candidates editors accept | ≥ 60% |
| **Recall** | (a) Share of clips from *past top-performing ads* the AI also finds; (b) misses found in a weekly 50-class spot-check of AI-rejected classes | ≥ 75% of historical winners |
| Time class-end → brief | Median | < 2 hours |
| Clip → ad conversion | Accepted clips launched as ads within 14 days | ≥ 60% |
| Ad performance, AI-sourced vs manual | Hook rate (3-sec views ÷ impressions), hold rate, cost per lead | At least parity by day 60, better by day 90 |
| Compliance incidents | PII, consent, claim issues reaching an editor | 0 |
| Adoption | % of candidates actioned within 48h; weekly active users | ≥ 90% |

**False positives.** Every rejection carries a code (R1–R7). The weekly reject review sorts by code and turns the top one into a prompt or script change: R1 becomes a stricter visual rule, R3 a tighter ASR gate, R2 more weight on teacher-reaction lines. I keep a changelog (`prompts/CHANGELOG.md`) so prompt changes are traceable and reversible.

### D3. 30-60-90

| | Days 1–30: prove it in shadow | Days 31–60: make it the default | Days 61–90: scale and learn |
|---|---|---|---|
| **Goal** | Know the real baseline and whether the AI finds what humans find | AI shortlist becomes the daily queue | All 500 classes screened; the loop learns from ad results |
| **Do** | Week 1: time-study 2 execs + 2 editors for 3 days; get the 4 MP4s plus ~20 more classes; finish the competitor scan with screenshots; Legal reviews consent wording. Weeks 2–4: run Miner + Verifier on 100 past classes; compare with what humans actually picked; run live in shadow on new classes | Switch English and Gita to AI-first, then Maths/Science; turn on video triage and rough-cut export; weekly reject review; prompt v2 and v3; per-region (GCC/US) variants of each brief; start Meta → Sheet feedback | 100% coverage; link every clip to its ad's hook rate, hold rate and cost per lead; re-weight the rubric by bucket; improve ASR for Hindi/Malayalam; hand the teacher-tone view to Academics; document the SOP and train a backup owner |
| **Exit criteria** | Precision ≥ 40%; ≥ 70% of historical winners recovered; 0 PII incidents; review ≤ 5 min per class | Precision ≥ 50%; review hours down ≥ 80%; AI clips at parity on hook rate | Precision ≥ 60%; ≥ 180 accepted clips/week; cost per usable clip ≤ ₹400; quarterly review set |
| **Biggest risk** | The baseline is much better than I assumed | Editors still don't trust it | Rubric drifts toward what the model likes, not what converts |

### D4. What I'd tell you I didn't do

- I didn't watch any video. The briefs are text-only and say so.
- I didn't open Meta Ad Library; the competitor section is partial and labelled.
- The "second-look" pass in the sample is me re-reading with the Verifier checklist, not an independent model call. In production those are separate calls on different models.
- The ROI numbers are assumptions. The sensitivity table is there so you can see how much each one matters.
- The Miner prompt hasn't been tested across hundreds of classes. Four is enough to find bugs (it found one in my own script), not enough to claim accuracy.

## Appendix: what's in the repo

| Path | What it is |
|---|---|
| `prompts/01_moment_miner_system_prompt.md` | The production Miner prompt, with the user-message template |
| `prompts/02_verifier_and_visual_triage_prompts.md` | Red-team verifier, video triage, re-transcription rule |
| `scripts/preprocess_vtt.py` | Parse VTT, pseudonymise, flag, child-talk share |
| `scripts/verify_quotes.py` | Fails the run if any quote isn't in the raw VTT (25/25 pass) |
| `scripts/roi_model.py` | Every number in D1 |
| `scripts/build_outputs.py` | Builds the Sheet CSV and Markdown briefs from JSON |
| `data/processed/` | Pseudonymised transcripts and window flags for all 4 classes |
| `output/ad_briefs.md / .json` | The 5 extracted briefs |
| `output/rejected_log.md` | What was thrown away and why |
| `sheets/google_sheet_template_with_sample_rows.csv` | Import into Google Sheets; has the sample rows |
