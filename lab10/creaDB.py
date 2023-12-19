import sqlite3

conn=sqlite3.connect('social.db')

cursor= conn.cursor()

#create table

com1 = """CREATE TABLE IF NOT EXISTS post(post_id INTEGER PRIMARY KEY, username TEXT, data TEXT, testo TEXT, imgProfilo TEXT, imgPost TEXT)""" 

cursor.execute(com1)


#create another table

com2= """CREATE TABLE IF NOT EXISTS commento(comment_id INTEGER PRIMARY KEY, username TEXT,commento TEXT, rating INTEGER, imgCommento TEXT, post_id INTEGER, 
FOREIGN KEY(post_id) REFERENCES post(post_id))"""

cursor.execute(com2)

#add tuples

cursor.execute("INSERT INTO post VALUES (0, 'Davide', '2 giorni fa', 'ciao', 'img/facciaD.jpg' ,'img/davide.jpg'")
cursor.execute("INSERT INTO post VALUES (1, 'Michele', '2 giorni fa', 'come', 'img/facciaM.jpg' ,'img/davide.jpg'")
cursor.execute("INSERT INTO post VALUES (2, 'Federico', '2 giorni fa', 'va', 'img/facciaF.jpg' ,'img/davide.jpg'")

cursor.execute("INSERT INTO commento VALUES (0, 'Anonimo', 'brutto', 1, ' ', 0)")

conn.commit()

cursor.close()

conn.close()

#get results

#cursor.execute("SELECT *FROM purchases")

#results=cursor.fethall()
#print(results)

#update tuples

#cursor.execute("UPDATE purchases SET total_cost = 3.67 WHERE purchase_id =54")

#delete

#cursor.execute("DELETE FROM purchases WHERE purchase_id =54")