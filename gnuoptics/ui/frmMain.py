## -*- coding: utf-8 -*-
import sys,  psycopg2,  psycopg2.extras
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from Ui_frmMain import *
from frmAbout import *
from frmAccess import *
from wdgProveedores import *
from wdgCaja import *
from wdgClientes import *
from wdgFacturas import *
from wdgInventario import *
from frmTablasAuxiliares import *
from config import *
from errores import *

class frmMain(QMainWindow, Ui_frmMain):#    
    def __init__(self, parent = 0,  flags = False):
        """
        Constructor
        
        @param parent The parent widget of this dialog. (QWidget)
        @param name The name of this dialog. (QString)
        @param modal Flag indicating a modal dialog. (boolean)
        """
        QMainWindow.__init__(self, None)
        self.setupUi(self)
        self.showMaximized()
        self.cfg=config()
        
        self.w=QWidget()       
        self.w.setAttribute(Qt.WA_DeleteOnClose) 
        
        access=frmAccess(self)
        QObject.connect(access.cmdYN, SIGNAL("rejected()"), self, SLOT("on_actionSalir_activated()"))
        access.exec_()
        self.cfg.db=q2s(access.txtDB.text())
        self.cfg.port=q2s(access.txtPort.text())
        self.cfg.pg_user=q2s(access.txtUser.text()) 
        self.cfg.contry=q2s(access.txtPass.text()) 
        self.cfg.server=q2s(access.txtServer.text()) 
        
        self.cfg.connect()
        cur = self.cfg.con.cursor()
        try:
            cur.execute("SELECT * FROM  usuarios where pg_user=%s", (self.cfg.pg_user, ))
        except psycopg2.Error,  e:
            Errores.psycopg(e)
            return            
        for rec in cur:
            self.cfg.id_usuarios=rec['id_usuarios']
            self.cfg.usuario=rec['usuario']
            self.cfg.administrador=rec['administrador']
            self.cfg.comercial=rec['comercial']
            self.cfg.gerente=rec['gerente']
            self.cfg.consejoadministracion=rec['consejoadministracion']
        cur.close()        
        self.cfg.disconnect()         
        
        #Acceso a actionTablasAuxiliares
        self.actionTablasAuxiliares.setEnabled( False)
        if self.cfg.gerente==True:
            self.actionTablasAuxiliares.setEnabled( True)

        
    @pyqtSignature("")
    def on_actionAcercaDe_activated(self):
        fr=frmAbout(self, "frmabout")
        fr.open()
    
    @QtCore.pyqtSlot()      
    def on_actionSalir_activated(self):
        sys.exit()

    @QtCore.pyqtSlot()  
    def on_actionCaja_activated(self):
        self.w.close()
        self.w=wdgCaja(self.cfg)
        self.w.setAttribute(Qt.WA_DeleteOnClose)         
        self.layout.addWidget(self.w)
        self.w.show()
            
    @QtCore.pyqtSlot()  
    def on_actionClientes_activated(self):
        self.w.close()
        self.w=wdgClientes(self.cfg)
        self.w.setAttribute(Qt.WA_DeleteOnClose)         
        self.w.load_data_clientes()
        self.layout.addWidget(self.w)
        self.w.show()
        
    @QtCore.pyqtSlot()  
    def on_actionFacturas_activated(self):
        self.w.close()
        self.w=wdgFacturas(self.cfg)
        self.w.setAttribute(Qt.WA_DeleteOnClose)         
        self.w.load_data()
        self.layout.addWidget(self.w)
        self.w.show()
                
    @QtCore.pyqtSlot()  
    def on_actionInventario_activated(self):
        self.w.close()
        self.w=wdgInventario(self.cfg)
        self.w.setAttribute(Qt.WA_DeleteOnClose)         
        self.w.load_data()
        self.layout.addWidget(self.w)
        self.w.show()
        
    @QtCore.pyqtSlot()  
    def on_actionProveedores_activated(self):
        self.w.close()
        self.w=wdgProveedores(self.cfg)
        self.w.setAttribute(Qt.WA_DeleteOnClose)       
        self.w.load_data_proveedores()
        self.layout.addWidget(self.w)
        self.w.show()
                
    @QtCore.pyqtSlot()  
    def on_actionTablasAuxiliares_activated(self):
        w=frmTablasAuxiliares(self.cfg)
        w.tblTipos_reload()
        w.exec_()
        
    def closeEvent(self,  event):
        self.on_actionSalir_activated()
