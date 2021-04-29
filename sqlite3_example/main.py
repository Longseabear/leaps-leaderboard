import sqlite3

conn = sqlite3.connect("test.db")
conn.row_factory = sqlite3.Row

cur = conn.cursor()

"""
create table t (row int);
insert into t values (1),(2),(3);
SELECT AVG((t.row - sub.a) * (t.row - sub.a)) as var from t, 
    (SELECT AVG(row) AS a FROM t) AS sub;
"""
#cur.execute("create table datas (val int)")
cur.execute("insert into datas values (1),(2),(3)")
#conn.commit()
cur.execute('''select * from datas''')
for row in cur:
    print([i for i in row])

for row in cur.execute('''SELECT AVG(datas.val * datas.val) as squareMean, AVG (datas.val) as meanSquare from datas, 
    (SELECT AVG(val) AS a FROM datas) AS sub''').fetchall():
    print(row.keys())

input()


cur.execute("select * from customer")
rows = cur.fetchall()
for row in rows:
    print(row.keys())

print(cur.execute("select count(*) from customer group by region").fetchall())
data = cur.execute("select count(*) from customer group by region").fetchall()
#print(data.tables)
print(data[0].keys())
print(len(data))
# insert example

print(cur.execute('''SELECT name FROM PRAGMA_TABLE_INFO('customer')''').fetchall()[2]['name'])
conn.close()

# witth conn으로 커넥션에 대한 처리 가능

# select 머시기 from where 조건 (= != IS NULL / IS NOT NULL)
# SELECT FROM WHERE ORDER BY 정렬의 기준이 되는 컬럼, DESC하면 내림차순
# SELECT A FROM TABLE WHERE 조건 ORDER BY 정렬의기준이되는 컬럼 LIMIT

# SELECT COUNT(*) AS 개수 FROM 테이블 명 (NULL 포함해서 카운트

# INNER JOIN, LEFT JOIN, CROSS JOIN


