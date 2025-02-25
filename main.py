# coding:utf-8
import os
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication
from qfluentwidgets import (NavigationItemPosition, 
                            FluentWindow, FluentBackgroundTheme,
                            FluentTranslator)
from qfluentwidgets import FluentIcon as FIF
from common.config import cfg
from common.signal_bus import signalBus
from SettingUI import SettingInterface

from MainWindow import MainWindowInterface

# Window class inherits from FluentWindow and serves as the main application window
class Window(FluentWindow):

    def __init__(self):
        super().__init__()
        self.initWindow()

        # create sub interface
        self.mainWindow = MainWindowInterface(self)
        self.settingInterface = SettingInterface(self)

        signalBus.switchToSampleCard.connect(self.switchToSample)

        self.initNavigation()

    def initNavigation(self):
        self.addSubInterface(self.mainWindow, FIF.CONNECT, '主界面', NavigationItemPosition.SCROLL)

        self.addSubInterface(self.settingInterface, FIF.SETTING, '设置', NavigationItemPosition.BOTTOM)

    def initWindow(self):
        """
        Initializes the main window properties such as size, title, icon, and position.

        Last modified: 2024-07-01 by 申凯诚
        """

        self.resize(800, 600)
        self.setWindowIcon(QIcon('./resource/logo.png'))
        self.setWindowTitle('标题')

        self.setMicaEffectEnabled(False)

        desktop = QApplication.screens()[0].availableGeometry() 
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)

        # use custom background color theme (only available when the mica effect is disabled)
        self.setCustomBackgroundColor(*FluentBackgroundTheme.DEFAULT_BLUE)

        self.show()
        QApplication.processEvents()
    
    def switchToSample(self, routeKey, index):
        """ switch to sample """
        self.stackedWidget.setCurrentWidget(getattr(self, routeKey), False)
        
if __name__ == '__main__':

    # enable dpi scale
    if cfg.get(cfg.dpiScale) != "Auto":
        os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
        os.environ["QT_SCALE_FACTOR"] = str(cfg.get(cfg.dpiScale))

    # create application
    app = QApplication(sys.argv)
    app.setAttribute(Qt.ApplicationAttribute.AA_DontCreateNativeWidgetSiblings)

    # internationalization
    locale = cfg.get(cfg.language).value
    translator = FluentTranslator(locale)

    app.installTranslator(translator)

    # create main window
    w = Window()
    w.show()

    app.exec()
