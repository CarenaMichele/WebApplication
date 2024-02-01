from flask import Flask, render_template, request, redirect, url_for, flash
#from datetime import date
import posts_dao, os
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
#from flask_session import Session
from models import User
from werkzeug.security import generate_password_hash, check_password_hash

app= Flask(__name__) #qualunque sia il nome dell'app viene rimpiazzato in tempo di esecuzione
app.config['SECRET_KEY']=os.urandom(24)

login_manager=LoginManager()
login_manager.init_app(app)

@app.route('/')  #quando il server riceve una richiesta get in questo caso, allora deve eseguire il contenuto della funzione
def index():
   return render_template('index.html')

@app.route('/Page_login')
def Page_login():
   return render_template('login.html')

@app.route('/sign_up')
def sign_up():
   return render_template('signup.html')

@app.route('/profiloL')
def profiloL():
   annunci=posts_dao.get_annunci(current_user.id) #a volte non funziona
   app.logger.info(annunci)
   return render_template('profiloL.html', annunci=annunci)

@app.route('/profiloC')
def profiloC():
   return render_template('profiloC.html')

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


@app.route('/newAnn', methods=['POST'])
@login_required
def new_ann():
   try:
      annuncio=request.form.to_dict()
      app.logger.info(annuncio)
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
      if 'arredato' in annuncio:
         app.logger.info('è arredato? '+ annuncio['arredato'])
      if 'disponibile' in annuncio:
         app.logger.info('è disponibile? '+ annuncio['disponibile'])

      annuncio['idLocatore']=current_user.id #uso di current_user per passare idLocatore nel db
      #app.logger.info(annuncio['idLocatore'])

      foto=request.files.getlist('imgAnnuncio') #getlist serve per ottenere una lista di file 
      #app.logger.info(foto)
      file_paths=[] #vettore per inserire tutte le foto di quell'annuncio e passarle al db
      for file in foto:
          file.save('static/img/'+file.filename)
          fileP='img/'+file.filename
          file_paths.append(fileP)
      
      #app.logger.info(file_paths)
          
       # dalla funzione add_ann faccio ritornare l'id dell'annuncio
       #appena inserito per usarlo nella tabella foto come chiave esterna
      sol= posts_dao.add_ann(annuncio)

      app.logger.info(sol['idAnnuncio'])
      success=posts_dao.add_foto(file_paths, sol['idAnnuncio'])

      if success:
         flash('Annuncio creato correttamente!', 'success')
      else:
         raise Exception
               
   except Exception:
      flash("Errore nella creazione dell'annuncio: riprova!", 'danger')

   return redirect(url_for('profiloL'))





@login_manager.user_loader
def load_user(user_id):
    db_user=posts_dao.get_user_by_id(user_id)
    user = User(id=db_user['idUtente'],	
                username=db_user['username'],		
                password=db_user['password'],
                tipo=db_user['tipo'])
    return user