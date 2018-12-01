## -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import sys
from Ui_frmAccess import *

class frmAccess(QDialog, Ui_frmAccess):
    def __init__(self, parent = None, name = None, modal = False):
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

    
    @pyqtSignature("")
    def on_cmdYN_accepted(self):
        self.done(0)

    @pyqtSignature("")
    def on_cmdYN_rejected(self):
        print "No se ha creado ninguna conexión"
        sys.exit(255)
