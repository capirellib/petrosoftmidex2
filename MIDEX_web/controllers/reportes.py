# -*- coding: utf-8 -*-
# intente algo como


from reportlab.platypus import Paragraph
from reportlab.platypus import Image
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Spacer
from reportlab.platypus import Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import A4,inch,landscape
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY,TA_LEFT,TA_CENTER
from reportlab.graphics.shapes import Drawing, Rect
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime
import time
import cStringIO
import csv
import variables

def consulta():
    form = FORM(
        H2('Seleccione el Tipo de Impresion'),
        
        A(TAG.BUTTON("....PDF....", _type="submit", _name="yes", _value="yes")),
        #A(TAG.BUTTON("", _type="", _name="", _value="")),
        A(TAG.BUTTON("..EXCEL... ", _type="submit", _name="no", _value="no")),)

    if form.accepts(request, session):
        response.flash = "Formulario Aceptado "
        if request.vars.yes:
            session.flash = "Impresion Pdf "
            variables.imprime='pdf'
            #redirect(URL('reportes', 'turnos',args=('pdf')))


        if request.vars.no:
               response.flash = "Impresion exe"
               variables.imprime='exe'
               
        redirect(URL('reportes', 'turnos'))
    return dict(dict(form=form))




def turnos():
    #s_turno =db().select(db.turnos.ALL,orderby =~ db.turnos.nroturno)
    headers={'turnos.nroturno':'Turno','turnos.inicio':'Inicio', 'turnos.fin':'Fin' }
    fields =  (db.turnos.nroturno,db.turnos.inicio,db.turnos.fin)
    #consul = db.despachos.turno==el_turno
    consul = db.turnos.nroturno
    id = db.turnos.nroturno
    orden=~db.turnos.nroturno
    grid = SQLFORM.grid(consul,
                        csv = False,
                        fields = fields,
                        field_id = id,
                        searchable=False,
                        sortable=False,
                        headers = headers,
                        paginate =15,
                        deletable=False,
                        create=False,
                        editable=False,
                        details=False,
                        orderby=orden,
                        links=[lambda row: A('Despacho',_class="btn", _href=URL('despacho', args=row.nroturno)),
                               lambda row: A('Aforadores x Despacho',_class="btn", _href=URL('afodespacho', args=row.nroturno)),
                               lambda row: A('Producros x Despacho',_class="btn", _href=URL('proddespacho', args=row.nroturno)),
                               lambda row: A('Aforadores',_class="btn", _href=URL('aforador', args=row.nroturno))
                               ],
                        )
    if variables.imprime=='pdf':
        message=' Imprimiendo a Pdf s '
    else:
        message=' Genera Archivo de exportacion a Planilla de Calculos'
    return(dict(grid=grid,message=message))





def despacho():
    nro=request.args[0]

    #consulta=(db.despachos.turno==nro & db.despachos.pico==db.picos.nropico & db.picos.tanque==db.tanques.nrotanque & db.tanques.combustible==db.producto.nroprod)
    consulta=(db.despachos.turno==nro)&(db.despachos.pico==db.picos.nropico)&(db.picos.tanque==db.tanques.nrotanque)&(db.tanques.combustible==db.producto.nroprod)
    q_despacho = db(consulta).select(db.despachos.ALL,db.producto.descripcion,orderby=~db.despachos.nrodesp)
    #q_despacho = db(consulta).select(db.despachos.ALL,orderby=~db.despachos.nrodesp)
    #datos = db().select(db.producto.ALL)
    #redirect(URL('reportes', 'excelExport',vars= (datos)))

    if variables.imprime=='pdf':
        
        t_final=[]
        v1="Nro Dsep."
        v2="Pico-Producto"
        v3="Inicio"
        v4="Fin"
        v5="Vol. Inicial"
        v6="Vol. Final"
        v7="Vol. Vendido"
        v8="Fac. Inicial"
        v9="Fac. Final"
        v10="Fac. Vendido"
    
        lis=v1,v2,v3,v4,v5,v6,v7,v8,v9,v10
        tabla=list(lis)
        t_final.append(tabla)
        total_de_litros=0
        total_de_pesos=0
        for elem in q_despacho:
            v1=str(elem.despachos.nrodesp)
            v2=str(elem.despachos.pico)+'-'+elem.producto.descripcion
            #v2=str(elem.pico)
            v3=(elem.despachos.horainicio).strftime("%d/%m/%Y   %H:%M")
            v4=(elem.despachos.horafin).strftime("%d/%m/%Y   %H:%M")
            v5=str(elem.despachos.volinicial)
            v6=str(elem.despachos.volfinal)
            v7=str(elem.despachos.volvta)
            v8=str(elem.despachos.factinicial)
            v9=str(elem.despachos.factfinal)
            v10=str(elem.despachos.facvta)
            #"{0:.2f}".format(elem.picos.totalvoldif)
            v7=("{0:.2f}".format(elem.despachos.volvta))
            v10=("{0:.2f}".format(elem.despachos.facvta))
    
            total_de_litros=total_de_litros+elem.despachos.volvta
            total_de_pesos=total_de_pesos+elem.despachos.facvta
            lis=v1,v2,v3,v4,v5,v6,v7,v8,v9,v10
            tabla=list(lis)
            t_final.append(tabla)
    
    
        ''' Cargar Totales'''
        v1=str()
        v2=str()
        v3=str()
        v4=str("Totales")
        v5=str()
        v6=str()
        v7=("{0:.2f}".format(total_de_litros))
        v8=str()
        v9=str()
        v10=("{0:.2f}".format(total_de_pesos))
        lis=v1,v2,v3,v4,v5,v6,v7,v8,v9,v10
        tabla=list(lis)
        t_final.append(tabla)
    ##        story1.append(Paragraph(str(elem.nroturno)+'..'+str(elem1.inicio)+'..'+str(elem1.fin),styles["Normal"]))
    
    ## INICIA EL REPORTE
        p = ParagraphStyle('parrafos')
        p.alignment = TA_LEFT
        p.fontSize = 10
        p.fontName="Times-Roman"
        fe=datetime.now()
        fe.isoformat()
        #fe.strftime("%c")
        fecha_hora = "Fecha y hora  "+fe.strftime("%d/%m/%Y   %H:%M")
        #time.strftime("%c")
        title = "Listado de Depachos  - Turno : "+str(nro)
        subtitle =""
        styles = getSampleStyleSheet()
        story1 = []
        story1.append(Paragraph((fecha_hora),p))
        story1.append(Spacer(0,10))
        story1.append(Paragraph((title),styles["Title"]))
        story1.append(Paragraph((subtitle),styles["Heading4"]))
        story1.append(Spacer(0,10))
        tabla=Table(t_final)
        tabla.setStyle([('TEXTCOLOR',(0,0),(6,0),colors.red),('TEXTCOLOR',(0,1),(3,-1),colors.blue)])
        tabla.setStyle([('BACKGROUND',(4,1),(-1,-1),colors.gray)])
        tabla.setStyle([('BOX',(0,0),(-1,-1),0.25,colors.black)])
        tabla.setStyle([('INNERGRID',(0,0),(-1,-1),0.25,colors.black)])
        tabla.setStyle([('ALIGN',(4,1),(-1,-1),'RIGHT')])
        tabla.setStyle([('FONTSIZE',(0,0),(-1,-1),7)])
        story1.append(tabla)
        story1.append(Spacer(0,10))
    
        #story1.append(Spacer(0,20))
        #story1.append(Spacer(0,20))
        #total_tabla= "Total Venta de Litros "+ "{0:.2f}".format(total_de_litros)
        #story1.append(Paragraph((total_tabla),styles["Heading4"]))
        buffer1 = cStringIO.StringIO()
        ###
        #buffer1 = 'buffer1.pdf'
        #size=landscape(A4)
        size=A4
        doc = SimpleDocTemplate(buffer1,pagesize=size)
        doc.build(story1)
        pdf = buffer1.getvalue(doc)
        
        buffer1.close()
    #filename = request.args(0)
    #if filename:
    #    header = {'Content-Disposition': 'attachment; filename=' + filename}
    #else:
        response.headers['Content-Type']='application/pdf'
    
    else:
        #response.headers['Content-Type']='application/pdf'
        ###archivo para exel
        stream=cStringIO.StringIO()
        q_despacho.export_to_csv_file(stream)
        response.headers['Content-Type']='application/vnd.ms-excel'
        #response.headers['filename']='despacho.xls'
        #response.write(stream.getvalue(), escape=True)
        pdf = stream.getvalue(q_despacho)
        stream.close()

    #response.headers.update(header)

    return pdf


def aforador():
    nro=request.args[0]
    nro1=int(nro)-1
    s_turno =db(db.turnos.nroturno == nro).select(db.turnos.ALL)
    s_turno1 =db(db.turnos.nroturno == nro1).select(db.turnos.ALL)
    pico = db().select(db.picos.ALL,orderby=db.picos.nropico)

    for elem in pico:
        if (elem.surtidor==1 and elem.manguera==1):
            ini = s_turno1[0].pico1volfinal
            fin = s_turno[0].pico1volfinal

        elif (elem.surtidor==1 and elem.manguera==2):
            ini = s_turno1[0].pico2volfinal
            fin = s_turno[0].pico2volfinal

        elif (elem.surtidor==1 and elem.manguera==3):
            ini = s_turno1[0].pico3volfinal
            fin = s_turno[0].pico3volfinal

        elif (elem.surtidor==1 and elem.manguera==4):
            ini = s_turno1[0].pico4volfinal
            fin = s_turno[0].pico4volfinal

        elif (elem.surtidor==2 and elem.manguera==1):
            ini = s_turno1[0].pico5volfinal
            fin = s_turno[0].pico5volfinal

        elif (elem.surtidor==2 and elem.manguera==2):
            ini = s_turno1[0].pico6volfinal
            fin = s_turno[0].pico6volfinal

        elif (elem.surtidor==2 and elem.manguera==3):
            ini = s_turno1[0].pico7volfinal
            fin = s_turno[0].pico7volfinal

        elif (elem.surtidor==2 and elem.manguera==4):
            ini = s_turno1[0].pico8volfinal
            fin = s_turno[0].pico8volfinal

        elif (elem.surtidor==3 and elem.manguera==1):
            ini = s_turno1[0].pico9volfinal
            fin = s_turno[0].pico9volfinal

        elif (elem.surtidor==3 and elem.manguera==2):
            ini = s_turno1[0].pico10volfinal
            fin = s_turno[0].pico10volfinal

        elif (elem.surtidor==3 and elem.manguera==3):
            ini = s_turno1[0].pico11volfinal
            fin = s_turno[0].pico11volfinal

        elif (elem.surtidor==3 and elem.manguera==4):
            ini = s_turno1[0].pico12volfinal
            fin = s_turno[0].pico12volfinal

        elif (elem.surtidor==4 and elem.manguera==1):
            ini = s_turno1[0].pico13volfinal
            fin = s_turno[0].pico13volfinal

        elif (elem.surtidor==4 and elem.manguera==2):
            ini = s_turno1[0].pico14volfinal
            fin = s_turno[0].pico14volfinal

        elif (elem.surtidor==4 and elem.manguera==3):
            ini = s_turno1[0].pico15volfinal
            fin = s_turno[0].pico15volfinal

        elif (elem.surtidor==4 and elem.manguera==4):
            ini = s_turno1[0].pico16volfinal
            fin = s_turno[0].pico16volfinal

        elif (elem.surtidor==5 and elem.manguera==1):
            ini = s_turno1[0].pico1vol
            fin = s_turno[0].pico1vol

        elif (elem.surtidor==5 and elem.manguera==2):
            ini = s_turno1[0].pico2vol
            fin = s_turno[0].pico2vol

        elif (elem.surtidor==5 and elem.manguera==3):
            ini = s_turno1[0].pico3vol
            fin = s_turno[0].pico3vol

        elif (elem.surtidor==5 and elem.manguera==4):
            ini = s_turno1[0].pico4vol
            fin = s_turno[0].pico4vol

        elif (elem.surtidor==6 and elem.manguera==1):
            ini = s_turno1[0].pico5vol
            fin = s_turno[0].pico5vol

        elif (elem.surtidor==6 and elem.manguera==2):
            ini = s_turno1[0].pico6vol
            fin = s_turno[0].pico6vol

        elif (elem.surtidor==6 and elem.manguera==3):
            ini = s_turno1[0].pico7vol
            fin = s_turno[0].pico7vol

        elif (elem.surtidor==6 and elem.manguera==4):
            ini = s_turno1[0].pico8vol
            fin = s_turno[0].pico8vol

        elif (elem.surtidor==7 and elem.manguera==1):
            ini = s_turno1[0].pico9vol
            fin = s_turno[0].pico9vol

        elif (elem.surtidor==7 and elem.manguera==2):
            ini = s_turno1[0].pico10vol
            fin = s_turno[0].pico10vol

        elif (elem.surtidor==7 and elem.manguera==3):
            ini = s_turno1[0].pico11vol
            fin = s_turno[0].pico11vol

        elif (elem.surtidor==7 and elem.manguera==4):
            ini = s_turno1[0].pico12vol
            fin = s_turno[0].pico12vol

        elif (elem.surtidor==8 and elem.manguera==1):
            ini = s_turno1[0].pico13vol
            fin = s_turno[0].pico13vol

        elif (elem.surtidor==8 and elem.manguera==2):
            ini = s_turno1[0].pico14vol
            fin = s_turno[0].pico14vol

        elif (elem.surtidor==8 and elem.manguera==3):
            ini = s_turno1[0].pico15vol
            fin = s_turno[0].pico15vol

        elif (elem.surtidor==8 and elem.manguera==4):
            ini = s_turno1[0].pico16vol
            fin = s_turno[0].pico16vol
###########################################################

        if (elem.surtidor==9 and elem.manguera==1):
            ini = s_turno1[0].pico1v
            fin = s_turno[0].pico1v
        elif (elem.surtidor==9 and elem.manguera==2):
            ini = s_turno1[0].pico2v
            fin = s_turno[0].pico2v
        elif (elem.surtidor==9 and elem.manguera==3):
            ini = s_turno1[0].pico3v
            fin = s_turno[0].pico3v
        elif (elem.surtidor==9 and elem.manguera==4):
            ini = s_turno1[0].pico4v
            fin = s_turno[0].pico4v


        elif (elem.surtidor==10 and elem.manguera==1):
            ini = s_turno1[0].pico5v
            fin = s_turno[0].pico5v
        elif (elem.surtidor==10 and elem.manguera==2):
            ini = s_turno1[0].pico6v
            fin = s_turno[0].pico6v
        elif (elem.surtidor==10 and elem.manguera==3):
            ini = s_turno1[0].pico7v
            fin = s_turno[0].pico7v
        elif (elem.surtidor==10 and elem.manguera==4):
            ini = s_turno1[0].pico8v
            fin = s_turno[0].pico8v



        elif (elem.surtidor==11 and elem.manguera==1):
            ini = s_turno1[0].pico9v
            fin = s_turno[0].pico9v
        elif (elem.surtidor==11 and elem.manguera==2):
            ini = s_turno1[0].pico10v
            fin = s_turno[0].pico10v
        elif (elem.surtidor==11 and elem.manguera==3):
            ini = s_turno1[0].pico11v
            fin = s_turno[0].pico11v
        elif (elem.surtidor==11 and elem.manguera==4):
            ini = s_turno1[0].pico12v
            fin = s_turno[0].pico12v

        elif (elem.surtidor==12 and elem.manguera==1):
            ini = s_turno1[0].pico13v
            fin = s_turno[0].pico13v
        elif (elem.surtidor==12 and elem.manguera==2):
            ini = s_turno1[0].pico14v
            fin = s_turno[0].pico14v
        elif (elem.surtidor==12 and elem.manguera==3):
            ini = s_turno1[0].pico15v
            fin = s_turno[0].pico15v
        elif (elem.surtidor==12 and elem.manguera==4):
            ini = s_turno1[0].pico16v
            fin = s_turno[0].pico16v

        elif (elem.surtidor==13 and elem.manguera==1):
            ini = s_turno1[0].pico17v
            fin = s_turno[0].pico17v
        elif (elem.surtidor==13 and elem.manguera==2):
            ini = s_turno1[0].pico18v
            fin = s_turno[0].pico18v
        elif (elem.surtidor==13 and elem.manguera==3):
            ini = s_turno1[0].pico19v
            fin = s_turno[0].pico19v
        elif (elem.surtidor==13 and elem.manguera==4):
            ini = s_turno1[0].pico20v
            fin = s_turno[0].pico20v


        elif (elem.surtidor==14 and elem.manguera==1):
            ini = s_turno1[0].pico21v
            fin = s_turno[0].pico21v
        elif (elem.surtidor==14 and elem.manguera==2):
            ini = s_turno1[0].pico22v
            fin = s_turno[0].pico22v
        elif (elem.surtidor==14 and elem.manguera==3):
            ini = s_turno1[0].pico23v
            fin = s_turno[0].pico23v
        elif (elem.surtidor==14 and elem.manguera==4):
            ini = s_turno1[0].pico24v
            fin = s_turno[0].pico24v

        elif (elem.surtidor==15 and elem.manguera==1):
            ini = s_turno1[0].pico25v
            fin = s_turno[0].pico25v
            
        elif (elem.surtidor==15 and elem.manguera==2):
            ini = s_turno1[0].pico26v
            fin = s_turno[0].pico26v

        elif (elem.surtidor==15 and elem.manguera==3):
            ini = s_turno1[0].pico27v
            fin = s_turno[0].pico27v

        elif (elem.surtidor==15 and elem.manguera==4):
            ini = s_turno1[0].pico28v
            fin = s_turno[0].pico28v

        elif (elem.surtidor==16 and elem.manguera==1):
            ini = s_turno1[0].pico29v
            fin = s_turno[0].pico29v

        elif (elem.surtidor==16 and elem.manguera==2):
            ini = s_turno1[0].pico30v
            fin = s_turno[0].pico30v

        elif (elem.surtidor==16 and elem.manguera==3):
            ini = s_turno1[0].pico31v
            fin = s_turno[0].pico31v

        elif (elem.surtidor==16 and elem.manguera==4):
            ini = s_turno1[0].pico32v
            fin = s_turno[0].pico132v

            
        db.executesql('UPDATE picos SET totalvolinicial='+str(ini)+',totalvolfinal='+str(fin)+',totalvoldif='+str(fin-ini)+' WHERE picos.surtidor='+str(elem.surtidor)+' and picos.manguera='+str(elem.manguera)+';')

    consulta=(db.picos.tanque==db.tanques.nrotanque)&(db.tanques.combustible==db.producto.nroprod)

    picosur = db(consulta).select(db.picos.nropico,db.picos.surtidor,db.picos.manguera,db.producto.descripcion,db.producto.preciocred,db.picos.totalvolinicial,db.picos.totalvolfinal,db.picos.totalvoldif,orderby=db.picos.nropico)

#'''Datos para el reporte '''


    t_final=[]
    v1="Nro Pico"
    v2="Surtidor"
    v3="Manguera"
    v4="Prodcuto"
    v5="Volumen Inicial"
    v6="Volumen Final"
    v7="Volumen Vendido"
    lis=v1,v2,v3,v4,v5,v6,v7
    tabla=list(lis)
    t_final.append(tabla)
    total_de_litros=0
    for elem in picosur:
        v1=str(elem.picos.nropico)
        v2=str(elem.picos.surtidor)
        v3=str(elem.picos.manguera)
        v4=str(elem.producto.descripcion)
        v5=("{0:.2f}".format(elem.picos.totalvolinicial))
        v6=("{0:.2f}".format(elem.picos.totalvolfinal))
        #"{0:.2f}".format(elem.picos.totalvoldif)
        v7=("{0:.2f}".format(elem.picos.totalvoldif))
        total_de_litros=total_de_litros+elem.picos.totalvoldif
        lis=v1,v2,v3,v4,v5,v6,v7
        tabla=list(lis)
        t_final.append(tabla)
    ''' Cargar Totales'''
    v1=str()
    v2=str()
    v3=str()
    v4=str("Totales")
    v5=str()
    v6=str()
    v7=str("{0:.2f}".format(total_de_litros))
    lis=v1,v2,v3,v4,v5,v6,v7
    tabla=list(lis)
    t_final.append(tabla)
##        story1.append(Paragraph(str(elem.nroturno)+'..'+str(elem1.inicio)+'..'+str(elem1.fin),styles["Normal"]))

## INICIA EL REPORTE
    p = ParagraphStyle('parrafos')
    p.alignment = TA_LEFT
    p.fontSize = 10
    p.fontName="Times-Roman"
    fe=datetime.now()
    fe.isoformat()
    #fe.strftime("%c")
    fecha_hora = "Fecha y hora  "+fe.strftime("%d/%m/%Y   %H:%M")
    title = "Listado de Aforadores - Turno : "+str(s_turno[0].nroturno)
    subtitle =" Fecha y hora de Inicio  "+(s_turno[0].inicio).strftime("%d/%m/%Y   %H:%M")  +" al "+(s_turno[0].fin).strftime("%d/%m/%Y   %H:%M")
    styles = getSampleStyleSheet()
    story1 = []
    story1.append(Paragraph((fecha_hora),p))
    story1.append(Spacer(0,10))
    story1.append(Paragraph((title),styles["Title"]))
    story1.append(Paragraph((subtitle),styles["Title"]))
    story1.append(Spacer(0,10))
    tabla=Table(t_final)
    tabla.setStyle([('TEXTCOLOR',(0,0),(6,0),colors.red),('TEXTCOLOR',(0,1),(3,-1),colors.blue)])
    tabla.setStyle([('BACKGROUND',(4,1),(-1,-1),colors.gray)])
    tabla.setStyle([('BOX',(0,0),(-1,-1),0.25,colors.black)])
    tabla.setStyle([('INNERGRID',(0,0),(-1,-1),0.25,colors.black)])
    tabla.setStyle([('ALIGN',(4,1),(-1,-1),'RIGHT')])
    tabla.setStyle([('FONTSIZW',(0,0),(-1,-1),3)])
    story1.append(tabla)
    story1.append(Spacer(0,10))
    #story1.append(Spacer(0,20))
    #story1.append(Spacer(0,20))
    #total_tabla= "Total Venta de Litros "+ "{0:.2f}".format(total_de_litros)
    #story1.append(Paragraph((total_tabla),styles["Heading4"]))
    buffer1 = cStringIO.StringIO()
    #size=landscape(A4)
    size=A4
    doc = SimpleDocTemplate (buffer1,pagesize=size)
        #doc.build(story1,onFirstPage=_doNothing , onLaterPages=_doNothing)
    doc.build(story1)
    response.headers['Content-Type']='application/pdf'
    pdf = buffer1.getvalue(doc)
    buffer1.close()
    
    if variables.imprime=='exe':
        stream=cStringIO.StringIO()
        picosur.export_to_csv_file(stream)
        response.headers['Content-Type']='application/vnd.ms-excel'
        #response.headers['filename']='despacho.xls'
        #response.write(stream.getvalue(), escape=True)
        pdf = stream.getvalue(picosur)
        stream.close()

        
    return pdf


def afodespacho():
    nro=request.args[0]

#    despachos.pico = picos.nropico AND
#    picos.tanque = tanques.nrotanque AND
#    tanques.combustible = producto.nroprod;

    consulta=(db.despachos.turno==nro)&((db.despachos.pico==db.picos.nropico)&(db.picos.tanque==db.tanques.nrotanque)&(db.tanques.combustible==db.producto.nroprod))
    
    group=(db.despachos.pico,db.producto.descripcion,db.picos.surtidor,db.picos.manguera)

   # q_despacho = db(consulta).select(db.despachos.pico,db.producto.descripcion,db.despachos.volvta.sum(),groupby=(group),orderby=db.despachos.pico)

    q_despacho = db(consulta).select(db.despachos.pico,db.picos.surtidor,db.picos.manguera,db.producto.descripcion,db.despachos.volvta.sum().with_alias('volvta') ,db.despachos.facvta.sum().with_alias('facvta'),orderby=db.despachos.pico,groupby=group)
#    print(q_despacho)
#    print("")
#    print("")
#    for elem in q_despacho:
#        print(elem)
#        print("")
#        print("")
#        var1=elem.volvta
#        var2=var1
#    return(dict(form=q_despacho,var=var2))
#'''Datos para el reporte '''

    t_final=[]
    v1="Pico"
    v2="Surtidor"
    v3="Manguera"
    v4="Producto"
    v5="Vol. Venta"
    v6="Pesos Venta"
#    v7="Vol. Vendido"
#    v8="Fac. Inicial"
#    v9="Fac. Final"
#    v10="Fac. Vendido"
#
    lis=v1,v2,v3,v4,v5,v6
    tabla=list(lis)
    t_final.append(tabla)
    total_de_litros=0
    total_de_pesos=0
    for elem in q_despacho:
        v1=str(elem.despachos.pico)
        v2=str(elem.picos.surtidor)
        v3=str(elem.picos.manguera)
        v4=str(elem.producto.descripcion)
        v5=("{0:.2f}".format(elem.volvta))
        v6=("{0:.2f}".format(elem.facvta))
#        v7=str(elem.volvta)
#        v8=str(elem.factinicial)
#        v9=str(elem.factfinal)
#        v10=str(elem.facvta)
#        #"{0:.2f}".format(elem.picos.totalvoldif)
#        v7=("{0:.2f}".format(elem.volvta))
#        v10=("{0:.2f}".format(elem.facvta))
#
        total_de_litros=total_de_litros+elem.volvta
        total_de_pesos=total_de_pesos+elem.facvta
        lis=v1,v2,v3,v4,v5,v6
        tabla=list(lis)
        t_final.append(tabla)


    ''' Cargar Totales'''
    v1=str()
    v2=str()
    v3=str()
    v4=str("Totales")
    v5=("{0:.2f}".format(total_de_litros))
    v6=("{0:.2f}".format(total_de_pesos))
#    v7=("{0:.2f}".format(total_de_litros))
#    v8=str()
#    v9=str()
#    v10=("{0:.2f}".format(total_de_pesos))
    lis=v1,v2,v3,v4,v5,v6
    tabla=list(lis)
    t_final.append(tabla)
###        story1.append(Paragraph(str(elem.nroturno)+'..'+str(elem1.inicio)+'..'+str(elem1.fin),styles["Normal"]))
#
### INICIA EL REPORTE
    p = ParagraphStyle('parrafos')
    p.alignment = TA_LEFT
    p.fontSize = 12
    p.fontName="Times-Roman"
    fe=datetime.now()
    fe.isoformat()
    #fe.strftime("%c")
    fecha_hora = "Fecha y hora  "+fe.strftime("%d/%m/%Y   %H:%M")
    #time.strftime("%c")
    title = "Listado de Totales de Aforadores de acuerdo a Despachos- Turno : "+str(nro)
    subtitle =""
    styles = getSampleStyleSheet()
    story1 = []
    story1.append(Paragraph((fecha_hora),p))
    story1.append(Spacer(0,10))
    story1.append(Paragraph((title),styles["Title"]))
    story1.append(Paragraph((subtitle),styles["Heading4"]))
    story1.append(Spacer(0,10))
    tabla=Table(t_final)
    tabla.setStyle([('TEXTCOLOR',(0,-1),(0,-1),colors.red),('TEXTCOLOR',(0,1),(3,-1),colors.blue)])
    tabla.setStyle([('BACKGROUND',(4,1),(-1,-1),colors.gray)])
    tabla.setStyle([('BOX',(0,0),(-1,-1),0.25,colors.black)])
    tabla.setStyle([('INNERGRID',(0,0),(-1,-1),0.25,colors.black)])
    tabla.setStyle([('ALIGN',(4,1),(-1,-1),'RIGHT')])
    tabla.setStyle([('FONTSIZE',(0,0),(-1,-1),7)])
    story1.append(tabla)
    story1.append(Spacer(0,10))
#
    #story1.append(Spacer(0,20))
    #story1.append(Spacer(0,20))
    #total_tabla= "Total Venta de Litros "+ "{0:.2f}".format(total_de_litros)
    #story1.append(Paragraph((total_tabla),styles["Heading4"]))
    buffer1 = cStringIO.StringIO()
    #size=landscape(A4)
    size=A4
    doc = SimpleDocTemplate(buffer1,pagesize=size)
    doc.build(story1)
    pdf = buffer1.getvalue(doc)
    buffer1.close()


    response.headers['Content-Type']='application/pdf'
    if variables.imprime=='exe':
        stream=cStringIO.StringIO()
        q_despacho.export_to_csv_file(stream)
        response.headers['Content-Type']='application/vnd.ms-excel'
        pdf = stream.getvalue(q_despacho)
        stream.close()

#
    return pdf


def proddespacho():
    nro=request.args[0]

#    despachos.pico = picos.nropico AND
#    picos.tanque = tanques.nrotanque AND
#    tanques.combustible = producto.nroprod;

    consulta=(db.despachos.turno==nro)&((db.despachos.pico==db.picos.nropico)&(db.picos.tanque==db.tanques.nrotanque)&(db.tanques.combustible==db.producto.nroprod))
    
    group=(db.producto.nroprod,db.producto.descripcion)

   # q_despacho = db(consulta).select(db.despachos.pico,db.producto.descripcion,db.despachos.volvta.sum(),groupby=(group),orderby=db.despachos.pico)

    q_despacho = db(consulta).select(db.producto.nroprod.with_alias('nroprod'),db.producto.descripcion.with_alias('descripcion'),db.despachos.volvta.sum().with_alias('volvta') ,db.despachos.facvta.sum().with_alias('facvta'),orderby=db.producto.nroprod,groupby=group)
#'''Datos para el reporte '''

    t_final=[]
    v1="Nro.Prod"
    v2="Producto"
    v3="Vol. Venta"
    v4="Pesos Venta"
#
    lis=v1,v2,v3,v4
    tabla=list(lis)
    t_final.append(tabla)
    total_de_litros=0
    total_de_pesos=0
    for elem in q_despacho:
        v1=str(elem.nroprod)
        v2=str(elem.descripcion)
        v3=("{0:.2f}".format(elem.volvta))
        v4=("{0:.2f}".format(elem.facvta))
#
        total_de_litros=total_de_litros+elem.volvta
        total_de_pesos=total_de_pesos+elem.facvta
        lis=v1,v2,v3,v4
        tabla=list(lis)
        t_final.append(tabla)


    ''' Cargar Totales'''
    v1=str()
    v2=str("Totales")
    v3=("{0:.2f}".format(total_de_litros))
    v4=("{0:.2f}".format(total_de_pesos))
    lis=v1,v2,v3,v4
    tabla=list(lis)
    t_final.append(tabla)
###        story1.append(Paragraph(str(elem.nroturno)+'..'+str(elem1.inicio)+'..'+str(elem1.fin),styles["Normal"]))
#
### INICIA EL REPORTE
    p = ParagraphStyle('parrafos')
    p.alignment = TA_LEFT
    p.fontSize = 12
    p.fontName="Times-Roman"
    fe=datetime.now()
    fe.isoformat()
    #fe.strftime("%c")
    fecha_hora = "Fecha y hora  "+fe.strftime("%d/%m/%Y   %H:%M")
    #time.strftime("%c")
    title = "Listado de Totales de Aforadores de acuerdo a Despachos- Turno : "+str(nro)
    subtitle =""
    styles = getSampleStyleSheet()
    story1 = []
    story1.append(Paragraph((fecha_hora),p))
    story1.append(Spacer(0,10))
    story1.append(Paragraph((title),styles["Title"]))
    story1.append(Paragraph((subtitle),styles["Heading4"]))
    story1.append(Spacer(0,10))
    tabla=Table(t_final)
    tabla.setStyle([('TEXTCOLOR',(0,-1),(0,-1),colors.red),('TEXTCOLOR',(0,1),(3,-1),colors.blue)])
    tabla.setStyle([('BACKGROUND',(4,1),(-1,-1),colors.gray)])
    tabla.setStyle([('BOX',(0,0),(-1,-1),0.25,colors.black)])
    tabla.setStyle([('INNERGRID',(0,0),(-1,-1),0.25,colors.black)])
    tabla.setStyle([('ALIGN',(4,1),(-1,-1),'RIGHT')])
    tabla.setStyle([('FONTSIZE',(0,0),(-1,-1),7)])
    story1.append(tabla)
    story1.append(Spacer(0,10))
#
    buffer1 = cStringIO.StringIO()

    size=A4
    doc = SimpleDocTemplate(buffer1,pagesize=size)
    doc.build(story1)
    pdf = buffer1.getvalue(doc)
    buffer1.close()
    
    response.headers['Content-Type']='application/pdf'
    if variables.imprime=='exe':
        stream=cStringIO.StringIO()
        q_despacho.export_to_csv_file(stream)
        response.headers['Content-Type']='application/vnd.ms-excel'
        pdf = stream.getvalue(q_despacho)
        stream.close()



    return pdf

def excelExport():
    #print(request.vars)
    datos = request.vars
    #datos=db().select(db.producto.ALL)
    return dict(datos=datos)
