import os
from openai import OpenAI

oa_api_key ="sk-jKGQkB5cMb_KqwcL16qnqMDJh6qN93ej-0HjF4zl5bT3BlbkFJ8KZBQlGcGK_seuWQjVWUiTw4CvQofs_JrWQh2gGtUA"

client = OpenAI(
    api_key="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",  # This is the default and can be omitted
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Say this is a test",
        }
    ],
    model="gpt-4o",
)