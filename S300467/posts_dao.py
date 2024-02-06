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
            cursor.execute('INSERT INTO FOTO(urlFoto, idAnnuncio, rimosso) VALUES (?,?,?)', (i, id, 'FALSE'))
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

    sql = '''SELECT  ANNUNCI.idAnnuncio, titolo, indirizzo, tipoCasa, numeroLocali, descrizione, 
    prezzoMensile, arredamento, disponibilita, urlFoto FROM ANNUNCI, FOTO 
    where ANNUNCI.idUtente = ? and ANNUNCI.idAnnuncio = FOTO.idAnnuncio and FOTO.rimosso= 'FALSE' 
    GROUP BY ANNUNCI.idAnnuncio'''
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
           where ANNUNCI.idAnnuncio = ? and ANNUNCI.idAnnuncio = FOTO.idAnnuncio and FOTO.rimosso ='FALSE' 
           GROUP BY ANNUNCI.idAnnuncio'''
    cursor.execute(sql, (id,))
    annuncio= cursor.fetchone()  #vedere se meglio fetchone o fetchall
    #print(annuncio['foto_concatenate'])

    cursor.close()
    conn.close()

    return annuncio

def mod_ann(annuncio, id):
    conn =sqlite3.connect('db/affitti.db')
    conn.row_factory = sqlite3.Row 
    cursor= conn.cursor()
    success=False
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

def mod_foto(foto,id):
    conn=sqlite3.connect('db/affitti.db')
    conn.row_factory=sqlite3.Row
    cursor=conn.cursor()
    success=False

    cursor.execute('SELECT urlFoto FROM FOTO WHERE idAnnuncio=? ',(id,))
    immDB = [row['urlFoto'] for row in cursor.fetchall()]
    print(immDB)
    print(foto)
    for immNuova in foto:
            if immNuova not in immDB:
            # Se l'immagine non è presente nel database, inseriscila
                cursor.execute('INSERT INTO FOTO (urlFoto, idAnnuncio, rimosso)VALUES (?, ?, ?)', (immNuova, id, 'FALSE'))
                conn.commit()
            success = True

    for immPresente in immDB:
        if immPresente not in foto:
            # Se l'immagine non è più presente nel vettore, segnala come "rimosso"
            cursor.execute('UPDATE FOTO SET rimosso = ? WHERE urlFoto = ? AND idAnnuncio=?', ('TRUE',immPresente, id))
            conn.commit()
            success = True

    return success

'''def mod_foto(foto, id):
    conn=sqlite3.connect('db/affitti.db')
    conn.row_factory=sqlite3.Row
    cursor=conn.cursor()
    success=False
    #vado a prendere tutte le foto presenti nel db di quel annuncio
    try:
        sql='SELECT urlFoto FROM FOTO WHERE idAnnuncio=?'
        cursor.execute(sql, (id,))
        listaFoto= cursor.fetchall()
        #print(listaFoto)
        success=True

        #for i in listaFoto:
         #   print(listaFoto[i])

        
    except sqlite3.Error as e:
        print("errore:", e)
        conn.rollback()

    cursor.close()
    conn.close()
    return success'''

    

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


def get_allAnnunci():
    conn =sqlite3.connect('db/affitti.db')
    conn.row_factory = sqlite3.Row 
    cursor= conn.cursor()

    sql = '''SELECT ANNUNCI.* ,GROUP_CONCAT(urlFoto, ',') AS foto_concatenate, UTENTI.nome, UTENTI.cognome
        FROM ANNUNCI, FOTO, UTENTI
        where ANNUNCI.idAnnuncio = FOTO.idAnnuncio and ANNUNCI.disponibilita = 'SI' and UTENTI.idUtente=ANNUNCI.idUtente and FOTO.rimosso='FALSE'
        GROUP BY ANNUNCI.idAnnuncio
        ORDER BY ANNUNCI.prezzoMensile DESC'''
    cursor.execute(sql, ())
    annunci= cursor.fetchall()

    cursor.close()
    conn.close()

    return annunci

def ordina(info):
    conn =sqlite3.connect('db/affitti.db')
    conn.row_factory = sqlite3.Row 
    cursor= conn.cursor()

    if info == 'numLocali':
        sql = '''SELECT ANNUNCI.* ,GROUP_CONCAT(urlFoto, ',') AS foto_concatenate 
            FROM ANNUNCI, FOTO 
            where ANNUNCI.idAnnuncio = FOTO.idAnnuncio and ANNUNCI.disponibilita = 'SI' and FOTO.rimosso='FALSE'
            GROUP BY ANNUNCI.idAnnuncio
            ORDER BY ANNUNCI.numeroLocali ASC, ANNUNCI.PrezzoMensile DESC'''
    else:
        sql = '''SELECT ANNUNCI.* ,GROUP_CONCAT(urlFoto, ',') AS foto_concatenate 
            FROM ANNUNCI, FOTO 
            where ANNUNCI.idAnnuncio = FOTO.idAnnuncio and ANNUNCI.disponibilita = 'SI' and FOTO.rimosso='FALSE'
            GROUP BY ANNUNCI.idAnnuncio
            ORDER BY ANNUNCI.prezzoMensile DESC, ANNUNCI.numeroLocali ASC'''
    cursor.execute(sql, ())
    annunci= cursor.fetchall()

    cursor.close()
    conn.close()

    return annunci

def gestioneOra(id, data):
    conn =sqlite3.connect('db/affitti.db')
    conn.row_factory = sqlite3.Row 
    cursor= conn.cursor()
    print(id,data)
    try:
        sql = "SELECT fasciaOraria FROM PRENOTAZIONI WHERE stato = 'accettata' AND Data=? AND idAnnuncio=?"
        cursor.execute(sql, (data,id))
        dataOra= cursor.fetchall() #come risultato tutte le ore non più disponibili
    except sqlite3.Error as e:
        print("ERROR",str(e))
        conn.rollback()

    cursor.close()
    conn.close()

    return dataOra


def add_prenotazione(idAnnuncio, info):
    conn=sqlite3.connect('db/affitti.db')
    conn.row_factory=sqlite3.Row
    cursor=conn.cursor()
    success=False
    sql ='INSERT INTO PRENOTAZIONI(Data, tipoVisita, fasciaOraria, stato, motivazioneRifiuto, idAnnuncio, idUtente) VALUES(?,?,?,?,?,?,?)'
    #non usare tipo NUMERIC nel db per il prezzo perchè da db locked error 
    try:
        cursor.execute(sql, (info['data'], info['modVisita'], info['fasciaOraria'], info['stato'], info['motivazioneRifiuto'], idAnnuncio, info['idUtente']))
        conn.commit()
        success=True
    except Exception as e:
        print("ERROR",str(e))
        conn.rollback()

    cursor.close()
    conn.close()

    return success


def prenotazioni(idAnnuncio, idUtente):
    conn =sqlite3.connect('db/affitti.db')
    conn.row_factory = sqlite3.Row 
    cursor= conn.cursor()

    sql = 'SELECT * FROM PRENOTAZIONI where idAnnuncio=? and idUtente=? and stato !="rifiutata"'

    cursor.execute(sql, (idAnnuncio,idUtente))
    sol= cursor.fetchall()

    cursor.close()
    conn.close()

    return sol

def get_prenotazioniC(id):
    conn =sqlite3.connect('db/affitti.db')
    conn.row_factory = sqlite3.Row 
    cursor= conn.cursor()

    sql = 'SELECT  * FROM PRENOTAZIONI where idUtente = ?'
    cursor.execute(sql, (id,))
    prenotazioni= cursor.fetchall()

    cursor.close()
    conn.close()

    return prenotazioni

def get_prenotazioniL(id):
    conn =sqlite3.connect('db/affitti.db')
    conn.row_factory = sqlite3.Row 
    cursor= conn.cursor()

    sql1='SELECT * FROM PRENOTAZIONI WHERE idUtente = ?'
    sql2='SELECT PRENOTAZIONI.* FROM PRENOTAZIONI, ANNUNCI\
          WHERE PRENOTAZIONI.idAnnuncio = ANNUNCI.idAnnuncio\
          AND ANNUNCI.idUtente = ?'
    result1 = cursor.execute(sql1, (id,)).fetchall()
    result2 = cursor.execute(sql2, (id,)).fetchall()

    cursor.close()
    conn.close()

    return result1, result2

#cambia in base a se il tipo è uguale ad accetta o rifiuta
def mod_richiesta(dati, tipo):
    conn =sqlite3.connect('db/affitti.db')
    conn.row_factory = sqlite3.Row 
    cursor= conn.cursor()
    success=False
    if tipo=='accetta':
        sql ='UPDATE PRENOTAZIONI SET stato=? WHERE idAnnuncio= ? AND Data=? AND fasciaOraria=? '
        cursor.execute(sql, ('accettata', dati['idAnnuncio'], dati['data'], dati['fasciaOraria']))
        conn.commit()
        success=True
    else:
        sql ='UPDATE PRENOTAZIONI SET stato=?, motivazioneRifiuto=? WHERE idAnnuncio= ? AND Data=? AND fasciaOraria=? '
        cursor.execute(sql, ('rifiutata', dati['motivoRifiuto'], dati['idAnnuncio'], dati['data'], dati['fasciaOraria']))
        conn.commit()
        success=True
    
    cursor.close()
    conn.close()

    return success
