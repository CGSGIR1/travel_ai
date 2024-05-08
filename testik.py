idf = "NDBhNDQ2MmItN2U3NC00N2E0LTkzYjAtMzY5MzQyZjA3M2U1OjM4ZGMwOWEzLTIwOTEtNDBmZi1hNjVjLWUwMjRmMTZhYjNhNQ=="
"""Пример работы с чатом через gigachain"""
from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat

# Авторизация в сервисе GigaChat
chat = GigaChat(credentials=f'{idf}', verify_ssl_certs=False)

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
