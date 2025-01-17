import pymongo
import pymssql

SQL_EXPORT_DB = 'nosqlprj'
RECORDS_COL = 'records'

client = pymongo.MongoClient('mongodb://172.16.13.26:27023/')
mydb = client[SQL_EXPORT_DB]
mycol = mydb[RECORDS_COL]

client_3sh = pymongo.MongoClient('mongodb://172.16.13.26:27030/')
mydb_3sh = client_3sh[SQL_EXPORT_DB]
mycol_3sh = mydb_3sh[RECORDS_COL]

client_6sh = pymongo.MongoClient('mongodb://172.16.13.26:27032/')
mydb_6sh = client_6sh[SQL_EXPORT_DB]
mycol_6sh = mydb_6sh[RECORDS_COL]

conn = pymssql.connect(server='172.16.8.10\RICESTSQLSERVER', user='sa', password='RICEST@SQLSERVER2008', database='NOSQL_db')  
cursor = conn.cursor()
 
cursor.execute('SELECT TOP(3000000) ID, DocID, Abstract FROM [NOSQL_db].[dbo].[LangFilterIEEE]')

sum = 0
all = []
bulks = 0
for item in cursor:
    new_dict = {}
    new_dict['_id'] = item[0]
    new_dict['DocID'] = item[1]
    new_dict['Abstract'] = item[2]
    all += [new_dict]
    sum+=1
    if sum == 1:
        mycol.insert_many(all)
        mycol_3sh.insert_many(all)
        mycol_6sh.insert_many(all)
        sum = 0
        bulks += 1
        left = 60 - bulks
        print("\r%d bulks migrated to Mongo. %d left." % (bulks, left), end="")
        all = []