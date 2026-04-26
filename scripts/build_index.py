import os
import glob
import chromadb
from langchain_text_splitters import RecursiveCharacterTextSplitter

def build_index():
    print("Initializing ChromaDB...")
    # Initialize ChromaDB locally
    client = chromadb.PersistentClient(path="./.chroma_data")

    # Create or get the collection
    collection = client.get_or_create_collection(name="knowledge_base")

    # Gather all markdown documents
    docs_dir = "./docs"
    markdown_files = glob.glob(f"{docs_dir}/**/*.md", recursive=True)

    if not markdown_files:
        print("No markdown files found in /docs")
        return

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        length_function=len,
        is_separator_regex=False,
    )

    documents = []
    metadatas = []
    ids = []

    print(f"Found {len(markdown_files)} markdown files.")

    doc_id = 1
    for filepath in markdown_files:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        chunks = text_splitter.split_text(content)
        for i, chunk in enumerate(chunks):
            documents.append(chunk)
            metadatas.append({"source": filepath, "chunk_index": i})
            ids.append(f"doc_{doc_id}_{i}")
        doc_id += 1

    if documents:
        print(f"Upserting {len(documents)} chunks to ChromaDB...")
        collection.upsert(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        print("Index build complete!")
    else:
        print("No content to index.")

if __name__ == "__main__":
    build_index()
