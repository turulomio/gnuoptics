## -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from Ui_ibmProveedores import *
from apoyo import *
import psycopg2,  psycopg2.extras

class ibmProveedores(QDialog, Ui_ibmProveedores):
    def __init__(self, cfg,  id_proveedores= None,  parent = None, name = None, modal = False):

            
        QDialog.__init__(self, parent)
        if name:
            self.setObjectName(name)
        self.setupUi(self)
        self.cfg=cfg
        self.reg=None
        self.id_proveedores=id_proveedores
        if self.id_proveedores!=None:
            self.lblTitulo.setText("Modificar proveedor")
            self.setWindowTitle("gnuOptics > Proveedores > Modificar")
            
            #consigue el registro de id_proveedores
            self.cfg.connect()
            cur = self.cfg.con.cursor()
            cur.execute("select * from proveedores where id_proveedores=%s", (id_proveedores, ))
            self.reg= cur.fetchone()
            cur.close()                 
            self.cfg.disconnect() 
            self.txtProveedor.setText(s2q(self.reg['proveedor']))
            self.txtCIF.setText(s2q(self.reg['cif']))
            self.txtTelefono.setText(s2q(self.reg['telefono']))
            self.txtEmail.setText(s2q(self.reg['email']))
            self.txtDireccion.setText(s2q(self.reg['direccion']))
            self.txtCiudad.setText(s2q(self.reg['ciudad']))
            self.txtCodigoPostal.setText(s2q(self.reg['codigopostal']))
            self.txtPais.setText(s2q(self.reg['pais']))

    @pyqtSignature("")
    def on_cmdYN_accepted(self):
            
        if self.id_proveedores==None: #insertar
            self.cfg.connect()
            cur = self.cfg.con.cursor()
            cur.execute("insert into proveedores(proveedor, cif, telefono, email, direccion, ciudad, codigopostal, pais) values ( %s, %s, %s, %s, %s, %s, %s, %s)", (q2s(self.txtProveedor.text()), q2s(self.txtCIF.text()), q2s(self.txtTelefono.text()), q2s(self.txtEmail.text()), q2s(self.txtDireccion.text()), q2s(self.txtCiudad.text()), q2s(self.txtCodigoPostal.text()), q2s(self.txtPais.text())))
            self.cfg.con.commit()
            cur.close()
            self.cfg.disconnect() 
            self.done(0)
        else: #modificar
            self.cfg.connect()
            cur = self.cfg.con.cursor()
            sql="update proveedores set proveedor=%s, cif=%s, telefono=%s, email=%s, direccion=%s, ciudad=%s, codigopostal=%s, pais=%s where id_proveedores=%s"
            data=(q2s(self.txtProveedor.text()), q2s(self.txtCIF.text()), q2s(self.txtTelefono.text()), q2s(self.txtEmail.text()), q2s(self.txtDireccion.text()), q2s(self.txtCiudad.text()), q2s(self.txtCodigoPostal.text()), q2s(self.txtPais.text()),  self.id_proveedores )
            cur.execute(sql, data )
            self.cfg.con.commit()
            cur.close()
            self.cfg.disconnect() 
            self.done(0)

    @pyqtSignature("")        
    def on_cmdYN_rejected(self):
        self.done(0)