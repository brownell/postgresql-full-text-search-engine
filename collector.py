
import json
import os
import psycopg2
import psycopg2.extensions
import psycopg2.extras
import psycopg2.pool
import pprint

db_connection = psycopg2.connect(os.environ['MUTABLE_DATABASE_URL'])
cursor = db_connection.cursor()

db_connection_tsv = psycopg2.connect(os.environ['DB_URL'])
cursor_tsv = db_connection_tsv.cursor()
cursor_tsv.execute('SELECT tsv from fulltext_search')
tsvs = cursor_tsv.fetchall();
for tsv in tsvs:
    print(tsv)

cursor.execute( 'SELECT dataset_id, name, metadata FROM dataset offset 220 limit 10' )
datasets = cursor.fetchall();
cursor.close()

for dataset in datasets:
    # print('id', dataset[0], 'name', dataset[1], '\nmetadata', dataset[2], type(dataset[2]))
    query = "INSERT INTO fulltext_search (doc) VALUES (%s) RETURNING tsv"
    doc = str(dataset[0]) + ' ' + dataset[1] + ' ' + json.dumps(dataset[2]).replace('{','').replace('}','').replace('null','').replace(':','')
    print(doc, '\n')
    cursor_tsv.execute(query, [doc])
db_connection_tsv.commit()
cursor_tsv.close()
