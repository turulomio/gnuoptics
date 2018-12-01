DESTDIR ?= /usr

PREFIXBIN=$(DESTDIR)/bin
PREFIXLIB=$(DESTDIR)/lib/gnuoptics
PREFIXSHARE=$(DESTDIR)/share/gnuoptics 

install:
	echo "Instalando en ${DESTDIR}"
	pyrcc4 images/gnuoptics.qrc > images/gnuoptics_rc.py
	pyuic4 ui/ibmAlbaranes.ui > ui/Ui_ibmAlbaranes.py    
	pyuic4 ui/ibmClientes.ui > ui/Ui_ibmClientes.py
	pyuic4 ui/ibmFacturas.ui > ui/Ui_ibmFacturas.py
	pyuic4 ui/ibmProveedores.ui > ui/Ui_ibmProveedores.py
	pyuic4 ui/frmAbout.ui > ui/Ui_frmAbout.py 
	pyuic4 ui/frmAccess.ui > ui/Ui_frmAccess.py 
	pyuic4 ui/frmMain.ui > ui/Ui_frmMain.py
	pyuic4 ui/frmTablasAuxiliares.ui > ui/Ui_frmTablasAuxiliares.py
	pyuic4 ui/wdgCaja.ui > ui/Ui_wdgCaja.py
	pyuic4 ui/wdgClientes.ui > ui/Ui_wdgClientes.py
	pyuic4 ui/wdgFacturas.ui > ui/Ui_wdgFacturas.py
	pyuic4 ui/wdgInventario.ui > ui/Ui_wdgInventario.py
	pyuic4 ui/wdgProveedores.ui > ui/Ui_wdgProveedores.py
	pylupdate4 gnuoptics.pro
	lrelease gnuoptics.pro
	install -o root -d $(PREFIXBIN)
	install -o root -d $(PREFIXLIB)
	install -o root -d $(PREFIXSHARE)                                                      
	install -m 755 -o root gnuoptics.py $(PREFIXBIN)/gnuoptics
	install -m 644 -o root ui/*.py $(PREFIXLIB)                
	install -m 644 -o root images/*.py $(PREFIXLIB)
	install -m 644 -o root i18n/*.qm $(PREFIXSHARE)

uninstall:
	rm $(PREFIXBIN)/gnuoptics
	rm -Rf $(PREFIXLIB)
	rm -Rf $(PREFIXSHARE)



