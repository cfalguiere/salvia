# This module handle documents
import logging
import os
import shutil
from tempfile import NamedTemporaryFile
from typing import Any, Dict, List

from langchain.document_loaders import (
    TextLoader,
    UnstructuredPDFLoader,
    UnstructuredPowerPointLoader,
    UnstructuredWordDocumentLoader,
)
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS

logging_level = logging.INFO
logging.basicConfig(format="[%(levelname)s] %(asctime)s %(message)s", level=logging_level)
logger = logging.getLogger(__name__)


class Corpus:
    """
    Creates a corpus object.

    The prupose of this class is to load and split document, feed the vector store
    and provide utilities related to document management.

    If no embedding is provided, an embedding model is created from get_text_embeddings
    using parameters in llm_context.
    Unit tests give fake embeddings as parameter.

    Args:
        llm_context (dict(str, str)): a doctionnary of configuration parameters.
        embeddings (langchain.embeddings.penAIEmbeddings, optional): an embedding model
    """

    def __init__(self, llm_context: Dict[str, str] = None, embeddings=None):
        self.llm_context = llm_context
        self.embeddings = embeddings
        self.vector_store = None
        self.uploaded_documents = []
        self.generated_documents = []
        self.paths = []

    def load_documents(self, document_uris: List[Any]) -> List[Any]:
        """
        Loads all documents found in the list of uploaded files in the GUI.

        Documents may be of type PDF, PowerPoint, Doc or plain text.
        The name and type of the document are added as metadaa.

        Args:
            document_uris (list(UploadedFile)): the documents to be loaded

        Returns:
            list(langchain.schema.Document): A list of document objects
        """
        # keep track of documents
        self.uploaded_documents.extend(document_uris)

        type_switch = {
            "text/plain": self.load_from_uploaded_text,
            "application/pdf": self.load_from_uploaded_pdf,
            "application/vnd.openxmlformats-officedocument.presentationml.presentation": self.load_from_uploaded_pptx,
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document": self.load_from_uploaded_docx,
        }

        # TODO other formats
        logger.info(f"Found {len(document_uris)} document uri(s)")
        logger.info(document_uris)

        all_documents = []
        for uri in document_uris:
            # suffix = Path(uri).suffix
            logger.info(f"Found {uri.name} a {uri.type} document")
            if uri.type in type_switch:
                # documents = self.load_from_uploaded_pdf(uri)
                documents = type_switch[uri.type](uri)
                logger.info(f"Loaded document {uri.name} - Got {len(documents)} document(s)")

                # set metadata
                for document in documents:
                    document.metadata = {"path": uri.name, "type": uri.type}

                all_documents.extend(documents)
            else:
                logger.info(f"Unknown document type {uri.type} for document {uri.name}")
                # TODO user warning

        logger.info(f"Loaded {len(all_documents)} document(s)")
        return all_documents

    def split_documents(self, documents: List[Any], chunk_size: int = 1000, chunk_overlap: int = 100) -> List[Any]:
        """
        Splits each document of the list of document passed as parameter.

        The splitter is a langchain.text_splitter.RecursiveCharacterTextSplitter.
        (check RecursiveCharacterTextSplitter documentation)

        Args:
            documents (list(langchain.schema.Document)): the documents to be splitted
            chunk_size (int): the size of the chunks
            chunk_overlap (int): the ampunt of overlap between chunks

        Returns:
            list(langchain.schema.Document): A list of documents resulting from the split
        """
        # Get your splitter ready.
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

        # Split your docs into texts.
        texts = text_splitter.split_documents(documents)

        return texts

    def build_vector_store(self, documents: List[Any]) -> Any:
        """
        Build a vectore store from the  documents or chunk passed as parameters.

        Args:
            documents (List(langchain.schema.Document)): the documents to put in the vectore store

        Returns:
            langchain.vectorstores.FAISS: The vector store
        """
        # build a vectore store from the given documents or chunks
        if not self.embeddings:
            self.embeddings = self.get_text_embeddings()

        self.add_generated_document(f"The company has {len(self.uploaded_documents)} policies.")
        all_documents = []
        all_documents.extend(documents)
        all_documents.extend(self.generated_documents)
        # Embedd your texts andd store them in the vector database.
        # database is in memory.
        self.vector_store = FAISS.from_documents(all_documents, self.embeddings)
        logger.info("VectorStore is ready")
        return self.vector_store

    def save_vector_store(self, path: str):
        self.vector_store .save_local(path)

    def load_vector_store(self, path: str):
        if not self.embeddings:
            self.embeddings = self.get_text_embeddings()
        self.vector_store = FAISS.load_local(path, self.embeddings)


    def get_count(self) -> int:
        """
        Get the number of uploaded documents.

        May not match the number of documents of the vector store.
        The vectore store actually store chunks of documents.

        Returns:
            int: The number of documents
        """
        return len(self.uploaded_documents)

    def get_vector_store(self) -> Any:
        """
        Get the vector store instance.

        Returns:
            langchain.vectorstores.FAISS: The vector store
        """
        return self.vector_store

    def get_text_embeddings(self) -> Any:
        """
        Setup the membedding model.

        Returns:
            langchain.embeddings.OpenAIEmbeddings: The embedding model
        """
        # Get embedding engine ready.
        embeddings = OpenAIEmbeddings(
            openai_api_type=self.llm_context["openai_api_type"],
            openai_api_base=self.llm_context["openai_api_base"],
            openai_api_key=self.llm_context["openai_api_key"],
            # deployment=self.llm_context["deployment_name"],
            model=self.llm_context["embedding_model_name"],
            chunk_size=1,
        )
        return embeddings

    def load_from_uploaded_pdf(self, uploaded_file_uri):
        """
        Extracts text from a PDF file using langchain's UnstructuredPDFLoader.

        The text is embedded in a Document object and the loader returns a list of documents.

        Args:
            file_path (str): The path to the file.

        Returns:
            list(langchain.schema.Document): A list of documents.
        """
        # Save the uploaded PDF file to a temporary file
        with NamedTemporaryFile(delete=False) as tmp_file:
            shutil.copyfileobj(uploaded_file_uri, tmp_file)

        # Load the PDF file using UnstructuredPDFLoader
        loader = UnstructuredPDFLoader(tmp_file.name)
        documents = loader.load()

        # Extract the text from the PDF pages
        # text = ''
        # for page in document.pages:
        # text += page.text.strip() + '\n\n'

        # Remove the temporary file
        os.unlink(tmp_file.name)

        return documents

    def load_from_uploaded_pptx(self, uploaded_file_uri):
        """
        Extracts text from a PPTX file using langchain's UnstructuredPowerPointLoader.

        The text is embedded in a Document object and the loader returns a list of documents.

        Args:
            file_path (str): The path to the file.

        Returns:
            list(langchain.schema.Document): A list of documents.
        """
        # Load the PPTX file using UnstructuredPowerPointLoader
        # Save the uploaded  file to a temporary file
        with NamedTemporaryFile(delete=False) as tmp_file:
            shutil.copyfileobj(uploaded_file_uri, tmp_file)

        loader = UnstructuredPowerPointLoader(tmp_file.name)
        presentations = loader.load()

        # Remove the temporary file
        os.unlink(tmp_file.name)

        return presentations

    def load_from_uploaded_docx(self, uploaded_file_uri):
        """
        Extracts text from a .docx file using langchain's UnstructuredDocxLoader.

        The text is embedded in a Document object and the loader returns a list of documents.

        Args:
            file_path (str): The path to the file.

        Returns:
            list(langchain.schema.Document): A list of documents.
        """
        # Load the .docx file using UnstructuredDocxLoader
        # Load the PPTX file using UnstructuredPowerPointLoader
        # Save the uploaded  file to a temporary file
        with NamedTemporaryFile(delete=False) as tmp_file:
            shutil.copyfileobj(uploaded_file_uri, tmp_file)

        loader = UnstructuredWordDocumentLoader(tmp_file.name)
        documents = loader.load()

        # Extract the text from the .docx file
        # text = ""
        # for para in document.paragraphs:
        #    text += para.text.strip() + "\n\n"

        # return text.strip()

        # Remove the temporary file
        os.unlink(tmp_file.name)

        return documents

    def load_from_uploaded_text(self, uploaded_file_uri):
        """
        Extracts text from a TXT file using langchain's TextReader.

        The text is embedded in a Document object and the loader returns a list of documents.

        Args:
            file_path (str): The path to the file.

        Returns:
            list(langchain.schema.Document): A list of documents.
        """
        # Load the PPTX file using UnstructuredPowerPointLoader
        # Save the uploaded  file to a temporary file
        with NamedTemporaryFile(delete=False) as tmp_file:
            shutil.copyfileobj(uploaded_file_uri, tmp_file)

        loader = TextLoader(tmp_file.name)
        texts = loader.load()

        # Remove the temporary file
        os.unlink(tmp_file.name)

        return texts

    def add_generated_document(self, text: str) -> None:
        """
        Add a document in the corpus based on the text passed as parameter.

        Args:
            text (str): the text to add as a document
        """
        document = Document(page_content=text, metadata={"path": "instructions", "type": "text/plain"})
        self.generated_documents.append(document)

    def add_summary_document(self, document_type: str) -> None:
        """
        Add a summary document stating the number of documents and the list of documents.

        Args:
            document_type (str): the text defining the type of document for the user
        """
        texts = []
        texts.append(
            "You will use this document when you are asked the number of documents, or the list of documents\n"
        )
        texts.append(f"The company has {len(self.uploaded_documents)} {document_type}. \n")
        texts.append(f"Here is the list of {document_type} of the company available to the assistant:")
        for uploaded_document in self.uploaded_documents:
            texts.append(f"{uploaded_document.name}")
        summary = "\n".join(texts)
        logger.info(f"{summary=}")
        self.add_generated_document(summary)
