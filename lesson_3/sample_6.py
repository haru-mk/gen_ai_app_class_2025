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

def chat():
    print("Geminiとの会話を開始します。「終了」と入力すると会話を終了します。")
    print("--------------------")
    
    while True:
        user_input = input("あなた: ")
        
        if user_input.lower() == "終了":
            print("会話を終了します。")
            break
            
        try:
            response = generate(user_input)
            print("Gemini:", response)
            print("--------------------")
        except Exception as e:
            print(f"エラーが発生しました: {e}")
            print("もう一度試してください。")
            print("--------------------")

if __name__ == "__main__":
    chat()
    