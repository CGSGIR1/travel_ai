import settings
from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat
from ModelLoad import GigachatStart, AIResponse

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
import promts
# Авторизация в сервисе GigaChat
import faiss

llm, GigaRet = GigachatStart()
embeddings = HuggingFaceEmbeddings(model_name=settings.emmbedding_model_name)

db = FAISS.load_local(settings.FAISS_FOLDER, embeddings, allow_dangerous_deserialization=True)

rez = AIResponse('Выкса',  GigaRet)

print("Bot: ", rez)


# тестируем ретривер
#rez = db.similarity_search_with_score('Выкса')
##for row in rez:
#    print(row[0].metadata['source'], row[0].metadata['Объект'])