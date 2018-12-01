## -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
def q2s(q):
    """Qstring to python string en utf8"""
    return str(QString.toUtf8(q))
    
def s2q(st):
    """utf8 python string to qstring"""
    if st==None:
        return QString("")
    else:
        return QString(st.decode("UTF8"))

def c2b(state):
    """QCheckstate to python bool"""
    if state==Qt.Checked:
        return True
    else:
        return False

def b2c(booleano):
    """QCheckstate to python bool"""
    if booleano==True:
        return Qt.Checked
    else:
        return Qt.Unchecked     
        
def d2s(date):
    """Qdate to python string"""
    return str(date.toString(Qt.ISODate))
    
def s2d(s):
    """python string isodate 2 qdate"""
    a=str(s).split("-")
    return QDate(int(a[0]), int(a[1]),  int(a[2]))

def euros(n):
    return str(n) +" €"
    
def qtablewidgetitemeuros2float(item):
    """Convierte un QStrring con una cadena de euros a float."""
    if item == None:
        return 0.0
    str=q2s(item.text())
    if str==None or str=="":
        return 0.0
    else:
        return float(str[:-3]) #Es 3 por el utf8
    
