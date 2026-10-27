
from __future__ import annotations

import re
from typing import Dict, List, Tuple

_RULES: List[Tuple[str, re.Pattern]] = [
    (
        "bounce",
        re.compile(
            r"mailer-daemon|postmaster|delivery status notification|undeliverable|"
            r"returned mail|delivery has failed|delivery failed|address not found|"
            r"could not be delivered|message was rejected|recipient address rejected|"
            r"mailbox unavailable|aflewering het misluk|boodskap kon nie afgelewer word nie",
            re.I,
        ),
    ),
    (
        "ooo",
        re.compile(
            r"out of (the )?office|automatic reply|auto-?reply|autoreply|"
            r"on (annual )?leave|away until|afwesig|outomatiese antwoord|"
            r"nie op kantoor|limited access to (my )?email|"
            r"currently unavailable|back on \w+day|ek is met verlof|"
            r"ek is nie beskikbaar nie",
            re.I,
        ),
    ),
    (
        "optout",
        re.compile(
            r"\bno,? thanks?\b|\bnot interested\b|\bunsubscribe\b|"
            r"remove (me|us)|take (me|us) off|^\s*stop\b|"
            r"do not (contact|email)|don'?t (contact|email)|"
            r"\bnee,? dankie\b|nie belangstel|verwyder (my|ons)|"
            r"we already have|not for us|not required|"
            r"please stop|no further emails|do not send (me|us)|"
            r"moet my nie (kontak|e-pos) nie|verwyder my van die lys",
            re.I | re.M,
        ),
    ),
    (
        "price",
        re.compile(
            r"how much|what('?s| is| does) (the |it )?cost|"
            r"\bprice\b|pricing|\bquote\b|\bfees?\b|"
            r"\bcosts?\b|\brates?\b|\bestimate\b|"
            r"hoeveel|\bprys\b|\bkoste\b|kwotasie|tariewe|"
            r"wat kos|wat is julle tariewe",
            re.I,
        ),
    ),
    (
        "interested",
        re.compile(
            r"^\s*(yes|ja)\b|\binterested\b|\bkeen\b|sounds good|"
            r"\bsure\b|tell me more|more info|more information|"
            r"\bcall me\b|give (me|us) a call|"
            r"please (call|phone) (me|us)|please contact (me|us)|"
            r"come (past|in|by)|when (can|could) you|"
            r"let'?s (chat|talk|meet)|\bbook\b|\bvisit\b|"
            r"\bgraag\b|bel (my|ons)|stuur (meer )?inligting|"
            r"klink goed|ek stel belang|maak gerus 'n afspraak",
            re.I | re.M,
        ),
    ),
    (
        "forwarded",
        re.compile(
            r"forward(ed|ing)? (it|this|the e-?mail)|"
            r"pass(ed)? (it|this) on|i'?ll pass|"
            r"stuur (die )?e-?pos aan|aangestuur|"
            r"will (let|ask) (the )?(doctor|dr|owner|manager)|"
            r"speak to (the |our )?(doctor|dr|owner|manager)|"
           r"contact (our|the) (manager|owner|practice manager)|"
r"speak to (our|the) (practice manager|manager|owner)|"
            r"sent this to (the |our )?(team|manager|doctor)|"
            r"ek sal dit aanstuur|ek sal dit deurgee|"
            r"ek sal met die (eienaar|bestuurder|dokter) praat",
            re.I,
        ),
    ),
]


def strip_quoted(text: str) -> str:
    out = []
    for line in (text or "").splitlines():
        s = line.strip()
        if s.startswith(">"):
            continue
        if re.match(
            r"^(on .{5,120} wrote:|op .{5,120} (geskryf|het geskryf):|-{2,}\s*original message|"
            r"from: .+@|sent from my|-----)",
            s,
            re.I,
        ):
            break
        out.append(line)
    return "\n".join(out).strip()


def classify(subject: str, body: str, headers: Dict[str, str]) -> str:
    auto = (headers.get("auto-submitted") or "").lower()
    if (auto and auto != "no") or headers.get("x-autoreply") or headers.get("x-autorespond"):
        return "ooo"

    blob = f"{subject}\n{body}"
    for label, rx in _RULES:
        if rx.search(blob):
            return label
    return "other"
