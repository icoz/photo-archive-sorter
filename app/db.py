#!/usr/bin/env python3
# coding: utf8

import pymongo
import gridfs

# import sys
from config import DATABASE_URI, DATABASE_NAME


# establish a connection to the database
# connection = pymongo.MongoClient("mongodb://localhost")
db_connection = pymongo.MongoClient(DATABASE_URI)

def _db_open(db_name):
    return db_connection.__getattr__(db_name)


db = _db_open(DATABASE_NAME)
fs = gridfs.GridFS(db, "files")
ObjectId = pymongo.bulk.ObjectId
# https://api.mongodb.com/python/current/api/gridfs/index.html


# new file
# with fs.new_file(**kwargs) as f:
#     f.write(...)
### OR ####
# fs.put(data, **kwargs)

# kwargs: 
# "_id": unique ID for this file (default: ObjectId) - this "_id" must not have already been used for another file
# "filename": human name for the file
# "contentType" or "content_type": valid mime-type for the file
# "chunkSize" or "chunk_size": size of each of the chunks, in bytes (default: 255 kb)
# "encoding": encoding used for this file. In Python 2, any unicode that is written to the file will be converted to a str. In Python 3, any str that is written to the file will be converted to bytes.

# https://api.mongodb.com/python/current/api/pymongo/client_session.html#pymongo.client_session.ClientSession
# orders = client.db.orders
# inventory = client.db.inventory
# with client.start_session() as session:
#     with session.start_transaction():
#         orders.insert_one({"sku": "abc123", "qty": 100}, session=session)
#         inventory.update_one({"sku": "abc123", "qty": {"$gte": 100}},
#                              {"$inc": {"qty": -100}}, session=session)


