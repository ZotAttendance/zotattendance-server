from pymongo import MongoClient


def get_user_record(user_details):
    mongo_client = MongoClient('localhost', 27017)
    sso_collection = mongo_client['zotattendance-core']['user_details']
    user_record = sso_collection.find_one({"campus_id":user_details['campus_id']})
    if not user_record:
        user_record = get_new_user_record(user_details['campus_id'],user_details['ucinetid'])
        sso_collection.insert_one(user_record)
    else:
        user_record.pop("_id")
    return user_record


def get_new_user_record(campus_id, ucinetid):
    # TODO(Duo Wang): pull class enrollment data from Canvas instead of hard-coding classes
    return {
        "campus_id": campus_id,
        "ucinetid": ucinetid,
        "courses": ["CS222P", "CS295P", "CS261P"]
    }