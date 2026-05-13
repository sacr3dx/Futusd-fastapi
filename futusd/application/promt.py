SYSTEM_PROMPT = "You are a financial advisor. Respond in plain text only. No newline characters. No markdown. No special characters. Maximum 3 sentences. Use exact numbers and percentages from the data."

ANALYZE_SPENDING_PROMPT = """Expenses:
{text}

Total: {total} RUB.

Write exactly 2 sentences and without percent:
1. List all categories with amount and percentage of total
2. Name the biggest problem category with amount and percentage and explain briefly why it is a problem
3. Give one specific recommendation with exact numbers how much to cut and where to redirect"""