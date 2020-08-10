# -*- coding: utf-8 -*-

from pydal import DAL, Field

def db():

    db = DAL("postgres:psycopg2://postgres:postgres@192.168.0.188/midex")


    migrate = False
    fake_migrate = False
    db.define_table('producto',
                    Field('nroprod', type = 'id'),
                    Field('preciocred',type = 'decimal(15,2)'),
                    Field('preciocont', type = 'decimal(15,2)'),
                    Field('descripcion',type = 'string', length=30),
                    Field('volvta',type = 'decimal(15,3)'),
                    Field('facvta',type = 'decimal(15,3)'),
                    migrate=migrate,fake_migrate=fake_migrate
                )



    db.define_table('precio',
                    Field('nrocambio', type = 'id'),
                    Field('hora',type = 'datetime'),
                    Field('newprice', type = 'decimal(15,2)', label = 'Precio'),
                    Field('combustible', db.producto,label = 'Combustible' ),
                    Field('on_line', type = 'boolean', default = False),
                    Field('cemprod', type ='integer'),
                    migrate=migrate,fake_migrate=fake_migrate
                )

    db.define_table('tanques',
                    Field('nrotanque', type = 'id'),
                    Field('volumen',type = 'double',unique = True),
                    Field('combustible', db.producto),
                    migrate=migrate,fake_migrate=fake_migrate
                    )


    db.define_table('picos',
                    Field('nropico', type = 'id'),
                    Field('surtidor',type = 'integer' ),
                    Field('manguera',type = 'integer'),
                    Field('tiposurtidor',type = 'string',pyt =0),
                    Field('tanque', db.tanques),
                    Field('estado', type = 'string' , default = 'Fuera de Linea'),
                    Field('nesta', type = 'integer', default = 0 ),
                    Field('totalvolinicial', type = 'decimal(15,3)', default = 0 ),
                    Field('totalvolfinal', type = 'decimal(15,3)', default = 0 ),
                    Field('totalvoldif', type = 'decimal(15,3)', default = 0 ),
                    migrate=migrate,fake_migrate=fake_migrate
                    )

    db.define_table('turnos',
                    Field('nroturno', type = 'id'),
                    Field('inicio',type = 'datetime'),
                    Field('fin',type = 'datetime'),
                    Field('cerrado', type = 'boolean', default = False),
                    Field('pico1volfinal', type = 'decimal(15,3)',default =0 ),
                    Field('pico2volfinal', type = 'decimal(15,3)',default =0),
                    Field('pico3volfinal', type = 'decimal(15,3)',default =0),
                    Field('pico4volfinal', type = 'decimal(15,3)',default =0),
                    Field('pico5volfinal', type = 'decimal(15,3)',default =0),
                    Field('pico6volfinal', type = 'decimal(15,3)',default =0),
                    Field('pico7volfinal', type = 'decimal(15,3)',default =0),
                    Field('pico8volfinal', type = 'decimal(15,3)',default =0),
                    Field('pico9volfinal', type = 'decimal(15,3)',default =0),
                    Field('pico10volfinal', type = 'decimal(15,3)',default =0),
                    Field('pico11volfinal', type = 'decimal(15,3)',default =0),
                    Field('pico12volfinal', type = 'decimal(15,3)',default =0),
                    Field('pico13volfinal', type = 'decimal(15,3)',default =0),
                    Field('pico14volfinal', type = 'decimal(15,3)',default =0),
                    Field('pico15volfinal', type = 'decimal(15,3)',default =0),
                    Field('pico16volfinal', type = 'decimal(15,3)',default =0),
                    Field('pico3vol', type = 'decimal(15,3)',default =0),
                    Field('pico4vol', type = 'decimal(15,3)',default =0),
                    Field('pico5vol', type = 'decimal(15,3)',default =0),
                    Field('pico6vol', type = 'decimal(15,3)',default =0),
                    Field('pico7vol', type = 'decimal(15,3)',default =0),
                    Field('pico8vol', type = 'decimal(15,3)',default =0),
                    Field('pico9vol', type = 'decimal(15,3)',default =0),
                    Field('pico10vol', type = 'decimal(15,3)',default =0),
                    Field('pico11vol', type = 'decimal(15,3)',default =0),
                    Field('pico12vol', type = 'decimal(15,3)',default =0),
                    Field('pico13vol', type = 'decimal(15,3)',default =0),
                    Field('pico14vol', type = 'decimal(15,3)',default =0),
                    Field('pico15vol', type = 'decimal(15,3)',default =0),
                    Field('pico16vol', type = 'decimal(15,3)',default =0),
                    Field('activo', type ='integer',default =0),
                    Field('pico1v', type = 'decimal(15,3)',default =0),
                    Field('pico2v', type = 'decimal(15,3)',default =0),
                    Field('pico3v', type = 'decimal(15,3)',default =0),
                    Field('pico4v', type = 'decimal(15,3)',default =0),
                    Field('pico5v', type = 'decimal(15,3)',default =0),
                    Field('pico6v', type = 'decimal(15,3)',default =0),
                    Field('pico7v', type = 'decimal(15,3)',default =0),
                    Field('pico8v', type = 'decimal(15,3)',default =0),
                    Field('pico9v', type = 'decimal(15,3)',default =0),
                    Field('pico10v', type = 'decimal(15,3)',default =0),
                    Field('pico13v', type = 'decimal(15,3)',default =0),
                    Field('pico14v', type = 'decimal(15,3)',default =0),
                    Field('pico15v', type = 'decimal(15,3)',default =0),
                    Field('pico16v', type = 'decimal(15,3)',default =0),
                    Field('pico17v', type = 'decimal(15,3)',default =0),
                    Field('pico18v', type = 'decimal(15,3)',default =0),
                    Field('pico19v', type = 'decimal(15,3)',default =0),
                    Field('pico20v', type = 'decimal(15,3)',default =0),
                    Field('pico21v', type = 'decimal(15,3)',default =0),
                    Field('pico25v', type = 'decimal(15,3)',default =0),
                    Field('pico26v', type = 'decimal(15,3)',default =0),
                    Field('pico27v', type = 'decimal(15,3)',default =0),
                    Field('pico28v', type = 'decimal(15,3)',default =0),
                    Field('pico29v', type = 'decimal(15,3)',default =0),
                    Field('pico30v', type = 'decimal(15,3)',default =0),
                    Field('pico31v', type = 'decimal(15,3)',default =0),
                    Field('pico32v', type = 'decimal(15,3)',default =0),
                    migrate=migrate,fake_migrate=fake_migrate
                    )

    db.define_table('despachos',
                    Field('nrodesp', type = 'id'),
                    Field('horainicio',type = 'datetime'),
                    Field('horafin',type = 'datetime'),
                    Field('volinicial',type = 'decimal(15,3)'),
                    Field('volfinal',type = 'decimal(15,3)'),
                    Field('factinicial',type = 'decimal(15,2)'),
                    Field('tipofact',type = 'string',default='C'),
                    Field('pico',type = db.picos),
                    Field('factfinal',type = 'decimal(15,2)'),
                    Field('turno',db.turnos),
                    Field('volvta',type = 'decimal(15,3)'),
                    Field('facvta',type = 'decimal(15,2)'),
                    Field('nrocem', type ='integer'),
                    Field('pago', type ='string',default = '00'),
                    migrate=migrate,fake_migrate=fake_migrate
                    )
    return(db) 



