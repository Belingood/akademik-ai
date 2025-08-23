# AkademikAI 🎓

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Framework: FastAPI](https://img.shields.io/badge/Framework-FastAPI-green.svg)](https://fastapi.tiangolo.com/)
[![AI Framework: LangChain](https://img.shields.io/badge/AI-LangChain-purple.svg)](https://www.langchain.com/)

AkademikAI is a Retrieval-Augmented Generation (RAG) API designed to serve as an intelligent information assistant for a university. It leverages a vector database populated with content from the university's official website to provide accurate, context-aware answers to user questions.

---

## ✨ Features

-   **Intelligent Q&A**: Ask complex questions in natural language and get concise, factual answers.
-   **Source Verification**: Every answer is backed by source links to the original web pages, ensuring transparency and trust.
-   **Multi-language Support**: The API can generate answers in different languages (e.g., Polish, English) based on a simple parameter.
-   **Fast & Scalable**: Built with FastAPI for high performance and powered by state-of-the-art language models and vector search.
-   **Easy to Set Up**: Comes with clear instructions for local setup and a GPU-accelerated option for building the knowledge base.

---

## 🛠️ Technology Stack

-   **Backend**: FastAPI
-   **AI Orchestration**: LangChain
-   **LLM**: GPT-4o (via OpenAI API)
-   **Vector Database**: ChromaDB
-   **Embedding Model**: `intfloat/multilingual-e5-large`
-   **Configuration**: Pydantic

---

## 🚀 Getting Started

Follow these instructions to set up and run the project locally.

### 1. Prerequisites

-   Python 3.9+
-   Git

### 2. Clone the Repository

```bash
git clone https://github.com/your-username/akademik-ai.git
cd akademik-ai
```

### 3. Set Up the Environment

Create and activate a virtual environment:

```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
.\venv\Scripts\activate
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

The application requires an OpenAI API key.

1.  Copy the example environment file:
    ```bash
    cp .env.example .env
    ```
2.  Open the newly created `.env` file and add your OpenAI API key:
    ```
    OPENAI_API_KEY="sk-YourSecretKeyGoesHere"
    ```

### 5. Build the Knowledge Base (Indexing)

To answer questions, the system needs a processed knowledge base. This process is called indexing. You have two options:

#### Option A: Local Indexing (Simple but Slow)

This method is suitable for small datasets or for quick tests. For a full dataset, this process can take many hours on a standard CPU.

-   Ensure your data file is located at `data/content.jsonl`.
-   Run the indexing script from your terminal:
    ```bash
    python scripts/build_index.py
    ```
    This will create the vector database in the `vector_db/` directory.

#### Option B: GPU-Accelerated Indexing in the Cloud (Recommended)

This method uses Google Colab's free or paid GPU resources and is **significantly faster** (1-2 hours instead of 10+ hours). This is the recommended approach for large datasets.

1.  Navigate to the `colab_notebooks/` directory.
2.  Open the `AkademikAI_Indexing_GPU.ipynb` notebook in Google Colab.
3.  Follow the step-by-step instructions within the notebook to upload your data, run the GPU-powered indexing, and download the finished database as a `.zip` archive.
4.  Unzip the archive and place the `vector_db` folder in the root of this project.

### 6. Run the API Server

Once your `vector_db` directory is ready, start the FastAPI server:

```bash
uvicorn src.main:app --reload
```

The API will be running at `http://127.0.0.1:8000`.

### 7. Explore the API

Open your web browser and navigate to **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)** to access the interactive Swagger UI documentation. You can test the `/api/v1/ask` endpoint directly from your browser.

---

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.