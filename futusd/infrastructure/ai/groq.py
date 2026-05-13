from groq import AsyncGroq
from groq.types.chat import ChatCompletionUserMessageParam, ChatCompletionSystemMessageParam

from futusd.domain.entities import SpendingDM
from futusd.application.promt import ANALYZE_SPENDING_PROMPT, SYSTEM_PROMPT

class GroqAdapter:
    def __init__(self, api_key: str):
        self._client = AsyncGroq(api_key=api_key)

    async def analyze_saver(self, spending: list[SpendingDM]) -> str:
        text = "\n".join([
            f"{s.category}: {s.base} RUB"
            for s in spending
        ])
        total = sum(s.base for s in spending)

        response = await self._client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                ChatCompletionSystemMessageParam(role="system", content=SYSTEM_PROMPT),
                ChatCompletionUserMessageParam(
                    role="user",
                    content=ANALYZE_SPENDING_PROMPT.format(text=text, total=total)
                )
            ]
        )
        result = response.choices[0].message.content
        return result.replace("\n", "").strip()