from groq import AsyncGroq
from groq.types.chat import ChatCompletionUserMessageParam, ChatCompletionSystemMessageParam

from futusd.config import GroqConfig
from futusd.domain.entities import SpendingDM
from futusd.application.promt import ANALYZE_SPENDING_PROMPT, SYSTEM_PROMPT

class GroqAdapter:
    def __init__(self, groq_config: GroqConfig):
        self._client = AsyncGroq(api_key=groq_config.api_key)
        self._model = groq_config.model

    async def analyze_saver(self, spending: list[SpendingDM]) -> str:
        text = "\n".join([
            f"{s.category}: {s.base} RUB"
            for s in spending
        ])
        total = sum(s.base for s in spending)

        response = await self._client.chat.completions.create(
            model = self._model,
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