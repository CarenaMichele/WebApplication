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
    cursor2=conn.cursor()
    #success= False
    sql ='INSERT INTO ANNUNCI(titolo, indirizzo, tipoCasa, numeroLocali, descrizione, prezzoMensile, arredamento, disponibilita, idUtente) VALUES(?,?,?,?,?,?,?,?,?)'
    #non usare tipo NUMERIC nel db per il prezzo perchè da db locked error 
    try:
        cursor.execute(sql, (annuncio['titolo'], annuncio['indirizzo'], annuncio['tipoC'], annuncio['numLocali'], annuncio['descrizione'], annuncio['prezzoM'], annuncio['arredato'], annuncio['disponibile'], annuncio['idLocatore']))
        conn.commit()
        #success=True
    except Exception as e:
        print("ERROR",str(e))
        conn.rollback()
    
    cursor.close()

    sql2 = 'SELECT idAnnuncio FROM ANNUNCI where titolo=? and idUtente=?'

    cursor2.execute(sql2, (annuncio['titolo'], annuncio['idLocatore']))
    sol= cursor2.fetchone()

    cursor2.close()
    conn.close()

    return sol

def add_foto(foto, id):
    conn=sqlite3.connect('db/affitti.db')
    conn.row_factory=sqlite3.Row
    cursor=conn.cursor()
    success=False
    try:
        for i in foto:
            cursor.execute('INSERT INTO FOTO(urlFoto, idAnnuncio) VALUES (?,?)', (i, id))
        conn.commit()
        success=True
    except Exception as e:
        print("ERROR", str(e))
        conn.rollback()

    cursor.close()
    conn.close()

    return success

def get_annunci(id):
    conn =sqlite3.connect('db/affitti.db')
    conn.row_factory = sqlite3.Row 
    cursor= conn.cursor()

    sql = 'SELECT  ANNUNCI.idAnnuncio, titolo, indirizzo, tipoCasa, numeroLocali, descrizione, \
    prezzoMensile, arredamento, disponibilita, urlFoto FROM ANNUNCI, FOTO \
    where ANNUNCI.idUtente = ? and ANNUNCI.idAnnuncio = FOTO.idAnnuncio \
    GROUP BY ANNUNCI.idAnnuncio'
    #uso del group by per raggruppare le informazioni identiche (foto) relative allo stesso idAnnuncio
    cursor.execute(sql, (id,))
    annunci= cursor.fetchall()
    #print(annunci)

    cursor.close()
    conn.close()

    return annunci

def get_singleAnnuncio(id):
    conn =sqlite3.connect('db/affitti.db')
    conn.row_factory = sqlite3.Row 
    cursor= conn.cursor()
    #utilizzo di GROUP_CONCAT per concatenare su un'unica riga tutte le foto di quell'annuncio
    sql = '''SELECT ANNUNCI.* ,GROUP_CONCAT(urlFoto, ',') AS foto_concatenate 
           FROM ANNUNCI, FOTO 
           where ANNUNCI.idAnnuncio = ? and ANNUNCI.idAnnuncio = FOTO.idAnnuncio 
           GROUP BY ANNUNCI.idAnnuncio'''
    cursor.execute(sql, (id,))
    annuncio= cursor.fetchone()  #vedere se meglio fetchone o fetchall
    #print(annunci)

    cursor.close()
    conn.close()

    return annuncio

def mod_ann(annuncio, id):
    conn =sqlite3.connect('db/affitti.db')
    conn.row_factory = sqlite3.Row 
    cursor= conn.cursor()
    success= False
    sql ='UPDATE ANNUNCI SET titolo=?, tipoCasa=?, numeroLocali=?, descrizione=?, prezzoMensile=?, arredamento=?, disponibilita=? WHERE idAnnuncio= ? '
    try:
        cursor.execute(sql, (annuncio['titolo'], annuncio['tipoC'], annuncio['numLocali'], annuncio['descrizione'], annuncio['prezzoM'], annuncio['arredato'], annuncio['disponibile'], id[0]))
        conn.commit()
        success=True
    except Exception as e:
        print("ERROR",str(e))
        conn.rollback()
    
    cursor.close()
    conn.close()

    return success

def get_id(annuncio):
    conn =sqlite3.connect('db/affitti.db')
    conn.row_factory = sqlite3.Row 
    cursor= conn.cursor()

    sql = 'SELECT idAnnuncio FROM ANNUNCI where indirizzo=? and idUtente=?'

    cursor.execute(sql, (annuncio['indirizzo'], annuncio['idLocatore']))
    sol= cursor.fetchone()

    cursor.close()
    conn.close()

    return sol