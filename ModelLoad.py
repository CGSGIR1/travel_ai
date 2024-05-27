from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
import promts
import settings

class ClassModelLoad:

    def __init__(self):
        # Авторизация в сервисе GigaChat
        self.chat = GigaChat(credentials=settings.idf, verify_ssl_certs=False)

        self.messages = [
            SystemMessage(
                content=promts.main_gid
            )
        ]

    def GigachatStart(self):
        embeddings = HuggingFaceEmbeddings(model_name=settings.emmbedding_model_name)
        db = FAISS.load_local(settings.FAISS_FOLDER, embeddings, allow_dangerous_deserialization=True)
        llm = GigaChat(credentials=settings.idf, verify_ssl_certs=False)

        return llm, db

    def GigachatMainGidAnswer(self, user_input):
        # Ввод пользователя
        self.messages.append(HumanMessage(content=user_input))
        res = self.chat(self.messages)
        self.messages.append(res)
        # Ответ модели
        return res.content

    def AIResponse(self, request, llm, GigaRet):
        rez = GigaRet.similarity_search_with_score(request, 20)
        context = ''
        for row in rez:
            context += row[0].metadata['source']
            context += ' ' + row[0].metadata['Объект'] + '; '

        promt = promts.gid_with_instrution.format(request, context)
        llm = GigaChat(credentials=settings.idf, verify_ssl_certs=False)

        messages = [
            SystemMessage(
                content=promt
            )
        ]
        res = llm(messages)
        return res.content
