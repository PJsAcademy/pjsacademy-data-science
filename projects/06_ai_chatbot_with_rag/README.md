# 🤖 Project 06 — AI Chatbot with RAG

**Phase 5 — GenAI & LLMs** | Advanced

---

## 🎯 What You'll Build
A chatbot that answers questions from YOUR documents — no hallucination, cites sources. Built with LangChain + RAG.

## 🛠️ Skills Practiced
- RAG — Retrieval Augmented Generation
- LangChain — document loading, chunking, retrieval
- Vector databases — Chroma
- OpenAI API / any LLM

## 📦 What You Need
- Python 3.10+
- OpenAI API key (or use free Ollama locally)
- Any PDF document to chat with

## 🚀 Steps
1. Load your PDF document
2. Chunk into smaller pieces
3. Embed and store in vector DB
4. Build retrieval chain
5. Chat with your document!

## 💻 Code
```python
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI

# 1. Load document
loader = PyPDFLoader('your_document.pdf')
documents = loader.load()

# 2. Chunk
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
chunks = splitter.split_documents(documents)
print(f"Created {len(chunks)} chunks")

# 3. Embed and store
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(chunks, embeddings)

# 4. Build RAG chain
retriever = vectorstore.as_retriever(search_kwargs={'k': 5})
chain = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model='gpt-4o', temperature=0),
    retriever=retriever,
    return_source_documents=True
)

# 5. Chat!
while True:
    question = input("\nAsk a question (q to quit): ")
    if question == 'q': break
    result = chain(question)
    print(f"\n💬 Answer: {result['result']}")
    print(f"📄 Source: {result['source_documents'][0].metadata}")
```

## 📈 What You'll Learn
- How ChatGPT plugins work under the hood
- Build your own document Q&A in 50 lines
- RAG vs fine-tuning — when to use which

---

*Course: [Data Science Mastery — PJS Academy](https://pjsacademy.com)*
