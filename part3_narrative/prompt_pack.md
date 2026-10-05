# Reliable AI Narrative Prompt Pack

## Trigger

Run this narrative step only after the SQL output has been validated by the Python guardrail engine.

The input must contain verified monthly category revenue and the calculated MoM growth values.

## Inputs

The narrative step receives:

- Month being analyzed
- Previous-month revenue by category
- Current-month revenue by category
- Calculated MoM percentage
- Flag status from the guardrail engine
- Category name
- Verified revenue values from SQL

## Prompt

You are a business analyst creating a concise reseller-performance narrative.

Use only the verified values provided in the input.

For each flagged category:

1. State the verified MoM change.
2. Clearly separate facts from possible explanations.
3. Explain the business implication.
4. Suggest a reasonable next action.
5. Do not invent data, causes, or customer behaviour.

Use the following structure:

### Context
State the verified business result.

### Insight
Explain what the change means. Label explanations as hypotheses when they are not directly supported by the data.

### Implication
Explain why the result matters to the business.

### Action
Suggest a practical next step based only on the available evidence.

Do not introduce unsupported facts or numerical values.

## Checklist

Before accepting the narrative, verify:

- [ ] All numerical values match the verified SQL/Python output.
- [ ] Facts and hypotheses are clearly separated.
- [ ] No unsupported causes are presented as facts.
- [ ] The business implication is clear.
- [ ] The recommended action is relevant to the observed change.
- [ ] No raw reseller names are exposed in the external narrative.