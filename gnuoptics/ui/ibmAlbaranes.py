## -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from Ui_ibmAlbaranes import *
from apoyo import *
import psycopg2,  psycopg2.extras

class ibmAlbaranes(QDialog, Ui_ibmAlbaranes):
    def __init__(self, cfg,   id_proveedores=None, id_albaranes= None,  parent = None, name = None, modal = False):
        QDialog.__init__(self, parent)
        if name:
            self.setObjectName(name)
        self.setupUi(self)
        self.cfg=cfg
        self.reg=None
        self.id_albaranes=id_albaranes
        self.id_proveedores=id_proveedores
        self.showMaximized()
        self.selArticulo=None
        

        self.tblArticulos.setColumnWidth(0, 100)
        self.tblArticulos.setColumnWidth(1, 300)
        self.tblArticulos.setColumnWidth(2, 450)
        self.tblArticulos.setColumnWidth(3, 100)
        self.tblArticulos.setColumnWidth(4, 100)
        self.tblArticulos.setColumnWidth(5, 100)  

        self.cfg.connect()
        cur = self.cfg.con.cursor()
        cur.execute("select id_proveedores, proveedor, cif from proveedores order by proveedor, cif")
        for i in cur:
            self.cmbProveedores.addItem(s2q(i['proveedor'] + " ("+i['cif']+")"),  i['id_proveedores'])            
        cur.close()          
        self.cfg.disconnect() 

        self.cfg.connect()
        cur = self.cfg.con.cursor()
        cur.execute("select * from tipos order by tipo")
        for i in cur:
            self.cmbTipos.addItem(s2q(i['tipo']),  i['id_tipos'])            
        cur.close()      
        self.cfg.disconnect()     
        if self.id_proveedores!=None: #En caso de que se envie con el constructor
            self.cmbProveedores.setCurrentIndex(self.cmbProveedores.findData(self.id_proveedores))            
            
        if self.id_albaranes!=None:
            self.lblTitulo.setText(s2q("Modificar albarán"))
            self.setWindowTitle("gnuOptics > Proveedores > Modificar")
            self.grpInsercion.setEnabled(True)
            self.grpArticulos.setEnabled(True)
            self.cmdAlbaran.setText(s2q("Modifica los datos del albarán"))
            
            #consigue el registro de id_proveedores
            self.cfg.connect()
            cur = self.cfg.con.cursor()
            cur.execute("select * from albaranes where id_albaranes=%s", (self.id_albaranes, ))
            self.reg= cur.fetchone()
            cur.close()                 
            self.cfg.disconnect() 
            self.cmbProveedores.setCurrentIndex(self.cmbProveedores.findData(self.reg['id_proveedores']))
            self.calendar.setSelectedDate(s2d(self.reg['fecha']))
            self.chkInventariado.setCheckState(b2c(self.reg['inventariado']))
            
            self.load_data_articulos()

    def load_data_articulos(self):
        self.cfg.connect()
        cur = self.cfg.con.cursor()
        cur.execute("SELECT * FROM  articulos, tipos where articulos.id_tipos=tipos.id_tipos and articulos.id_albaranes="+str(self.id_albaranes)+" order by tipo, modelo,id_articulos;")
        self.tblArticulos.setRowCount(cur.rowcount);
        self.lblTotalArticulos.setText(s2q(str(cur.rowcount) +" artículos"))
        coste=0
        for rec in cur:
            self.tblArticulos.setItem(cur.rownumber-1, 0,QTableWidgetItem(str(rec['id_articulos'])) )
            self.tblArticulos.setItem(cur.rownumber-1, 1, QTableWidgetItem(s2q(rec['tipo'])))
            self.tblArticulos.setItem(cur.rownumber-1, 2, QTableWidgetItem(s2q(rec['modelo'])))
            self.tblArticulos.setItem(cur.rownumber-1, 3, QTableWidgetItem(str(rec['compra'])))
            self.tblArticulos.setItem(cur.rownumber-1, 4, QTableWidgetItem(str(rec['venta'])))
            self.tblArticulos.setItem(cur.rownumber-1, 5, QTableWidgetItem(str(rec['id_facturas'])))
            coste=coste+rec['compra']
        self.lblTotalCoste.setText(s2q(str(coste) +" €"))
        cur.close()        
        self.cfg.disconnect() 


    @QtCore.pyqtSlot()  
    def on_actionArticuloBorrar_activated(self):
        self.cfg.connect()
        cur = self.cfg.con.cursor()
        cur.execute("delete from articulos where id_articulos=%s", (self.selArticulo, ))
        self.cfg.con.commit()
        cur.close()     
        self.cfg.disconnect() 
        self.load_data_articulos()
        self.tblArticulos.clearSelection()

    @pyqtSignature("")
    def on_cmdAlbaran_clicked(self):           
        
        id_proveedores=self.cmbProveedores.itemData(self.cmbProveedores.currentIndex()).toInt()[0]
        chkInventariado=c2b(self.chkInventariado.checkState())
        date=d2s(self.calendar.selectedDate())
        if self.id_albaranes==None: #insertar
            self.cfg.connect()
            cur = self.cfg.con.cursor()
            cur.execute("insert into albaranes(fecha,id_proveedores, inventariado) values ( %s, %s, %s)", (date, id_proveedores, chkInventariado))
            self.cfg.con.commit()
            cur.close()
            self.cfg.disconnect() 
            self.done(0)
        else: #modificar
            self.cfg.connect()
            cur = self.cfg.con.cursor()
            sql="update albaranes set fecha=%s, id_proveedores=%s, inventariado=%s where id_albaranes=%s"
            data= (date, id_proveedores, chkInventariado,  self.id_albaranes )
            cur.execute(sql, data )
            self.cfg.con.commit()
            cur.close()
            self.cfg.disconnect() 
            self.done(0)

    @pyqtSignature("")
    def on_cmdArticulo_clicked(self):
        self.cfg.connect()
        cur = self.cfg.con.cursor()
        id_tipos=self.cmbTipos.itemData(self.cmbTipos.currentIndex()).toInt()[0]
        data= (self.id_albaranes, id_tipos, q2s(self.txtModelo.text()),  round(self.txtCompra.text().toFloat()[0], 2),  round(self.txtVenta.text().toFloat()[0], 2))
        print data
        for i in range(self.spnCantidad.value()):
            cur.execute("insert into articulos(id_albaranes, id_tipos, modelo,  compra, venta) values ( %s, %s, %s, %s, %s)", data)
        self.cfg.con.commit()
        cur.close()
        self.cfg.disconnect() 
        self.spnCantidad.setValue(1)
        self.load_data_articulos()
        
    def on_tblArticulos_itemSelectionChanged(self):
        for i in self.tblArticulos.selectedItems():#itera por cada item no row.
            self.selArticulo=int(self.tblArticulos.item(i.row(), 0).text())
        print "Seleccionado:",  self.selArticulo

    def on_tblArticulos_customContextMenuRequested(self,  pos):
        if self.selArticulo==None:
            self.actionArticuloBorrar.setEnabled(False)
        else:
            self.actionArticuloBorrar.setEnabled(True)

        menu=QMenu()
        menu.addAction(self.actionArticuloBorrar)
        menu.exec_(self.tblArticulos.mapToGlobal(pos))