from newutils import *

es5_client = Elasticsearch5(HOSTIP + ':9205', timeout=120)
es5_client_3shard = Elasticsearch5(HOSTIP + ':9206', timeout=120)
mongo_client = pymongo.MongoClient('mongodb://%s:27023/' % HOSTIP)
mongo_client_3sh = pymongo.MongoClient('mongodb://%s:27030/' % HOSTIP)
mongo_client_6sh = pymongo.MongoClient('mongodb://%s:27032/' % HOSTIP)
mssql_client = pymssql.connect(server=HOSTIP, user='sa', password='MSSql-pwd', database=DB)
mysql_client = mysql.connector.connect(host='localhost', user="root", passwd="password", db=DB)

def runworkload(db, optype, ref, conn):
    times = []
    with open(ref,"r") as file1:
        line_no = 0
        while True:
            line = file1.readline()
            line_no += 1
            print("\r DB = %s | OP = %s | PROCESSING LINE %d" % (db, optype, line_no), end="")
            if line == "":
                break
            words = None
            if optype == EXACTPHRASE:
                words = [line.rstrip()]
            else:
                words = line.rstrip().split()
            if db == ELASTIC5:
                re = elastic5_search("nosqlprj", optype, words, conn)
            elif db == ELASTIC5_3:
                re = elastic5_search("nosqlprj-3shard", optype, words, conn)
            elif db == ELASTIC5_6:
                re = elastic5_search("nosqlprj-6shard", optype, words, conn)
            elif db == MONGODB:
                re = mongo_search(optype, words, conn, "nosqlprj")
            elif db == MONGODB_3:
                re = mongo_search(optype, words, conn, "nosqlprj-3shard")
            elif db == MONGODB_6:
                re = mongo_search(optype, words, conn, "nosqlprj-6shard")
            elif db == MSSQL:
                re = mssql_search(optype, words, conn)
            elif db == MYSQL:
                re = mysql_search(optype, words, conn)
            times += [re[1]] 
        print("\r DB = %s | OP = %s | DONE! | Total Queries = %d" % (db, optype, line_no-1), end="")
    mean = sum(times)/len(times)
    return mean*1000

SRC = "randomwordstemp.txt"
SRCP = "randomphrasetemp.txt"
OPS = [SINGLE, AND, OR ,EXACTPHRASE]
DBS = [(ELASTIC5, es5_client), (ELASTIC5_3, es5_client_3shard), (ELASTIC5_6, es5_client_3shard)]
DBS += [(MSSQL, mssql_client), (MYSQL, mysql_client)]
DBS += [(MONGODB, mongo_client), (MONGODB_3, mongo_client_3sh), (MONGODB_6, mongo_client_6sh)]

for db in DBS:
    for op in OPS:
        if op == EXACTPHRASE:
            src = SRCP
        else:
            src = SRC
        mean = runworkload(db[0], op, src, db[1])
        print(" | AvgLatency: %f ms" % mean)
