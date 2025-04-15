# Provectus Internship - Katarzyna Michalska

## Approach and Design Choices

For running a large language model locally, I used Ollama - a tool that allows you to download, run, and interact with open-source LLMs, because I already have professional experience working with it. For the language model itself, I selected LLaMA 3, an open-source solution from Meta. I opted for the smallest model in the LLaMA 3 family, as the application is relatively lightweight, and this size is sufficient for its needs.

Communication with the model is handled via API calls, where prompts are sent using HTTP POST requests. One of the initial tasks performed by the model is determining whether an uploaded document falls within the concert and entertainment domain. I use the same LLaMA 3 model with a simple prompt asking whether the given document relates to the relevant domain. The model is instructed to return only “yes” or “no.” This method is more robust and safer than manually searching for domain-specific keywords in the text, which could be error-prone or too rigid.

If the document is relevant, it proceeds to the next stage in the pipeline, where the model is prompted again - this time to generate a summary of the text. The system supports multiple document uploads at once, and in such cases, it returns multiple summaries together in a single output window.

For each ingested document, embeddings are created - this means converting text into machine - readable vector representations. For this purpose, I use the "all-MiniLM-L6-v2" model from SentenceTransformers, chosen for its compact size and efficiency. These embeddings are used when the user asks a question related to the uploaded documents. The system then performs a semantic search using FAISS to retrieve the top 3 most relevant summaries based on similarity, and this retrieved context is passed to LLaMA 3, which generates a final answer grounded in that information.

The frontend was built with Gradio, which I also had experience with. Gradio enables quick and intuitive UI development.

In addition, an extra feature was implemented: the ability to input the name of a band or artist, so the system will search online for upcoming concerts by that artist. This functionality was added in a separate tab to clearly distinguish it from the core RAG-based document processing.

To perform the external search, I used the SerpAPI, which allows querying Google search results programmatically. Since many websites block traditional scraping techniques, I extract snippets (page summaries) returned by the search engine instead of parsing full webpages. Although this approach is minimal, it proves effective in tests: LLaMA 3 can still provide meaningful answers about tour dates based on just these short summaries.


## Installation and Setup Instructions

### 1. Install Ollama

Start by installing Ollama by running the following command in your terminal (https://ollama.com/download):

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Once the installation is complete, pull the llama3 model:

```bash
ollama pull llama3
```

By default, Ollama runs on port 11434, but if another application is already using this port, you can check which port Ollama is using with the following command:

```bash
lsof -i -P | grep LISTEN | grep ollama
```

If necessary, you can change the port by editing the OLLAMA value in config.ini file.

### 2. Creating a Virtual Environment

Create a virtual environment:

```bash
python3 -m venv venv
```

### 3. Activating the Virtual Environment
Activate the virtual environment by running:


```bash
source venv/bin/activate
```

### 4. Installing Dependencies
After activating the virtual environment, install the required dependencies by running:

```bash
pip install -r requirements.txt
```

### 5. Running the Project
```bash
python main.py
```

After running the project, a link will be printed in the terminal, such as:

```
* Running on local URL: http://127.0.0.1:7860
```

### 6. Demo

https://github.com/user-attachments/assets/26644058-9359-4ace-ad2b-caba83e86613
