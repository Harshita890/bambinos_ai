# What the pipeline threw away, and why

Reading this is as important as reading the briefs. A filter you can't audit is just a slot machine.

## Class-level verdicts

| Class | Child share of words | Verdict | One-line reason |
|---|---|---|---|
| English 2125604619 | 51% | 2 PASS, several drops | Lots of child talk, but the teacher guilt-trips three times (16:29, 21:02, 30:18) so every clip needs a tone check |
| Gita 2125422751 | 19% | 1 PASS, 3 RESERVE | Warm teacher, good story engagement; religion + shared-screen video + a dark room limit what is usable |
| Science 2125687282 | 11% | 0 PASS, 1 HOLD | Teacher code-switches into Malayalam; ASR is soup; ~6 minutes of the class is a scheduling chat |
| Maths 2125736982 | 4% | **ZERO moments, escalate** | Teacher talks 96% of the words and repeatedly shames the child. Not an ad class. A coaching-needed class. |

## Maths (zero-moment class) - detail

Nothing here is usable, and that is the *right* output. These are the exclusion triggers (X3, X4, X5, X7) the Miner would hit, with the timestamps an Academics lead could jump to:

- 25:17 "It's stupid. I explained it taking 5-10 minutes..." (X4)
- 35:09 "Simple, simple, silly, silly things" / 37:40 "how many times do I need to say" (X4)
- 38:14-38:26 threatens to stop teaching; 39:07 "why you don't study at home?" (X4)
- 39:44 "it's the complete wastage for me to say anything" (X3/X4)
- 45:52-46:14 compares today's score with a future "full zero" (X4)
- 47:54 brings the child's father into it (X1/X4)
- 48:30 "I will ask you what to teach..." (X4, sarcasm)
- The only child words in the whole class are ~155 words out of ~3,900. There is no child-led moment to find.

**Recommendation:** the same run that returns `[]` should push a row to a private "Teacher-tone review" tab for the Academics lead. The ad pipeline accidentally becomes a free quality monitor. This is not a pipeline output I'd share with the wider marketing team.

## Individual candidates that were dropped or parked

| Where | What it is | Result | Why |
|---|---|---|---|
| English 1:36-2:44 | Child chooses between a dance competition and a cricket tournament abroad | DROP (X1) | A fun, very natural exchange, but the child names where he is travelling and when. Travel plans are location data on a minor. |
| English 3:19-4:16 | "Which beach?" / "You have to know the name" | DROP | Charming, but the teacher pushes ("You have to know the name") and the ASR on the child's reply is unreliable |
| English 16:29, 21:02, 30:18 | Teacher: "not talking to you today", "I'll cry now", "I'm very angry today" | DROP (X4) | Guilt-trip tone. Also marks the whole class for a tone review |
| English 23:13-23:48 | Door interruption, child says "they paid $100" | DROP (X2, X7) | Payment mention plus someone else at the door |
| English 37:57 | "I saw what mommy just did..." | DROP (X7) | Parent in frame/audible |
| Gita 22:25-22:48 | Teacher notices "it's too dark in your room... not good to watch your screen in a dark room" | RESERVE 6.5 | Lovely Teacher-Knows-My-Child moment (B4). But the footage is dark by definition, shows a child's room, and the eyesight line drifts toward a health claim (X6). Needs a light-fixed re-cut or a voice-over version. |
| Gita 26:14-28:22 | "Why do we pray?" -> "because he is brave" | RESERVE 6.3 | Strong values moment (B6), but it is a 70s teacher monologue; 12-25s cut loses the point. Better as a carousel quote. |
| Gita 36:58-37:29 | Child says her birthday is in January; teacher says "January 21" | DROP (X1) | Birthday is PII, however sweet |
| Gita 45:04-45:27 | Child's attempt at "Saraswati" | DROP (X3, X10) | Child mispronounces a deity's name; ASR renders it as something that could be read badly. Embarrassment risk. |
| Gita 41:43-42:29 | Child forgets the breath question, baby brother noise | DROP (X7) | Sibling audible |
| Science 35:41-41:26 | Teacher and child discuss class schedule, "how old are you?" | DROP (X1, X2) | Admin chat and personal details, ~6 minutes |
| Science 52:05 | "Trivandrum based... Bangalore based" | DROP (X1) | Location |
| Science 46:20 | Child says "I didn't understand" | RESERVE (human only) | Actually a great B3 moment (a child safe enough to say it, the reverse of Maths). But the ASR around it is unreadable. Re-transcribe first. |
| Science 29:05-30:57 | Two-boys-and-a-robot "soup" explainer | DROP | The teacher is reading slide text; child barely speaks |

## What this says about hit-rate

4 classes -> 2 classes with a transcript-level PASS (50%), 3 PASS clips + 1 RESERVE + 1 HOLD. After the video check I'd expect somewhere around half of the PASS clips to survive. That is the number I'd measure properly in the first 30 days instead of assuming it (see the rollout plan).
