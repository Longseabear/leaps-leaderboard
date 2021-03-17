import flask
import pymysql
import OpenSSL
import sqlite3

con = sqlite3.connect('example.db')
cur = con.cursor()

# cur.execute('''CREATE TABLE stocks
#                (date text, trans text, symbol text, qty real, price real)''')
#cur.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

t = ('2016',)

purchases = [('2006-03-28', 'BUY', 'IBM', 1000, 45.00),
             ('2006-04-05', 'BUY', 'MSFT', 1000, 72.00),
             ('2006-04-06', 'SELL', 'IBM', 500, 53.00),
            ]

cur.executemany('INSERT INTO stocks VALUES (?,?,?,?,?)', purchases)
con.commit()

cur.execute('SELECT * from stocks')
print(cur.fetchall())

con.commit()
con.close()