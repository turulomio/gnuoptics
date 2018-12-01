## -*- coding: utf-8 -*-

import psycopg2,  psycopg2.extras
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from Ui_wdgClientes import *
from ibmFacturas import *
from ibmClientes import *

class wdgClientes(QWidget, Ui_wdgClientes):
    def __init__(self, cfg,  parent=None):
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.cfg=cfg
        self.tblClientes.setColumnWidth(0, 100)
        self.tblClientes.setColumnWidth(1, 200)
        self.tblClientes.setColumnWidth(2, 300)
        self.tblClientes.setColumnWidth(3, 100)
        self.tblClientes.setColumnWidth(4, 100)
        self.tblClientes.setColumnWidth(5, 200)
        self.tblClientes.setColumnWidth(6, 300)
        self.tblClientes.setColumnWidth(7, 150)
        self.tblClientes.setColumnWidth(8, 100)
        self.tblClientes.setColumnWidth(9, 100)
        self.tblClientes.verticalHeader().hide()
        self.tblClientes.setAlternatingRowColors(True)
        
        self.tblFacturas.setColumnWidth(0, 100)
        self.tblFacturas.setColumnWidth(1, 200)
        self.tblFacturas.setColumnWidth(2, 400)
        self.tblFacturas.setColumnWidth(3, 100)
        self.tblFacturas.setColumnWidth(4, 100)
        self.tblFacturas.setColumnWidth(5, 100)
        self.tblFacturas.verticalHeader().hide()
        self.tblFacturas.setAlternatingRowColors(True)
        self.selCliente=None
        self.selFactura=None



    def load_data_clientes(self):
        self.cfg.connect()
        cur = self.cfg.con.cursor()
        cur.execute("select * from clientes where (upper(nombre) like upper('%"+q2s(self.txtBusqueda.text())+"%') or upper(apellidos) like upper('%"+q2s(self.txtBusqueda.text())+"%') or upper(nif) like upper('%"+q2s(self.txtBusqueda.text())+"%')) and id_clientes >0 order by nombre, apellidos, nif")
        self.tblClientes.setRowCount(cur.rowcount);
        for rec in cur:
            self.tblClientes.setItem(cur.rownumber-1, 0,QTableWidgetItem(str(rec['id_clientes'])) )
            self.tblClientes.setItem(cur.rownumber-1, 1, QTableWidgetItem(s2q(rec['nombre'])))
            self.tblClientes.setItem(cur.rownumber-1, 2, QTableWidgetItem(s2q(rec['apellidos'])))
            self.tblClientes.setItem(cur.rownumber-1, 3, QTableWidgetItem(s2q(rec['nif'])))
            self.tblClientes.setItem(cur.rownumber-1, 4, QTableWidgetItem(s2q(rec['telefono'])))
            self.tblClientes.setItem(cur.rownumber-1, 5, QTableWidgetItem(s2q(rec['email'])))
            self.tblClientes.setItem(cur.rownumber-1, 6, QTableWidgetItem(s2q(rec['direccion'])))
            self.tblClientes.setItem(cur.rownumber-1, 7, QTableWidgetItem(s2q(rec['ciudad'])))
            self.tblClientes.setItem(cur.rownumber-1, 8, QTableWidgetItem(s2q(rec['codigopostal'])))
            self.tblClientes.setItem(cur.rownumber-1, 9, QTableWidgetItem(s2q(rec['pais'])))
        cur.close()        
        self.cfg.disconnect()
        
    def load_data_facturas(self, id_clientes):
        self.cfg.connect()
        cur = self.cfg.con.cursor()
        cur.execute("SELECT facturas.id_facturas, hora, nombre, apellidos, pagado, facturas_venta(facturas.id_facturas) as coste, facturas_articulos(facturas.id_facturas) as articulos FROM facturas, clientes where facturas.id_clientes=clientes.id_clientes and clientes.id_clientes="+str(id_clientes)+" order by hora;")
        self.tblFacturas.setRowCount(cur.rowcount);
        for rec in cur:
            self.tblFacturas.setItem(cur.rownumber-1, 0,QTableWidgetItem(str(rec['id_facturas'])) )
            self.tblFacturas.setItem(cur.rownumber-1, 1, QTableWidgetItem(str(rec['hora'])))
            self.tblFacturas.setItem(cur.rownumber-1, 2, QTableWidgetItem(s2q(str(rec['nombre'])+" "+str(rec['apellidos']))))
            self.tblFacturas.setItem(cur.rownumber-1, 3, QTableWidgetItem(str(rec['articulos'])))
            self.tblFacturas.setItem(cur.rownumber-1, 4, QTableWidgetItem(s2q(euros(rec['coste']))))
            self.tblFacturas.setItem(cur.rownumber-1, 5, QTableWidgetItem(str(rec['pagado'])))
        cur.close()       
        self.cfg.disconnect()
        
    @QtCore.pyqtSlot()  
    def on_actionClienteBorrar_activated(self):
        self.cfg.connect()
        cur = self.cfg.con.cursor()
        cur.execute("delete from clientes where id_clientes=%s", (self.selCliente, ))
        self.cfg.con.commit()
        cur.close()     
        self.cfg.disconnect() 
        self.load_data_clientes()
        self.tblClientes.clearSelection()

    @QtCore.pyqtSlot()  
    def on_actionClienteNuevo_activated(self):
        i=ibmClientes(self.cfg,  None)
        i.exec_()
        self.load_data_clientes()

    @QtCore.pyqtSlot()  
    def on_actionClienteModificar_activated(self):
        i=ibmClientes(self.cfg, self.selCliente)
        i.exec_()        
        self.load_data_clientes()

    @QtCore.pyqtSlot()  
    def on_actionFacturaCliente_activated(self):
        w=ibmFacturas(self.cfg,  self.selCliente)
        w.showMaximized()
        w.exec_()
        self.load_data_facturas(self.selCliente)        
                
    @QtCore.pyqtSlot()  
    def on_actionFacturaClienteGenerico_activated(self):
        w=ibmFacturas(self.cfg,  0)
        w.showMaximized()
        w.exec_()
        self.load_data_facturas(self.selCliente)        
        
    @QtCore.pyqtSlot()  
    def on_actionFacturaModificar_activated(self):
        w=ibmFacturas(self.cfg, None,  self.selFactura)
        w.showMaximized()
        w.exec_()        
        self.load_data_facturas(self.selCliente)        
        
    def on_txtBusqueda_textChanged(self):
#        if len(self.txtBusqueda.text())>0:
        print "Buscando clientes " + self.txtBusqueda.text()
        self.load_data_clientes()
            

    def on_tblClientes_customContextMenuRequested(self,  pos):
        menu=QMenu()
        menu.addAction(self.actionClienteNuevo)
        menu.addAction(self.actionClienteModificar)
        menu.addAction(self.actionClienteBorrar)
           
        if self.selCliente==None:
            self.actionClienteBorrar.setEnabled(False)
            self.actionClienteModificar.setEnabled(False)
        else:
            self.actionClienteBorrar.setEnabled(True)
            self.actionClienteModificar.setEnabled(True)

        menu.exec_(self.tblClientes.mapToGlobal(pos))



    def on_tblClientes_itemSelectionChanged(self):
        for i in self.tblClientes.selectedItems():#itera por cada item no row.
            self.selCliente=int(self.tblClientes.item(i.row(), 0).text())
        self.load_data_facturas(self.selCliente)        
        self.tblFacturas.clearSelection()
        self.selFactura=None
        print "Seleccionado:",  self.selCliente,  self.selFactura

    def on_tblFacturas_itemSelectionChanged(self):
        for i in self.tblFacturas.selectedItems():#itera por cada item no row.
            self.selFactura=int(self.tblFacturas.item(i.row(), 0).text())
        print "Seleccionado:",  self.selCliente,  self.selFactura

    def on_tblFacturas_customContextMenuRequested(self,  pos):
        menu=QMenu()
        menu.addAction(self.actionFacturaCliente)
        menu.addAction(self.actionFacturaClienteGenerico)
        menu.addAction(self.actionFacturaModificar)
        menu.addAction(self.actionFacturaBorrar)
        
        if self.selCliente==None:
            self.actionFacturaCliente.setEnabled(False)
        else:
            self.actionFacturaCliente.setEnabled(True)
            
        if self.selFactura==None:
            self.actionFacturaBorrar.setEnabled(False)
            self.actionFacturaModificar.setEnabled(False)
        else:
            self.actionFacturaBorrar.setEnabled(True)
            self.actionFacturaModificar.setEnabled(True)
            
        
        menu.exec_(self.tblFacturas.mapToGlobal(pos))
