import gradio as gr
from pathlib import Path
from ollama_pipeline import PipelineRAG


class UI:
    def __init__(self):
        self.ingestor = PipelineRAG()

    def process_files(self, files):
        if not files:
            return "No files uploaded"

        if isinstance(files, str):
            files = [files]
        elif isinstance(files, list) and isinstance(files[0], str):
            pass
        else:
            try:
                files = [files.name]
            except AttributeError:
                return "Unrecognized input data type"

        messages = []
        for file_path in files:
            try:
                text = Path(file_path).read_text(encoding="utf-8", errors="ignore")
                result = self.ingestor.process_document(text)
                messages.append(f"{Path(file_path).name}:\n\n{result}\n")
            except Exception as e:
                messages.append(f"Error processing file {file_path}: {str(e)}")

        return "\n\n--------------------------------------------------\n\n".join(messages)

    def handle_document_query(self, query):
        if not query.strip():
            return "Please enter a question about the documents."
        return self.ingestor.query_document(query)

    def handle_artist_query(self, artist_name):
        if not artist_name.strip():
            return "Please enter an artist's name to search for their concert information."
        return self.ingestor.search_artist_concerts(artist_name)

    def launch_interface(self):
        with (gr.Blocks(theme=gr.themes.Soft(primary_hue=gr.themes.colors.green, secondary_hue=gr.themes.colors.green))
              as demo):
            gr.Markdown("## Concert Tour Document Processing System")

            with gr.Tab("Upload document & ask about it"):
                file_input = gr.File(label="Upload TXT document(s)", file_types=[".txt"], file_count="multiple")
                process_output = gr.Textbox(label="Processing result")
                query_input = gr.Textbox(label="Ask about the documents",
                                         placeholder="Ask a question about the document")
                query_output = gr.Textbox(label="Answer")
                process_btn = gr.Button("Process document(s)")
                query_btn = gr.Button("Ask question")

            with gr.Tab("Search artist concerts"):
                artist_input = gr.Textbox(label="Artist/Band name",
                                          placeholder="Lady Gaga")
                artist_output = gr.Textbox(label="Tour info")
                search_btn = gr.Button("Search tour info")

            process_btn.click(fn=self.process_files, inputs=file_input, outputs=process_output)
            query_btn.click(fn=self.handle_document_query, inputs=query_input, outputs=query_output)
            search_btn.click(fn=self.handle_artist_query, inputs=artist_input, outputs=artist_output)

        demo.launch()


