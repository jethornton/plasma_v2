from functools import partial
import os
import math

HOME = os.path.expanduser("~")

def initCreate(parent):
  parent.squareGenFileBtn.clicked.connect(partial(squareSubroutine, parent))

def squareSubroutine(parent):
  """
  feed rate must be set
  hypotenuse * sin angle a = length of leg
  length of leg * the square root of 2 = length of the hypotenuse
  hypotenuse * math.sin(math.radians(45)) = length of leg
  Note that all of the trig functions convert between an angle and the ratio of
  two sides  of a triangle. cos, sin, and tan take an angle in radians as input
  and return the ratio; acos, asin, and atan take a ratio as input and return an
  angle in radians. You only convert the angles, never the ratios.
  """
  part = []
  subName = parent.squareSubName.text()
  leadIn = float(parent.squareLeadIn.text())
  leadInLeg = leadIn * math.sin(math.radians(45))
  leadOut = float(parent.squareLeadOut.text())
  leadOutLeg = leadIn * math.sin(math.radians(45))
  xPlus = float(parent.xSquareWidth.text()) + leadInLeg
  xMinus = float(parent.xSquareStart.text()) + leadInLeg
  yPlus = float(parent.ySquareDepth.text()) + leadInLeg
  yMinus = float(parent.ySquareStart.text()) + leadInLeg
  xPlusStr = str(xPlus)
  xMinusStr = str(xMinus)
  yPlusStr = str(yPlus)
  yMinusStr = str(yMinus)
  if subName.isdigit():
    part.append('o{} sub'.format(subName)) # start a numbered subroutine
  else:
    part.append('o<{}> sub'.format(subName)) # start a named subroutine
  if leadIn <> '0':  # lead in move
    part.append('G3 X{} Y{} I{} J{}'.format(leadInLeg, leadInLeg, 0, leadInLeg))
  part.append('G1 X{} Y{}'.format(xMinus, yPlus)) # basic box
  part.append('G1 X{} Y{}'.format(xPlus, yPlus)) #
  part.append('G1 X{} Y{}'.format(xPlus, yMinus)) #
  part.append('G1 X{} Y{}'.format(xMinus, yMinus)) #
  if leadOut <> '0': # calculate lead out arc
    part.append('G3 X0 Y0 I0 J-{}'.format(leadOutLeg)) #
  if subName.isdigit():
    part.append('o{} endsub'.format(subName)) # end a numbered subroutine
  else:
    part.append('o<{}> endsub'.format(subName)) # end a named subroutine

  fileName = subName + '.ngc'
  filePath = os.path.join(HOME, 'linuxcnc', 'parts', fileName)
  try:
    with open(filePath,'w') as f:
      for line in part:
        f.write(line + '\n')
  except (OSError, IOError) as error:
    parent.statusbar.showMessage(error, 6000)
  else:
    parent.statusbar.showMessage('File Saved as {}'.format(filePath), 6000)

  #for line in part:
  #  print(line)
