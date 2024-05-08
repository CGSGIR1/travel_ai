from pickle import load
from chromadb.config import Settings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.schema import HumanMessage
from langchain.chat_models.gigachat import GigaChat

idf = "Y2I5NzU5ZTMtMTZhMy00YzhmLTgwODAtNTAwZWQ1ZGEwYzMzOjU0YmY4ZjQwLWI5NTgtNDJiNi1iZGVjLWRhODI5MTY5NWEzMg=="

with open('./DataBase/documents.pkl', 'rb') as fp:
    documents = load(fp)
with open('./DataBase/embeddings.pkl', 'rb') as fp:
    embeddings = load(fp)
llm = GigaChat(credentials=idf, verify_ssl_certs=False)

db = Chroma.from_documents(
   documents,
   embeddings,
   client_settings=Settings(anonymized_telemetry=False),
)
qa_chain = RetrievalQA.from_chain_type(llm, retriever=db.as_retriever())
def AIResponse():
   AIResponse = input("Q: ")
   resansw =qa_chain({"query": AIResponse})
   return resansw['result']
