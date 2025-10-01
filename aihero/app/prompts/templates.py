# Input template for evaluation prompts using XML-style formatting
user_prompt_template = """
<INSTRUCTIONS>
{instructions}
</INSTRUCTIONS>

<QUESTION>
{question}
</QUESTION>

<LOG>
{log}
</LOG>

<ANSWER>
{answer}
</ANSWER>
""".strip()

# Input template for question generation from chunks
qg_prompt_template = """
You are helping to create test questions for an AI agent.

Based on the provided content (<CONTENT>), generate **one** realistic question.

Output only the question text.
""".strip()
