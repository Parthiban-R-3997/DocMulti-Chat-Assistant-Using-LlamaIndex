# DocMulti Chat Assistant Using LlamaIndex 🦙

## Overview
DocMulti Chat Assistant is a powerful Streamlit-based application that leverages LlamaIndex to provide an interactive chat interface for querying multiple documents. This tool excels at processing and understanding complex data structures, ensuring that no information is lost during the parsing and indexing stages.


## Deployed Link
DocMulti-Chat-Assistant app is Deployed And Available [Here](https://huggingface.co/spaces/Parthiban97/DocMulti_Chat_Assistant_Using_LlamaIndex)


## Screenshots
![llamaindex_1](https://github.com/user-attachments/assets/15b00af3-e8a6-4a09-a0ab-b5bf9fe53f54)
![llamaindex_2](https://github.com/user-attachments/assets/7d8925f2-6be2-4588-a0ad-d88ec14c8dec)
![llamaindex_3](https://github.com/user-attachments/assets/595e7cd3-d99a-41c4-8a2a-66efddc9b4aa)
![llamaindex_4](https://github.com/user-attachments/assets/7224ff3e-e47a-471f-bceb-6a699f1d228c)
![llamaindex_5](https://github.com/user-attachments/assets/c1b1b728-eb23-4ebf-a92b-9712ca8bff9c)

## Features
- **Multi-Document Support**: Upload and process multiple document types.
- **Advanced Parsing**: Option to use LlamaParse for complex documents with graphs and tables.
- **Customizable Models**: Choose from various Groq models for text generation.
- **Flexible Embedding**: Utilizes Google's Gemini for document embedding.
- **Interactive Chat Interface**: Engage in a conversation about your documents.
- **Memory Retention**: Maintains context across multiple queries using a chat memory buffer.
- **Custom Parsing Instructions**: Tailor the document parsing process with custom instructions.
- **Custom Prompt Templates**: Define your own prompts for more specific interactions.

## Components
- **Streamlit**: For the web interface.
- **LlamaIndex**: Core indexing and querying engine.
- **Groq**: Large Language Model for text generation.
- **Google Gemini**: For document embedding.
- **LlamaParse**: Optional advanced document parser.

## Usage
1. Launch the Streamlit app.
2. In the sidebar:
   - Enter your API keys for Groq, Google, and Llama Cloud.
   - Select a Groq model.
   - Upload your documents.
   - Choose whether to use LlamaParse.
   - Set any advanced options like custom parsing instructions or prompt templates.
3. Click "Start Document Indexing" to process your documents.
4. Once indexed, use the chat interface to ask questions about your documents.

## Supported Document Types
The application supports a wide range of document formats, including but not limited to:
- PDF, DOCX, TXT, HTML, XLSX, CSV
- Image formats (JPG, PNG, etc.)
- And many more (see SUPPORTED_EXTENSIONS in the code for a full list)

## Advanced Features
- **Custom Parsing Instructions**: Tailor how LlamaParse extracts information from your documents.
- **Custom Prompt Templates**: Create specific prompts to guide the AI's responses.
- **Adjustable Model Parameters**: Select different Groq models to balance between speed and capability.

## Notes
- Ensure you have valid API keys for Groq, Google, and Llama Cloud before using the application.
- Processing time may vary depending on the number and complexity of uploaded documents.

## Troubleshooting
- If you encounter errors during document processing, check your API keys and internet connection.
- For issues with specific document types, try toggling the LlamaParse option.

## Contributing
Contributions to improve DocMulti Chat Assistant are welcome. Please submit pull requests or open issues on the project repository.

