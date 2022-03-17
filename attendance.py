import imp
from pymongo import MongoClient
from plugins import popquiz

def get_attendance_data(campus_id,course_code,class_num):
    return popquiz.get_attendance(campus_id,course_code,class_num) 