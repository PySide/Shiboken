import unittest
import sys

from helper import UsesQApplication
from PySide.QtGui import QLayout, QWidget, QPushButton, QWidgetItem, QHBoxLayout

class MyLayout(QLayout):
    def __init__(self, parent=None):
        QLayout.__init__(self, parent)
        self._list = []

    def addItem(self, item):
        self.add(item)

    def addWidget(self, widget):
        self.add(QWidgetItem(widget))

    def itemAt(self, index):
        if index < len(self._list):
            return self._list[index]

        return None

    def count(self):
        return len(self._list)

    def add(self, item):
        self._list.append(item)



#Test if a layout implemented in python, the QWidget.setLayout works
#fine because this implement som layout functions used in glue code of
#QWidget, then in c++ when call a virtual function this need call the QLayout
#function implemented in python

class QLayoutTest(UsesQApplication):
    def testOwnershipTransfer(self):
        b = QPushButton("teste")
        l = MyLayout()

        l.addWidget(b)

        self.assertEqual(sys.getrefcount(b), 2)

        w = QWidget()

        #transfer ref
        w.setLayout(l)

        self.assertEqual(sys.getrefcount(b), 3)


    def testReferenceTransfer(self):
        b = QPushButton("teste")
        l = QHBoxLayout()

        # keep ref
        l.addWidget(b)
        self.assertEqual(sys.getrefcount(b), 3)

        w = QWidget()

        # transfer ref
        w.setLayout(l)

        self.assertEqual(sys.getrefcount(b), 3)

        # release ref
        del w

        self.assertEqual(sys.getrefcount(b), 2)

if __name__ == '__main__':
    unittest.main()