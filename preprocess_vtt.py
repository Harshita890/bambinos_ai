#!/usr/bin/env python3
"""
preprocess_vtt.py  --  Step 2 of the Bambinos clip-mining pipeline.

What it does (no LLM involved, so it is free and deterministic):
  1. Parses a WebVTT class transcript.
  2. Works out who is the teacher vs. the child (teacher = most words spoken).
  3. Pseudonymises names -> TEACHER / CHILD, so child PII never reaches an LLM or a Sheet.
  4. Cuts the class into ~60-second windows and gives each one:
       - asr_quality   (0-1) how much the text looks like real English. Low = re-transcribe before trusting a quote.
       - visual_risk   hints: phrases that suggest camera-off / screen-share / interruptions / glitches.
       - admin_hit     price, schedule, payment, location talk (hard-exclusion material).
       - tone_hit      shaming or guilt-trip language from the teacher.
  5. Writes <session>.clean.txt (what the LLM reads) and <session>.windows.jsonl (the flags).

Usage:
  python preprocess_vtt.py path/to/Class.vtt out_dir [--alias Name1,Name2,...]

--alias is for names the ASR spelled differently from the speaker label
(e.g. a child's name that shows up as "Zyan", "Zion" and "Ziyang" in the same class).
"""
import re, sys, json, os, collections

STOP = set("""the a an and or but if so of to in on at for with from by as is are was were be been am i you he she it we they me my your his her
our their this that these those there here what which who whom when where why how do does did done not no yes can could will would should
have has had just very okay ok oh well now then than too also all some any one two get got go going gone come let us""".split())

VISUAL_PATTERNS = {
    "camera_or_screen": r"\b(can you see|do you see|see my screen|share (the |my )?screen|sharing the screen|show (me|my)|turn on|camera|i can'?t see|you'?re (a )?mute|muted|unmute|video on your screen|play the video|watch the video|clip)\b",
    "interruption":     r"\b(somebody('?s| is) at the door|someone('?s| is) at the door|one moment|mommy|mummy|baby brother|noise|disturb)\b",
    "lighting_env":     r"\b(too dark|dark room|light turned|my light|background)\b",
    "tech_glitch":      r"\b(rejoin|can'?t hear|couldn'?t hear|not working|wrong button|freez|lag)\b",
    "off_screen_work":  r"\b(notebook|write (it )?down|take out|pencil|worksheet)\b",
}
ADMIN_PATTERNS = r"(\bprice\b|\bfees?\b|\bpayment\b|\bpaid\b|\$\s?\d+|₹|\bfree slot\b|\bslot\b|\binvoice\b|\brefund\b|\baddress\b|\btrivandrum\b|\bbangalore\b|\bkerala\b|\bwhatsapp\b)"
# Tone: teacher-to-child shaming / guilt-trips only. (An earlier draft flagged "very angry" about a god in a story
# and "Silly me" said by the teacher about herself - both false positives. This list is a REVIEW FLAG, not a verdict.)
TONE_PATTERNS = r"(silly,? silly|silly simple|it'?s stupid|wastage|how many times do i|not (at all )?(learning|understanding)|why you don'?t study|i will not (teach|say)|really very naughty|beings are naughty|i'?ll cry now|making me (so )?sad|i'?m (very )?angry|i am (very )?angry)"

def ts(h, m, s):
    return int(h) * 3600 + int(m) * 60 + int(s)


def load_vtt(path):
    raw = open(path, encoding="utf-8").read().split("\n\n")
    cues = []
    for block in raw[1:]:
        lines = block.strip().split("\n")
        if len(lines) < 3:
            continue
        m = re.match(r"(\d+):(\d+):(\d+)\.\d+ --> (\d+):(\d+):(\d+)\.\d+", lines[1])
        if not m:
            continue
        txt = " ".join(lines[2:]).strip()
        sp, sep, body = txt.partition(": ")
        if not sep:
            sp, body = "UNKNOWN", txt
        cues.append(dict(start=ts(*m.group(1, 2, 3)), end=ts(*m.group(4, 5, 6)), speaker=sp.strip(), text=body.strip()))
    return cues


def roles(cues):
    """Teacher = the named speaker with the most words, unless the file already labels someone 'Child'/'Student'.
    (In the English sample the child out-talks the teacher, so word count alone gets it wrong.)"""
    words = collections.Counter()
    for c in cues:
        words[c["speaker"]] += len(c["text"].split())
    kid_labels = {s for s in words if s.strip().lower() in ("child", "student", "kid")}
    candidates = [s for s in words if s not in kid_labels]
    teacher = max(candidates, key=lambda s: words[s]) if candidates else words.most_common(1)[0][0]
    return teacher, words


def pseudonymise(cues, teacher, aliases):
    names = set()
    for sp in {c["speaker"] for c in cues}:
        for part in re.split(r"\s+", sp):
            if len(part) > 2 and part.lower() != "child":
                names.add(part)
    names |= {a.strip() for a in aliases if a.strip()}
    pat = None
    if names:
        pat = re.compile(r"\b(" + "|".join(sorted(map(re.escape, names), key=len, reverse=True)) + r")\b", re.I)
    out = []
    for c in cues:
        role = "TEACHER" if c["speaker"] == teacher else "CHILD"
        t = pat.sub("[NAME]", c["text"]) if pat else c["text"]
        out.append({**c, "role": role, "text": t})
    return out


_LEX = None
def _lexicon():
    """English word list from Hunspell (ships with most Linux boxes / LibreOffice). Falls back to None."""
    global _LEX
    if _LEX is None:
        _LEX = set()
        for path in ("/usr/share/hunspell/en_US.dic", "/usr/share/myspell/en_US.dic"):
            if os.path.exists(path):
                for line in open(path, encoding="utf-8", errors="ignore").read().splitlines()[1:]:
                    _LEX.add(line.split("/")[0].lower())
                break
    return _LEX

def _known(tok, lex):
    t = tok.replace("'s", "").replace("n't", "").replace("'ll", "").replace("'m", "").replace("'re", "").replace("'ve", "").replace("'d", "")
    if t in lex or t + "n" in lex: return True
    for suf, rep in (("s", ""), ("es", ""), ("ed", ""), ("ed", "e"), ("ing", ""), ("ing", "e"), ("ly", ""), ("ies", "y"), ("er", ""), ("est", ""), ("ness", "")):
        if t.endswith(suf) and (t[: -len(suf)] + rep) in lex:
            return True
    if len(t) > 3 and t[-1] == t[-2] and t[:-1] in lex: return True   # running -> run
    return False

def asr_quality(text):
    """1.0 = reads like normal English. Lower = many words that are not English
    (transliterated Malayalam/Hindi, mangled names, ASR soup). Share of in-dictionary words, rescaled so ~0.93 -> 1.0."""
    lex = _lexicon()
    toks = [t for t in re.findall(r"[a-zA-Z']+", text.lower()) if len(t) > 2]
    if len(toks) < 8 or not lex:
        return None
    known = sum(_known(t, lex) for t in toks) / len(toks)
    return round(min(1.0, known / 0.93), 2)


def windows(cues, size=60):
    if not cues:
        return []
    end = max(c["end"] for c in cues)
    res = []
    for w0 in range(0, end + 1, size):
        sel = [c for c in cues if w0 <= c["start"] < w0 + size]
        if not sel:
            continue
        text = " ".join(c["text"] for c in sel)
        vis = {k: bool(re.search(p, text, re.I)) for k, p in VISUAL_PATTERNS.items()}
        res.append(dict(
            t0=w0, t1=w0 + size, label=f"{w0 // 60}:{w0 % 60:02d}",
            child_words=sum(len(c["text"].split()) for c in sel if c["role"] == "CHILD"),
            teacher_words=sum(len(c["text"].split()) for c in sel if c["role"] == "TEACHER"),
            asr_quality=asr_quality(text),
            visual_risk=[k for k, v in vis.items() if v],
            admin_hit=bool(re.search(ADMIN_PATTERNS, text, re.I)),
            tone_hit=bool(re.search(TONE_PATTERNS, text, re.I)),
        ))
    return res


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    path, out = sys.argv[1], sys.argv[2]
    aliases = sys.argv[sys.argv.index("--alias") + 1].split(",") if "--alias" in sys.argv else []
    os.makedirs(out, exist_ok=True)
    stem = os.path.splitext(os.path.basename(path))[0]
    cues = load_vtt(path)
    teacher, wc = roles(cues)
    cues = pseudonymise(cues, teacher, aliases)
    wins = windows(cues)
    with open(f"{out}/{stem}.clean.txt", "w") as f:
        for c in cues:
            f.write(f"[{c['start'] // 60}:{c['start'] % 60:02d}-{c['end'] // 60}:{c['end'] % 60:02d}] {c['role']}: {c['text']}\n")
    with open(f"{out}/{stem}.windows.jsonl", "w") as f:
        for w in wins:
            f.write(json.dumps(w) + "\n")
    qs = sorted(w["asr_quality"] for w in wins if w["asr_quality"] is not None)
    med = qs[len(qs) // 2] if qs else "n/a"
    print(f"{stem}: {len(cues)} cues, {len(wins)} windows | speakers by words: {dict(wc)}")
    print(f"   median ASR quality {med} | windows <0.70: {sum(q < 0.70 for q in qs)}/{len(qs)}"
          f" | admin windows: {sum(w['admin_hit'] for w in wins)} | tone-flag windows: {sum(w['tone_hit'] for w in wins)}"
          f" | visual-risk windows: {sum(bool(w['visual_risk']) for w in wins)}")


if __name__ == "__main__":
    main()
