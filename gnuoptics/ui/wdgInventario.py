## -*- coding: utf-8 -*-
import psycopg2,  psycopg2.extras

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from Ui_wdgInventario import *
from apoyo import *

class wdgInventario(QWidget, Ui_wdgInventario):
    def __init__(self, cfg,  parent=None):
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.cfg=cfg
        self.table.setColumnWidth(0, 300)
        self.table.setColumnWidth(1, 450)
        self.table.setColumnWidth(2, 100)
        self.table.setColumnWidth(3, 100)
        self.table.verticalHeader().hide()
        self.table.setAlternatingRowColors(True)


    def load_data(self):
        self.cfg.connect()
        cur = self.cfg.con.cursor()
        cur.execute("select tipo, modelo, count(modelo) as count , round(sum(compra)::numeric,2) as total from articulos, tipos where tipos.id_tipos=articulos.id_tipos and articulos.id_facturas is null group by tipo, modelo order by tipo, modelo;")

        
#        cur.execute("SELECT * FROM articulos, tipos, albaranes, proveedores where upper( tipo || ' ' || modelo) like upper('%"+str(self.txtBusqueda.text())+"%') and articulos.id_albaranes=albaranes.id_albaranes and tipos.id_tipos=articulos.id_tipos and proveedores.id_proveedores=albaranes.id_proveedores order by tipo, modelo, id_articulos;")
        self.table.setRowCount(cur.rowcount);
        for rec in cur:
            self.table.setItem(cur.rownumber-1, 0, QTableWidgetItem(s2q(rec['tipo'])))
            self.table.setItem(cur.rownumber-1, 1, QTableWidgetItem(s2q(rec['modelo'])))
            self.table.setItem(cur.rownumber-1, 2, QTableWidgetItem(str(rec['count'])))
            self.table.setItem(cur.rownumber-1, 3, QTableWidgetItem(s2q(euros(rec['total']))))
        cur.close()        
        self.cfg.disconnect() 
        self.lblTotal.setText(s2q(str(cur.rowcount) +" productos de inventario"))
        
    def on_txtBusqueda_textChanged(self):
        if len(self.txtBusqueda.text())>0:
            print "Buscando Inventario " + self.txtBusqueda.text()
            self.load_data()
            
            

    def on_tblAlbaranes_customContextMenuRequested(self,  pos):
        menu=QMenu()
        menu.addAction(self.actionSoloAlbaranes)
        menu.addAction(self.actionFiltrarInventariados)
        menu.exec_(self.tblAlbaranes.mapToGlobal(pos))
