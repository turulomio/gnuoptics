## -*- coding: utf-8 -*-

import psycopg2,  psycopg2.extras
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from apoyo import *
from Ui_wdgCaja import *

class wdgCaja(QWidget, Ui_wdgCaja):
    def __init__(self, cfg,  parent=None):
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.cfg=cfg
        self.tblAnual.setColumnWidth(0, 150)
        self.tblAnual.setColumnWidth(1, 400)
        self.tblAnual.setColumnWidth(2, 150)


        self.tblArticulos.setColumnWidth(0, 100)
        self.tblArticulos.setColumnWidth(1, 400)
        self.tblArticulos.setColumnWidth(2, 400)
        self.tblArticulos.setColumnWidth(3, 100)
        self.tblArticulos.setColumnWidth(4, 400)
        self.tblArticulos.setColumnWidth(5, 100)
        

        self.tblFacturas.setColumnWidth(0, 100)
        self.tblFacturas.setColumnWidth(1, 250)
        self.tblFacturas.setColumnWidth(2, 400)
        self.tblFacturas.setColumnWidth(3, 100)
        self.tblFacturas.setColumnWidth(4, 100)
        
        self.load_data_diaria_articulos()
        self.load_data_diaria_facturas()
        self.load_data_anual()
        
        #Acceso a Caja Anual
        self.tabCajas.setTabEnabled(1, False)
        if self.cfg.consejoadministracion==True:
            self.tabCajas.setTabEnabled(1, True)
        elif self.cfg.gerente==True:
            self.tabCajas.setTabEnabled(1, True)
            




    def load_data_anual(self):

        #datos compra
        year=2010
        self.cfg.connect()
        cur = self.cfg.con.cursor()
        cur.execute("select date_part('month', fecha) as mes, sum(compra) as compra from articulos, albaranes where albaranes.id_albaranes=articulos.id_albaranes and date_part('year', fecha)=%s group by date_part('month',albaranes.fecha) ;", (year, ))
        for rec in cur:
            self.tblAnual.setItem(rec['mes']-1, 0,QTableWidgetItem(s2q(euros(rec['compra']))))
        cur.close()        
        
        #datos venta
        year=2010
        cur = self.cfg.con.cursor()
        cur.execute("select date_part('month', hora) as mes ,  sum(venta) as venta from articulos, facturas where facturas.id_facturas=articulos.id_facturas and articulos.id_facturas is not null and date_part('year', hora)=2010 group by date_part('month', hora) ;", (year, ))
        for rec in cur:
            self.tblAnual.setItem(rec['mes']-1, 1,QTableWidgetItem(s2q(euros(rec['venta']))))
        cur.close()        
        self.cfg.disconnect()
        
        #datos ganancia
        for i in range(self.tblAnual.rowCount()):
            compra=qtablewidgetitemeuros2float(self.tblAnual.item(i, 0))
            venta=qtablewidgetitemeuros2float(self.tblAnual.item(i, 1))
            self.tblAnual.setItem(i, 2, QTableWidgetItem(s2q(euros(venta-compra))))


    def load_data_diaria_articulos(self):
        #datos compra
        ventas=0
        self.cfg.connect()
        cur = self.cfg.con.cursor()
        data=( self.calendar.selectedDate().year(),  self.calendar.selectedDate().month(),   self.calendar.selectedDate().day() )        
        cur.execute("select * from proveedores, albaranes, articulos, tipos, facturas, clientes where proveedores.id_proveedores=albaranes.id_proveedores and  articulos.id_albaranes=albaranes.id_albaranes and facturas.id_clientes=clientes.id_clientes and tipos.id_tipos=articulos.id_tipos and articulos.id_facturas=facturas.id_facturas and date_part('year', hora)=%s and date_part('month', hora)=%s and date_part('day', hora)=%s;", data)
        self.tblArticulos.setRowCount(cur.rowcount);
        for rec in cur:
            self.tblArticulos.setItem(cur.rownumber-1, 0,QTableWidgetItem(str(rec['id_articulos'])) )
            self.tblArticulos.setItem(cur.rownumber-1, 1, QTableWidgetItem(s2q(rec['tipo'] )+ s2q(". ")+ s2q(rec['modelo'])))
            self.tblArticulos.setItem(cur.rownumber-1, 2, QTableWidgetItem(s2q(rec['nombre']) + " "+ s2q(rec['apellidos'])))
            self.tblArticulos.setItem(cur.rownumber-1, 3, QTableWidgetItem(s2q(euros(rec['venta']))))
            self.tblArticulos.setItem(cur.rownumber-1, 4, QTableWidgetItem(s2q(rec['proveedor'])))
            self.tblArticulos.setItem(cur.rownumber-1, 5, QTableWidgetItem(str(rec['id_facturas'])))
            ventas=ventas+rec['venta']
        self.lblTotalArticulos.setText(s2q("Total artículos: " + str(cur.rowcount)))
        self.lblTotalVentas.setText(s2q("Total ventas: " + str(ventas) + " €"))
        cur.close()       
        self.cfg.disconnect() 
        
    def load_data_diaria_facturas(self):
        #datos compra
        self.cfg.connect()
        cur = self.cfg.con.cursor()
        data=( self.calendar.selectedDate().year(),  self.calendar.selectedDate().month(),   self.calendar.selectedDate().day() )        
        cur.execute("select facturas.id_facturas, facturas_articulos(facturas.id_facturas) as articulos, facturas_venta(facturas.id_facturas) as ventas, hora, nombre, apellidos from facturas, clientes where facturas.id_clientes=clientes.id_clientes and date_part('year', hora)=%s and date_part('month', hora)=%s and date_part('day', hora)=%s;", data)
        self.tblFacturas.setRowCount(cur.rowcount);
        for rec in cur:
            self.tblFacturas.setItem(cur.rownumber-1, 0,QTableWidgetItem(str(rec['id_facturas'])) )
            self.tblFacturas.setItem(cur.rownumber-1, 1, QTableWidgetItem(str(rec['hora'])))
            self.tblFacturas.setItem(cur.rownumber-1, 2, QTableWidgetItem(s2q(rec['nombre']) + " "+ s2q(rec['apellidos'])))
            self.tblFacturas.setItem(cur.rownumber-1, 3, QTableWidgetItem(str(rec['articulos'])))
            self.tblFacturas.setItem(cur.rownumber-1, 4, QTableWidgetItem(s2q(euros(rec['ventas']))))
        self.lblTotalFacturas.setText("Total facturas: " + str(cur.rowcount))
        cur.close()                
        self.cfg.disconnect()

    @pyqtSignature("")
    def on_calendar_selectionChanged(self):
        self.load_data_diaria_articulos()
        self.load_data_diaria_facturas()
