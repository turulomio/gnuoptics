## -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from apoyo import *
import sys
import psycopg2,  psycopg2.extras
from Ui_frmTablasAuxiliares import *

class frmTablasAuxiliares(QDialog, Ui_frmTablasAuxiliares):
    def __init__(self, cfg,  parent = None, name = None, modal = False):
        """
        Constructor
        
        @param parent The parent widget of this dialog. (QWidget)
        @param name The name of this dialog. (QString)
        @param modal Flag indicating a modal dialog. (boolean)
        """
        QDialog.__init__(self,  parent)
        if name:
            self.setObjectName(name)
        self.setModal(True)
        self.setupUi(self)

        self.cfg=cfg

        self.tblTipos.setContextMenuPolicy(Qt.CustomContextMenu);
        self.tblTipos.setAlternatingRowColors(True)
        
    @QtCore.pyqtSlot()  
    def on_actionTiposBorrar_activated(self):
        id_tipos= int(self.tblTipos.item(self.tblTipos.currentRow(), 0).text())
        self.cfg.connect()
        cur = self.cfg.con.cursor()
        cur.execute("delete from tipos where id_tipos=%s", (id_tipos, ))
        self.cfg.con.commit()
        cur.close()     
        self.cfg.disconnect()
        self.tblTipos_reload()

    @QtCore.pyqtSlot()  
    def on_actionTiposNuevo_activated(self):
        tipo=QInputDialog().getText(self,  "gnuOptics > Tablas auxiliares > Nuevo tipo",  "Introduce un nuevo tipo")
        self.cfg.connect()
        cur = self.cfg.con.cursor()
        cur.execute("insert into tipos(tipo) values (%s);", (q2s(QString(tipo[0])), ))
        self.cfg.con.commit()
        cur.close()     
        self.cfg.disconnect()
        self.tblTipos_reload()


    @QtCore.pyqtSlot()  
    def on_actionTiposModificar_activated(self):
        id_tipos= int(self.tblTipos.item(self.tblTipos.currentRow(), 0).text())
        self.cfg.connect()
        cur = self.cfg.con.cursor()
        cur.execute("select * from tipos where id_tipos=%s", (id_tipos, ))
        reg= cur.fetchone()
        cur.close()               
        
        tipo=QInputDialog().getText(self,  "gnuOptics > Tablas auxiliares > Modificar tipo",  "Modifica el tipo", QLineEdit.Normal,   s2q(reg['tipo']))        
        
        cur = self.cfg.con.cursor()
        cur.execute("update tipos set tipo= %s where id_tipos= %s", (q2s(tipo[0]),  id_tipos ))
        self.cfg.con.commit()
        cur.close()     
        self.cfg.disconnect()
        self.tblTipos_reload()
        
    def on_tblTipos_customContextMenuRequested(self,  pos):
        menu=QMenu()
        menu.addAction(self.actionTiposNuevo)
        menu.addAction(self.actionTiposModificar)
        menu.addAction(self.actionTiposBorrar)
        menu.exec_(self.tblTipos.mapToGlobal(pos))

    def tblTipos_reload(self):
        self.cfg.connect()
        cur = self.cfg.con.cursor()
        cur.execute("SELECT * FROM tipos order by tipo;")
        self.tblTipos.setRowCount(cur.rowcount);
        for rec in cur:
            self.tblTipos.setItem(cur.rownumber-1, 0,QTableWidgetItem(str(rec['id_tipos'])) )
            self.tblTipos.setItem(cur.rownumber-1, 1, QTableWidgetItem(s2q(rec['tipo'])))
        cur.close()      
        self.cfg.disconnect()  
        
        
        