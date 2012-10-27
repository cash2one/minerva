#!/usr/bin/env python
#

from pymongo.connection import Connection
MONGO_CON = '127.0.0.1:27017'
mongo_con = Connection(MONGO_CON)
from pymongo.database import Database
MONGO_DB = 'searchet'
mongo_db = Database(mongo_con, MONGO_DB)
from pymongo.collection import Collection
MONGO_COL = 'penser'
mongo_col = Collection(mongo_db, MONGO_COL)

mongo_col.insert({"uir":1,"name":"penser"})
mongo_col.insert({"uir":1,"name":"vim"})

data = mongo_col.find_one({"name":"vim"})

for d in data:
    print d

print data
a = data["name"]
print a