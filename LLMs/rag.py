# 1️⃣ Import libraries
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import Ollama
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.schema import Document
from langchain.chains import RetrievalQA

# 2️⃣ Hardcoded text
text = """
Java is a high-level, class-based, object-oriented programming language and platform released by Sun Microsystems in 1995. 
Designed to be portable across platforms ("write once, run anywhere") using the Java Virtual Machine (JVM), 
it is widely used for building secure, robust, and scalable applications, including Android apps, web backends, and enterprise software. 
"""

# Wrap text into a Document
documents = [Document(page_content=text)]

# 3️⃣ Split text into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=150,    # smaller for demo
    chunk_overlap=30
)
docs = text_splitter.split_documents(documents)

# 4️⃣ Load local embeddings model
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# 5️⃣ Create FAISS vector store
vectorstore = FAISS.from_documents(docs, embeddings)

# 6️⃣ Create retriever (top 2 chunks)
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

# 7️⃣ Load local LLM
llm = Ollama(
    model="llama3",   # your local Ollama model
    temperature=0
)

# 8️⃣ Create RAG chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True
)

# 9️⃣ Ask a question
query = "What is JAVA?"
response = qa_chain.invoke({"query": query})

print("Answer:", response["result"])
