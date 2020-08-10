import PythonGrid
import modelo.db_dato as db

db = db.db()

grid = PythonGrid ( 'SELECT * FROM orders' , 'orderNumber' , 'orders' )
return render_template ( 'grid.html' , title = 'demo' , grid = grid ) 