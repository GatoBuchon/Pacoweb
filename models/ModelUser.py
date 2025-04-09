from .entities.user import User

class ModuleUser():
    @classmethod
    def login(self, db, user):
        try:
            cur=db.connection.cursor()
            sql="SELECT idUsuario, Nombre, Password FROM usuario WHERE Nombre='{}'".format(user.username)
            cur.execute(sql)
            row=cur.fetchone()
            if row != None:
                user=User(row[0],row[1],user.check_password(row[2],user.password),None)
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_by_id(self, db, idusuario):
        try:
            cur=db.connection.cursor()
            sql="SELECT idUsuario, Nombre, TipoUsuario FROM usuario WHERE idUsuario='{}'".format(idusuario)
            cur.execute(sql)
            row=cur.fetchone()
            if row != None:
                return User(row[0], row[1], None, row[2])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)