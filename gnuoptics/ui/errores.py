## -*- coding: utf-8 -*-
import   psycopg2,  psycopg2.extras,  sys
from PyQt4.QtGui import *
from apoyo import *

class Errores():        
    @staticmethod
    def database(e):        
        m=QMessageBox()
        print e
        m.setText(s2q(str(e) + "\nVuelva a entrar al programa"))
        m.exec_()
        sys.exit(255)
        
    @staticmethod
    def psycopg(e):        
        m=QMessageBox()
        print e
        m.setText(s2q(e.pgerror))
        m.exec_()        
        
    @staticmethod
    def permisos(e):        
        m=QMessageBox()
        m.setText("No tiene suficientes permisos. Consulte con el gerente")
        m.exec_()        
