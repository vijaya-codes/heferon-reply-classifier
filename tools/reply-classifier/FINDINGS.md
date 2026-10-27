# Reply Classifier Findings

## Baseline test results

- Total pytest tests: 91
- Passed: 51
- Expected failures (xfail): 40
- Unexpected failures: 0
- Test dataset: 90 fictional reply cases across seven labels, plus one quoted-text test.

## Observed weaknesses

### 1. Bounce detection
Several delivery-failure messages are classified as `other`, including alternative wording and Afrikaans examples.

**Proposed fix:** Expand bounce patterns to cover common delivery failure, rejected recipient, and undeliverable-message wording.

### 2. Out-of-office detection
Some absence and automatic-reply phrases are classified as `other`.

**Proposed fix:** Expand out-of-office patterns and preserve header-based detection for automatic replies.

### 3. Opt-out detection
Some Afrikaans opt-out messages and alternative unsubscribe wording are classified as `other`.

**Proposed fix:** Add appropriate Afrikaans and English opt-out phrases.

### 4. Price detection
Some requests for rates, costs, estimates, and pricing are classified as `other`.

**Proposed fix:** Expand price-related keywords and phrases.

### 5. Interested detection
Several meeting requests and positive responses are classified as `other`.

**Proposed fix:** Expand interest and meeting-intent patterns without incorrectly matching unrelated replies.

### 6. Forwarded detection
Some forwarding messages are classified as `other`. One forwarding case is classified as `interested`, suggesting that rule order or pattern overlap needs review.

**Proposed fix:** Improve forwarding patterns and test rule priority against overlapping phrases.

## Follow-up work

1. Update the classifier rules in a separate change.
2. Rerun the complete pytest suite.
3. Remove `xfail` markers from cases that are fixed.
4. Keep any remaining expected failures documented with specific reasons.
5. Confirm all seven labels remain reachable and the automatic-reply header tests still pass.

# Reply Classifier Findings

## Test coverage

The test suite uses fictional email replies stored in `cases.json`. It checks the classifier's expected labels and includes a test for removing quoted reply text.

The latest test run reports:

- **63 passed**
- **28 xfailed** (known baseline failures)
- **0 unexpected failures**

## Improvements made

The classification rules were expanded to recognise additional wording, including:

- **Bounce:** delivery failures and undeliverable-message wording.
- **Price:** more variations of cost, pricing, fees, rates, and Afrikaans price questions.
- **Interested:** additional positive replies and requests for contact or information.
- **Forwarded:** additional wording about passing messages to managers or other contacts.
- **Opt-out:** more ways to decline contact, including Afrikaans wording.

The forwarded rule was also updated to recognise “Please speak to our practice manager”.

Twelve cases previously marked as expected failures now match their expected labels and have had their `xfail` markers removed.

## Known limitations

Twenty-eight cases remain marked as expected failures. These represent classification gaps that need further investigation. The `xfail` markers allow the suite to pass while making those known gaps visible.

The classifier uses keyword and regular-expression rules, so context and negation can still cause incorrect labels. For example, a message asking not to receive a quote could be mistaken for a pricing enquiry if the rules are not sufficiently specific.

The `strip_quoted` helper is tested separately; the classifier does not currently call it before matching rules.

## Suggested next steps

1. Review the 28 remaining expected failures and group them by cause.
2. Improve the rules carefully, keeping existing passing cases green.
3. Remove each `xfail` marker when its case is correctly classified.
4. Keep all examples fictional and avoid storing real email content or personal information.
