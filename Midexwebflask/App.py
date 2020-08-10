# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, url_for, flash
#from flask_mysqldb import MySQL
#from PythonGrid import pythonGrid
from flask_weasyprint import HTML, render_pdf
#from flask_gridify import FlaskGridify
import modelo.dbdato as db
from flaskwebgui import FlaskUI #get the FlaskUI class
#from multiprocessing import Process, freeze_support


#Inicializa Dbf
db = db.db()

# initializations
app = Flask(__name__)
# settings
app.secret_key = "mysecretkey"



# routes
@app.route('/')
def Index():
    ## Revisando el TunoS
    turno=turnos()
    
    #Prepara los datos para Visualizar los Surtidores y su estado
    imag1 =  db.executesql('select distinct(surtidor), nesta from picos order by surtidor')
    imag={}
    for im in imag1:
        imag[im[0]]=im[1]
    
    #Detalle de Los Picos
    pico = db().select(db.picos.ALL,orderby=db.picos.nropico)  
             
    return render_template('imagen.html', imag = imag,pico=pico , turno = turno[1],turno_activo=int(turno[2]))


@app.route('/despachos')
def despachos():
    turno=turnos()
    consulta=(db.despachos.turno==turno[0])&(db.despachos.pico==db.picos.nropico)&(db.picos.tanque==db.tanques.nrotanque)&(db.tanques.combustible==db.producto.nroprod)
    q_despacho = db(consulta).select(db.producto.descripcion,db.picos.nropico,db.picos.surtidor,db.picos.manguera,db.despachos.ALL,orderby=~db.despachos.nrodesp)
    return render_template ('despachos.html', turno = turno[1],turno_activo=int(turno[2]),despa=q_despacho) 


@app.route('/detalledespacho/<nrodes>')
## Muestra el detalle del despacho
def detalledespacho(nrodes):
    turno=turnos()
    consulta=(db.despachos.turno==turno[0])&(db.despachos.pico==db.picos.nropico)&(db.picos.tanque==db.tanques.nrotanque)&(db.tanques.combustible==db.producto.nroprod)&(db.despachos.nrodesp==nrodes)
    q_despa = db(consulta).select(db.producto.descripcion,db.picos.nropico,db.picos.surtidor,db.picos.manguera,db.despachos.ALL,orderby=~db.despachos.nrodesp)
    return render_template('detalledespacho.html',ddespa=q_despa,turno = turno[1],turno_activo=int(turno[2]))

### Determina el Numero de Turno (FUNCION LOCAL)
def turnos():
    try:
        el_turno = db(db.turnos.cerrado==False).select(db.turnos.nroturno,db.turnos.inicio,db.turnos.activo)[0]
        turno_activo = (float(el_turno.activo))
        turno=" Turno en Curso : " + str(el_turno.nroturno)+"    Fecha de Inicio : "+el_turno.inicio.strftime("%d/%m/%Y   %H:%M")
    except:
        el_turno = (db(db.turnos).select(db.turnos.nroturno,db.turnos.inicio,db.turnos.activo)).last()
        el_turno =str(el_turno.nroturno)+"    Fecha de Inicio :   "+el_turno.inicio.strftime("%d/%m/%Y   %H:%M")
        turno=" Turno en Curso (!! Atencion Turno Cerrado !!) :  " + str(el_turno)
    
    return(el_turno.nroturno,turno,turno_activo)


@app.route('/webturnos')
## Muestra el detalle del despacho
def webturnos():
    turno=turnos()
    consulta=db().select(db.turnos.nroturno,db.turnos.inicio,db.turnos.fin,db.turnos.cerrado, orderby=db.turnos.nroturno)
    print(consulta)
    #render_pdf(url_for('turnos.html', tturno=consulta,turno = turno[1],turno_activo=int(turno[2])))
    return render_template('turnos.html',tturno=consulta,turno = turno[1],turno_activo=int(turno[2]))


@app.route('/webturnos.pdf')
## Muestra el detalle del despacho
def webturnos_pdf():
    turno=turnos()
    consulta=db().select(db.turnos.nroturno,db.turnos.inicio,db.turnos.fin,db.turnos.cerrado, orderby=db.turnos.nroturno)
    return render_pdf(url_for('webturnos', tturno=consulta,turno = turno[1],turno_activo=int(turno[2])))
    



@app.route('/prueba')
def prueba():
    return render_template ('prueba.html') 



#def run_browser():
#    import webbrowser
#    chrome = webbrowser.get(r'C:\\Program\ Files\ (x86)\\Google\\Chrome\\Application\\chrome.exe --window-size=500,500 --app=%s')
#    chrome.open('http://localhost:3070')



#def run_app():
#    #from app import webapp
#    app.run(port=3070, debug=True) #debug=True) #, use_reloader=False)
#    import webbrowser
#    chrome = webbrowser.get(r'C:\\Program\ Files\ (x86)\\Google\\Chrome\\Application\\chrome.exe --window-size=500,500 --app=%s')
#    chrome.open('http://localhost:3070')
    #app.config['SEND_FILE_MAX_AGE_DEFAULT']=0
    #ui = FlaskUI(app,port=3080)
    #ui.run()


#if __name__ == '__main__':
#    freeze_support()

#    a = Process(target=run_app)
#    a.daemon = True
#    a.start()

#    b = Process(target=run_browser)
#    b.start()
#    b.join()







# starting the app
if __name__ == "__main__":
    app.config['SEND_FILE_MAX_AGE_DEFAULT']=0
    #ui = FlaskUI(app,width=500,port=4000)
    #ui.run()
   
    app.run(port=3020, debug=True)


