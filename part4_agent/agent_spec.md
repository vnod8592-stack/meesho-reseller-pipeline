# Agent Workflow Specification

## Purpose

The mock agent takes a monthly category revenue feed, validates it, calculates month-over-month growth, identifies important changes, and prepares a small number of draft messages.

The agent does not send messages automatically. All drafted messages are held for human approval.

## Workflow

The agent follows these steps in order:

1. **Intake and validate**
   - Read the input feed.
   - Run the Part 2 validation function.

2. **Hard stop invalid feeds**
   - If validation fails, stop the workflow.
   - Return the validation errors.
   - Do not calculate alerts or draft messages.

3. **Calculate MoM growth**
   - Compare the current month with the previous month.
   - Use the existing `mom_growth()` function.

4. **Identify flagged categories**
   - Use the existing `is_flagged()` function.
   - Categories with absolute growth greater than 8% are flagged.

5. **Sort flagged categories**
   - Sort flagged categories by the absolute value of MoM growth, from largest to smallest.

6. **Draft up to 3 messages**
   - Draft messages only for the three largest flagged movements.
   - Include the category and verified MoM percentage.

7. **Suppress remaining flagged categories**
   - Flagged categories outside the top three are placed in `suppressed_categories`.

8. **Escalate exact boundary**
   - A category with exactly +8% or -8% growth is placed in `escalated_categories`.
   - It is not treated as a normal flagged category.

## Human Approval

The agent only prepares drafts.

The final action is:

`drafted_and_held_for_approval`

A human must review and approve any message before it could be sent.

## JSON Output

The runner returns:

```json
{
  "run_month": "...",
  "validation_status": "valid",
  "validation_errors": [],
  "flagged_categories": [],
  "suppressed_categories": [],
  "escalated_categories": [],
  "action_taken": "drafted_and_held_for_approval"
}
```

For an invalid feed, the action is:

`hard_stop`

No messages are drafted from an invalid feed.

## Safety Rules

- Use verified SQL/Python values only.
- Do not invent business numbers.
- Do not ignore validation errors.
- Do not automatically send messages.
- Draft no more than three notifications.
- Keep exact-boundary cases separate for escalation.
- Keep the workflow deterministic and reproducible.