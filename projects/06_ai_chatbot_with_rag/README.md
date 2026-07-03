# 🤖 Project 06 — AI Chatbot with RAG

**Phase 5 — GenAI & LLMs** | Beginner → Advanced (3 Versions)

---

## 🗺️ Version Roadmap

| Version | What You Build | Complexity |
|---------|---------------|------------|
| v1.0 — Starter | Basic RAG — chat with one PDF using LangChain | ⭐ Beginner |
| v2.0 — Improved | Multi-document RAG + source citations + conversation memory | ⭐⭐ Intermediate |
| v3.0 — Production | RAG with re-ranking, guardrails, eval metrics + Streamlit UI | ⭐⭐⭐ Advanced |

---

## 📦 What You Need
- Python 3.10+
- OpenAI API key (free credits at platform.openai.com) OR Ollama locally (free)
- Any PDF document to chat with

---

## 🟢 v1.0 — Basic RAG

**Skills:** PDF loading, chunking, ChromaDB, RetrievalQA

```python
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
import os

os.environ["OPENAI_API_KEY"] = "YOUR_KEY"

# 1. Load PDF
loader = PyPDFLoader('your_document.pdf')
documents = loader.load()
print(f"Loaded {len(documents)} pages")

# 2. Chunk into smaller pieces
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(documents)
print(f"Created {len(chunks)} chunks")

# 3. Embed and store in ChromaDB
embeddings  = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(chunks, embeddings, persist_directory='./db')

# 4. Build RAG chain
retriever = vectorstore.as_retriever(search_kwargs={'k': 4})
chain = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model='gpt-4o-mini', temperature=0),
    retriever=retriever,
    return_source_documents=True
)

# 5. Chat!
while True:
    question = input("\n❓ Ask a question (q to quit): ")
    if question.lower() == 'q':
        break
    result = chain.invoke(question)
    print(f"\n💬 {result['result']}")
    print(f"📄 Source: Page {result['source_documents'][0].metadata.get('page', '?')}")
```

**What v1 teaches:** How RAG works — instead of hallucinating, the LLM reads YOUR document first.

---

## 🟡 v2.0 — Multi-Document RAG with Memory

**New in v2:** Load multiple PDFs, conversation memory (follow-up questions), source citations per chunk, custom system prompt

```python
import os
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate

os.environ["OPENAI_API_KEY"] = "YOUR_KEY"

# --- Load Multiple PDFs from a folder ---
def load_documents(docs_folder='./documents'):
    Path(docs_folder).mkdir(exist_ok=True)
    loader = DirectoryLoader(docs_folder, glob='**/*.pdf',
                             loader_cls=PyPDFLoader, show_progress=True)
    documents = loader.load()
    print(f"Loaded {len(documents)} pages from {docs_folder}")

    # Add source filename to metadata
    for doc in documents:
        doc.metadata['source_name'] = Path(doc.metadata['source']).name
    return documents

documents = load_documents('./documents')

# --- Chunking ---
splitter = RecursiveCharacterTextSplitter(
    chunk_size=600,
    chunk_overlap=100,
    separators=["\n\n", "\n", ". ", " ", ""]
)
chunks = splitter.split_documents(documents)
print(f"Created {len(chunks)} chunks from {len(documents)} pages")

# --- Vector Store ---
embeddings  = OpenAIEmbeddings(model='text-embedding-3-small')
vectorstore = Chroma.from_documents(
    chunks, embeddings,
    persist_directory='./chroma_db',
    collection_name='course_documents'
)
retriever = vectorstore.as_retriever(
    search_type='mmr',       # Maximal Marginal Relevance — avoids repetitive chunks
    search_kwargs={'k': 5, 'fetch_k': 20}
)

# --- Custom Prompt ---
QA_PROMPT = PromptTemplate.from_template("""
You are a helpful study assistant for a Data Science course.
Use ONLY the context below to answer. If the answer is not in the context, say:
"I couldn't find this in the provided documents."

Context:
{context}

Chat History:
{chat_history}

Question: {question}

Answer concisely and cite the source document name when possible:
""")

# --- Memory (remembers last 5 turns) ---
memory = ConversationBufferWindowMemory(
    memory_key='chat_history',
    return_messages=True,
    output_key='answer',
    k=5
)

# --- Conversational RAG Chain ---
chain = ConversationalRetrievalChain.from_llm(
    llm=ChatOpenAI(model='gpt-4o-mini', temperature=0),
    retriever=retriever,
    memory=memory,
    return_source_documents=True,
    combine_docs_chain_kwargs={'prompt': QA_PROMPT}
)

# --- Chat with source citations ---
print("\n📚 Multi-Document RAG Chatbot Ready!")
print("Loaded documents:", list(set(d.metadata['source_name'] for d in documents)))

while True:
    question = input("\n❓ Question (q to quit): ")
    if question.lower() == 'q':
        break
    result = chain.invoke({'question': question})
    print(f"\n💬 {result['answer']}")

    # Show sources
    sources = set()
    for doc in result['source_documents']:
        src  = doc.metadata.get('source_name', 'unknown')
        page = doc.metadata.get('page', '?')
        sources.add(f"{src} (p.{page})")
    if sources:
        print(f"📄 Sources: {' | '.join(sources)}")
```

**What v2 adds over v1:**
- DirectoryLoader — load ALL PDFs in a folder at once
- MMR retrieval — avoids returning 5 identical chunks
- ConversationBufferWindowMemory — "what did I ask before?" now works
- Custom prompt — stops hallucination, forces document grounding
- Source name + page number on every answer

---

## 🔴 v3.0 — Production RAG with Re-Ranking, Guardrails & Evaluation

**New in v3:** Re-ranking with cross-encoder, hallucination guardrail, RAG evaluation (faithfulness + answer relevancy), Streamlit UI

```python
# Part A — Cross-Encoder Re-Ranking
from sentence_transformers import CrossEncoder
import numpy as np

reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

def retrieve_and_rerank(question, vectorstore, top_k=10, final_k=4):
    # Step 1: Retrieve 10 candidates
    candidates = vectorstore.similarity_search(question, k=top_k)

    # Step 2: Re-rank using cross-encoder (slower, more accurate)
    pairs = [[question, doc.page_content] for doc in candidates]
    scores = reranker.predict(pairs)

    # Step 3: Return top 4 after re-ranking
    ranked = sorted(zip(scores, candidates), reverse=True)
    return [doc for _, doc in ranked[:final_k]]

# Usage:
# top_docs = retrieve_and_rerank("What is gradient descent?", vectorstore)
```

```python
# Part B — Hallucination Guardrail
from langchain_openai import ChatOpenAI

def check_faithfulness(question, answer, context_chunks):
    """Check if the answer is grounded in the retrieved context."""
    llm = ChatOpenAI(model='gpt-4o-mini', temperature=0)
    context_text = '\n\n'.join([c.page_content for c in context_chunks])

    guard_prompt = f"""
    Context from documents:
    {context_text}

    Question: {question}
    Answer given: {answer}

    Is this answer fully supported by the context above?
    Reply with only: FAITHFUL or HALLUCINATED
    Then on the next line, give a one-sentence reason.
    """
    result = llm.invoke(guard_prompt).content
    verdict = 'FAITHFUL' if 'FAITHFUL' in result.upper() else 'HALLUCINATED'
    reason  = result.split('\n')[1] if '\n' in result else ''
    return verdict, reason

# Usage:
# verdict, reason = check_faithfulness(question, answer, retrieved_docs)
# if verdict == 'HALLUCINATED':
#     answer = "I could not find a reliable answer in the documents."
```

```python
# Part C — RAG Evaluation with RAGAS-style metrics
def evaluate_rag(qa_pairs, chain):
    """
    Evaluate RAG pipeline on a set of QA pairs.
    qa_pairs = [{"question": "...", "expected": "..."}, ...]
    """
    from difflib import SequenceMatcher

    results = []
    for pair in qa_pairs:
        result = chain.invoke({'question': pair['question']})
        answer = result['answer']

        # Approximate answer similarity (use RAGAS library for production)
        similarity = SequenceMatcher(None, answer.lower(),
                                     pair['expected'].lower()).ratio()
        results.append({
            'question':  pair['question'],
            'answer':    answer[:100],
            'expected':  pair['expected'][:100],
            'similarity': round(similarity, 3),
            'pass':      similarity > 0.5
        })

    import pandas as pd
    df = pd.DataFrame(results)
    print(f"\nRAG Evaluation Results:")
    print(f"  Questions tested: {len(df)}")
    print(f"  Pass rate:        {df['pass'].mean():.0%}")
    print(f"  Avg similarity:   {df['similarity'].mean():.3f}")
    print(df[['question', 'similarity', 'pass']].to_string(index=False))
    return df

# Example usage:
# test_cases = [
#     {"question": "What is overfitting?", "expected": "When a model performs well on training..."},
#     {"question": "Define gradient descent", "expected": "An optimisation algorithm..."}
# ]
# evaluate_rag(test_cases, chain)
```

```python
# Part D — Streamlit Chat UI (app.py)
import streamlit as st
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferWindowMemory
import os

st.set_page_config(page_title="Course Chatbot", page_icon="🤖", layout="wide")
st.title("🤖 Data Science Course Assistant — PJS Academy")
st.caption("Ask anything from the course materials")

os.environ["OPENAI_API_KEY"] = st.secrets.get("OPENAI_API_KEY", "YOUR_KEY")

@st.cache_resource
def init_chain():
    vectorstore = Chroma(persist_directory='./chroma_db',
                         embedding_function=OpenAIEmbeddings())
    memory = ConversationBufferWindowMemory(
        memory_key='chat_history', return_messages=True,
        output_key='answer', k=5)
    return ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(model='gpt-4o-mini', temperature=0),
        retriever=vectorstore.as_retriever(search_kwargs={'k': 4}),
        memory=memory, return_source_documents=True
    )

chain = init_chain()

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg['role']):
        st.markdown(msg['content'])

if question := st.chat_input("Ask a question about the course..."):
    st.session_state.messages.append({'role': 'user', 'content': question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Searching course materials..."):
            result = chain.invoke({'question': question})
            answer = result['answer']
            sources = set(d.metadata.get('source', '')
                          for d in result['source_documents'])

        st.markdown(answer)
        if sources:
            st.caption(f"📄 Sources: {' | '.join(sources)}")

    st.session_state.messages.append({'role': 'assistant', 'content': answer})
```

**What v3 adds over v2:**
- Cross-encoder re-ranking — better retrieval quality without changing the vector store
- Hallucination guardrail — GPT-4o checks its own answer against the context
- RAG evaluation — measure your chatbot's quality with test cases
- Streamlit chat UI — production-ready with message history, source display

---

## 📈 Learning Progression Summary

```
v1 → "Here is what page 3 says about X" — basic retrieval
v2 → "Based on your last question, here is what 3 documents say..." — memory + multi-source
v3 → Retrieval → Re-rank → Answer → Guardrail check → Evaluate — production pipeline
```

---

*Course: [Data Science Mastery — PJS Academy](https://pjsacademy.com)*
