from pymongo import MongoClient, ReadPreference

Args = {
    "destination_mongo_uri": "",
    "source_mongo_uri": "",
}

source_client = MongoClient(Args["source_mongo_uri"])
source_secondary_db = source_client.get_database(
    "nailedit",
    read_preference=ReadPreference.SECONDARY,
)

dest_client = MongoClient(Args["destination_mongo_uri"])
dest_secondary_db = dest_client.get_database(
    "naily_prod",
    read_preference=ReadPreference.SECONDARY,
)


def get_yolo_tagged_data_from_nailedit():
    search_query = {
        "member": "yolo",
        "is_tagged": True,
    }
    projection = {
        "_id": False,
        "cropped_id": True,
        "bounding_box": True,
        "categories": True,
    }

    cropped_nails = source_secondary_db.get_collection("categories").find(search_query, projection)
    return list(cropped_nails)


def get_nail_image_from_naily(nail_id: str):
    search_query = {
        "nail_id": nail_id,
    }
    projection = {
        "_id": False,
        "thumb_image": True,
    }

    nail = dest_secondary_db.get_collection("nails").find_one(search_query, projection)
    return dict(nail) if nail else dict()
