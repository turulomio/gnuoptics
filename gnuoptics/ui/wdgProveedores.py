## -*- coding: utf-8 -*-
import psycopg2,  psycopg2.extras

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from Ui_wdgProveedores import *
from ibmProveedores import *
from ibmAlbaranes import *

class wdgProveedores(QWidget, Ui_wdgProveedores):
    def __init__(self, cfg,  parent=None):
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.cfg=cfg
        self.selProveedor=None
        self.selAlbaran=None
        
        self.tblProveedores.setColumnWidth(0, 100)
        self.tblProveedores.setColumnWidth(1, 300)
        self.tblProveedores.setColumnWidth(2, 100)
        self.tblProveedores.setColumnWidth(3, 100)
        self.tblProveedores.setColumnWidth(4, 200)
        self.tblProveedores.setColumnWidth(5, 300)
        self.tblProveedores.setColumnWidth(6, 150)
        self.tblProveedores.setColumnWidth(7, 100)
        self.tblProveedores.setColumnWidth(8, 100)
        self.tblProveedores.verticalHeader().hide()
        self.tblProveedores.setAlternatingRowColors(True)
        self.tblProveedores.setContextMenuPolicy(Qt.CustomContextMenu);

         
        self.tblAlbaranes.setColumnWidth(0, 100)
        self.tblAlbaranes.setColumnWidth(1, 100)
        self.tblAlbaranes.setColumnWidth(2, 300)
        self.tblAlbaranes.setColumnWidth(3, 100)
        self.tblAlbaranes.setColumnWidth(4, 150)
        self.tblAlbaranes.setColumnWidth(5, 100)
        self.tblAlbaranes.setContextMenuPolicy(Qt.CustomContextMenu);
        self.tblAlbaranes.verticalHeader().hide()
        self.tblAlbaranes.setAlternatingRowColors(True)

    def load_data_proveedores(self):
        self.cfg.connect()
        cur = self.cfg.con.cursor()
        cur.execute("SELECT * FROM proveedores where upper(proveedor) like upper('%"+str(self.txtBusqueda.text())+"%') or upper(cif) like upper('%"+str(self.txtBusqueda.text())+"%') order by proveedor;")
        self.tblProveedores.setRowCount(cur.rowcount);
        for rec in cur:
            self.tblProveedores.setItem(cur.rownumber-1, 0,QTableWidgetItem(str(rec['id_proveedores'])) )
            self.tblProveedores.setItem(cur.rownumber-1, 1, QTableWidgetItem(s2q(rec['proveedor'])))
            self.tblProveedores.setItem(cur.rownumber-1, 2, QTableWidgetItem(s2q(rec['cif'])))
            self.tblProveedores.setItem(cur.rownumber-1, 3, QTableWidgetItem(s2q(rec['telefono'])))
            self.tblProveedores.setItem(cur.rownumber-1, 4, QTableWidgetItem(s2q(rec['email'])))
            self.tblProveedores.setItem(cur.rownumber-1, 5, QTableWidgetItem(s2q(rec['direccion'])))
            self.tblProveedores.setItem(cur.rownumber-1, 6, QTableWidgetItem(s2q(rec['ciudad'])))
            self.tblProveedores.setItem(cur.rownumber-1, 7, QTableWidgetItem(s2q(rec['codigopostal'])))
            self.tblProveedores.setItem(cur.rownumber-1, 8, QTableWidgetItem(s2q(rec['pais'])))
        cur.close()        
        self.cfg.disconnect() 
        
    def load_data_albaranes(self, id_proveedores):
        self.cfg.connect()
        cur = self.cfg.con.cursor()
        cur.execute("SELECT id_albaranes, fecha, proveedor, albaranes_articulos(albaranes.id_albaranes) as articulos, albaranes_compra(albaranes.id_albaranes) as compra, inventariado FROM albaranes,proveedores where albaranes.id_proveedores="+str(id_proveedores)+" and albaranes.id_proveedores=proveedores.id_proveedores order by fecha;")
        self.tblAlbaranes.setRowCount(cur.rowcount);
        for rec in cur:
            self.tblAlbaranes.setItem(cur.rownumber-1, 0,QTableWidgetItem(str(rec['id_albaranes'])) )
            self.tblAlbaranes.setItem(cur.rownumber-1, 1, QTableWidgetItem(str(rec['fecha'])))
            self.tblAlbaranes.setItem(cur.rownumber-1, 2, QTableWidgetItem(s2q(rec['proveedor'])))
            self.tblAlbaranes.setItem(cur.rownumber-1, 3, QTableWidgetItem(str(rec['articulos'])))
            self.tblAlbaranes.setItem(cur.rownumber-1, 4, QTableWidgetItem(s2q(euros(rec['compra']))))
            self.tblAlbaranes.setItem(cur.rownumber-1, 5, QTableWidgetItem(str(rec['inventariado'])))
        cur.close()       
        self.cfg.disconnect()  

    @QtCore.pyqtSlot()  
    def on_actionAlbaranBorrar_activated(self):
        id_proveedores= int(self.tblProveedores.item(self.tblProveedores.currentRow(), 0).text())
        id_albaranes= int(self.tblAlbaranes.item(self.tblAlbaranes.currentRow(), 0).text())
        self.cfg.connect()
        cur = self.cfg.con.cursor()
        cur.execute("delete from albaranes where id_albaranes=%s", (id_albaranes, ))
        self.cfg.con.commit()
        cur.close()     
        self.cfg.disconnect() 
        self.load_data_albaranes(id_proveedores)

    @QtCore.pyqtSlot()  
    def on_actionAlbaranNuevo_activated(self):
        if self.tblProveedores.item(self.tblProveedores.currentRow(), 0)!=None:
            id_proveedores= int(self.tblProveedores.item(self.tblProveedores.currentRow(), 0).text())
            i=ibmAlbaranes(self.cfg,  id_proveedores)
        else:
#            m=QMessageBox()
#            m.setText("Debe seleccionar un proveedor")
#            m.exec_();            
#            return
            i=ibmAlbaranes(self.con)
        i.setModal(True)
        i.exec_()
        self.load_data_albaranes(id_proveedores)

    @QtCore.pyqtSlot()  
    def on_actionAlbaranModificar_activated(self):
        i=ibmAlbaranes(self.cfg, self.selProveedor,  self.selAlbaran)
        i.setModal(True)
        i.exec_()        
        self.load_data_albaranes(self.selProveedor)


    @QtCore.pyqtSlot()  
    def on_actionProveedorBorrar_activated(self):
        id_proveedores= int(self.tblProveedores.item(self.tblProveedores.currentRow(), 0).text())
        self.cfg.connect()
        cur = self.cfg.con.cursor()
        cur.execute("delete from proveedores where proveedores.id_proveedores=%s", (id_proveedores, ))
        self.cfg.con.commit()
        cur.close()     
        self.cfg.disconnect() 
        self.load_data_proveedores()

    @QtCore.pyqtSlot()  
    def on_actionProveedorNuevo_activated(self):
        i=ibmProveedores(self.cfg)
        i.setModal(True)
        i.exec_()
        self.load_data_proveedores()

    @QtCore.pyqtSlot()  
    def on_actionProveedorModificar_activated(self):
        id_proveedores= int(self.tblProveedores.item(self.tblProveedores.currentRow(), 0).text())
        print "Proveedor a modificar:",  id_proveedores
        i=ibmProveedores(self.cfg, id_proveedores)
        i.setModal(True)
        i.exec_()
        self.load_data_proveedores()

    def on_txtBusqueda_textChanged(self):
#        if len(self.txtBusqueda.text())>0:
        print "Buscando proveedores " + self.txtBusqueda.text()
        self.load_data_proveedores()


    def on_tblAlbaranes_itemSelectionChanged(self):
        for i in self.tblAlbaranes.selectedItems():#itera por cada item no row.
            self.selAlbaran=int(self.tblAlbaranes.item(i.row(), 0).text())
        print "Seleccionado:",  self.selProveedor,  self.selAlbaran

    def on_tblAlbaranes_customContextMenuRequested(self,  pos):

        if self.selAlbaran==None:
            self.actionAlbaranBorrar.setEnabled(False)
            self.actionAlbaranModificar.setEnabled(False)
        else:
            self.actionAlbaranBorrar.setEnabled(True)
            self.actionAlbaranModificar.setEnabled(True)

        menu=QMenu()
        menu.addAction(self.actionAlbaranNuevo)
        menu.addAction(self.actionAlbaranBorrar)
        menu.addAction(self.actionAlbaranModificar)
        menu.addSeparator()
        menu.addAction(self.actionSoloAlbaranes)
        menu.addAction(self.actionFiltrarInventariados)
        menu.exec_(self.tblAlbaranes.mapToGlobal(pos))

#            
#        if self.selAlbaran==None:
#            self.actionFacturaBorrar.setEnabled(False)
#            self.actionFacturaModificar.setEnabled(False)
#        else:
#            self.actionFacturaBorrar.setEnabled(True)
#            self.actionFacturaModificar.setEnabled(True)
#            
        



    def on_tblProveedores_customContextMenuRequested(self,  pos):        
        print "Seleccionado:",  self.selProveedor,  self.selAlbaran
        if self.selProveedor==None:
            self.actionProveedorBorrar.setEnabled(False)
            self.actionProveedorModificar.setEnabled(False)
        else:
            self.actionProveedorBorrar.setEnabled(True)
            self.actionProveedorModificar.setEnabled(True)
        menu=QMenu()
        menu.addAction(self.actionProveedorNuevo)
        menu.addAction(self.actionProveedorModificar)
        menu.addAction(self.actionProveedorBorrar)
        menu.exec_(self.tblProveedores.mapToGlobal(pos))




    def on_tblProveedores_itemSelectionChanged(self):
        for i in self.tblProveedores.selectedItems():#itera por cada item no row.
            self.selProveedor=int(self.tblProveedores.item(i.row(), 0).text())
        self.load_data_albaranes(self.selProveedor)        
        self.tblAlbaranes.clearSelection()
        self.selAlbaran=None
        print "Seleccionado:",  self.selProveedor,  self.selAlbaran