from pymongo import MongoClient
from datetime import datetime, timedelta
from django.utils import timezone
import certifi

connection_string = "mongodb+srv://jay5150:AR53hole!!5150@footydb01.rn0e5.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(connection_string, tlsCAFile=certifi.where())
dbname = client['footy']


def add_record(collection, document):
    collection_name = dbname[collection]
    collection_name.insert_one(document)


def update_record(collection, record, document):
    collection_name = dbname[collection]
    collection_name.replace_one(record, document)


def update_one_record(collection, filter_doc, update_doc):
    collection_name = dbname[collection]
    collection_name.update_one(filter_doc, update_doc, upsert=True)


def count_documents(collection, query):
    collection_name = dbname[collection]
    return collection_name.count_documents(query)


def document_exists(collection, query):
    count = count_documents(collection, query)
    if count == 0 or count is None:
        return False
    else:
        return True


def get_single_info(collection, query):
    collection_name = dbname[collection]
    return collection_name.find_one(query,{'_id': False})


def get_multiple_info(collection, querystring):
    a_list = []
    collection_name = dbname[collection]
    for x in collection_name.find(querystring):
        a_list.append(x)
    return a_list


def get_info_conditional_or(collection, query):
    querystring = {"$or": query}
    a_list = []
    collection_name = dbname[collection]
    for x in collection_name.find(querystring):
        a_list.append(x)
    return a_list

def get_info_conditional_and(collection, query):
    querystring = {"$and":query}
    a_list = []
    collection_name = dbname[collection]
    for x in collection_name.find(querystring):
        a_list.append(x)
    return a_list


def get_all_info(collection):
    a_list = []
    collection_name = dbname[collection]
    for x in collection_name.find({}):
        a_list.append(x)
    return a_list


def check_last_updated(collection, query):
    collection_name = dbname[collection]
    record = collection_name.find_one(query)
    if record is not None:
        x = record['last_updated']
        time_delta = datetime.utcnow() - x
        return time_delta
    else:
        return timezone.timedelta(hours=1)


