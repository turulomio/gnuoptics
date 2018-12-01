## -*- coding: utf-8 -*-
import psycopg2,  psycopg2.extras

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from Ui_ibmClientes import *
from apoyo import *

class ibmClientes(QDialog,  Ui_ibmClientes):
    def __init__(self, cfg, id_clientes=None,   parent=None):
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.cfg=cfg
        self.reg=None
        self.id_clientes=id_clientes
        if self.id_clientes!=None:
            self.lblTitulo.setText("Modificar cliente")
            self.setWindowTitle("gnuOptics > Clientes > Modificar")
            
            #consigue el registro de id_clientes
            self.cfg.connect()
            cur = self.cfg.con.cursor()
            cur.execute("select * from clientes where id_clientes=%s", (id_clientes, ))
            self.reg= cur.fetchone()
            cur.close()                 
            self.cfg.disconnect() 
            self.txtNombre.setText(s2q(self.reg['nombre']))
            self.txtApellidos.setText(s2q(self.reg['apellidos']))
            self.txtNIF.setText(s2q(self.reg['nif']))
            self.txtTelefono.setText(s2q(self.reg['telefono']))
            self.txtEmail.setText(s2q(self.reg['email']))
            self.txtDireccion.setText(s2q(self.reg['direccion']))
            self.txtCiudad.setText(s2q(self.reg['ciudad']))
            self.txtCodigoPostal.setText(s2q(self.reg['codigopostal']))
            self.txtPais.setText(s2q(self.reg['pais']))

    @pyqtSignature("")
    def on_cmdYN_accepted(self):            
        self.cfg.connect()
        cur = self.cfg.con.cursor()
        if self.id_clientes==None: #insertar
            cur.execute("insert into clientes(nombre, apellidos, nif, telefono, email, direccion, ciudad, codigopostal, pais) values ( %s, %s,  %s, %s, %s, %s, %s, %s, %s)", (q2s(self.txtNombre.text()), q2s(self.txtApellidos.text()), q2s(self.txtNIF.text()), q2s(self.txtTelefono.text()), q2s(self.txtEmail.text()), q2s(self.txtDireccion.text()), q2s(self.txtCiudad.text()), q2s(self.txtCodigoPostal.text()), q2s(self.txtPais.text())))
        else: #modificar
            sql="update clientes set nombre=%s, apellidos=%s, nif=%s, telefono=%s, email=%s, direccion=%s, ciudad=%s, codigopostal=%s, pais=%s where id_clientes=%s"
            data=(q2s(self.txtNombre.text()), q2s(self.txtApellidos.text()),  q2s(self.txtNIF.text()), q2s(self.txtTelefono.text()), q2s(self.txtEmail.text()), q2s(self.txtDireccion.text()), q2s(self.txtCiudad.text()), q2s(self.txtCodigoPostal.text()), q2s(self.txtPais.text()),  self.id_clientes )
            cur.execute(sql, data )
        self.cfg.con.commit()
        cur.close()
        self.cfg.disconnect() 
        self.done(0)

    @pyqtSignature("")        
    def on_cmdYN_rejected(self):
        self.done(0)
