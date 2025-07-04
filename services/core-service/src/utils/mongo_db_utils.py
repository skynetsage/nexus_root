from datetime import datetime
from bson import ObjectId


def convert_mongo_doc_to_json(doc: dict) -> dict:
    if not doc:
        return doc
    converted = {}
    for key, value in doc.items():
        if isinstance(value, ObjectId):
            converted[key] = str(value)
        elif isinstance(value, datetime):
            converted[key] = value.isoformat()
        else:
            converted[key] = value
    return converted
