# -*- coding: utf-8 -*-
import datetime
migrate = True


db.define_table('prodview',
				Field('nropico', type = 'integer'),
				Field('surtidor',type = 'integer', requires=IS_INT_IN_RANGE(1, 33)),
				Field('manguera',type = 'integer', requires=IS_INT_IN_RANGE(1, 5)),
				Field('tiposurtidor',type = 'string'),
				Field('tanque', type = 'integer'),
				Field('estado', type = 'string' , default = 'Fuera de Linea'),
				Field('nesta', type = 'integer', default = 0 ),
				Field('nrotanque', type = 'integer'),
				Field('volumen',type = 'double'),
				Field('combustible', type = 'integer'),
				Field('nroprod',  type = 'integer'),
				Field('preciocred',type = 'double'),
				Field('preciocont', type = 'double'),
				Field('descripcion',type = 'string', length=30),
				Field('volvta',type = 'double'),
				Field('facvta',type = 'double'),
				migrate=False
			    )

db.define_table('view_precio',
				Field('nrocambio', type = 'id'),
				Field('hora',type = 'datetime'),
				Field('newprice', type = 'double'),
				Field('combustible', db.producto, default=session.id),
				Field('descripcion',type = 'string', length=30),
				Field('on_line', type = 'boolean', default = False),
			    Field('cemprod', type ='integer'),
				migrate=False
			   )
