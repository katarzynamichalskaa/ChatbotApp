from typing import Tuple

import faiss
import numpy as np
import configparser
from serpapi import GoogleSearch
import requests
from sentence_transformers import SentenceTransformer


class PipelineRAG:
    def __init__(self):
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")
        self.bing_api_key, self.port = self._load_config()
        self.uri = f"http://localhost:{self.port}/api/generate"
        self.model_name = "llama3"
        self.index = None
        self.docs = []

    @staticmethod
    def _load_config() -> tuple[str, str]:
        config = configparser.ConfigParser()
        config.read('config.ini')
        return config['API']['key'], config['OLLAMA']['port']

    def _send_prompt(self, prompt: str) -> str:
        response = requests.post(self.uri, json={
            "model": self.model_name,
            "prompt": prompt,
            "stream": False
        })
        if response.status_code == 200:
            return response.json()["response"]
        else:
            return "Error while generating the response."

    def summarize_document(self, text: str) -> str:
        prompt = f"Please summarize the following concert tour document briefly:\n\n{text}"
        return self._send_prompt(prompt)

    def is_tour_related(self, text: str) -> str:
        prompt = (f"Please check if the following document is related to concert tour domain. "
                  f"Answer ONLY yes or no:\n\n{text}")
        return self._send_prompt(prompt)

    def ingest_summary(self, summary: str):
        self.docs.append(summary)
        embedding = self.embedder.encode([summary])
        if self.index is None:
            self.index = faiss.IndexFlatL2(embedding.shape[1])
        self.index.add(np.array(embedding))

    def process_document(self, raw_text: str) -> str:
        response = self.is_tour_related(raw_text)
        if response.lower() == 'no':
            return (
                "Sorry, I cannot ingest documents with other themes.\n"
                "The document appears to be unrelated to concert tours, venues, or live events."
            )

        summary = self.summarize_document(raw_text)
        self.ingest_summary(summary)
        return (f"Thank you for sharing! Your document has been successfully added to the database. "
                f"Here is a brief summary:\n\n{summary}")

    def query_document(self, question: str, top_k: int = 3) -> str:
        if self.index is None:
            return "The knowledge base is empty. Please add a document first."
        query_vec = self.embedder.encode([question])
        D, I = self.index.search(np.array(query_vec), top_k)
        context = "\n".join([self.docs[i] for i in I[0]])

        full_prompt = f"Using the following context, answer the user's question:\n\n{context}\n\nQuestion: {question}"
        return self._send_prompt(full_prompt)

    def search_artist_concerts(self, artist_name):
        params = {
            "engine": "bing",
            "q": f"{artist_name} tour 2025",
            "cc": "US",
            "api_key": self.bing_api_key
        }

        search = GoogleSearch(params)
        data = search.get_dict()
        table = []
        for i in range(len(data.get('organic_results', ''))):
            results = data['organic_results'][i].get('snippet', '')
            table.append(results)
        result = ", ".join(table)
        if not result:
            result = f"There is no information about {artist_name} tour in 2025."

        prompt = (f"Based on the following content: \n{result}, "
                  f"return the information about {artist_name} tour.")
        return self._send_prompt(prompt)
