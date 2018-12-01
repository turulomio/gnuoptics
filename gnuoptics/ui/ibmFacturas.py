## -*- coding: utf-8 -*-

import psycopg2,  psycopg2.extras
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from Ui_ibmFacturas import *
from apoyo import *

class ibmFacturas(QDialog, Ui_ibmFacturas):
    def __init__(self, cfg,  id_clientes=None,  id_facturas=None,   parent=None):
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.cfg=cfg
        self.articulos=[]
        self.coste=0
        self.id_facturas=id_facturas
        self.hora.setDateTime(QDateTime.currentDateTime())

        self.tblInventario.setColumnWidth(0, 75)
        self.tblInventario.setColumnWidth(1, 200)
        self.tblInventario.setColumnWidth(2, 350)
        self.tblInventario.setColumnWidth(3, 75)
        
        self.tblArticulos.setColumnWidth(0, 75)
        self.tblArticulos.setColumnWidth(1, 200)
        self.tblArticulos.setColumnWidth(2, 350)
        self.tblArticulos.setColumnWidth(3, 75)

        if id_facturas!=None:# Modificación  de una factura
            self.cfg.connect()
            cur = self.cfg.con.cursor()
            cur.execute("select * from facturas where id_facturas=%s" % (self.id_facturas, ))
            for i in cur:
                self.id_clientes=i['id_clientes']           
            cur.close()         
            self.cfg.disconnect() 
        else:
            self.id_clientes=id_clientes
        
        self.cfg.connect()
        cur = self.cfg.con.cursor()
        cur.execute("select id_clientes, nombre, apellidos from clientes order by nombre, apellidos")
        for i in cur:
            self.cmbClientes.addItem(s2q(i['nombre'] + " "+str(i['apellidos'])),  i['id_clientes'])            
        cur.close()         
        self.cfg.disconnect() 
        if self.id_clientes==0:
            self.radAnonimo.setChecked(True)
        else:
            self.radCliente.setChecked(True)
            self.cmbClientes.setCurrentIndex(self.cmbClientes.findData(self.id_clientes))  #siempre hay un cliente
            

        self.grpCliente.setEnabled(False)
        if self.id_facturas!=None:        
            self.cfg.connect()
            cur = self.cfg.con.cursor()
            cur.execute("select * from articulos where id_facturas=%s" %(self.id_facturas, ))
            print "Articulos en factura", self.id_facturas,  cur.rowcount
            for i in cur:
                self.articulos.append(i['id_articulos'])            
            cur.close()       
            self.cfg.disconnect() 
        self.load_articulos()
        self.load_inventario()
            
            
    def load_inventario(self):   
        self.cfg.connect()
        cur = self.cfg.con.cursor()     
        if len(self.articulos)>0:
            notin=" and id_articulos not in (" + str(self.articulos)[1:-1] +") "
        else:
            notin=" "
        cur.execute("SELECT * FROM  articulos, tipos where articulos.id_tipos=tipos.id_tipos "+notin+" and articulos.id_facturas is null order by tipo, modelo,id_articulos;")
        self.tblInventario.setRowCount(cur.rowcount);
        for rec in cur:
            self.tblInventario.setItem(cur.rownumber-1, 0,QTableWidgetItem(str(rec['id_articulos'])) )
            self.tblInventario.setItem(cur.rownumber-1, 1, QTableWidgetItem(s2q(rec['tipo'])))
            self.tblInventario.setItem(cur.rownumber-1, 2, QTableWidgetItem(s2q(rec['modelo'])))
            self.tblInventario.setItem(cur.rownumber-1, 3, QTableWidgetItem(str(rec['venta'])))
        cur.close()        
        self.cfg.disconnect() 
                
    def load_articulos(self):       
        if len(self.articulos)>0:
            notin=" and id_articulos in (" + str(self.articulos)[1:-1] +") "
            self.cmdQuit.setEnabled(True)
        else:
            notin=" and id_articulos in (-1) "
            self.cmdQuit.setEnabled(False)
            return
        self.coste=0
        self.cfg.connect()
        cur = self.cfg.con.cursor()
        cur.execute("SELECT * FROM  articulos, tipos where articulos.id_tipos=tipos.id_tipos "+notin+" order by tipo, modelo,id_articulos;")
        self.tblArticulos.setRowCount(cur.rowcount);
        for rec in cur:
            self.tblArticulos.setItem(cur.rownumber-1, 0,QTableWidgetItem(str(rec['id_articulos'])) )
            self.tblArticulos.setItem(cur.rownumber-1, 1, QTableWidgetItem(s2q(rec['tipo'])))
            self.tblArticulos.setItem(cur.rownumber-1, 2, QTableWidgetItem(s2q(rec['modelo'])))
            self.tblArticulos.setItem(cur.rownumber-1, 3, QTableWidgetItem(str(rec['venta'])))
            self.coste=round(self.coste+ rec['venta'], 2)
        cur.close()        
        self.cfg.disconnect() 
        self.show_totals()



    def show_totals(self):
        self.lblTotalArticulos.setText(s2q( str(len(self.articulos)) + " artículos"))
        self.lblTotalVenta.setText(s2q("Total venta: "+ euros(self.coste)))
        
    @pyqtSignature("")
    def on_cmdAdd_clicked(self):
        id_articulos= int(self.tblInventario.item(self.tblInventario.currentRow(), 0).text())              
        self.articulos.append(id_articulos)
        self.load_articulos()
        self.load_inventario()
        self.show_totals()
        
    @pyqtSignature("")
    def on_cmdQuit_clicked(self):
        id_articulos= int(self.tblArticulos.item(self.tblArticulos.currentRow(), 0).text())              
        self.coste=self.coste- float(self.tblInventario.item(self.tblInventario.currentRow(), 3).text())  
        self.articulos.remove(id_articulos)
        self.load_articulos()
        self.load_inventario()
        self.show_totals()
        
    @pyqtSignature("")
    def on_cmdFactura_clicked(self):
        id_clientes=self.cliente()
#        chkInventariado=c2b(self.chkInventariado.checkState())
        hora=d2s(self.hora.dateTime())
        
        self.cfg.connect()
        cur = self.cfg.con.cursor()
        if self.id_facturas==None: #insertar
            cur.execute("insert into facturas(hora,id_clientes, id_usuarios) values ( %s, %s, %s) returning id_facturas", (hora, id_clientes, self.cfg.id_usuarios))
            for rec in cur:
                self.id_facturas=rec['id_facturas']            
            cur.execute("update articulos set id_facturas= %s where id_articulos in ("+str(self.articulos)[1:-1] +") ", (self.id_facturas, ))
        else: #modificar
            #Modifica la hora de la factura
            cur.execute("update facturas set hora=now() where id_facturas=%s" %(self.id_facturas, ))
            #Libera los artículos de la factura a modificar
            cur.execute("update articulos set id_facturas=NULL where id_facturas=%s ", (self.id_facturas, ))
            #Atrapa los articulos de la factura modificada
            cur.execute("update articulos set id_facturas= %s where id_articulos in ("+str(self.articulos)[1:-1] +") ", (self.id_facturas,))

        self.cfg.con.commit()
        cur.close()         
        self.cfg.disconnect() 
        self.done(0)        
        
    def cliente(self):
        if self.radAnonimo.isChecked():
            return 0
        else:
            return self.cmbClientes.itemData(self.cmbClientes.currentIndex()).toInt()[0]            
