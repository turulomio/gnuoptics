## -*- coding: utf-8 -*-
import   psycopg2,  psycopg2.extras
from errores import *
class config():
    def __init__(self):
        self.con=None
        self.id_usuarios=None
        self.usuario=None
        self.administrador=False
        self.comercial=False
        self.gerente=False
        self.consejoadministracion=False
        self.contry=None
        self.con=None
        self.db=None
        self.port=None
        self.strcon=None
        
##    @staticmethod
    def connect(self):        
        strcon="dbname='%s' port='%s' user='%s' host='%s' password='%s'" % (self.db,  self.port, self.pg_user, self.server,  self.contry)
        try:
            self.con=psycopg2.extras.DictConnection(strcon)
        except psycopg2.Error,  e:
            Errores.database(e)
        
    def disconnect(self):
        self.con.close()
#        print "La conexion tiene valor",  self.con
