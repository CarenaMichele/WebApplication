from flask import Flask, render_template, request, redirect, url_for, flash
import posts_dao, os
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
#from flask_session import Session
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta

app= Flask(__name__) #qualunque sia il nome dell'app viene rimpiazzato in tempo di esecuzione
app.config['SECRET_KEY']=os.urandom(24)

login_manager=LoginManager()
login_manager.init_app(app)

#app.config['PERMANENT_SESSION_LIFETIME']=timedelta(days=365)
@app.route('/<info>')
@app.route('/')  #quando il server riceve una richiesta get in questo caso, allora deve eseguire il contenuto della funzione
def index(info=None):
   if info is not None:
      if info=='numLocali':
         annunci=posts_dao.ordina(info)
      else:
         annunci=posts_dao.ordina(info)
      return render_template('index.html', allAnnunci=annunci)
   else:
      allAnnunci=posts_dao.get_allAnnunci()
      return render_template('index.html', allAnnunci=allAnnunci)

@app.route('/Page_login')
def Page_login():
   return render_template('login.html')

@app.route('/sign_up')
def sign_up():
   return render_template('signup.html')

   
@app.route('/profilo')
@app.route('/profilo/<int:id>')
@login_required
def profilo(id=None): #annuncio=None significa che il parametro è opzionale. 
   #Se il parametro non viene fornito nell'URL, annuncio sarà impostata a None di default
   if id is not None:
      annunci=posts_dao.get_annunci(current_user.id)
      annuncio=posts_dao.get_singleAnnuncio(id)
      return render_template('profilo.html', annunci=annunci, annuncio=annuncio)
   else:
      prenotazioni=posts_dao.get_prenotazioni(current_user.id, current_user.tipo)
      annunci=posts_dao.get_annunci(current_user.id)
      return render_template('profilo.html', annunci=annunci, prenotazioni=prenotazioni)


@app.route('/signup', methods=['POST'])
def signup():
  try:
      new_user_from_form = request.form.to_dict()

      if new_user_from_form ['nome'] == '':
         raise Exception

      if new_user_from_form ['cognome'] == '':
          raise Exception
      
      if new_user_from_form ['username'] == '':
          raise Exception
      
      if new_user_from_form ['password'] == '':
          raise Exception
      
      if 'tipo' in new_user_from_form:
         app.logger.info('il tipo scelto '+ new_user_from_form['tipo'])
      

    
      new_user_from_form ['password'] = generate_password_hash(new_user_from_form ['password'])
      app.logger.info(new_user_from_form['password'])

      success = posts_dao.crea_utente(new_user_from_form)

      if success:
         return redirect(url_for('Page_login'))
      else:
          raise Exception
     
  except Exception:
   flash('Errore nella registrazione: riprova!', 'danger')
  

  return redirect(url_for('sign_up'))


@app.route('/login', methods=['POST'])
def login():
   try:
      utente_form = request.form.to_dict()
      #app.logger.info(utente_form)

      if utente_form['username']=='' or utente_form['password']=='':
         raise Exception
      utente_db = posts_dao.get_user_by_username(utente_form['username'])
      #app.logger.info(utente_db.utente_id,utente_db.username)
      if utente_db and check_password_hash(utente_db['password'], utente_form['password']):
         new = User(id=utente_db['idUtente'],
                    username=utente_db['username'], 
                    password=utente_db['password'],
                    tipo=utente_db['tipo'])
         login_user(new, True) #funzione che usa loginManager per autenticare l'utente
         flash('Benvenuto '+utente_db['username']+'!', 'success')
         return redirect(url_for('index'))
      else:
         print("errore")
         raise Exception
         
   except Exception:
      flash('Errore nel login: riprova!', 'danger')
      return redirect(url_for('Page_login'))
   
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/Ann/<par>', methods=['POST'])
@login_required
def Ann(par):
   try:
     
      annuncio=request.form.to_dict()
      #app.logger.info(annuncio['indirizzo'])
      #app.logger.info(annuncio)
      if annuncio['titolo']=='':
         raise Exception
      if annuncio['indirizzo']=='':
         raise Exception
      if annuncio['tipoC']=='':
         raise Exception
      if annuncio['numLocali']=='':
         raise Exception
      if annuncio['descrizione']=='':
         raise Exception
      if annuncio["prezzoM"]=='':
         raise Exception
      #if 'arredato' in annuncio:
         #app.logger.info('è arredato? '+ annuncio['arredato'])
      #if 'disponibile' in annuncio:
         #app.logger.info('è disponibile? '+ annuncio['disponibile'])

      annuncio['idLocatore']=current_user.id #uso di current_user per passare idLocatore nel db
      foto=request.files.getlist('imgAnnuncio') #getlist serve per ottenere una lista di file 
      #massimo 5 foto posso aggiungere
      
      if par == 'new':
         #forse è meglio usarlo sia per la creazione che per la modifica
         if len(foto)>5:
         #flash("Impossibile inserire più di 5 foto: riprova!", 'danger')
             raise Exception
         else:
            file_paths=[] #vettore per inserire tutte le foto di quell'annuncio e passarle al db
            for file in foto:
               file.save('static/img/'+file.filename)
               fileP='img/'+file.filename
               file_paths.append(fileP)
         #app.logger.info(par)
         sol= posts_dao.add_ann(annuncio)
         # dalla funzione add_ann faccio ritornare l'id dell'annuncio
         #appena inserito per usarlo nella tabella foto come chiave esterna
         success=posts_dao.add_foto(file_paths, sol['idAnnuncio'])
      else:
         app.logger.info(par)
         id=posts_dao.get_id(annuncio)
         #app.logger.info(id[0])
         success=posts_dao.mod_ann(annuncio,id)

         #DA GESTIRE MODIFICA DELLE FOTO
         #success=posts_dao.mod_foto(file_paths,id[0])

      if success and par=='new':
         flash('Annuncio creato correttamente!', 'success')
      elif success and par=='mod':
         flash('Annuncio modificato correttamente!', 'success')
      else:
        raise Exception
               
   except Exception:
      flash("Errore nella creazione dell'annuncio: riprova!", 'danger')

   return redirect(url_for('profilo'))


@app.route('/modificaAnn/<int:id>', methods=['POST']) #passo come parametro id per capire qual è la riga del db da modificare
@login_required
def mod_ann(id):
   #something
   #annuncio=posts_dao.get_singleAnnuncio(id)
   #app.logger.info(annuncio)
   return redirect(url_for('profilo', id=id))


@app.route('/rimuoviFoto/<int:id>', methods=['POST'])
@login_required
def rimuovi_foto(id):
   foto=request.form['image_url']
   app.logger.info(foto)
   success=posts_dao.remove_foto(foto,id)

   if success:
      flash('Foto rimossa correttamente!', 'success')
   else:
      flash('Errore nella rimozione della foto','danger')
   return redirect(url_for('profilo', id=id))

@app.route('/filtro', methods=['POST'])
def filtro():
    info=request.form.get('selFiltro')
    #app.logger.info(info)
    return redirect(url_for('index', info=info))

#route per inizializzare campi input del form della prenotazione, parametro è idAnnuncio
@app.route('/prenotazione/<int:id>', methods=['GET','POST'])
@login_required
def prenotazione(id):
   idUtente=current_user.id
   sol=posts_dao.get_prenotazioni(id, idUtente)
   app.logger.info(sol)
   if sol == []:
      oggi=datetime.now().date()
      domani=oggi+timedelta(days=1)
      setteGiorniDopo=oggi+timedelta(days=7)

      #formatto le date nel formato richiesto dall'input date
      #formato generale = YYYY-MM-DD
      #isoformat = fornisce rappresentazione di una data in formato stringa
      domaniForm = domani.isoformat() 
      setteGiorniDopoForm = setteGiorniDopo.isoformat()
      return render_template('prenotazione.html', id=id, domani=domaniForm, setteGiorniDopo=setteGiorniDopoForm)
   else:
      flash("Hai già fatto una richiesta di visita per questa casa! Attendi la conferma del locatore", 'danger')
      return redirect(url_for('index'))

#route per andare a prendere le fasce orarie a partire dalla data
@app.route('/gestioneOra/<int:id>', methods=['POST'])
def gestioneOra(id):
   oggi=datetime.now().date()
   domani=oggi+timedelta(days=1)
   setteGiorniDopo=oggi+timedelta(days=7)
   domaniForm = domani.isoformat() 
   setteGiorniDopoForm = setteGiorniDopo.isoformat()

   richiestaPren=request.form.to_dict()
   #data=request.form.get('data')
   #modVisita=request.form.get('modVisita')
   
   if richiestaPren['data']:
   #come risultato tutte le ore di quel giorno già prese per quell'annuncio
      fasceOrNonDisp=posts_dao.gestioneOra(id, richiestaPren['data'])
      return render_template('prenotazione.html', id=id, domani=domaniForm, setteGiorniDopo=setteGiorniDopoForm, orari=fasceOrNonDisp, richiesta= richiestaPren)
   else:
      flash('Inserisci la Data!','danger')
      return render_template('prenotazione.html', id=id, domani=domaniForm, setteGiorniDopo=setteGiorniDopoForm)
   
#route per aggiungere prenotazione (parametro è idAnnuncio)
@app.route('/aggPrenotazione/<int:id>', methods=['POST'])
@login_required
def aggPrenotazione(id):
   info=request.form.to_dict()

   if info['data']=='':
         success=False
   if info['fasciaOraria']=='':
         success=False

   info['idUtente'] = current_user.id
   info['stato'] ='richiesta'
   info['motivazioneRifiuto']=None
   success=posts_dao.add_prenotazione(id, info)

   if success:
      flash('Prenotazione richiesta correttamente!', 'success')
     
   else:
      flash('Errore nella richiesta della prenotazione!','danger')
      #return render_template('prenotazione.html', id=id, domani=domaniForm, setteGiorniDopo=setteGiorniDopoForm)
   return redirect(url_for('index'))

@app.route('/gestioneStatoRichiesta', methods=['POST'])
def gestioneStatoRichiesta():
   if 'btnRichiesta' in request.form:
      if request.form['btnRichiesta'] =='accetta':
         dati=request.form.to_dict()
         app.logger.info(dati['idAnnuncio'])
         success=posts_dao.mod_richiesta(dati)
         app.logger.info(success)
      else:
         app.logger.info("rifiuta")

      if success:
         flash("Visita accettata correttamente!", "success")

      return redirect(url_for('profilo'))

@login_manager.user_loader
def load_user(user_id):
    db_user=posts_dao.get_user_by_id(user_id)
    user = User(id=db_user['idUtente'],	
                username=db_user['username'],		
                password=db_user['password'],
                tipo=db_user['tipo'])
    return user