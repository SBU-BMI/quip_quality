from PyQt4 import QtCore, QtGui
from os import listdir
from os.path import isfile, join
import sys
import openslide

from PIL import Image, ImageDraw
from PIL.ImageQt import ImageQt
Image.Image.tostring = Image.Image.tobytes

id_role = QtCore.Qt.UserRole

class PhotoViewer(QtGui.QGraphicsView):
    def __init__(self, parent):
        super(PhotoViewer, self).__init__(parent)
        self._zoom = 0
        self._scene = QtGui.QGraphicsScene(self)
        self._photo = QtGui.QGraphicsPixmapItem()
        self._scene.addItem(self._photo)
        self.setScene(self._scene)
        self.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(30, 30, 30)))
        self.setFrameShape(QtGui.QFrame.NoFrame)

    def fitInView(self):
        rect = QtCore.QRectF(self._photo.pixmap().rect())
        if not rect.isNull():
            unity = self.transform().mapRect(QtCore.QRectF(0, 0, 1, 1))
            self.scale(1 / unity.width(), 1 / unity.height())
            viewrect = self.viewport().rect()
            scenerect = self.transform().mapRect(rect)
            factor = min(viewrect.width() / scenerect.width(),
                         viewrect.height() / scenerect.height())
            self.scale(factor, factor)
            self.centerOn(rect.center())
            self._zoom = 0

    def setPhoto(self, pixmap=None):
        self._zoom = 0
        if pixmap and not pixmap.isNull():
            self.setDragMode(QtGui.QGraphicsView.ScrollHandDrag)
            self._photo.setPixmap(pixmap)
            self.fitInView()
        else:
            self.setDragMode(QtGui.QGraphicsView.NoDrag)
            self._photo.setPixmap(QtGui.QPixmap())

    def zoomFactor(self):
        return self._zoom

    def wheelEvent(self, event):
        if not self._photo.pixmap().isNull():
            if event.delta() > 0:
                factor = 1.25
                self._zoom += 1
            else:
                factor = 0.8
                self._zoom -= 1
            if self._zoom > 0:
                self.scale(factor, factor)
            elif self._zoom == 0:
                self.fitInView()
            else:
                self._zoom = 0

class Window(QtGui.QWidget):
    def __init__(self):

        #dictionary of where clauses for current query
        self.query_dict = {}

        super(Window, self).__init__()
        self.viewer = PhotoViewer(self)
        #self.edit = QtGui.QLineEdit(self)
        #self.edit.setReadOnly(True)
        #self.button = QtGui.QToolButton(self)
        #self.button.setText('...')
        #self.button.clicked.connect(self.setRootDir)
        #self.queryInput = QtGui.QLineEdit("Query", self)
        #self.queryInput.setMaxLength(128)
        #self.queryButton = QtGui.QToolButton(self)
        #self.queryButton.setText("Edit Query")
        #self.queryButton.clicked.connect(self.showQueryDialog)
        self.tileList = QtGui.QListWidget()
        self.tileList.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tileList.currentItemChanged.connect(self.viewTile)

        layout = QtGui.QGridLayout(self)
        layout.addWidget(self.viewer, 0, 0, 1, 3)
        #layout.addWidget(QtGui.QLabel("Set Results Dir", self), 1, 0, 1, 1)
        #layout.addWidget(self.edit, 1, 1, 1, 1)
        #layout.addWidget(self.button, 1, 2, 1, 1)
        #layout.addWidget(QtGui.QLabel("Query", self), 2, 0, 1, 1)
        #layout.addWidget(self.queryInput, 2, 1, 1, 1)
        #layout.addWidget(self.queryButton, 2, 2, 1, 1)
        layout.addWidget(self.tileList, 3, 0, 1, 3)

        # Adjust the layout so that the Image gets more space than the tile list
        layout.setRowStretch(0, 3)
        layout.setRowStretch(3, 1)

#Adjust this to populate the tile list appropriately 
    def setRootDir(self):
        path = QtGui.QFileDialog.getExistingDirectory(
            self, 'Choose Results Directory', '/lustre/atlas/proj-shared/csc143/lot/u24/test')
        if path:
            self.rootDir = str(path)
            self.edit.setText(path)
            self.refreshTileList()

    def refreshTileList(self):
        files = [f for f in listdir(self.rootDir) if isfile(join(self.rootDir, f)) and f.startswith("TCGA") and f.endswith("overlay.png")]
        for f in files:
            self.tileList.addItem(QtGui.QListWidgetItem(f))

    def showResultsInList(self):
        for r in range (len (self.results) ):
            #Grab size from ith entry in the results
            size = int(self.results.iloc[r]["AreaInPixels"]) 
            name = self.results.iloc[r]["fname"]
            iname = name.split('/')[5][:-4]

            this_item = QtGui.QListWidgetItem("Result: %i, Name: %s, Size: %i"%(r,iname,size))
            this_item.setData (id_role, r)
            self.tileList.addItem(this_item)

    def viewTile(self):
        #print self.results

        id = self.tileList.currentItem().data(id_role).toInt()[0] #I'm not sure why toInt returns an (i, True) tuple
        print id

        fname = self.results.iloc[id]['fname']

        rawpoly = self.results.iloc[id]['Polygon']
        bbox = getbb (rawpoly)
        margin = 100
        offset = (bbox[0]-margin, bbox[1]-margin)

        oslide = openslide.OpenSlide(fname)
        imgPIL = oslide.read_region(offset, 0, (bbox[2]-bbox[0]+2*margin,bbox[3]-bbox[1]+2*margin)) # expects (x,y), , (h,w)

        #Draw the polygon points on the pillow image
        polypts = rawpoly[1:-1].split(':')

        #print polypts 
        #print len (polypts)
        #print range (0, len (polypts), 2)

        adjpts = []

        for i in range (0, len (polypts), 2):
            adjpts.append (int(float(polypts[i])) - offset[0])
            adjpts.append (int(float(polypts[i+1])) - offset[1]) 

        adjpts.append (adjpts[0])
        adjpts.append (adjpts[1]) # Add the first point again at the end to complete the polygon

        #print adjpts

        draw = ImageDraw.Draw(imgPIL)
        draw.line(adjpts, fill=(0,255,0), width=3)
        #draw.line((0,0,200,200), fill=(0,128,0), width=3)
        del draw

        imgqt = ImageQt(imgPIL)
        imgqtgui = QtGui.QImage(imgqt)
        pix = QtGui.QPixmap.fromImage(imgqtgui)        

        self.viewer.setPhoto(pix)
        #self.viewer.setPhoto(QtGui.QPixmap(fname))

    def updateQuery(self):
        print "Update query here"

        # Grab all of the entries from the form, and adjust the query dict
        

        self.d.done(0)

    def showQueryDialog(self):
        self.d = QtGui.QDialog()
        self.d.setWindowTitle("Edit Query")
        self.d.setWindowModality(QtCore.Qt.ApplicationModal)
       
        variables = ["elongation", "height", "width"] #or whatever...
        gts = {}
        lts = {}

        dlayout = QtGui.QGridLayout(self.d)
        row = 0

        # Add rows for each variable
        for v in variables:
            dlayout.addWidget(QtGui.QLabel(v, self), row, 0, 1, 1)
            gt = QtGui.QLineEdit("*", self)
            lt = QtGui.QLineEdit("*", self)
            dlayout.addWidget(gt, row, 1, 1, 1)
            dlayout.addWidget(lt, row, 2, 1, 1)
        
            row = row + 1

        # Add ok, cancel buttons
        dblayout = QtGui.QGridLayout()
        d_ok_button = QtGui.QToolButton(self)
        d_ok_button.setText("OK")
        d_ok_button.clicked.connect(self.updateQuery)
        d_cancel_button = QtGui.QToolButton(self)
        d_cancel_button.setText("Cancel")
        d_cancel_button.clicked.connect(self.d.done)
        dblayout.addWidget(d_ok_button, 0, 1, 1, 1) 
        dblayout.addWidget(d_cancel_button, 0, 0, 1, 1) 
        dlayout.addLayout(dblayout, row, 0, 1, 3)

        self.d.exec_()


def getbb(polystr):
    #poly_pts = plotframe['Polygon'][event.ind].values[0][1:-1].split(':') # the [1:-1] is to strip the [ and ] from the ends of the string
    poly_pts = polystr[1:-1].split(':') # the [1:-1] is to strip the [ and ] from the ends of the string
    # Need min and max of evens, and min and max of odds, then subtract
    # the tile offsets from the filename
    evens = range(0, len(poly_pts), 2)
    odds = range(1, len(poly_pts), 2)

    minx = 1000000000
    maxx = 0
    miny = 1000000000
    maxy = 0

    for i in evens:
        me = int(float(poly_pts[i]))
        if me > maxx:
            maxx = me
        if me < minx:
            minx = me

    for i in odds:
        me = int(float(poly_pts[i]))
        if me > maxy:
            maxy = me
        if me < miny:
            miny = me

    print "found", minx, miny, maxx, maxy

    # Adjust to tile coordinates
    # Commented, because here we need global coordinates
    #tilex, tiley = getxy(the_file)
    #minx = minx - tilex
    #miny = miny - tiley
    #maxx = maxx - tilex
    #maxy = maxy - tiley

    return (minx, miny, maxx, maxy)

def start(results): # results is a pandas dataframe


    #app = QtGui.QApplication(sys.argv)
    app = QtGui.QApplication(["Curation Viewer"])
    window = Window()
    window.results = results
    window.showResultsInList()
    window.setGeometry(500, 300, 800, 800)
    window.show()
    sys.exit(app.exec_())


    
