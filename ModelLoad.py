from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat
import settings
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.embeddings.gigachat import GigaChatEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import logging
import promts


def GigachatStart():
    embeddings = HuggingFaceEmbeddings(model_name=settings.emmbedding_model_name)
    db = FAISS.load_local(settings.FAISS_FOLDER, embeddings, allow_dangerous_deserialization=True)
    llm = GigaChat(credentials=settings.idf, verify_ssl_certs=False)

    return llm, db

def AIResponse(request, GigaRet):
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
