from qtpyvcp.widgets.form_widgets.main_window import VCPMainWindow
from PyQt5.QtSql import QSqlDatabase

# Setup logging
from qtpyvcp.utilities import logger
LOG = logger.getLogger('qtpyvcp.' + __name__)

import plasma_v2.part_nest as partNest
import plasma_v2.nozzles as nozzles

import os
current_path = os.path.dirname(os.path.realpath(__file__)) + '/'


class MyMainWindow(VCPMainWindow):
  """Main window class for the VCP."""
  def __init__(self, *args, **kwargs):
    super(MyMainWindow, self).__init__(*args, **kwargs)

    db = QSqlDatabase.addDatabase('QSQLITE')
    db.setDatabaseName(current_path + 'plasma.db')
    if db.open():
      print("Connection success !")
    else:
      print("Connection failed !\n{}".format(db.lastError().text()))

    nozzles.Setup(self)
    partNest.initPartNest(self)


  def on_exitAppBtn_clicked(self):
    self.app.quit()

