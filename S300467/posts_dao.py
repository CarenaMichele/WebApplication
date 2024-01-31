import sqlite3

def crea_utente(nuovo_utente):
    query = 'INSERT INTO UTENTI(nome,cognome,username,password,tipo) VALUES (?,?,?,?,?)'

    connection = sqlite3.connect('db/affitti.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    success = False

    try:
        cursor.execute(query, (nuovo_utente['nome'],nuovo_utente['cognome'], nuovo_utente['username'], nuovo_utente['password'], nuovo_utente['tipo']))
        connection.commit()
        success = True
    except Exception as e:
        print('Error', str(e))
        connection.rollback()

    cursor.close()
    connection.close()

    return success

def get_user_by_id(id_utente):
    query = 'SELECT * FROM UTENTI WHERE idUtente = ?'

    connection = sqlite3.connect('db/affitti.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute(query, (id_utente,))

    result = cursor.fetchone()
    
    cursor.close()
    connection.close()

    return result

def get_user_by_username(username):
    conn =sqlite3.connect('db/affitti.db')
    conn.row_factory = sqlite3.Row 
    cursor= conn.cursor()

    sql = 'SELECT * FROM UTENTI where username=?'
    cursor.execute(sql, (username, ))
    user= cursor.fetchone()

    cursor.close()
    conn.close()

    return user

def add_ann(annuncio):
    conn =sqlite3.connect('db/affitti.db')
    conn.row_factory = sqlite3.Row 
    cursor= conn.cursor()

    #sql2= 'SELECT utente_id FROM utenti WHERE username=?'
    #cursor.execute(sql2, (commento['username'],))
    #idUtente=cursor.fetchone()

    success= False
    sql ='INSERT INTO ANNUNCI(titolo, indirizzo, tipoCasa, numeroLocali, descrizione, prezzoMensile, arredamento, disponibilita, idUtente) VALUES(?,?,?,?,?,?,?,?,?)'
    #non usare tipo NUMERIC nel db per il prezzo perchè da db locked error 
    try:
        cursor.execute(sql, (annuncio['titolo'], annuncio['indirizzo'], annuncio['tipoC'], annuncio['numLocali'], annuncio['descrizione'], annuncio['prezzoM'], annuncio['arredato'], annuncio['disponibile'], annuncio['idLocatore']))
        conn.commit()
        success=True
    except Exception as e:
        print("ERROR",str(e))
        conn.rollback()

    cursor.close()
    conn.close()

    return success