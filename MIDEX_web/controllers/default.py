# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

# ---- example index page ----



def index():
    #grid = SQLFORM.grid(db.producto)
    redirect(URL('default', 'imagen'))
    #return dict(grid=grid)

def despacho():
    el_turno = db(db.turnos.cerrado==False).select(db.turnos.nroturno)[0]
    headers={'despachos.nrodesp':'Des','despachos.horainicio':'Inicio', 'despachos.horafin':'Fin', 'despachos.pico':'N° Pico','despachos.volvta':'Volumen','despachos.facvta':'Pesos'}
    fields =  (db.despachos.nrodesp,db.despachos.horainicio,db.despachos.horafin,db.despachos.pico,db.despachos.volvta,db.despachos.facvta)
    #consul = db.despachos.turno==el_turno
    consul = db.despachos.turno==el_turno
    orden=~db.despachos.nrodesp
    grid = SQLFORM.grid(consul,csv = False,
                        fields = fields,
                        headers = headers,
                        paginate =25,
                        sortable=True,
                        deletable=False,
                        editable=False,
                        details=False,
                        orderby=orden,)
    return dict(grid=grid)


def imagen():
    #CONSULTA DE DESPACHOS
    try:
        #el_turno = db(db.turnos.cerrado==False).select(db.turnos.nroturno,db.turnos.inicio)[0]
        el_turno = db(db.turnos.cerrado==False).select(db.turnos.nroturno,db.turnos.inicio,db.turnos.activo)[0]
        turno_activo = (float(el_turno.activo))
        #el_inicio = el_turno[1]
        #el_turno = el_turno[0]
        turno=" Turno en Curso : " + str(el_turno.nroturno)+"    Fecha de Inicio : "+el_turno.inicio.strftime("%d/%m/%Y   %H:%M")
        #+str(el_turno.activo)
        #+ " fecha de Inicio : "+str(el_inicio)
    except:
        el_turno = (db(db.turnos).select(db.turnos.nroturno,turnos.inicio,db.turnos.activo)).last()
        el_turno =el_turno.nroturno++"    Fecha de Inicio : "+el_turno.inicio.strftime("%d/%m/%Y   %H:%M")
        turno=" Turno en Curso (!! Atencion Turno Cerrado !!):  " + str(el_turno)

    headers={'despachos.nrodesp':'Des','despachos.horainicio':'Inicio', 'despachos.horafin':'Fin', 'despachos.pico':'N° Pico','despachos.volvta':'Volumen','despachos.facvta':'Pesos'}
    fields =  (db.despachos.nrodesp,db.despachos.horainicio,db.despachos.horafin,db.despachos.pico,db.despachos.volvta,db.despachos.facvta)
    #consul = db.despachos.turno==el_turno
    consul = db.despachos.turno==el_turno
    id = db.despachos.nrodesp
    orden=~db.despachos.nrodesp
    
    grid = SQLFORM.grid(consul,csv = False,
                        fields = fields,
                        field_id = id,
                        searchable=False,
                        sortable=True,
                        headers = headers,
                        paginate =15,
                        deletable=False,
                        create=False,
                        editable=False,
                        details=False,
                        orderby=orden,)
    #FIMAL CONSULTA DE DESPACHOS (grid)

    #ADMINISTRACION DE IMAGENES(imag)
    #imag1 =  db.executesql('select * from picos order by nropico')

    imag1 =  db.executesql('select distinct(surtidor), nesta from picos order by surtidor')
    imag2 =  db.executesql('select distinct(surtidor), nesta from picos where nesta<>2 order by surtidor')

    imag={}
    cant = (len(imag1)+1)
    for can in range(32):
        imag[can+1]=0


    for im in imag1:
        imag[im[0]]=im[1]

    for im in imag2:
        imag[im[0]]=im[1]


    #FINALIZAR ADMINISTRACION DE IMAGENES

    #CONSULTA DE PICOS
    headers1={'prodview.nropico':'N.Picos','prodview.surtidor':'Surt.', 'prodview.manguera':'Mang.','prodview.descripcion':'Descripcion','prodview.preciocont':'Precio Uni', 'prodview.estado':'Estado'}
    fields1 = (db.prodview.nropico,db.prodview.surtidor,db.prodview.manguera,db.prodview.descripcion,db.prodview.preciocont,db.prodview.estado)
    #consul1 = db((db.picos.tanque==db.tanques.nrotanque)).select(db.picos.nropico)
    #consul1 = db((db.picos.tanque==db.tanques.nrotanque)).select(db.picos.nropico,db.picos.surtidor,db.picos.manguera,db.producto.descripcion,db.picos.estado)
    #consul1 =db.executesql('SELECT picos.nropico,picos.surtidor,picos.manguera,producto.descripcion,producto.preciocont,picos.estado FROM picos,tanques,producto WHERE picos.tanque=tanques.nrotanque and tanques.combustible=producto.nroprod;')
    consul1 = db.prodview.nropico
    orden1=db.prodview.nropico
    id1=db.prodview.nropico

    pico = SQLFORM.grid(consul1,
                        csv = False,
                        searchable=False,
                        fields = fields1,
                        field_id = id1,
                        sortable=False,
                        headers = headers1,
                        paginate =16,
                        deletable=False,
                        create=False,
                        editable=False,
                        details=False,
                        orderby=orden1,)
    #FIMAL CONSULTA DE DESPACHOS (pico)


    return dict(grid=grid,imag=imag,pico=pico,turno=T(turno),imag1=imag1,turno_activo=turno_activo)

def cierre():
    form = FORM(
        P(TAG.BUTTON("Cerrar Turno", _type="btn", _name="yes", _value="yes")),
        #A(TAG.BUTTON("", _type="", _name="", _value="")),
        P(TAG.BUTTON("  Retornar                                            ", _type="btn", _name="no", _value="no")),)

    if form.accepts(request, session):
        response.flash = "Formulario Aceptado "
        if request.vars.yes:
            session.flash = "Cerrando Turno "
            db(db.turnos).update(cerrado = True)


        if request.vars.no:
               response.flash = "Retornar a Pagina de Inicio"
               redirect(URL('default', 'imagen'))

    return dict(dict(form=form))





def despacho1():
    #nro=request.args[0]

    consulta=(db.despachos.turno==5)&(db.despachos.pico==db.picos.nropico)&(db.picos.tanque==db.tanques.nrotanque)&(db.tanques.combustible==db.producto.nroprod)

    q_despacho = db(consulta).select(db.producto.descripcion,db.despachos.ALL,orderby=~db.despachos.nrodesp)
    #q_despacho = db(consulta).select(db.despachos.ALL,orderby=~db.despachos.nrodesp)
    #datos = db().select(db.producto.ALL)
    #redirect(URL('reportes', 'excelExport',vars= (datos)))
    for elem in q_despacho:
        print(elem.producto.descripcion)
        v1=elem.producto.descripcion
    return(dict(grid=q_despacho,msg=v1))


#@auth.requires_login()
#@auth.requires(True, requires_login=False)
def precio():
    #CONSULTA DE PRECIOS
    headers1={'precio.combustible':'Combustible','producto.descripcion':'Descripcion', 'precio.newprice':'Precio','precio.on_line':'en linea'}
    fields1 = (db.precio.combustible,db.producto.descripcion,db.precio.newprice,db.precio.on_line)
    consul1 = (db.precio.combustible==db.producto.nroprod)
    message='Formulario para Cambio de Precio'
    #=db.producto.nroprod
    orden1=db.precio.combustible
    id1=db.precio.combustible
    #return dict(precio=fields1)

     #****OCULTO ALGUNOS CAMPOSos
    if 'edit' in request.args:
         db.precio.nrocambio.writable = False
         db.precio.nrocambio.readable = False
         db.precio.hora.writable = False
         db.precio.hora.readable = False
         db.precio.cemprod.writable = False
         db.precio.cemprod.readable = False
         db.precio.combustible.writable = False
         db.precio.combustible.readable = True
         db.producto.descripcion.writable = False
         db.producto.descripcion.readable = True
         db.precio.newprice.writable = True
         db.precio.newprice.readable = True



    #*****
    precio = SQLFORM.grid(consul1,
                        csv = False,
                        searchable=False,
                        fields = fields1,
                        field_id = id1,
                        editable=True,
                        sortable=True,
                        create=False,
                        headers = headers1,
                        paginate =16,
                        deletable=False,
                        details=False,
                        orderby=orden1,
                        user_signature=False,
                        formargs={},
                        #links=[lambda row: A('Editar',_class="btn", _href=URL('camprecio', args = row.combustible))],
    )

    return dict(precio=precio,message=message)


#def camprecio():
#    nro=request.args
#    print('*****')
#    print(nro)
#    print('*****')
#    #nro=request.args[0].combustible
#    print('*****')
#    print(nro)
#    print('*****')
#    return(dict(numero=nro))
#

# ---- API (example) -----
#@auth.requires_login()
#def api_get_user_email():
#    if not request.env.request_method == 'GET': raise HTTP(403)
#    return response.json({'status':'success', 'email':auth.user.email})

# ---- Smart Grid (example) -----
@auth.requires_membership('admin') # can only be accessed by members of admin groupd
def grid():
    response.view = 'generic.html' # use a generic view
    tablename = request.args(0)
    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=False, editable=True)
    return dict(grid=grid)

# ---- Embedded wiki (example) ----
def wiki():
    auth.wikimenu() # add the wiki to the menu
    return auth.wiki()

# ---- Action for login/register/etc (required for auth) -----
def user():
#    """
#    exposes:
#    http://..../[app]/default/user/login
#    http://..../[app]/default/user/logout
#    http://..../[app]/default/user/register
#    http://..../[app]/default/user/profile
#    http://..../[app]/default/user/retrieve_password
#    http://..../[app]/default/user/change_password
#    http://..../[app]/default/user/bulk_register
#    use @auth.requires_login()
#        @auth.requires_membership('group name')
#        @auth.requires_permission('read','table name',record_id)
#    to decorate functions that need access control
#    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
#    """
    return dict(form=auth())

# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)
