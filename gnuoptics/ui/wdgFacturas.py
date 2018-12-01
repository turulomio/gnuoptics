## -*- coding: utf-8 -*-
import psycopg2,  psycopg2.extras

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from Ui_wdgFacturas import *
from apoyo import *
from ibmFacturas import *

class wdgFacturas(QWidget, Ui_wdgFacturas):
    def __init__(self,cfg,  parent=None):
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.cfg=cfg
        self.table.setColumnWidth(0, 100)
        self.table.setColumnWidth(1, 200)
        self.table.setColumnWidth(2, 400)
        self.selFactura=None


    def load_data(self):
        self.cfg.connect()
        cur = self.cfg.con.cursor()
        cur.execute("select facturas.id_facturas, hora, nombre, apellidos, pagado, facturas_venta(facturas.id_facturas) as venta, facturas_articulos(facturas.id_facturas) as articulos   from facturas, clientes where clientes.id_clientes=facturas.id_clientes order by hora;")

        
#        cur.execute("SELECT * FROM articulos, tipos, albaranes, proveedores where upper( tipo || ' ' || modelo) like upper('%"+str(self.txtBusqueda.text())+"%') and articulos.id_albaranes=albaranes.id_albaranes and tipos.id_tipos=articulos.id_tipos and proveedores.id_proveedores=albaranes.id_proveedores order by tipo, modelo, id_articulos;")
        self.table.setRowCount(cur.rowcount);
        for rec in cur:
            self.table.setItem(cur.rownumber-1, 0, QTableWidgetItem(str(rec['id_facturas'])))
            self.table.setItem(cur.rownumber-1, 1, QTableWidgetItem(str(rec['hora'])))
            self.table.setItem(cur.rownumber-1, 2, QTableWidgetItem(s2q(str(rec['nombre'])+" "+str(rec['apellidos']))))            
            self.table.setItem(cur.rownumber-1, 3, QTableWidgetItem(str(rec['articulos'])))
            self.table.setItem(cur.rownumber-1, 4, QTableWidgetItem(s2q(euros(rec['venta']))))
            self.table.setItem(cur.rownumber-1, 5, QTableWidgetItem(str(rec['pagado'])))
        cur.close()        
        self.cfg.disconnect() 
        self.lblTotal.setText(s2q(str(cur.rowcount) +" productos de Facturas"))


    @QtCore.pyqtSlot()  
    def on_actionFacturaClienteGenerico_activated(self):
        w=ibmFacturas(self.con,  0)
        w.showMaximized()
        w.exec_()
        self.load_data()
        
    @QtCore.pyqtSlot()  
    def on_actionFacturaModificar_activated(self):
        w=ibmFacturas(self.con, None,  self.selFactura)
        w.showMaximized()
        w.exec_()        
        self.load_data()

    def on_txtBusqueda_textChanged(self):
        if len(self.txtBusqueda.text())>0:
            print "Buscando Facturas " + self.txtBusqueda.text()
            self.load_data()
            
    def on_table_itemSelectionChanged(self):
        for i in self.table.selectedItems():#itera por cada item no row.
            self.selFactura=int(self.table.item(i.row(), 0).text())
        print "Seleccionado:",   self.selFactura

    def on_table_customContextMenuRequested(self,  pos):
        menu=QMenu()
        menu.addAction(self.actionFacturaClienteGenerico)
        menu.addAction(self.actionFacturaModificar)
        menu.addAction(self.actionFacturaBorrar)

        if self.selFactura==None:
            self.actionFacturaBorrar.setEnabled(False)
            self.actionFacturaModificar.setEnabled(False)
        else:
            self.actionFacturaBorrar.setEnabled(True)
            self.actionFacturaModificar.setEnabled(True)
            
        
        menu.exec_(self.table.mapToGlobal(pos))

        
