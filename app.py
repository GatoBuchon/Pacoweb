import os
from flask import Flask, render_template, request,redirect,url_for, flash,jsonify
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_paginate import Pagination, get_page_parameter

from models.ModelUser import ModuleUser
from models.entities.user import User

app = Flask(__name__)
csrf=CSRFProtect()
#-------------------------------------------Conexion a la base datos ---------------------------------------------------
app.config['MYSQL_HOST']= 'localhost'
app.config['MYSQL_USER'] = 'lobato'
app.config['MYSQL_PASSWORD'] = 'gatito'
app.config['MYSQL_DB'] = 'buerreras'

db=MySQL(app)
app.secret_key='mysecretkey'

Login_manager_app=LoginManager(app)

@Login_manager_app.user_loader
def load_user(idUsuario):
    return ModuleUser.get_by_id(db,idUsuario)


#----------------------------------Materiales-------------------------------------------------------------------
PER_PAGE = 5
def Material_Paginar(page):
    cur=db.connection.cursor()
    offset = (page - 1) * PER_PAGE
    sql = "SELECT * FROM materiales LIMIT %s OFFSET %s"
    cur.execute(sql, (PER_PAGE, offset))
    resultados_pagina_actual = cur.fetchall()
    sql_total = "SELECT COUNT(*) FROM materiales"
    cur.execute(sql_total)
    total_results = cur.fetchone()[0]

    cur.close()

    return resultados_pagina_actual, total_results

@app.route('/materiales')
@login_required
def Material_Ver ():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    resultados_pagina_actual, total_results = Material_Paginar(page)
    pagination = Pagination(page=page, per_page=PER_PAGE, total=total_results, outer_window=20, inner_window=20)
    return render_template('materiales.html', pagination=pagination, materiales=resultados_pagina_actual)

#----------------------------------Imprimir Materiales-------------------------------------------------------------------
@app.route('/Imprimir')
@login_required
def ImprimirM():
    cur=db.connection.cursor()
    sql="SELECT * FROM materiales ORDER BY idMateriales desc"
    cur .execute(sql)
    materiales=cur.fetchall()
    print(materiales)
    return render_template('ImprimirLM.html', materiales=materiales)

#--------------------------------------Agregar materiales---------------------------------------------------------------

@app.route("/agregarMaterial")
@login_required
def agregarM():
 return render_template("AgregarM.html")

@app.route ('/guaradarMaterial', methods=['POST'])
@login_required
def RegistrarM():
    if request.method == 'POST':
       NombreMateial = request.form['NombreMateial']
       Cantidad = request.form['Cantidad']
       Precio = request.form['Precio']
       Marca  = request.form['Marca']
    
       cur=db.connection.cursor()
       sql="INSERT INTO materiales (NombreMateial, Cantidad, Precio, Marca ) VALUES (%s, %s, %s, %s)"
       valores=(NombreMateial, Cantidad, Precio, Marca)
       cur.execute(sql,valores)
       db.connection.commit() 
       flash('Material registrado')
       return redirect(url_for('Material_Ver'))
    
#----------------------------------------Editar materiales----------------------------------------------------------------

@app.route('/EditarMaterial/<string:id>')
@login_required
def editarM(id):
  print(id)
  cur=db.connection.cursor()
  sql="SELECT * FROM materiales WHERE idMateriales={0}".format(id)
  cur.execute(sql)
  NombreMaterial=cur.fetchall()
  print(NombreMaterial[0])
  return render_template('EditarM.html', NombreMaterial=NombreMaterial[0])
  
@app.route ('/EditarMaterial/<string:id>', methods=['POST'])
@login_required
def editarMA(id):
    if request.method == 'POST':
       NombreMateial = request.form['NombreMateial']
       Cantidad = request.form['Cantidad']
       Precio = request.form['Precio']
       Marca  = request.form['Marca']
       cur=db.connection.cursor()
       sql="UPDATE materiales SET NombreMateial=%s, Cantidad=%s, Precio=%s, Marca=%s WHERE idMateriales=%s"
       valores=(NombreMateial, Cantidad, Precio, Marca,id)
       cur.execute(sql,valores)
       db.connection.commit() 
       flash('Material editado')
    return redirect(url_for('Material_Ver'))

#----------------------------------------Eliminar materiales----------------------------------------------------------------

@app.route('/EliminarMaterial/<string:id>')
@login_required
def EliminarM(id):
  print(id)
  cur=db.connection.cursor()
  sql="DELETE FROM materiales WHERE idMateriales={0}".format(id)
  cur.execute(sql)
  db.connection.commit()
  flash('Material eliminado')
  return redirect(url_for('Material_Ver'))

#----------------------------------------Usuarios---------------------------------------------------------------- 

@app.route('/Usuarios')
@login_required
def Usuarios_Ver ():
    cur=db.connection.cursor()
    sql="SELECT * FROM usuario ORDER BY idUsuario desc"
    cur.execute(sql)
    usuario=cur.fetchall()
    print(usuario)
    return render_template('Usuarios.html', usuario=usuario)

#--------------------------------------Agregar usuarios---------------------------------------------------------------

@app.route("/agregarUsuario")
def agregarU():
  return render_template("AgregarU.html")

@app.route ('/guaradarUsuarios', methods=['POST'])
def RegistrarU():
    if request.method == 'POST':
       Nombre = request.form['Nombre']
       Password = request.form['Password']
       TipoUsuario = request.form['TipoUsuario']
      
       
       cur=db.connection.cursor()
       sql="INSERT INTO Usuario (Nombre, Password, TipoUsuario) VALUES (%s, %s,%s)"
       valores=(Nombre, generate_password_hash(Password),TipoUsuario)
       cur.execute(sql,valores)
       db.connection.commit() 
       flash('Usuario registrado')
       return redirect(url_for('Usuarios_Ver'))

#----------------------------------------Editar usuarios----------------------------------------------------------------

@app.route('/EdiUsuario/<string:id>')
@login_required
def editarU(id):
  print(id)
  cur=db.connection.cursor()
  sql="SELECT * FROM usuario WHERE idUsuario={0}".format(id)
  cur.execute(sql)
  Nombre=cur.fetchall()
  print(Nombre[0])
  return render_template('EditarU.html', Nombre=Nombre[0])
  
@app.route ('/EditarU/<string:id>', methods=['POST'])
def EditarUU(id):
    if request.method == 'POST':
       Nombre = request.form['Nombre']
       Password = request.form['Password']
       Pass=generate_password_hash(Password)
       TipoUsuario = request.form['TipoUsuario']
     
       cur=db.connection.cursor()
       sql="UPDATE usuario SET Nombre=%s, Password=%s, TipoUsuario=%s WHERE idUsuario=%s"
       valores=(Nombre,Pass,TipoUsuario,id)
       cur.execute(sql,valores)
       db.connection.commit() 
       flash('Usuario editado')
    return redirect(url_for('Usuarios_Ver'))

#----------------------------------------Eliminar usuarios----------------------------------------------------------------

@app.route('/ElimiU/<string:id>')
@login_required
def EliminarU(id):
  print(id)
  cur=db.connection.cursor()
  sql="DELETE FROM usuario WHERE idUsuario={0}".format(id)
  cur.execute(sql)
  db.connection.commit()
  flash('Usuario eliminado')
  return redirect(url_for('Usuarios_Ver'))

#----------------------------------------Pedidos-----------------------------------------------------------------------

@app.route('/Pedidos')
@login_required
def Pedidoss_Ver ():
    cur=db.connection.cursor()
    sql="SELECT * FROM pedidos ORDER BY idPedidos desc"
    cur.execute(sql)
    pedidos=cur.fetchall()
    print(pedidos)
    return render_template('pedidos.html', pedidos=pedidos)

#--------------------------------------Agregar pedido-------------------------------------------------------------------------------------

@app.route("/agregarPedido")
@login_required
def agregarp():
  return render_template("AgregarP.html")

@app.route ('/guaradarPedidos', methods=['POST'])
@login_required
def RegistrarP():
    if request.method == 'POST':
       Color = request.form['Color']
       Cantidad_bu = request.form['Cantidad_bu']
       Fecha = request.form['Fecha']
       Cuenta = request.form['Cuenta']
       Modelo_Camioneta = request.form['Modelo_Camioneta']
       Cliente = request.form['Cliente']
       L = request.form['L']
       ConL = request.form['ConL']
       TipoB = request.form['TipoB']
       cur=db.connection.cursor()
       sql="INSERT INTO pedidos (Color, Cantidad_bu, Fecha, Cuenta, Modelo_Camioneta, Cliente, L, ConL, TipoB) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
       valores=(Color, Cantidad_bu, Fecha, Cuenta, Modelo_Camioneta, Cliente, L, ConL, TipoB)
       cur.execute(sql,valores)
       db.connection.commit() 
       flash('Pedido registrado')
       return redirect(url_for('Pedidoss_Ver'))
    
#----------------------------------------Editar pedidos---------------------------------------------------------------------------------

@app.route('/EditarPedido/<string:id>')
@login_required
def editarP(id):
  print(id)
  cur=db.connection.cursor()
  sql="SELECT * FROM pedidos WHERE idPedidos={0}".format(id)
  cur.execute(sql)
  Color=cur.fetchall()
  print(Color[0])
  return render_template('Editarp.html', Color=Color[0])
  
@app.route ('/EditarPedidos/<string:id>', methods=['POST'])
@login_required
def EditarPP(id):
    if request.method == 'POST':
       Color = request.form['Color']
       Cantidad_bu = request.form['Cantidad_bu']
       Fecha = request.form['Fecha']
       Cuenta = request.form['Cuenta']
       Modelo_Camioneta = request.form['Modelo_Camioneta']
       Cliente = request.form['Cliente']
       L = request.form['L']
       ConL = request.form['ConL']
       TipoB = request.form['TipoB']
       cur=db.connection.cursor()
       sql="UPDATE pedidos SET Color=%s, Cantidad_bu=%s, Fecha=%s, Cuenta=%s, Modelo_Camioneta=%s, Cliente=%s, L=%s, ConL=%s, TipoB=%s WHERE idPedidos=%s"
       valores=(Color, Cantidad_bu, Fecha, Cuenta, Modelo_Camioneta, Cliente, L, ConL, TipoB, id)
       cur.execute(sql,valores)
       db.connection.commit() 
       flash('Pedido editado')
    return redirect(url_for('Pedidoss_Ver'))

#----------------------------------------Imprimir pedido---------------------------------------------------------------------------------

@app.route('/ImprimirPedido/<string:id>')
@login_required
def ImprimirP(id):
  print(id)
  cur=db.connection.cursor()
  sql="SELECT * FROM pedidos WHERE idPedidos={0}".format(id)
  cur.execute(sql)
  Color=cur.fetchall()
  print(Color[0])
  return render_template('imprimirp.html', Color=Color[0])
  
@app.route ('/ImprimirPedidos/<string:id>', methods=['POST'])
@login_required
def ImprimirPP(id):
    if request.method == 'POST':
       Color = request.form['Color']
       Cantidad_bu = request.form['Cantidad_bu']
       Fecha = request.form['Fecha']
       Cuenta = request.form['Cuenta']
       Modelo_Camioneta = request.form['Modelo_Camioneta']
       Cliente = request.form['Cliente']
       L = request.form['L']
       ConL = request.form['ConL']
       TipoB = request.form['TipoB']
       cur=db.connection.cursor()
       sql="UPDATE pedidos SET Color=%s, Cantidad_bu=%s, Fecha=%s, Cuenta=%s, Modelo_Camioneta=%s, Cliente=%s, L=%s, ConL=%s, TipoB=%s WHERE idPedidos=%s"
       valores=(Color, Cantidad_bu, Fecha, Cuenta, Modelo_Camioneta, Cliente, L, ConL, TipoB, id)
       cur.execute(sql,valores)
       db.connection.commit() 
    return redirect(url_for('Pedidoss_Ver'))

#----------------------------------------Eliminar pedidos--------------------------------------------------------------------------------------

@app.route('/EliminarPedido/<string:id>')
@login_required
def EliminarP(id):
  print(id)
  cur=db.connection.cursor()
  sql="DELETE FROM pedidos WHERE idPedidos={0}".format(id)
  cur.execute(sql)
  db.connection.commit()
  flash('Pedido eliminado')
  return redirect(url_for('Pedidoss_Ver'))

#------------------------------------------Burreras -------------------------------------------------------------------

@app.route('/Burreras')
@login_required
def Burreras_Ver ():
    cur=db.connection.cursor()
    sql="SELECT * FROM burreras ORDER BY IdBurreas desc"
    cur.execute(sql)
    cliente=cur.fetchall()
    print(cliente)
    return render_template('Burreras.html', cliente=cliente)

#--------------------------------------Agregar burreras-------------------------------------------------------------------------------------

@app.route("/agregarBurrera")
@login_required
def agregarB():
  return render_template("AgregarBR.html", clientes=listar_clientes())

@app.route ('/guaradarBRR', methods=['POST'])
@login_required
def RegistraBrr():
    if request.method == 'POST':
       Cliente = request.form['Cliente']
       Material_Ocupado = request.form['Material_Ocupado']
       Cantidad_bu = request.form['Cantidad_bu']
       Fecha= request.form['Fecha']
       cur=db.connection.cursor()
       sql="INSERT INTO burreras (Cliente, Material_Ocupado, Cantidad_bu, Fecha) VALUES (%s, %s, %s, %s)"
       valores=(Cliente, Material_Ocupado, Cantidad_bu, Fecha)
       cur.execute(sql,valores)
       db.connection.commit() 
       flash('Burreras registradas')
       return redirect(url_for('Burreras_Ver'))
    
def listar_clientes():
    cur=db.connection.cursor()
    sql="SELECT * FROM pedidos order by cliente asc"
    cur.execute(sql)
    cliente=cur.fetchall()
    cur.close()
    return cliente

#----------------------------------------Editar Burreras---------------------------------------------------------------------------------

@app.route('/EditarBurreras/<string:id>')
@login_required
def editarBb(id):
  print(id)
  cur=db.connection.cursor()
  sql="SELECT * FROM burreras WHERE IdBurreas={0}".format(id)
  cur.execute(sql)
  cliente=cur.fetchall()
  print(cliente[0])
  return render_template('EditarBR.html', cliente=cliente[0], clientes=listar_clientes())

@app.route ('/EditarBR/<string:id>', methods=['POST'])
@login_required
def EditarBr(id):
    if request.method == 'POST':
       Cliente = request.form['Cliente']
       Material_Ocupado = request.form['Material_Ocupado']
       Cantidad_bu = request.form['Cantidad_bu']
       Fecha= request.form['Fecha']
       cur=db.connection.cursor()
       sql="UPDATE burreras SET Cliente=%s, Material_Ocupado=%s, Cantidad_bu=%s, Fecha=%s WHERE IdBurreas=%s"
       valores=(Cliente, Material_Ocupado, Cantidad_bu, Fecha, id)
       cur.execute(sql,valores)
       db.connection.commit() 
       flash('Burreras editadas')
    return redirect(url_for('Burreras_Ver'))

#----------------------------------------Eliminar burreras--------------------------------------------------------------------------------------
@app.route('/ElirBR/<string:id>')
@login_required
def EliminarBR(id):
  print(id)
  cur=db.connection.cursor()
  sql="DELETE FROM burreras WHERE IdBurreas={0}".format(id)
  cur.execute(sql)
  db.connection.commit()
  flash('Burreras eliminadas')
  return redirect(url_for('Burreras_Ver'))

#----------------------------------------Imprimir Burreras---------------------------------------------------------------------------------

@app.route('/ImprimirBR/<string:id>')
@login_required
def Imprimirbrr(id):
  print(id)
  cur=db.connection.cursor()
  sql="SELECT * FROM burreras WHERE IdBurreas={0}".format(id)
  cur.execute(sql)
  cliente=cur.fetchall()
  print(cliente[0])
  return render_template('imprimirBR.html', cliente=cliente[0], clientes=listar_clientes())

@app.route ('/ImpriBR/<string:id>', methods=['POST'])
@login_required
def imBr(id):
    if request.method == 'POST':
       Cliente = request.form['Cliente']
       Material_Ocupado = request.form['Material_Ocupado']
       Cantidad_bu = request.form['Cantidad_bu']
       Fecha= request.form['Fecha']
       cur=db.connection.cursor()
       sql="UPDATE burreras SET Cliente=%s, Material_Ocupado=%s, Cantidad_bu=%s, Fecha=%s WHERE IdBurreas=%s"
       valores=(Cliente, Material_Ocupado, Cantidad_bu, Fecha, id)
       cur.execute(sql,valores)
       db.connection.commit() 
       flash('Burreras editadas')
    return redirect(url_for('Burreras_Ver'))

#----------------------------------------Login--------------------------------------------------------------------------------------

@app.route('/Deregreso')
def amonos():
  logout_user()
  return render_template('login.html')

@app.route('/login')
def login():
  return render_template('login.html')

@app.route('/loguear', methods=['POST'])
def loguear():
    if request.method == 'POST':
        Nombre = request.form['Nombre']
        Password = request.form['Password']
       
        user=User(0,Nombre,Password,None)
        loged_user=ModuleUser.login(db,user)

        if loged_user!= None:
          if loged_user.password:
            login_user(loged_user)
            return redirect(url_for('Todobien'))
          else:
            flash('Nombre de usuario y/o Contraseña incorrecta.')
            return render_template('login.html')
        else:
          flash('Nombre de usuario y/o Contraseña incorrecta.')
          return render_template('login.html')
    else:
      flash('Nombre de usuario y/o Contraseña incorrecta.')
      return render_template('login.html')


@app.route('/todobien')
@login_required
def Todobien():
 return render_template('bienvenida.html')


@app.route('/inicio')
def init():
        return render_template('layout.html')

@app.route('/cerrar')
def cerrar():
    return render_template('cerrar.html')
    
def query_string():
    print(request)
    print(request.args)
    print(request.args.get('parma1'))
    print(request.args.get('parma2'))
    return "Valores recibidos correrectamente"

def pagina_no_encontrada(error):
    #return render_template('404.html'), 404
    return redirect(url_for('uyno'))

@app.route('/Error')
def uyno():
   return render_template('404.html')
   
def acceso_no_autorizado(error):
    return redirect(url_for('login'))

    
if __name__ == '__main__':
 csrf.init_app(app)
 app.register_error_handler(404, pagina_no_encontrada)
 app.register_error_handler(401, acceso_no_autorizado)
 app.add_url_rule('/query_string', view_func=query_string)
 app.run(debug=True, port=8000)


