#dao sta per data access object 
import sqlite3

def get_utenti():
    conn=sqlite3.connect('db/social.db')
    conn.row_factory=sqlite3.Row
    cursor=conn.cursor()

    sql='SELECT username FROM utenti ORDER BY username ASC'
    cursor.execute(sql)
    utenti=cursor.fetchall()
    cursor.close()
    conn.close()

    return utenti

def get_posts():
    conn =sqlite3.connect('db/social.db')
    conn.row_factory = sqlite3.Row #di default è inizializzato a tupla,
    # noi però vogliamo a riga (sovrainsieme di un dizionario)
    cursor= conn.cursor()

    sql = 'SELECT post_id, data, testo, imgPost, imgProfilo, username, posts.utente_id FROM posts, utenti where posts.utente_id = utenti.utente_id ORDER BY data DESC'
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

    sql = 'SELECT post_id, data, testo, imgPost, imgProfilo, username FROM posts, utenti where post_id = ? and posts.utente_id = utenti.utente_id'
    cursor.execute(sql, (id,))
    post= cursor.fetchone()

    cursor.close()
    conn.close()

    return post

def add_post(post):
    conn =sqlite3.connect('db/social.db')
    conn.row_factory = sqlite3.Row 
    cursor =conn.cursor()

    sql2= 'SELECT utente_id FROM utenti WHERE username=?'
    cursor.execute(sql2, (post['username'],))
    idUtente=cursor.fetchone()
    #print(idUtente[0])

    success= False
    sql ='INSERT INTO posts(data, testo, imgPost, utente_id) VALUES(?,?,?,?)'
    
    try:
        cursor.execute(sql, (post['data'] ,post['testo'], post['imgPost'], idUtente[0]))
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

    sql = 'SELECT comment_id, commento, rating, post_id, dataP, username, imgProfilo FROM commenti, utenti where post_id = ? and commenti.utente_id = utenti.utente_id'
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

    sql2= 'SELECT utente_id FROM utenti WHERE username=?'
    cursor.execute(sql2, (commento['username'],))
    idUtente=cursor.fetchone()

    success= False
    sql ='INSERT INTO commenti(commento, rating, post_id, dataP, utente_id) VALUES(?,?,?,?,?)'
    
    try:
        cursor.execute(sql, (commento['commento'] ,commento['rating'], commento['post_id'], commento['dataP'], idUtente[0]))
        conn.commit()
        success=True
    except Exception as e:
        print("ERROR",str(e))
        conn.rollback()

    cursor.close()
    conn.close()

    return success

def get_user_by_username(username):
    conn =sqlite3.connect('db/social.db')
    conn.row_factory = sqlite3.Row 
    cursor= conn.cursor()

    sql = 'SELECT * FROM utenti where username=?'
    cursor.execute(sql, (username, ))
    user= cursor.fetchone()

    #print(user)

    cursor.close()
    conn.close()

    return user

def get_user_by_id(id_utente):
    query = 'SELECT * FROM utenti WHERE utente_id = ?'

    connection = sqlite3.connect('db/social.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute(query, (id_utente,))

    result = cursor.fetchone()
    
    cursor.close()
    connection.close()

    return result

def crea_utente(nuovo_utente):
    query = 'INSERT INTO utenti(username,imgProfilo,password) VALUES (?,?,?)'

    connection = sqlite3.connect('db/social.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    success = False

    try:
        cursor.execute(query, (nuovo_utente['username'],nuovo_utente['imgProfilo'], nuovo_utente['password']))
        connection.commit()
        success = True
    except Exception as e:
        print('Error', str(e))
        connection.rollback()

    cursor.close()
    connection.close()

    return success


