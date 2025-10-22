import os
from google import genai
from google.genai import types

api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(
    api_key=api_key,
)

model = "gemini-flash-lite-latest"

# 会話履歴を保持するリスト
conversation_history = []


def generate(prompt: str) -> str:
    # ユーザーのメッセージを履歴に追加
    conversation_history.append(
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=prompt),
            ],
        )
    )

    generate_content_config = types.GenerateContentConfig()

    response = client.models.generate_content(
        model=model,
        contents=conversation_history,
        config=generate_content_config,
    )

    # AIの応答を履歴に追加
    conversation_history.append(
        types.Content(
            role="model",
            parts=[
                types.Part.from_text(text=response.text),
            ],
        )
    )

    return response.text


if __name__ == "__main__":
    result = generate("私は田中です")
    print("--- 生成結果1 ---")
    print(result)
    print("------\n")

    result = generate("私の名前を教えてください。")
    print("--- 生成結果2 ---")
    print(result)
    print("------\n")
