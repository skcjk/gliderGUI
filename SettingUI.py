from qfluentwidgets import (ScrollArea, ExpandLayout,
                            SettingCardGroup,
                            OptionsSettingCard, CustomColorSettingCard,
                            setTheme, InfoBar,
                            setThemeColor)
from PyQt6.QtWidgets import QWidget, QLabel
from qfluentwidgets import FluentIcon as FIF
from common.config import cfg
from PyQt6.QtCore import Qt
from common.style_sheet import StyleSheet

# SettingInterface class inherits from ScrollArea and provides a settings interface
class SettingInterface(ScrollArea):
    """
    A settings interface allowing users to customize application settings like theme, color, and zoom.

    Attributes:
        scrollWidget (QWidget): The widget contained within the scroll area.
        expandLayout (ExpandLayout): The layout managing the settings cards.
        settingLabel (QLabel): The label displaying the settings title.
        personalGroup (SettingCardGroup): Group of setting cards for personalization settings.
        themeCard (OptionsSettingCard): Card for selecting the application theme.
        themeColorCard (CustomColorSettingCard): Card for selecting the theme color.
        zoomCard (OptionsSettingCard): Card for selecting the interface zoom level.
    
    Args:
        parent (QWidget, optional): The parent widget. Defaults to None.
    
    Last modified: 2024-07-01 by 申凯诚
    """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.scrollWidget = QWidget()
        self.expandLayout = ExpandLayout(self.scrollWidget)

        # setting label
        self.settingLabel = QLabel(self.tr("设置"), self)

        # personalization
        self.personalGroup = SettingCardGroup(
            self.tr('个性化'), self.scrollWidget)
        self.themeCard = OptionsSettingCard(
            cfg.themeMode,
            FIF.BRUSH,
            self.tr('应用主题'),
            self.tr("调整你的应用外观"),
            texts=[
                self.tr('浅色'), self.tr('深色'),
                self.tr('跟随系统设置')
            ],
            parent=self.personalGroup
        )
        self.themeColorCard = CustomColorSettingCard(
            cfg.themeColor,
            FIF.PALETTE,
            self.tr('主题色'),
            self.tr('调整你的应用的主题色'),
            self.personalGroup
        )
        self.zoomCard = OptionsSettingCard(
            cfg.dpiScale,
            FIF.ZOOM,
            self.tr("界面缩放"),
            self.tr("调整小部件和字体的大小"),
            texts=[
                "100%", "125%", "150%", "175%", "200%",
                self.tr("跟随系统设置")
            ],
            parent=self.personalGroup
        )

        self.__initWidget()

    def __initWidget(self):
        """
        Initializes the widget properties, including size, scroll policies, margins, and stylesheet.

        Last modified: 2024-07-01 by 申凯诚
        """

        self.resize(1000, 800)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 80, 0, 20)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)
        self.setObjectName('settingInterface')

        # initialize style sheet
        self.scrollWidget.setObjectName('scrollWidget')
        self.settingLabel.setObjectName('settingLabel')
        StyleSheet.SETTING_INTERFACE.apply(self)

        # initialize layout
        self.__initLayout()
        self.__connectSignalToSlot()

    def __initLayout(self):
        """
        Initializes the layout by positioning and adding setting cards to the expand layout.

        Last modified: 2024-07-01 by 申凯诚
        """

        self.settingLabel.move(36, 30)

        # add cards to group
        self.personalGroup.addSettingCard(self.themeCard)
        self.personalGroup.addSettingCard(self.themeColorCard)
        self.personalGroup.addSettingCard(self.zoomCard)

        # add setting card group to layout
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(36, 10, 36, 0)
        self.expandLayout.addWidget(self.personalGroup)

    def __connectSignalToSlot(self):
        """
        Connects signals to slots to handle theme and color changes, and to show a restart tooltip.

        Last modified: 2024-07-01 by 申凯诚
        """

        cfg.appRestartSig.connect(self.__showRestartTooltip)

        # personalization
        self.themeCard.optionChanged.connect(lambda ci: setTheme(cfg.get(ci)))
        self.themeColorCard.colorChanged.connect(lambda c: setThemeColor(c))

    def __showRestartTooltip(self):
        """
        Displays a tooltip informing the user that the application needs to be restarted for changes to take effect.

        Last modified: 2024-07-01 by 申凯诚
        """
        
        InfoBar.success(
            self.tr('设置成功'),
            self.tr('重启软件生效'),
            duration=1500,
            parent=self
        )