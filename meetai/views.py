from decouple import config
from rest_framework.response import Response
from rest_framework.views import APIView
import openai

openai.api_key = config("OPENAI_API_KEY")


def send_text(user_input):
    gpt_prompt: list[dict] = []
    gpt_prompt.append(
        {
            # 시스템 역할(기본설정) 주기
            "role": "system",
            "content": "Chat naturally, friendly like talking to Bestie. Response Korean, Shortly less than 120 letters.",
        }
    )

    # 최근 대화 2개 가져오기?
    if len(gpt_prompt) >= 4:
        prompt = gpt_prompt[len(gpt_prompt) - 4 :]

    gpt_prompt.append(
        {
            # user_input을 넣어준다!
            "role": "user",
            "content": user_input,
        }
    )

    answer = send_text(gpt_prompt)
    print(answer)
    gpt_prompt.append(
        {
            # 이전 대화 저장
            "role": "assistant",
            "content": answer,
        }
    )

    # with st.spinner("잠깐만! 생각 중이야!"):
    prompt = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        max_tokens=1024,
        messages=user_input,
        temperature=0.7,
        top_p=1,
        stream=True,
        presence_penalty=0.5,
    )
    # json response에서 필요한 부분만 불러옴
    return prompt["choices"][0]["message"]["content"]


class SendTextView(APIView):
    def post(self, request):
        print("⭐️", request.data["user_input"])
        user_input = request.data["user_input"]
        response = send_text(user_input)
        return Response({"message": response}, status=200)
