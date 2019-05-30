from functools import partial
from PyQt5.QtWidgets import QFileSystemModel, QTreeView
from PyQt5.QtCore import QDir, Qt
import linuxcnc
import os, time

HOME = os.path.expanduser("~")

def initPartNest(parent):
  parent.subModel = QFileSystemModel()
  parent.subModel.setRootPath('')
  parent.subTreeView.setModel(parent.subModel)
  parent.subTreeView.setRootIndex(parent.subModel.index('/home/john/linuxcnc'))

  parent.subTreeView.setAnimated(False)
  parent.subTreeView.setIndentation(20)
  parent.subTreeView.setSortingEnabled(True)

  parent.subTreeView.setColumnWidth(0, 250)
  parent.subTreeView.sortByColumn(0, Qt.AscendingOrder)

  parent.subTreeView.clicked.connect(partial(onClicked, parent))
  #parent.partsBuildLoadBtn.clicked.connect(partial(buildLoadCheck, parent))
  parent.partsBuildLoadBtn.clicked.connect(partial(nestedParts, parent))
  parent.partsBuildSaveBtn.clicked.connect(partial(buildSave, parent))

def onClicked(parent, index):
  path = parent.sender().model().filePath(index)
  parent.selectedFileLbl.setText(path)
  parent.statusbar.clearMessage()

def nestedParts(parent):
  if parent.selectedFileLbl.text():
    parent.statusbar.showMessage('Using {}'.format(parent.selectedFileLbl.text()))
  else:
    parent.statusbar.showMessage('A Subroutine File must be selected')
    return
  xCount = parent.xPartsCountSb.value()
  xSpacing = parent.xPartsSpacingSb.value()
  xRotation = parent.xPartRotationSb.value()
  yCount = parent.yPartsCountSb.value()
  ySpacing = parent.yPartsSpacingSb.value()
  yRotation = parent.yPartRotationSb.value()
  xEvenOffset = parent.xEvenOffsetSb.value()

  with open(parent.selectedFileLbl.text(), "r") as f:
     # returns a list of strings with \n removed
    sub = [x.strip() for x in f.readlines()]
  subIndex = next(i for i, s in enumerate(sub) if 'sub' in s)
  subName = sub[subIndex].split(' ')[0]
  # strip any program end lines % M2 M30
  programEnd = ['M2', 'm2', 'M30', 'm30', '%']
  for i in programEnd:
    if i in sub:
      itemCount = sub.count(i)
      for x in range(itemCount):
        del sub[sub.index(i)]
  if parent.partsTestRb.isChecked():
    sub.append('F75') # for testing
  else:
    sub.append('F{}'.format(parent.cutSpeedLbl.text()))
  sub.append('#<xStart> = [#5221 + #5420]') # get current absolute X position
  sub.append('G10 L20 P0 X0 Y0') # set current point as X0 Y0


  for i in range(yCount): # set rotation for the row
    sub.append('; Y Row {}'.format(i))
    if i % 2:
      rotation = yRotation
      offset = xEvenOffset
    else:
      rotation = xRotation
      offset = 0
    if i > 0: # move to next position
      sub.append('G10 L2 P0 X0 R0')
      sub.append('G0 X[#<xStart> + {}]'.format(offset))
      sub.append('G91')
      sub.append('G0 Y{}'.format(ySpacing))
      sub.append('G10 L20 P0 Y0')
      sub.append('G90')

    for i in range(xCount):
      sub.append('; X Col {}'.format(i))
      if i > 0: # move to next position
        sub.append('G91')
        sub.append('G10 L2 P0 R0')
        sub.append('G0 X{}'.format(xSpacing))
        sub.append('G90')
      sub.append('G10 L20 P0 X0')
      sub.append('G10 L2 P0 R{}'.format(rotation))
      if parent.partsTestRb.isChecked():
        sub.append('; Test Run no Plasma') # for testing
      else:
        pierceHeight = parent.pierceDelayLbl.text()
        pierceDelay = parent.pierceDelayLbl.text()
        cutHeight = parent.cutHeightLbl.text()
        sub.append('o<torch-probe> call [{}] [{}] [{}]'.format \
        (pierceHeight,pierceDelay,cutHeight))

      sub.append('{} call'.format(subName))


  sub.append('G10 L2 P0 X0 Y0')
  sub.append('M2')

  buildLoad(parent, sub)


def buildLoadCheck(parent):
  # check to see if the file exists then check to see if it is proper g code
  if os.path.exists(parent.selectedFileLbl.text()):
    parent.statusbar.showMessage('Building Wrapper')
    with open(parent.selectedFileLbl.text(), "r") as f:
       # returns a list of strings with \n removed
      sub = [x.strip() for x in f.readlines()]
    subIndex = next(i for i, s in enumerate(sub) if 'sub' in s)
    subName = sub[subIndex].split(' ')[0]
    # strip any program end lines % M2 M30
    programEnd = ['M2', 'm2', 'M30', 'm30', '%']
    for i in programEnd:
      if i in sub:
        itemCount = sub.count(i)
        for x in range(itemCount):
          del sub[sub.index(i)]
    sub.append('F75') # for testing

    xCount = parent.xPartsCountSb.value()
    xSpacing = parent.xPartsSpacingSb.value()
    xRotation = parent.xPartRotationSb.value()
    yCount = parent.yPartsCountSb.value()
    ySpacing = parent.yPartsSpacingSb.value()
    yRotation = parent.yPartRotationSb.value()

    if parent.yPartsCountSb.value() > 1:
      if parent.yPartsSpacingSb.value() != 0:
        for i in range(1, yCount):
          if i % 2:
            print('odd')
          else:
            print('even')
        return

      else:
        parent.statusbar.showMessage('Y Space must not be 0')

      if parent.xPartsCountSb.value() > 1:
        if parent.xPartsSpacingSb.value() != 0:
          sub.append('G10 L2 P0 R{}'.format(xRotation))
          sub.append('{} call'.format(subName))
          for i in range(1, xCount):
            sub.append('G91')
            sub.append('G10 L2 P0 R0')
            sub.append('G0 X{}'.format(xSpacing))
            sub.append('G90')
            sub.append('G10 L20 P0 X0')
            sub.append('G10 L2 P0 R{}'.format(xRotation))
            sub.append('{} call'.format(subName))
        else:
          parent.statusbar.showMessage('X Space must not be 0')

    else:
      if parent.xPartsCountSb.value() > 1:
        if parent.xPartsSpacingSb.value() > 0:
          
          sub.append('G10 L2 P0 R{}'.format(xRotation))
          sub.append('{} call'.format(subName))
          for i in range(1, parent.xPartsCountSb.value()):
            sub.append('G91')
            sub.append('G10 L2 P0 R0')
            sub.append('G0 X{}'.format(xSpacing))
            sub.append('G90')
            sub.append('G10 L20 P0 X0')
            sub.append('G10 L2 P0 R{}'.format(xRotation))
            sub.append('{} call'.format(subName))
        else:
          parent.statusbar.showMessage('X Space must be greater than 0')
      else:
        sub.append('G10 L2 P0 R{}'.format(xRotation))
        sub.append('{} call'.format(subName))

    sub.append('G10 L2 P0 X0 Y0')
    sub.append('M2')

    buildLoad(parent, sub)


  else:
    parent.statusbar.showMessage('Select a File First')

def buildLoad(parent, gcode):
  emcCommand = linuxcnc.command()
  contents = []
  with open('/tmp/qtpyvcp.ngc','w') as f:
    for line in gcode:
      contents.append(line)
    f.write('\n'.join(contents))
  emcCommand.reset_interpreter()
  emcCommand.program_open('/tmp/qtpyvcp.ngc')
  parent.statusbar.showMessage('File Loaded', 6000)



def buildSave(parent):
  pass

def gcodeLoad(parent):
  emcCommand = linuxcnc.command()
  gcode = []
  with open('/tmp/qtpyvcp.ngc','w') as f:
    for i in range(parent.gCodeList.count()):
      gcode.append(parent.gCodeList.item(i).text())
    f.write('\n'.join(gcode))
  emcCommand.reset_interpreter()
  emcCommand.program_open('/tmp/qtpyvcp.ngc')
  parent.statusbar.showMessage('File Loaded', 6000)


def gcodeSave(parent):
  gcode = []
  fileName = str(time.time()).split('.')[0] + '.ngc'
  filePath = os.path.join(HOME, 'linuxcnc', 'nc_files', fileName)
  try:
    with open(filePath,'w') as f:
      for i in range(parent.gCodeList.count()):
        gcode.append(parent.gCodeList.item(i).text())
      f.write('\n'.join(gcode))
  except (OSError, IOError) as error:
    parent.statusbar.showMessage(error, 6000)
  else:
    parent.statusbar.showMessage('File Saved as {}'.format(filePath), 6000)



