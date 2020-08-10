# -*- coding: utf-8 -*-

def turno_co():
    form=FORM(TABLE(TR("Turno Inicial:",INPUT(_type="text",_name="ini",requires=IS_NOT_EMPTY())),
                    TR("Turno Final:",INPUT(_type="text",_name="fin",requires=IS_NOT_EMPTY())),
                    TR(INPUT(_type="submit",_name="aceptar"))))
                    #TR(P((TAG.BUTTON("   Aceptar.    ", _type="submit", _name="aceptar", _value="aceptar"))))))
                    #P((TAG.BUTTON("   Cancelar   ", _type="submit", _name="cancelar", _value="cancelar"))))))

    if form.accepts(request.vars,session):
        response.flash="Formulario Completo"
        #session.vars.ini=request.vars.ini
        #session.vars.fin=request.vars.ini
        #response.flash=
        redirect(URL('corrige_base', 'proces',vars= dict(ini=request.vars.ini,fin=request.vars.fin)))
        #redirect(URL(ecuest, f='proces'))
        #if request.vars.cancelar:
        #    response.flash="Cancelando"
         #   redirect(URL('corrige_base', 'proces'))
            #redirect(URL('default', 'imagen'))

    #elif form.errors:
    #    response.flash="Formulario inválido"
    else:
        response.flash="por favor complete el formulario"

    #CONSULTA DE DESPACHOS
    #l_turno = db().select(db.turnos.ALL,orderby=db.turnos.id)
    #return dict(grid=form,vars=form.vars)
    return dict(grid=form)

def proces():
    session.flash="Proceso Terminado"
    #session.flash=session.vars.ini
    consulta=(db.turnos.nroturno>=request.vars['ini']) & (db.turnos.nroturno<=request.vars['fin'])
    el_turno =  db(consulta).select(db.turnos.ALL,orderby=db.turnos.id)
    el_pico = db().select(db.picos.ALL,orderby=db.picos.id)
    pi=len(el_pico)
    ra=len(el_turno)
    nu=[]
    var1=[]
    for i in range(ra):
        va=el_turno[i].nroturno
        p1=el_turno[i].pico1volfinal
        p2=el_turno[i].pico2volfinal
        p3=el_turno[i].pico3volfinal
        p4=el_turno[i].pico4volfinal
        p5=el_turno[i].pico5volfinal
        p6=el_turno[i].pico6volfinal
        p7=el_turno[i].pico7volfinal
        p8=el_turno[i].pico8volfinal
        p9=el_turno[i].pico9volfinal
        p10=el_turno[i].pico10volfinal
        p11=el_turno[i].pico11volfinal
        p12=el_turno[i].pico12volfinal
        p13=el_turno[i].pico13volfinal
        p14=el_turno[i].pico14volfinal
        p15=el_turno[i].pico15volfinal
        p16=el_turno[i].pico16volfinal
        p17=el_turno[i].pico1vol
        p18=el_turno[i].pico2vol
        p19=el_turno[i].pico3vol
        p20=el_turno[i].pico4vol
        p21=el_turno[i].pico5vol
        p22=el_turno[i].pico6vol
        p23=el_turno[i].pico7vol
        p24=el_turno[i].pico8vol
        p25=el_turno[i].pico9vol
        p26=el_turno[i].pico10vol
        p27=el_turno[i].pico11vol
        p28=el_turno[i].pico12vol
        p29=el_turno[i].pico13vol
        p30=el_turno[i].pico14vol
        p31=el_turno[i].pico15vol
        p32=el_turno[i].pico16vol
        consulta = (db.turnos.nroturno==va)
        db(consulta).update(
                pico1volfinal=0,
                pico2volfinal=0,
                pico3volfinal=0,
                pico4volfinal=0,
                pico5volfinal=0,
                pico6volfinal=0,
                pico7volfinal=0,
                pico8volfinal=0,
                pico9volfinal=0,
                pico10volfinal=0,
                pico11volfinal=0,
                pico12volfinal=0,
                pico13volfinal=0,
                pico14volfinal=0,
                pico15volfinal=0,
                pico16volfinal=0,
                pico1vol=0,
                pico2vol=0,
                pico3vol=0,
                pico4vol=0,
                pico5vol=0,
                pico6vol=0,
                pico7vol=0,
                pico8vol=0,
                pico9vol=0,
                pico10vol=0,
                pico11vol=0,
                pico12vol=0,
                pico13vol=0,
                pico14vol=0,
                pico15vol=0,
                pico16vol=0
                )
        relaci1={'(1,1)':'pico1volfinal',
                '(1,2)':'pico2volfinal',
                '(1,3)':'pico3volfinal',
                '(1,4)':'pico4volfinal',
                '(2,1)':'pico5volfinal',
                '(2,2)':'pico6volfinal',
                '(2,3)':'pico7volfinal',
                '(2,4)':'pico8volfinal',
                '(3,1)':'pico9volfinal',
                '(3,2)':'pico10volfinal',
                '(3,3)':'pico11volfinal',
                '(3,4)':'pico12volfinal',
                '(4,1)':'pico13volfinal',
                '(4,2)':'pico14volfinal',
                '(4,3)':'pico15volfinal',
                '(4,4)':'pico16volfinal',
                '(5,1)':'pico1vol',
                '(5,2)':'pico2vol',
                '(5,3)':'pico3vol',
                '(5,4)':'pico4vol',
                '(6,1)':'pico5vol',
                '(6,2)':'pico6vol',
                '(6,3)':'pico7vol',
                '(6,4)':'pico8vol',
                '(7,1)':'pico9vol',
                '(7,2)':'pico10vol',
                '(7,3)':'pico11vol',
                '(7,4)':'pico12vol',
                '(8,1)':'pico13vol',
                '(8,2)':'pico14vol',
                '(8,3)':'pico15vol',
                '(8,4)':'pico16vol',
                '(9,1)':'pico1v',
                '(9,2)':'pico2v',
                '(9,3)':'pico3v',
                '(9,4)':'pico4v',
                '(10,1)':'pico5v',
                '(10,2)':'pico6v',
                '(10,3)':'pico7v',
                '(10,4)':'pico8v',
                '(11,1)':'pico9v',
                '(11,2)':'pico10v',
                '(11,3)':'pico11v',
                '(11,4)':'pico12v',
                '(12,1)':'pico13v',
                '(12,2)':'pico14v',
                '(12,3)':'pico15v',
                '(12,4)':'pico16v',
                '(13,1)':'pico17v',
                '(13,2)':'pico18v',
                '(13,3)':'pico19v',
                '(13,4)':'pico20v',
                '(14,1)':'pico21v',
                '(14,2)':'pico22v',
                '(14,3)':'pico23v',
                '(14,4)':'pico24v',
                '(15,1)':'pico25v',
                '(15,2)':'pico26v',
                '(15,3)':'pico27v',
                '(15,4)':'pico28v',
                '(16,1)':'pico29v',
                '(16,2)':'pico30v',
                '(16,3)':'pico31v',
                '(16,4)':'pico32v',
                }

        relaci2={'(1)':p1,
                '(2)':p2,
                '(3)':p3,
                '(4)':p4,
                '(5)':p5,
                '(6)':p6,
                '(7)':p7,
                '(8)':p8,
                '(9)':p9,
                '(10)':p10,
                '(11)':p11,
                '(12)':p12,
                '(13)':p13,
                '(14)':p14,
                '(15)':p15,
                '(16)':p16,
                '(17)':p17,
                '(18)':p18,
                '(19)':p19,
                '(20)':p20,
                '(21)':p21,
                '(22)':p22,
                '(23)':p23,
                '(24)':p24,
                '(25)':p25,
                '(26)':p26,
                '(27)':p27,
                '(28)':p28,
                '(29)':p29,
                '(30)':p30,
                '(31)':p31,
                '(32)':p32,
                }


        for p in range(pi):
            nu_pi=el_pico[p].nropico
            su_pi=el_pico[p].surtidor
            ma_pi=el_pico[p].manguera
            valor='('+str(su_pi)+','+str(ma_pi)+')'
            valor1='('+str(nu_pi)+')'
            #rel='db.turnos.'+relaci1[valor]
            #rel=relaci1[valor]
            #rel2=relaci2[str(nu_pi)]
            cadena='{rel}={rel2}'
            upd=(cadena.format(rel=relaci1[valor],rel2=relaci2[valor1]))
            #upd= {rel:rel2}

            #consulta = (db.turnos.nroturno==va)
            upd='update turnos set '+upd+' where nroturno = '+str(va)
            #db(consulta).update(upd)

            db.executesql(upd)

#            if nu_pi=1:
#

        #var1.append(p32)
    #nu.append(var1)

    #redirect(URL('default', 'index'))
    return(dict(form=(upd)))
    #,var = str(nu[0][0])+str(nu[0][1])+str(nu[0][2])+str(nu[0][3])))