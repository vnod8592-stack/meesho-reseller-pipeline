# Meesho Reseller Analytics Pipeline

## Project Overview

This project analyzes reseller order data using SQL, Python guardrails, a reliable narrative layer, and a mock agent workflow.

The workflow is:

SQL → Python Guardrails → Narrative → Agent → Human Approval

## Project Parts

### Part 1 — SQL Business Query Engine

SQL is used to calculate:

- Monthly category revenue
- Region revenue
- Top 5 resellers
- Zero-order resellers
- June delivered Average Order Value

Run:

```powershell
python part1_sql/run_queries.py