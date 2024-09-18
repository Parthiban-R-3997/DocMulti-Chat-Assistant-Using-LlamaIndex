import streamlit as st
import os
import tempfile
from dotenv import load_dotenv
from llama_parse import LlamaParse
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Settings
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.llms.groq import Groq
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.postprocessor import SimilarityPostprocessor
from llama_index.core.query_engine import RetrieverQueryEngine
from langchain_core.messages import HumanMessage, AIMessage
from llama_index.core.memory import ChatMemoryBuffer
import time

load_dotenv()

st.set_page_config(page_title="Chat with Documents", page_icon=":books:")
st.title("DocMulti Chat Assistant Using LlamaIndex 🦙")

# Initialize chat history in session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Initialize memory buffer
if 'memory' not in st.session_state:
    st.session_state.memory = ChatMemoryBuffer.from_defaults(token_limit=4090)

SUPPORTED_EXTENSIONS = [
    '.pdf', '.602', '.abw', '.cgm', '.cwk', '.doc', '.docx', '.docm', '.dot', '.dotm',
    '.hwp', '.key', '.lwp', '.mw', '.mcw', '.pages', '.pbd', '.ppt', '.pptm', '.pptx',
    '.pot', '.potm', '.potx', '.rtf', '.sda', '.sdd', '.sdp', '.sdw', '.sgl', '.sti',
    '.sxi', '.sxw', '.stw', '.sxg', '.txt', '.uof', '.uop', '.uot', '.vor', '.wpd',
    '.wps', '.xml', '.zabw', '.epub', '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg',
    '.tiff', '.webp', '.htm', '.html', '.xlsx', '.xls', '.xlsm', '.xlsb', '.xlw', '.csv',
    '.dif', '.sylk', '.slk', '.prn', '.numbers', '.et', '.ods', '.fods', '.uos1', '.uos2',
    '.dbf', '.wk1', '.wk2', '.wk3', '.wk4', '.wks', '.123', '.wq1', '.wq2', '.wb1', '.wb2',
    '.wb3', '.qpw', '.xlr', '.eth', '.tsv'
]

# Sidebar configuration
if 'config' not in st.session_state:
    with st.sidebar:
        st.header("Configuration")
        st.markdown("Enter your API keys below:")

        # GROQ API Key input
        st.session_state.groq_api_key = st.text_input(
            "Enter your GROQ API Key", 
            type="password", 
            help="Get your API key from [GROQ Console](https://console.groq.com/keys)"
        )
        
        # Google API Key input
        st.session_state.google_api_key = st.text_input(
            "Enter your Google API Key", 
            type="password", 
            help="Get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey)"
        )

        # Llama Cloud API Key input
        st.session_state.llama_cloud_api_key = st.text_input(
            "Enter your Llama Cloud API Key", 
            type="password", 
            help="Get your API key from [Llama Cloud](https://cloud.llamaindex.ai/api-key)"
        )

        # Set environment variables
        os.environ["GROQ_API_KEY"] = st.session_state.groq_api_key
        os.environ["GOOGLE_API_KEY"] = st.session_state.google_api_key
        os.environ["LLAMA_CLOUD_API_KEY"] = st.session_state.llama_cloud_api_key

        # Model selection
        model_options = [
            "llama-3.1-70b-versatile",
            "llama-3.1-8b-instant",
            "llama3-8b-8192",
            "llama3-70b-8192",
            "mixtral-8x7b-32768",
            "gemma2-9b-it"
        ]
        st.session_state.selected_model = st.selectbox(
            "Select any Groq Model", 
            model_options
        )

        # Document upload
        st.session_state.uploaded_files = st.file_uploader(
            "Choose files", 
            accept_multiple_files=True, 
            type=SUPPORTED_EXTENSIONS, 
            key="file_uploader"
        )
        
        # Checkbox for LlamaParse usage
        st.session_state.use_llama_parse = st.checkbox(
            "Use LlamaParse for complex documents (graphs, tables, etc.)"
        )

        with st.expander("Advanced Options"): 
            # Parsing instruction input
            st.session_state.parsing_instruction = st.text_area(
                "Custom Parsing Instruction",
                value=st.session_state.get('parsing_instruction', "Extract all information"),
                help="Enter custom instructions for document parsing"
            )

            # Custom prompt template input
            st.session_state.custom_prompt_template = st.text_area(
                "Custom Prompt Template", 
                placeholder="Enter your custom prompt here...(Optional)", 
                value=st.session_state.get('custom_prompt_template', '')
            )

# Step 3: Load and parse documents
def parse_and_index_documents(uploaded_files, use_llama_parse, parsing_instruction):
    all_documents = []

    if st.session_state.use_llama_parse and os.environ.get("LLAMA_CLOUD_API_KEY"):
        with st.spinner("Using LlamaParse for document parsing"):
            parser = LlamaParse(result_type="markdown", parsing_instruction=parsing_instruction)
            for uploaded_file in st.session_state.uploaded_files:
                file_info_placeholder = st.empty()
                file_info_placeholder.info(f"Processing file: {uploaded_file.name}")
                with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[-1]) as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_file_path = tmp_file.name

                try:
                    parsed_documents = parser.load_data(tmp_file_path)
                    all_documents.extend(parsed_documents)
                except Exception as e:
                    st.error(f"Error parsing {uploaded_file.name}: {str(e)}")
                finally:
                    os.remove(tmp_file_path)
                    time.sleep(4)
                    file_info_placeholder.empty()
    else:
        with st.spinner("Using SimpleDirectoryReader for document parsing"):
            for uploaded_file in st.session_state.uploaded_files:
                file_info_placeholder = st.empty()
                file_info_placeholder.info(f"Processing file: {uploaded_file.name}")
                with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[-1]) as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_file_path = tmp_file.name

                try:
                    reader = SimpleDirectoryReader(input_files=[tmp_file_path])
                    docs = reader.load_data()
                    all_documents.extend(docs)
                except Exception as e:
                    st.error(f"Error loading {uploaded_file.name}: {str(e)}")
                finally:
                    os.remove(tmp_file_path)
                    time.sleep(4)
                    file_info_placeholder.empty()

    if not all_documents:
        st.error("No valid documents found.")
        return None

    with st.spinner("Creating Vector Store Index..."):
        try:
            groq_llm = Groq(model=st.session_state.selected_model)
            gemini_embed_model = GeminiEmbedding(model_name="models/embedding-001")

            Settings.llm = groq_llm
            Settings.embed_model = gemini_embed_model
            Settings.chunk_size = 2048

            index = VectorStoreIndex.from_documents(all_documents, embed_model=gemini_embed_model)
            
            # Create a retriever from the index
            retriever = VectorIndexRetriever(index=index, similarity_top_k=2)
            
            # Create a postprocessor
            postprocessor = SimilarityPostprocessor(similarity_cutoff=0.50)
            
            # Create the query engine
            query_engine = RetrieverQueryEngine(
                retriever=retriever,
                node_postprocessors=[postprocessor]
            )
            
            # Create a chat engine with memory, using the custom query engine
            chat_engine = index.as_chat_engine(
                chat_mode="condense_question",
                memory=st.session_state.memory,
                verbose=False
            )
            
            # Set the query engine for the chat engine
            chat_engine.query_engine = query_engine
            return chat_engine
        
        except Exception as e:
            st.error(f"Error building index: {str(e)}")
            return None
        
        
    st.success("Data Processed. Ready to answer your question!")


# Step 5: Start document indexing
if st.sidebar.button("Start Document Indexing"):
    if st.session_state.uploaded_files:
        try:
            chat_engine = parse_and_index_documents(st.session_state.uploaded_files, st.session_state.use_llama_parse, st.session_state.parsing_instruction)
            if chat_engine:
                    st.session_state.chat_engine = chat_engine
                    st.success("Data Processed.Ready to answer your question!!")
            else:
                    st.error("Failed to create data index store.")
        except Exception as e:
            st.error(f"An error occurred during indexing: {str(e)}")
    else:
        st.warning("Please upload at least one file.")

# Step 6: Querying logic
def get_response(query, chat_engine, custom_prompt):
    try:
        # Prepare the query
        if custom_prompt:
            query = f"{custom_prompt}\n\nQuestion: {query}"

        # Use the chat engine to get a response
        response = chat_engine.chat(query)

        # If response is empty or not valid
        if not response or not response.response:
            return "I couldn't find a relevant answer. Could you rephrase?"

        return response.response
    except Exception as e:
        st.error(f"Error processing query: {str(e)}")
        return "An error occurred."


st.markdown("---")
user_query = st.chat_input("Enter Your Question")

if user_query and "chat_engine" in st.session_state:
    # Add user's message to chat history
    st.session_state.chat_history.append({"role": "user", "content": user_query})

    # Get response from the chat engine
    response = get_response(user_query, st.session_state.chat_engine, st.session_state.custom_prompt_template)

    if response:
        # Add AI's response to chat history
        st.session_state.chat_history.append({"role": "assistant", "content": str(response)})

        # Display chat history
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.chat_message("user").write(message["content"])
            elif message["role"] == "assistant":
                st.chat_message("assistant").write(message["content"])
    else:
        st.warning("Unable to process the query.")