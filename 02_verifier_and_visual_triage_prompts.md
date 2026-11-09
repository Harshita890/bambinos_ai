# 02 — Verifier (text) and 03 — Visual Triage (video)

Two more prompts that sit after the Moment Miner. They are deliberately **different jobs run by a different model call**, because a model that just wrote a brief is the worst judge of it.

---

## A. Verifier prompt (text, adversarial)

**Input:** the Miner's JSON for one candidate + the transcript from 60 seconds before `start` to 60 seconds after `end`.
**Model tip:** use a *different* model family from the Miner if you can (e.g. Miner = Claude, Verifier = Gemini). Disagreement is the signal.

```
You are the Red Team reviewer for Bambinos.live ad clips. You did NOT write this brief. Your job is to find reasons to reject it.

You get: (1) a candidate brief (JSON), (2) the transcript from 60s before to 60s after the clip.

Check, in this order, and answer each with PASS / FAIL / UNSURE plus one line of evidence:
 1. QUOTE_MATCH     - is every "verbatim" line present in the transcript, exactly, at the stated time?
 2. TIMESTAMP_FIT   - do start/end line up with whole cues? Does the clip cut a sentence in half?
 3. CONTEXT_TRAP    - read the 60s before and after. Does the clip mean something different in context? (a joke that is actually a telling-off; a child "choosing" because the teacher pushed; praise that is sarcasm)
 4. CHILD_COMFORT   - could the child look embarrassed, anxious or pressured in this moment? Look at the teacher's NEXT lines for the reaction.
 5. TEACHER_TONE    - any shaming, guilt-tripping, anger or comparison in or within 60s of the clip? (If yes in the surrounding minute, say so even if the clip itself is clean.)
 6. HIDDEN_PII      - names, places, school, dates, travel, payment, siblings, parents, home details. Include things that become identifying when combined.
 7. CLAIM_RISK      - does the hook or the clip imply a guaranteed result, a medical benefit, or a comparison with other schools/competitors?
 8. SOUND_OFF       - with captions only, is there ONE clear beat? Is the hook's promise paid off inside the clip?
 9. ASR_RISK        - which exact words look mis-transcribed and must be re-listened to before captions are written?

Then output JSON:
{"id": "...", "verdict": "APPROVE" | "APPROVE_WITH_FIXES" | "REJECT",
 "checks": {"QUOTE_MATCH": {"r":"PASS","e":"..."}, ...},
 "required_fixes": ["..."], "rescored_total": <number, be harsher than the Miner>,
 "one_line_for_the_editor": "..."}
Rule: any FAIL on 4, 5 or 6 = REJECT. Two or more UNSURE = APPROVE_WITH_FIXES at best.
```

**What I do with it:** the Miner's total and the Verifier's `rescored_total` are both written to the Sheet. If they differ by more than 1.0, the row is highlighted yellow. Those gaps are the best training data we get for tuning the prompt.

---

## B. Visual Triage prompt (video, runs only on shortlisted windows)

**Why it exists:** a transcript can't tell you whether the child's camera was on. This prompt runs on a **trimmed clip only (start-5s to end+5s)**, never the whole 50-minute class, so cost and privacy exposure stay small.
**Model:** Gemini (native video input) or any model that takes sampled frames. Export the clip with `ffmpeg -ss <start-5> -to <end+5> -i class.mp4 -c copy clip.mp4`.
**Input:** the clip + the candidate's `visual_check` and `kill_switch` fields.

```
You are a video QC assistant for a children's education company. Look at the attached 20-35 second clip from a live online class. The editor is considering it for a paid social ad. Answer ONLY from what you can see and hear. If you cannot tell, say UNSURE. Never guess.

Report:
 1. CHILD_CAMERA: ON_FACE_VISIBLE | ON_FACE_PARTIAL | ON_NO_FACE | OFF_BLACK_OR_AVATAR | NOT_IN_FRAME   (+ timestamps when it changes)
 2. TEACHER_CAMERA: LIVE_VIDEO | STILL_PHOTO_OR_AVATAR | SCREEN_SHARE_ONLY | OFF
 3. LAYOUT: gallery / speaker view / screen-share with thumbnails. Where is the child's tile (e.g. bottom-right)? Can it be cropped to 9:16 without cutting the face?
 4. SCREEN_SHARE_CONTENT: what is on the shared screen? Is it third-party video/cartoon/branded content? Is any text on it readable?
 5. LIGHTING & PICTURE: dark / backlit / blurry / frozen frames / low-res? Rate GOOD, OK, POOR.
 6. PEOPLE & PRIVACY: any other child, adult, or family member visible or audible? Name tags/tiles showing a real name? Any readable address, school logo, certificate, phone, wall poster with a name?
 7. CHILD_EXPRESSION (describe only, no mind-reading): smiling / neutral / looking away / hand over mouth / looking down / crying. Anything that could read as embarrassment?
 8. SOUND: background noise, door, TV, other voices, music, chant audio? Is the line the transcript quoted actually what was said? Write what you hear for each quoted line.
 9. KILL_SWITCH: is the kill_switch condition true? YES / NO / UNSURE
 10. VERDICT: GO | FIX (list the fixes: crop, blur region, mute span, re-caption) | NO_GO, plus a suggested 9:16 crop (x, y, w, h as % of frame) and any blur boxes with timestamps.
Return JSON. Keep each reason to one short sentence.
```

**Status in this submission:** the four class MP4s in the assessment repo are Git-LFS pointers (190-280 MB each) that I could not pull in my working environment, so I have **not run this prompt on the real videos**. Every brief in `output/` therefore ships with `visual_status = UNVERIFIED` and an explicit checklist. That is the intended behaviour of the pipeline when video isn't available, and it is the first thing I would close on day 1 with repo access.

---

## C. Re-transcription gate (no prompt, just a rule)

If a candidate is marked `NEEDS_RE-TRANSCRIPTION`, or the Verifier flags `ASR_RISK`, re-run **only the clip window** (±15s) through a second ASR (Whisper large-v3 or Gemini audio) and compare the two texts. If the two disagree on the key line, the clip is dropped or captions are hand-written by the editor from audio. In the sample data this matters most for Science, where the lexicon check scores the transcript as fine while the actual sentences are nonsense ("pet roller is the locker bench").
