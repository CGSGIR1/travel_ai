import settings
from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat

# Авторизация в сервисе GigaChat
chat = GigaChat(credentials=settings.idf, verify_ssl_certs=False)

messages = [
    SystemMessage(
        content="Ты являеешься гидом по городам России. Твоя задача ответить на вопросы пользователей"
    )
]
def GptAnswer(user_input):
    # Ввод пользователя
    messages.append(HumanMessage(content=user_input))
    res = chat(messages)
    messages.append(res)
    # Ответ модели
    return res.content
