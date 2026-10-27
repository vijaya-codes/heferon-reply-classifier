import json
from pathlib import Path

# 12 fictional examples per label; no real emails or personal data.
groups = {
    "bounce": [
        ("Delivery has failed", {}),
        ("Undeliverable message", {}),
        ("The recipient address was rejected", {}),
        ("Your message could not be delivered", {}),
        ("Mail delivery subsystem: failure", {}),
        ("This mailbox does not exist", {}),
        ("Delivery status notification: failure", {}),
        ("The email address was not found", {}),
        ("E-pos aflewering het misluk", {}),
        ("Die boodskap kon nie afgelewer word nie", {}),
        ("Die e-posadres bestaan nie", {}),
        ("Aflewering is onsuksesvol", {}),
    ],
    "ooo": [
        ("I am out of office until Monday", {}),
        ("I am away from my desk", {}),
        ("Automatic reply: annual leave", {}),
        ("I will respond when I return", {}),
        ("Currently on vacation", {}),
        ("I am unavailable today", {}),
        ("Out of the office this week", {}),
        ("I will reply after my leave", {}),
        ("Ek is tans met verlof", {}),
        ("Ek is nie vandag beskikbaar nie", {}),
        ("Ek sal antwoord wanneer ek terug is", {}),
        ("I am away", {"auto-submitted": "auto-replied"}),
    ],
    "optout": [
        ("No thanks, unsubscribe me", {}),
        ("Please remove me from your list", {}),
        ("Stop emailing me", {}),
        ("We are not interested", {}),
        ("Do not contact us again", {}),
        ("Not for us, thank you", {}),
        ("Nee dankie", {}),
        ("Verwyder my asseblief van die lys", {}),
        ("Ons stel nie belang nie", {}),
        ("Moet asseblief nie weer e-pos stuur nie", {}),
        ("Please take us off your mailing list", {}),
        ("I do not want further emails", {}),
    ],
    "price": [
        ("Please send your pricing", {}),
        ("What does the service cost?", {}),
        ("Could you share your rates?", {}),
        ("Please provide a quote", {}),
        ("Can you send a price list?", {}),
        ("We would like a cost estimate", {}),
        ("Wat kos die diens?", {}),
        ("Stuur asseblief julle pryse", {}),
        ("Kan ek 'n kwotasie kry?", {}),
        ("Wat is julle tariewe?", {}),
        ("Please send details of your fees", {}),
        ("We need an estimate of the price", {}),
    ],
    "interested": [
        ("I am interested", {}),
        ("Please tell me more", {}),
        ("Can we arrange a meeting?", {}),
        ("I would like to discuss this", {}),
        ("This sounds useful", {}),
        ("Please contact me about next steps", {}),
        ("Ek stel belang", {}),
        ("Vertel my asseblief meer", {}),
        ("Kan ons 'n afspraak maak?", {}),
        ("Dit klink interessant", {}),
        ("I would like more information", {}),
        ("Let's discuss this further", {}),
    ],
    "forwarded": [
        ("I will forward this email", {}),
        ("Please contact our manager", {}),
        ("I have forwarded your message", {}),
        ("I will pass this on", {}),
        ("Forwarding this to the owner", {}),
        ("Please speak to our practice manager", {}),
        ("Ek stuur die e-pos aan", {}),
        ("Ek het jou boodskap aangestuur", {}),
        ("Ek sal dit aanstuur", {}),
        ("Kontak asseblief die bestuurder", {}),
        ("I will ask the owner to contact you", {}),
        ("Please pass this to the relevant person", {}),
    ],
    "other": [
        ("Hello there", {}),
        ("Thank you for your message", {}),
        ("Have a nice day", {}),
        ("I received your email", {}),
        ("We will consider it", {}),
        ("Please see my note below", {}),
        ("Goeie dag", {}),
        ("Dankie vir jou e-pos", {}),
        ("Ek het jou boodskap ontvang", {}),
        ("Lekker dag verder", {}),
        ("We are reviewing the information", {}),
        ("Thanks for getting in touch", {}),
    ],
}

cases = []
for label, examples in groups.items():
    for number, (text, headers) in enumerate(examples, start=1):
        cases.append({
            "id": f"{label}-{number:03}",
            "subject": "",
            "text": text,
            "headers": headers,
            "expected": label,
        })

# Additional tricky cases: expected results follow the label priority.
cases.extend([
    {
        "id": "tricky-001",
        "subject": "Automatic reply",
        "text": "I am away until Monday",
        "headers": {"auto-submitted": "auto-replied"},
        "expected": "ooo",
    },
    {
        "id": "tricky-002",
        "subject": "",
        "text": "Please stop contacting us",
        "headers": {"x-autoreply": "yes"},
        "expected": "ooo",
    },
    {
        "id": "tricky-003",
        "subject": "",
        "text": "Your message could not be delivered",
        "headers": {},
        "expected": "bounce",
    },
    {
        "id": "tricky-004",
        "subject": "",
        "text": "Not interested in receiving a quote",
        "headers": {},
        "expected": "optout",
    },
    {
        "id": "tricky-005",
        "subject": "",
        "text": "We are interested; please send your pricing",
        "headers": {},
        "expected": "price",
    },
    {
        "id": "tricky-006",
        "subject": "",
        "text": "I will forward this to the manager",
        "headers": {},
        "expected": "forwarded",
    },
])

output = Path("tools/reply-classifier/cases.json")
output.write_text(
    json.dumps(cases, indent=2, ensure_ascii=False) + "\n",
    encoding="utf-8",
)
print(f"Created {len(cases)} test cases in {output}")
