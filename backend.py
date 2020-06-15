from flask import Flask, request, Response
from flask import json

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


Base = declarative_base()

class ToJson():
    def to_json(self):
        return json.dumps({col.name: getattr(self, col.name) for col in self.__table__.columns })


class Producto(Base, ToJson):                   # public class Departamento extends Base {  }
    __tablename__ = 'productos'
    id = Column(Integer, primary_key=True)
    precio = Column(float)
    nombre = Column(String)

class ProductoVendido(Base, ToJson):                   # public class Departamento extends Base {  }
    __tablename__ = 'productosVendidos'
    id = Column(Integer, primary_key=True)
    id_producto = Column(Integer, ForeignKey('productos.id'))
    id_cliente = Column(Integer, ForeignKey('clientes.id'))
    precio = Column(float)
    cantidad = Column(Integer)
    producto = relationship(
        Producto,
        backref=backref('productos', uselist=True, cascade='delete,all')
    )
    cliente = relationship(
        Cliente,
        backref=backref('clientes', uselist=True, cascade='delete,all')
    )



class Cliente(Base, ToJson):
    __tablename__ = 'clientes'
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    apellido = Column(String)
    

engine = create_engine('sqlite:///base_servido2.sqlite')

session = sessionmaker()
session.configure(bind=engine)

app = Flask(__name__) 

@app.route('/crearbase')
def crear_base():
    Base.metadata.create_all(engine)
    return 'Ok'


@app.route('/compra', methods=['POST'])
def create_departamento():

    if request.is_json:

        req = request.get_json()
        nombreCliente = req.get("nombreCliente")
        productos = req.get("productos")

        cliente = Cliente(nombre=nombreCliente) 

        s = session()
        s.add(cliente)
        s.commit()

        # recorrer lista de productos y guardarlos en productos vendidos
    else
        return Response("{'mensaje_error':'El formato del body no es correcto'}", status=400, mimetype='application/json')



    return Response(status=201, mimetype='application/json')


if __name__ == '__main__':
    app.run(port=9001)
