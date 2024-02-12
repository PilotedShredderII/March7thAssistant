# coding:utf-8
from qfluentwidgets import (SettingCardGroup, PushSettingCard, ScrollArea,
                            InfoBar, PrimaryPushSettingCard, Pivot, qrouter)
from qfluentwidgets import FluentIcon as FIF
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWidgets import QWidget, QLabel, QFileDialog, QVBoxLayout, QStackedWidget
from PyQt5.QtGui import QDesktopServices

from .common.style_sheet import StyleSheet
from managers.config_manager import config


class ToolsInterface(ScrollArea):
    """ Setting interface """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.parent = parent
        self.scrollWidget = QWidget()
        self.vBoxLayout = QVBoxLayout(self.scrollWidget)

        self.toolsLabel = QLabel(self.tr("工具箱"), self)

        self.ToolsGroup = SettingCardGroup(self.tr('工具箱'), self.scrollWidget)
        self.gameScreenshotCard = PushSettingCard(
            self.tr('捕获'),
            FIF.PHOTO,
            self.tr("游戏截图"),
            self.tr("检查程序获取的图像是否正确，支持OCR识别文字（可用于复制副本名称）")
        )

        self.__initWidget()

    def __initWidget(self):
        # self.resize(1000, 800)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 80, 0, 20)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)
        self.setObjectName('toolsInterface')

        # initialize style sheet
        self.scrollWidget.setObjectName('scrollWidget')
        self.toolsLabel.setObjectName('toolsLabel')
        StyleSheet.TOOLS_INTERFACE.apply(self)

        self.__initLayout()
        self.__connectSignalToSlot()

    def __initLayout(self):
        self.toolsLabel.move(36, 30)
        # add cards to group
        self.ToolsGroup.addSettingCard(self.gameScreenshotCard)

        self.ToolsGroup.titleLabel.setHidden(True)

        # add setting card group to layout
        self.vBoxLayout.setSpacing(28)
        self.vBoxLayout.setContentsMargins(36, 10, 36, 0)
        self.vBoxLayout.addWidget(self.ToolsGroup)

    def __onGameScreenshotCardClicked(self):
        from tasks.base.windowswitcher import WindowSwitcher
        from module.automation.screenshot import Screenshot
        if WindowSwitcher.check_and_switch(config.game_title_name):
            result = Screenshot.take_screenshot(config.game_title_name)
            if result:
                import tkinter as tk
                from .tools.screenshot import ScreenshotApp

                root = tk.Tk()
                app = ScreenshotApp(root, result[0])
                root.mainloop()

    def __connectSignalToSlot(self):
        """ connect signal to slot """
        self.gameScreenshotCard.clicked.connect(self.__onGameScreenshotCardClicked)
