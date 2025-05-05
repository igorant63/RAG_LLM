from pathlib import Path
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.chat_models import GigaChat
from langchain_community.retrievers import LlamaIndexRetriever
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders.pdf import PyMuPDFLoader
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
)
from langchain.vectorstores import FAISS
from langchain_community.embeddings import  HuggingFaceEmbeddings

loader = DirectoryLoader(path=".", glob=f"**/*{'.pdf'}", loader_cls=PyMuPDFLoader)

documents = loader.load()
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,
    chunk_overlap=100,
)
documents = text_splitter.split_documents(documents)
print(f"Total documents: {len(documents)}")
device = "cuda"
model_name = "intfloat/multilingual-e5-small"
model_kwargs = {'device': 'cuda'}
encode_kwargs = {'normalize_embeddings': False}
embedding = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)
db = FAISS.from_documents(
    documents,
    embedding
)
db.save_local("faiss_index")
print("Completed!")
