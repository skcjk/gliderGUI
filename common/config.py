# coding:utf-8
import sys
from enum import Enum

from PyQt6.QtCore import QLocale
from qfluentwidgets import (qconfig, QConfig, ConfigItem, OptionsConfigItem, BoolValidator,
                            OptionsValidator, RangeConfigItem, RangeValidator,
                            FolderListValidator, Theme, FolderValidator, ConfigSerializer, __version__)
from PyQt6.QtSerialPort import QSerialPortInfo

class Language(Enum):

    CHINESE_SIMPLIFIED = QLocale(QLocale.Language.Chinese, QLocale.Country.China)
    CHINESE_TRADITIONAL = QLocale(QLocale.Language.Chinese, QLocale.Country.China)
    ENGLISH = QLocale(QLocale.Language.English)
    AUTO = QLocale()


class LanguageSerializer(ConfigSerializer):

    def serialize(self, language):
        return language.value.name() if language != Language.AUTO else "Auto"

    def deserialize(self, value: str):
        return Language(QLocale(value)) if value != "Auto" else Language.AUTO


def isWin11():

    return sys.platform == 'win32' and sys.getwindowsversion().build >= 22000


class Config(QConfig):
    
    # main window
    micaEnabled = ConfigItem("MainWindow", "MicaEnabled", isWin11(), BoolValidator())
    dpiScale = OptionsConfigItem(
        "MainWindow", "DpiScale", "Auto", OptionsValidator([1, 1.25, 1.5, 1.75, 2, "Auto"]), restart=True)
    language = OptionsConfigItem(
        "MainWindow", "Language", Language.AUTO, OptionsValidator(Language), LanguageSerializer(), restart=True)
    
    # serail
    availablPorts = QSerialPortInfo.availablePorts()
    portList = sorted([port.portName() for port in availablPorts], key=lambda x: int(x[3:]))
    if len(portList) == 0:
        portList =  [""]
    port = OptionsConfigItem("Serial", "COM", portList[0], OptionsValidator(portList))
    baudrate = OptionsConfigItem("Serial", "Baudrate", 9600, OptionsValidator([4800, 9600, 14400, 19200, 38400, 43000, 57600, 76800, 115200]))

    
    glideTimeCard  = RangeConfigItem("MainWindow", "glideTimeCard", 0, RangeValidator(-99999, 99999))
    cmdCard  = RangeConfigItem("MainWindow", "cmdCard", 0, RangeValidator(0, 8))
    sliderDownCard = RangeConfigItem("MainWindow", "sliderDownCard", 0, RangeValidator(-99999, 99999))
    sliderUpCard = RangeConfigItem("MainWindow", "sliderUpCard", 0, RangeValidator(-99999, 99999))
    sliderSpeedCard = RangeConfigItem("MainWindow", "sliderSpeedCard", 0, RangeValidator(-99999, 99999))
    oilDownCard = RangeConfigItem("MainWindow", "oilDownCard", 0, RangeValidator(-99999, 99999))
    oilUpCard = RangeConfigItem("MainWindow", "oilUpCard", 0, RangeValidator(-99999, 99999))
    sliderAngelCard = RangeConfigItem("MainWindow", "sliderAngelCard", 0, RangeValidator(-99999, 99999))
    timeIntervalCard = RangeConfigItem("MainWindow", "timeIntervalCard", 0, RangeValidator(-99999, 99999))
    throwDepthCard = RangeConfigItem("MainWindow", "throwDepthCard", 0, RangeValidator(-99999, 99999))

    
cfg = Config()
cfg.themeMode.value = Theme.AUTO
qconfig.load('config.json', cfg)