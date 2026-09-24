"""Create the local Qdrant collection when it does not exist."""

from app.settings import Settings
from app.vector import build_qdrant_client, ensure_collection


def main() -> None:
    settings = Settings()
    client = build_qdrant_client(
        url=settings.qdrant_url,
        api_key=settings.qdrant_api_key,
    )
    created = ensure_collection(
        client=client,
        collection_name=settings.qdrant_collection_name,
        vector_size=settings.qdrant_vector_size,
    )
    if created:
        print(f"Created collection: {settings.qdrant_collection_name}")
    else:
        print(f"Collection already exists: {settings.qdrant_collection_name}")


if __name__ == "__main__":
    main()
