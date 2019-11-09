
from sqlalchemy import *
import psycopg2


params = {
  'database': 'proj1part2',
  'user': 'zq2172',
  'password': '12345678',
  'host': '34.74.165.156',
  'port': 5432
}

conn = psycopg2.connect(**params)
cur = conn.cursor()
queryString = "SELECT c.name AS name FROM product p, belongs_to bt, categories c WHERE bt.product_id = p.product_id AND c.category_id = bt.category_id AND p.name LIKE 'Iphone%'"
cur.execute(queryString)
record = cur.fetchall()
print(record)

cur.execute("SELECT name FROM product")
products = cur.fetchall()
print(products)

cur.execute("SELECT count(*) FROM \"order\"")
count = cur.fetchone()
print(count[0])
