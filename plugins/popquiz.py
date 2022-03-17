from pymongo import MongoClient
import datetime

def handle(data, session):
    mongo_client = MongoClient('localhost', 27017)
    plugin_collection = mongo_client['zotattendance-plugins']['popquiz']
    record = {
        "campus_id": session['user_record']['campus_id'],
        "ucinetid": session['user_record']['ucinetid'],
        "response": data['response'],
        "time_str": str(datetime.datetime.now()),
        "course_code": data['course_code'],
        # FIXME(Duo Wang): get class num from timestamp instead of hard-coding
        "class_num": 1
    }
    plugin_collection.insert_one(record)

def get_attendance(campus_id,course_code,class_num):
    mongo_client = MongoClient('localhost', 27017)
    plugin_collection = mongo_client['zotattendance-plugins']['popquiz']
    return plugin_collection.find_one({"campus_id":campus_id, "course_code":course_code, "class_num":class_num})