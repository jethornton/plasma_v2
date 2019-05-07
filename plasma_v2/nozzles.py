from functools import partial

from PyQt5.QtSql import QSqlQueryModel, QSqlQuery
from PyQt5.QtWidgets import QDataWidgetMapper

def Setup(parent):
    parent.materialFwdBtn.clicked.connect(partial(materialFwd, parent))
    parent.materialBackBtn.clicked.connect(partial(materialBack, parent))
    parent.gaugeFwdBtn.clicked.connect(partial(gaugeFwd, parent))
    parent.gaugeBackBtn.clicked.connect(partial(gaugeBack, parent))
    parent.nozzleFwdBtn.clicked.connect(partial(nozzleFwd, parent))
    parent.nozzleBackBtn.clicked.connect(partial(nozzleBack, parent))
    parent.ampsFwdBtn.clicked.connect(partial(ampsFwd, parent))
    parent.ampsBackBtn.clicked.connect(partial(ampsBack, parent))

    materialInit(parent)


def materialInit(parent):
    parent.materialMapper = QDataWidgetMapper(parent)
    parent.materialModel = QSqlQueryModel(parent)
    materialSelect = 'SELECT DISTINCT material FROM cut_chart'
    parent.materialModel.setQuery(materialSelect)
    parent.materialMapper.setModel(parent.materialModel)
    parent.materialMapper.addMapping(parent.materialLbl, 0, b'text')
    parent.materialMapper.toLast()
    parent.materialLast = parent.materialMapper.currentIndex()
    parent.materialMapper.toFirst()
    gaugeInit(parent)

def materialFwd(parent):
    if parent.materialMapper.currentIndex() != parent.materialLast:
        parent.materialMapper.toNext()
    else:
        parent.materialMapper.toFirst()
    gaugeInit(parent)

def materialBack(parent):
    if parent.materialMapper.currentIndex() != 0:
        parent.materialMapper.toPrevious()
    else:
        parent.materialMapper.toLast()
    gaugeInit(parent)

def gaugeInit(parent):
    parent.gaugeMapper = QDataWidgetMapper(parent)
    parent.gaugeModel = QSqlQueryModel(parent)
    material = parent.materialLbl.text()
    gaugeSelect = "SELECT DISTINCT gauge FROM cut_chart \
        WHERE material = '{}' ORDER BY thickness DESC".format(material)
    parent.gaugeModel.setQuery(gaugeSelect)
    parent.gaugeMapper.setModel(parent.gaugeModel)
    parent.gaugeMapper.addMapping(parent.gaugeLbl, 0, b'text')
    parent.gaugeMapper.toLast()
    parent.gaugeLast = parent.gaugeMapper.currentIndex()
    parent.gaugeMapper.toFirst()
    nozzleInit(parent)

def gaugeFwd(parent):
    if parent.gaugeMapper.currentIndex() != parent.gaugeLast:
        parent.gaugeMapper.toNext()
    else:
        parent.gaugeMapper.toFirst()
    nozzleInit(parent)

def gaugeBack(parent):
    if parent.gaugeMapper.currentIndex() != 0:
        parent.gaugeMapper.toPrevious()
    else:
        parent.gaugeMapper.toLast()
    nozzleInit(parent)

def nozzleInit(parent):
    parent.nozzleMapper = QDataWidgetMapper(parent)
    parent.nozzleModel = QSqlQueryModel(parent)
    gauge = parent.gaugeLbl.text()
    material = parent.materialLbl.text()
    nozzleSelect = "SELECT DISTINCT nozzle FROM cut_chart \
      WHERE material = '{}' AND gauge = '{}'".format(material, gauge)
    parent.nozzleModel.setQuery(nozzleSelect)
    parent.nozzleMapper.setModel(parent.nozzleModel)
    parent.nozzleMapper.addMapping(parent.nozzleLbl, 0, b'text')
    parent.nozzleMapper.toLast()
    parent.nozzleLast = parent.nozzleMapper.currentIndex()
    if parent.nozzleLast > 0:
      parent.nozzleFwdBtn.setEnabled(True)
      parent.nozzleBackBtn.setEnabled(True)
    else:
      parent.nozzleFwdBtn.setEnabled(False)
      parent.nozzleBackBtn.setEnabled(False)
    parent.nozzleMapper.toFirst()
    ampsInit(parent)

def nozzleFwd(parent):
    if parent.nozzleMapper.currentIndex() != parent.nozzleLast:
        parent.nozzleMapper.toNext()
    else:
        parent.nozzleMapper.toFirst()
    ampsInit(parent)

def nozzleBack(parent):
    if parent.nozzleMapper.currentIndex() != 0:
        parent.nozzleMapper.toPrevious()
    else:
        parent.nozzleMapper.toLast()
    ampsInit(parent)

def ampsInit(parent):
    parent.ampsMapper = QDataWidgetMapper(parent)
    parent.ampsModel = QSqlQueryModel(parent)
    nozzle = parent.nozzleLbl.text()
    gauge = parent.gaugeLbl.text()
    ampsSelect = "SELECT DISTINCT amps FROM cut_chart \
        WHERE nozzle = '{}' AND gauge = '{}'".format(nozzle, gauge)
    parent.ampsModel.setQuery(ampsSelect)
    parent.ampsMapper.setModel(parent.ampsModel)
    parent.ampsMapper.addMapping(parent.ampsLbl, 0, b'text')
    parent.ampsMapper.toLast()
    parent.ampsLast = parent.ampsMapper.currentIndex()
    parent.ampsMapper.toFirst()
    if parent.ampsLast > 0:
      parent.ampsFwdBtn.setEnabled(True)
      parent.ampsBackBtn.setEnabled(True)
    else:
      parent.ampsFwdBtn.setEnabled(False)
      parent.ampsBackBtn.setEnabled(False)

    nozzleInfo(parent)

def ampsFwd(parent):
    if parent.ampsMapper.currentIndex() != parent.ampsLast:
        parent.ampsMapper.toNext()
    else:
        parent.ampsMapper.toFirst()
    nozzleInfo(parent)

def ampsBack(parent):
    if parent.ampsMapper.currentIndex() != 0:
        parent.ampsMapper.toPrevious()
    else:
        parent.ampsMapper.toLast()
    nozzleInfo(parent)


def nozzleInfo(parent):
    parent.nozzleInfoMapper = QDataWidgetMapper(parent)
    parent.nozzleInfoModel = QSqlQueryModel(parent)

    material = parent.materialLbl.text()
    gauge = parent.gaugeLbl.text()
    nozzle = parent.nozzleLbl.text()
    amps = parent.ampsLbl.text()

    nozzleInfoSelect = "SELECT voltage, amps, height, delay, speed, kerf FROM \
    cut_chart WHERE material = '{}' AND gauge = '{}' AND nozzle = '{}' AND \
    amps = '{}' ".format(material, gauge, nozzle, amps)

    parent.nozzleInfoModel.setQuery(nozzleInfoSelect)
    parent.nozzleInfoMapper.setModel(parent.nozzleInfoModel)
    parent.nozzleInfoMapper.addMapping(parent.cutVoltsLbl, 0, b'text')
    parent.nozzleInfoMapper.addMapping(parent.cutAmpsLbl, 1, b'text')
    parent.nozzleInfoMapper.addMapping(parent.cutHeightLbl, 2, b'text')
    parent.nozzleInfoMapper.addMapping(parent.cutDelayLbl, 3, b'text')
    parent.nozzleInfoMapper.addMapping(parent.cutSpeedLbl, 4, b'text')
    parent.nozzleInfoMapper.addMapping(parent.cutWidthLbl, 5, b'text')
    parent.nozzleInfoMapper.toFirst()




