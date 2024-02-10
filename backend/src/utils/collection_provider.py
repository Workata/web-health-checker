from tinydb import TinyDB
from typing import Dict


class CollectionProvider:
    COLLECTIONS_BASE_PATH: str = "./data/db"

    COLLECTION_NAME_TO_LOCATION: Dict[str, str] = {
        "services": f"{COLLECTIONS_BASE_PATH}/services.json",
    }

    def provide(self, collection_name: str) -> TinyDB:
        return TinyDB(self.COLLECTION_NAME_TO_LOCATION[collection_name])
