import hashlib
import time

import chromadb

MEMORY_PATH = "./data/memory"
COLLECTION_NAME = "conversations"
TOP_K = 3


def _get_collection() -> chromadb.Collection:
    client = chromadb.PersistentClient(path=MEMORY_PATH)
    return client.get_or_create_collection(COLLECTION_NAME)


def save(user_message: str, assistant_message: str) -> None:
    content = f"User: {user_message}\nAssistant: {assistant_message}"
    doc_id = hashlib.md5(content.encode()).hexdigest()

    collection = _get_collection()
    collection.upsert(
        ids=[doc_id],
        documents=[content],
        metadatas=[{"timestamp": time.time()}],
    )


def search(query: str) -> list[str]:
    collection = _get_collection()

    if collection.count() == 0:
        return []

    results = collection.query(
        query_texts=[query],
        n_results=min(TOP_K, collection.count()),
    )

    # Trier par timestamp décroissant (plus récent en premier)
    hits = zip(
        results["documents"][0],
        results["metadatas"][0],
    )
    sorted_hits = sorted(hits, key=lambda x: x[1]["timestamp"], reverse=True)

    return [doc for doc, _ in sorted_hits]
