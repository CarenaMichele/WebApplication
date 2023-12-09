#dao sta per data access object 
import sqlite3

def get_posts():
    conn =sqlite3.connect('db/social.db')
    conn.row_factory = sqlite3.Row #di default è inizializzato a tupla,
    # noi però vogliamo a riga (sovrainsieme di un dizionario)
    cursor= conn.cursor()

    sql = 'SELECT * FROM posts ORDER BY data DESC'
    cursor.execute(sql)
    posts= cursor.fetchall()
    #print(posts)

    cursor.close()
    conn.close()
    
    return posts

def get_post(id):
    conn =sqlite3.connect('db/social.db')
    conn.row_factory = sqlite3.Row 
    cursor= conn.cursor()

    sql = 'SELECT * FROM posts where post_id = ?'
    cursor.execute(sql, (id,))
    post= cursor.fetchone()

    cursor.close()
    conn.close()

    return post

def add_post(post):
    conn =sqlite3.connect('db/social.db')
    conn.row_factory = sqlite3.Row 
    cursor= conn.cursor()

    success= False
    sql ='INSERT INTO posts(username, data, testo, imgProfilo, imgPost) VALUES(?,?,?,?,?)'
    
    try:
        cursor.execute(sql, (post['username'],post['data'] ,post['testo'], post['imgProfilo'], post['imgPost']))
        conn.commit()
        success=True
    except Exception as e:
        print("ERROR",str(e))
        conn.rollback()

    cursor.close()
    conn.close()

    return success

def get_comments(id):
    conn =sqlite3.connect('db/social.db')
    conn.row_factory = sqlite3.Row 
    cursor= conn.cursor()

    sql = 'SELECT * FROM commenti where post_id = ?'
    cursor.execute(sql, (id,))
    comments= cursor.fetchall()
    print(comments)

    cursor.close()
    conn.close()

    return comments

def add_comment(commento):
    conn =sqlite3.connect('db/social.db')
    conn.row_factory = sqlite3.Row 
    cursor= conn.cursor()

    success= False
    sql ='INSERT INTO commenti(username, commento, rating, imgCommento, post_id) VALUES(?,?,?,?,?)'
    
    try:
        cursor.execute(sql, (commento['username'],commento['commento'] ,commento['rating'], commento['imgCommento'], commento['post_id']))
        conn.commit()
        success=True
    except Exception as e:
        print("ERROR",str(e))
        conn.rollback()

    cursor.close()
    conn.close()

    return success

