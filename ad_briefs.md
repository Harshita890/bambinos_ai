# Extracted ad briefs (4 real classes -> 5 candidates -> 3 editor-ready)

Source: `marketing/transcripts/*.vtt` in the assessment repo, run through `scripts/preprocess_vtt.py`, `prompts/01`, then a second-look pass with the `prompts/02` checklist.
All quotes are machine-checked against the raw VTT by `scripts/verify_quotes.py` (25/25 lines match, same cue, same speaker role).

**Important:** the class MP4s were Git-LFS pointers I could not download, so nothing below has been visually verified. Every brief carries a `visual_check` list and a `kill_switch` for the editor.

| Rank | ID | Window (final cut) | Bucket | Hook (first 3s, on-screen) | Miner / Verifier | Status |
|---|---|---|---|---|---|---|
| 1 | GITA-01 | 40:55-41:19 (24s) | B1 Unscripted Delight | Kid says meditation was too SHORT | 8.2 / 8.0 | PASS - send to editor, visual check first |
| 2 | ENG-02 | 12:26-12:57 (25s) | B2 Visible Learning | Watch him fix his own grammar | 7.7 / 7.4 | PASS - send to editor, visual check first |
| 3 | ENG-01 | 10:43-11:06 (23s) | B5 Curiosity Spark | 'Imagine a beach.' He saw an octopus. On the sand. | 7.5 / 7.1 | PASS - send to editor, visual check first |
| 4 | GITA-02 | 19:36-20:12 (24s) | B5 Curiosity Spark | Teacher stops the story at the scariest part | 7.2 / 6.8 | RESERVE (verifier re-score 6.8 < 7.0) |
| 5 | SCI-01 | 48:19-49:13 (n/as) | B3 Child Speaks Up | Why isn't petrol 'food' for a car? | 5.7 / 5.0 | HOLD - re-transcribe |

## GITA-01 - Gita (Little Yogi) - B1 Unscripted Delight
**Status:** PASS - send to editor, visual check first  
**Cut:** 40:55-41:19 (final 24s)  
**3-second hook (on-screen text):** Kid says meditation was too SHORT  
**Alt hook:** "It wasn't that long." - a child, right after meditation  
**Why it stops a parent:** Most parents expect a child to fidget through a calm-down activity; here the child volunteers that it wasn't long enough.

**Verbatim (from VTT, ASR errors left in on purpose):**
- `[40:55]` **TEACHER:** Very good. Now you can open your eyes. So how was it? Was it good?
- `[41:00]` **CHILD:** Yes, but
- `[41:01]` **CHILD:** I feel like it wasn't that long.
- `[41:06]` **TEACHER:** That's why we are not doing it for too long. Once you understand the drill and you understand how we are doing it, then we'll do it for longer time.

**Score:** 8.2 (hook 1.6 / authenticity 1.9 / parent value 1.5 / mute-legible 1.3 / feasibility 1.0 / warmth 0.9). Verifier re-score: 8.0.

**Geography fit:** India - High - parents want calm and focus without a lecture. GCC - Medium - fine if the chant audio is removed; religious context stays out of frame. US/UK/CA/AU - High - screen-time-guilty diaspora parents; 'my kid asked for MORE meditation' is the whole story.

**Compliance flags:**
- No child name spoken in this window (checked); Zoom tile may still show a name label - blur if visible
- Do not add any 'improves focus/anxiety' claim (X5/X6); the clip shows a child's reaction, nothing more
- Chant audio plays before 40:55 - start cut after it ends so no religious audio leaks into a GCC cut

**Editor must confirm on video:**
- [ ] Child camera ON with face visible at 41:00-41:05 (the reaction is the clip)
- [ ] Child expression reads as enthusiastic, not polite
- [ ] Background: no sibling/parent/room details (the same class has a baby-brother interruption at 42:25, just outside the cut)

**Editor instructions:** 9:16 crop on the child's tile, teacher in a small picture-in-picture only if her camera is live. Cold open: start on the child's line at 41:01 for ~3s with big caption 'It wasn't that long.' then jump back to 40:55 for the question, then play the teacher's reply to 41:19. Burn 2-line captions, highlight 'wasn't that long'. No background music (calm room tone only). Text end card: 'Real class. Real kid. Bambinos.live'. FALLBACK if the teacher's answer drags: end at 41:06 for a 10s reaction-only cut.

**Kill switch:** Child camera off or face not visible during 41:00-41:05

---

## ENG-02 - English - B2 Visible Learning
**Status:** PASS - send to editor, visual check first  
**Cut:** 12:26-12:28, 12:32-12:55 (final 25s)  
**3-second hook (on-screen text):** Watch him fix his own grammar  
**Alt hook:** 'I see... I saw.' 20 seconds in a real class  
**Why it stops a parent:** The child goes from 'I see' to 'I saw' mid-sentence right after a one-line nudge, which is the exact thing parents can't see happening in a school class of 40.

**Verbatim (from VTT, ASR errors left in on purpose):**
- `[12:26]` **TEACHER:** saw I saw.
- `[12:28]` **CHILD:** see.
- `[12:32]` **CHILD:** and I see turtles, I saw a crab, I saw a fish, I saw so many stuff and I saw sandwich and I saw a food and people and animals.

**Score:** 7.7 (hook 1.5 / authenticity 1.8 / parent value 1.9 / mute-legible 1.0 / feasibility 0.6 / warmth 0.9). Verifier re-score: 7.4.

**Geography fit:** India - High - spoken-English confidence is the #1 anxiety. GCC - High - same anxiety, English-medium schools. US/UK/CA/AU - Medium - lead with 'confidence' not 'fluency'.

**Compliance flags:**
- Teacher's lines around 12:18-12:24 are ASR-garbled; the correction is only real if the audio matches - re-listen before captioning
- Frame it as 'a moment from a real class', never 'learns grammar in 20 seconds' (X5)
- Within the same class the teacher guilt-trips the child later (16:29, 21:02, 30:18); this window is clean but see class_flags

**Editor must confirm on video:**
- [ ] Child camera ON, face visible
- [ ] Teacher's tile may be a still photo (the child asks about it at 8:55) - if so, do not show a 'teacher face' layout
- [ ] Hand-over-mouth or fidgeting that would read as discomfort

**Editor instructions:** Use the audio, not the ASR text, to write captions. Open on the child's final line, burn 'I see turtles, I saw a crab, I saw a fish' as karaoke captions and colour 'see' red then 'saw' green as they are spoken. Rewind 3s to show the teacher's nudge ('saw, I saw'). Trim the trailing 'Okay bye bye' (about 2s). 9:16 crop on the child. No music under speech. FALLBACK: if the correction is not audible, DROP (do not fake it).

**Kill switch:** Audio does not actually contain 'I see turtles, I saw a crab' with the see->saw switch

---

## ENG-01 - English - B5 Curiosity Spark
**Status:** PASS - send to editor, visual check first  
**Cut:** 10:43-11:06 (final 23s)  
**3-second hook (on-screen text):** 'Imagine a beach.' He saw an octopus. On the sand.  
**Alt hook:** This 'wrong' answer is why imagination class works  
**Why it stops a parent:** A funny, confident wrong answer ('I see a video of that') shows a child who is comfortable arguing with his teacher in English.

**Verbatim (from VTT, ASR errors left in on purpose):**
- `[10:43]` **TEACHER:** In the water you saw octopus on
- `[10:45]` **CHILD:** No, it's in the beach or to sand.
- `[10:52]` **TEACHER:** the sand. Quite strange.
- `[10:55]` **CHILD:** I see a video of that,
- `[10:58]` **TEACHER:** saw a video no in real did you see octopus can't be on the beach they'll die if they're on the beach okay

**Score:** 7.5 (hook 1.8 / authenticity 1.9 / parent value 1.3 / mute-legible 1.2 / feasibility 0.7 / warmth 0.6). Verifier re-score: 7.1.

**Geography fit:** India - High - spoken-English confidence + imagination. GCC - High. US/UK/CA/AU - Medium - the 'imagination' angle works, 'English' angle is weaker.

**Compliance flags:**
- CHILD_COMFORT is UNSURE: teacher says 'Quite strange' and 'they'll die' - confirm on video that the child is amused, not deflated (X3)
- Child's 10:45 line is partly garbled by ASR ('or to sand'); re-listen and re-caption
- Context before the clip (9:14-10:43) sets up 'imagine a beach'; the hook text must carry that or the clip is confusing on mute

**Editor must confirm on video:**
- [ ] Child expression at 10:52-10:58 (amused / defensive is fine, crestfallen is a kill)
- [ ] Child camera on, face visible; teacher may be a still photo
- [ ] Nothing identifying in the room

**Editor instructions:** Open with a 2s title card 'Teacher: Imagine you're at the beach.' then straight into the child's line. 9:16 crop on the child. Captions: write from audio. Cut at 11:06 on the teacher's 'okay'. Add a light sound-off-friendly emoji beat on 'I see a video of that' (a single octopus emoji, nothing else). Do NOT add mocking SFX.

**Kill switch:** Child looks embarrassed or the teacher's tone at 10:52-10:58 sounds sharp

---

## GITA-02 - Gita (Little Yogi) - B5 Curiosity Spark
**Status:** RESERVE (verifier re-score 6.8 < 7.0)  
**Cut:** 19:36-19:51, 20:03-20:12 (final 24s)  
**3-second hook (on-screen text):** Teacher stops the story at the scariest part  
**Alt hook:** 'Do you want Shiva to help this boy?'  
**Why it stops a parent:** The teacher turns a story into a question the child cares about ('yes, yes') and the child then describes the god's eyes unprompted, so the story is clearly landing.

**Verbatim (from VTT, ASR errors left in on purpose):**
- `[19:36]` **TEACHER:** But what about Shiva? Don't you think Shiva should come and help him?
- `[19:41]` **CHILD:** Yes,
- `[19:42]` **TEACHER:** What do you think? What do you want? You want Shiva to help him or not?
- `[19:46]` **CHILD:** yes,
- `[19:48]` **TEACHER:** You want Shiva to help this boy?
- `[19:50]` **CHILD:** yes, yes,
- `[20:03]` **TEACHER:** How do you think Shiva looks? the picture?
- `[20:06]` **CHILD:** the eyes look black and
- `[20:11]` **CHILD:** red.

**Score:** 7.2 (hook 1.6 / authenticity 1.6 / parent value 1.3 / mute-legible 1.1 / feasibility 0.7 / warmth 0.9). Verifier re-score: 6.8.

**Geography fit:** India - High - familiar story, devotional storytelling. GCC - Low - religion-specific, hold for local review. US/UK/CA/AU - High - diaspora parents looking for culture that isn't a lecture.

**Compliance flags:**
- The story is told over a screen-shared animated video (third-party content, X8) - the child's tile must be the visual, not the shared video
- Religious imagery: fine for India/diaspora, hold for GCC
- ASR garbles the story names elsewhere in the class; this window is clean

**Editor must confirm on video:**
- [ ] Child camera ON with face visible during 19:41-19:51 (the 'yes, yes' needs a face)
- [ ] What is on the shared screen during the cut - if it is the cartoon, crop it out entirely
- [ ] Lighting: the teacher notices the room is too dark at 22:29, so check that this earlier window is not also dark

**Editor instructions:** 9:16 crop on the child's tile only. Jump-cut: 19:36-19:51, then 20:03-20:12 (drop the 11s between). Caption the two questions in white, the child's answers in yellow. End on 'red.' with a beat of silence. No shared-screen footage. FALLBACK: if the child's camera is off, DROP - the clip has no value as audio.

**Kill switch:** Child's camera is off or the child's face is not visible

---

## SCI-01 - Science - B3 Child Speaks Up
**Status:** HOLD - re-transcribe  
**Cut:** 48:19-49:13 (final n/as)  
**3-second hook (on-screen text):** Why isn't petrol 'food' for a car?  
**Alt hook:** (parked until audio is re-transcribed)  
**Why it stops a parent:** The child reasons that fuel 'cannot repair ... growth', which is a real distinction between living and non-living things.

**Verbatim (from VTT, ASR errors left in on purpose):**
- `[48:19]` **CHILD:** Narlating machines use food to...
- `[48:25]` **TEACHER:** why is this fuel not considered food?
- `[48:56]` **CHILD:** it cannot repair part of course
- `[49:12]` **CHILD:** growth.

**Score:** 5.7 (hook 1.3 / authenticity 1.5 / parent value 1.6 / mute-legible 0.5 / feasibility 0.1 / warmth 0.7). Verifier re-score: 5.0.

**Geography fit:** India - Medium - concept lands, but teacher code-switches into Malayalam, so captions need a real transcript. GCC - Medium. US/UK/CA/AU - Medium.

**Compliance flags:**
- X10: ASR is not trustworthy here. Child's answer reads 'it does not provide a judgment, you have to put some costs in all the tests' before 'it cannot repair'; teacher lines are partly nonsense ('pet roller is the locker bench')
- 54s raw window is far too long; needs a re-transcribed 20s slice
- Dictionary-based ASR check scored this window as fine - only a human or a second ASR catches it

**Editor must confirm on video:**
- [ ] Everything - do not send to an editor until re-transcribed

**Editor instructions:** DO NOT SEND. Re-run the 48:10-49:20 slice through Whisper large-v3 or Gemini audio. If the child's sentence ('fuel can't repair the body or help it grow') is audible, re-score; otherwise DROP.

**Kill switch:** Second ASR does not reproduce the child's reasoning clearly

---
