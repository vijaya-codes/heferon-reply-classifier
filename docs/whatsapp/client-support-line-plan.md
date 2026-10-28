WhatsApp Client Support Line — Implementation Plan

Scope and rules
Build in the client's repository using the WhatsApp Business Platform (Meta Cloud API). The line responds only to customer-initiated messages. No broadcasts, marketing, or alerts. Because the client's business involves paid-entry prize games, check the current WhatsApp Business Messaging Policy before launch. This restriction is fixed.

Eugene and the client will confirm the final flows before implementation.

Support flows
Welcome/menu: Customer sends a message → bot welcomes them and lists support options → customer selects an option.

FAQs: Customer selects a question → bot returns the approved answer → ends or returns to menu.

Sign-up: Customer asks how to sign up → bot shares the approved client website link → ends.

Refunds/other queries: Customer asks about a refund or another issue → bot provides approved guidance or offers human support → ends or hands over.

Human handover: Customer requests a person or needs help the bot cannot provide → bot confirms the handover → authorised staff see the customer's number, message, relevant conversation context, and reason for handover in a restricted support view → staff respond manually.

STOP/START: Customer sends STOP → record opt-out and suppress further automated replies. START may re-enable support replies according to the agreed rules. Never use START as permission for marketing.

Meta setup
Create/configure a Meta developer app with the WhatsApp product.

Start with Meta's free test phone number and authorised test recipients.

Configure a public HTTPS webhook URL, verification token, and incoming-message subscription.

Configure approved message templates only if a permitted reply is needed outside the 24-hour customer-service window.

Before production, the client completes required business verification and real-number/WhatsApp Business Account setup. Obtain only developer-level app access; do not use live numbers or customer data before approval.

Webhook and security
Verify Meta's webhook challenge during setup. Validate X-Hub-Signature-256 against the raw request body using the app secret on every POST; reject invalid signatures. Deduplicate using the WhatsApp message ID and acknowledge/process webhooks promptly within Meta's requirements. Handle retries safely and log errors without exposing message contents or secrets.

Keep tokens in environment secrets, not source control. Test invalid signatures, duplicate events, STOP/START, timeouts, and failed sends.

Privacy (POPIA)
Store only what is needed: WhatsApp ID/number, opt-out status, message ID, minimal recent context, handover status, and timestamps. Avoid storing unnecessary message history or sensitive information. Encrypt data in transit and at rest, restrict access to authorised support staff, and set a deletion period with the client before launch. Document access and deletion procedures.

Inputs needed from Eugene/client
Repository access after plan approval; Meta app developer role only.

Confirmed flow list and escalation/contact process.

Approved FAQs, refund wording, sign-up URL, welcome/menu text, and STOP/START wording.

Decision on support staff access, data retention period, hosting, and who handles escalations.

Client to complete production business verification and approve any required templates.

Estimate and Friday deliverable
Step

Estimate

Policy/API research and plan

2 h

Repository setup and webhook skeleton

2–3 h

Flow implementation

4–6 h

Security, privacy and automated tests

3–4 h

Test-number integration and documentation

2 h

Total after access and approvals

13–17 h

By Friday: submit this plan as a pull request, confirm dependencies, and demonstrate a proposed test checklist. Implementation is conditional on approval and access; no live-number or real-customer-data work beforehand.

Done when: Eugene approves the plan in a pull-request comment.