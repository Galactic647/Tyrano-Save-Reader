from PySide2.QtCore import QMetaObject, QRect, QSize, Qt
from PySide2.QtGui import QFont
from PySide2.QtWidgets import (QMainWindow, QAction, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QTreeWidget, QLineEdit,
    QTreeWidgetItem, QProgressBar, QSizePolicy, QAbstractItemView, QPushButton, QSpacerItem, QRadioButton, QTabWidget,
    QGridLayout, QComboBox, QSpinBox, QMenuBar, QMenu, QListWidget, QListWidgetItem, QStackedWidget)


class TyranoBrowserUI(QMainWindow):
    def __init__(self, parent=None):
        super(TyranoBrowserUI, self).__init__(parent)
        if self.objectName():
            self.setObjectName('TyranoBrowserUI')
        self.resize(1111, 874)
        font = QFont()
        font.setPointSize(10)
        self.setFont(font)

        with open('ui/theme/dark-style.qss') as file:
            self.setStyleSheet(file.read())
        self.actionOpen_file = QAction(self)
        self.actionOpen_file.setObjectName('actionOpen_file')
        self.actionSave = QAction(self)
        self.actionSave.setObjectName('actionSave')
        self.actionSave_as = QAction(self)
        self.actionSave_as.setObjectName('actionSave_as')
        self.actionLoad_Template = QAction(self)
        self.actionLoad_Template.setObjectName('actionLoad_Template')
        self.actionAuto_Load_Template = QAction(self)
        self.actionAuto_Load_Template.setObjectName('actionAuto_Load_Template')
        self.actionAuto_Load_Template.setCheckable(True)
        self.actionAuto_Load_Template.setChecked(True)
        self.actionSave_Save_File = QAction(self)
        self.actionSave_Save_File.setObjectName('actionSave_Save_File')
        self.actionExport_Save_File = QAction(self)
        self.actionExport_Save_File.setObjectName('actionExport_Save_File')
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName('centralwidget')
        self.verticalLayoutWidget_2 = QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setObjectName('verticalLayoutWidget_2')
        self.verticalLayoutWidget_2.setGeometry(QRect(0, 10, 1111, 831))
        self.MainContainer = QVBoxLayout(self.verticalLayoutWidget_2)
        self.MainContainer.setObjectName('MainContainer')
        self.MainContainer.setContentsMargins(0, 0, 0, 0)
        self.InfoLabel = QLabel(self.verticalLayoutWidget_2)
        self.InfoLabel.setObjectName('InfoLabel')
        font1 = QFont()
        font1.setPointSize(9)
        self.InfoLabel.setFont(font1)
        self.InfoLabel.setAlignment(Qt.AlignCenter)

        self.MainContainer.addWidget(self.InfoLabel)

        self.ActionsSection = QTabWidget(self.verticalLayoutWidget_2)
        self.ActionsSection.setObjectName('ActionsSection')
        self.ActionsSection.setFont(font1)
        self.ActionsSection.setStyleSheet('')
        self.ScanTab = QWidget()
        self.ScanTab.setObjectName('ScanTab')
        self.verticalLayoutWidget = QWidget(self.ScanTab)
        self.verticalLayoutWidget.setObjectName('verticalLayoutWidget')
        self.verticalLayoutWidget.setGeometry(QRect(0, 0, 1101, 361))
        self.ScanActionBaseContainer = QVBoxLayout(self.verticalLayoutWidget)
        self.ScanActionBaseContainer.setObjectName('ScanActionBaseContainer')
        self.ScanActionBaseContainer.setContentsMargins(0, 0, 0, 0)
        self.ScanProgressBar = QProgressBar(self.verticalLayoutWidget)
        self.ScanProgressBar.setObjectName('ScanProgressBar')
        self.ScanProgressBar.setStyleSheet('')
        self.ScanProgressBar.setValue(24)
        self.ScanProgressBar.setTextVisible(False)

        self.ScanActionBaseContainer.addWidget(self.ScanProgressBar)

        self.ScanWidgetsContainer = QGridLayout()
        self.ScanWidgetsContainer.setObjectName('ScanWidgetsContainer')
        self.ScanActionContainer = QVBoxLayout()
        self.ScanActionContainer.setObjectName('ScanActionContainer')
        self.ScanButtonContainer = QHBoxLayout()
        self.ScanButtonContainer.setObjectName('ScanButtonContainer')
        self.ScanButtonContainer.setContentsMargins(5, -1, 5, -1)
        self.ScanButton = QPushButton(self.verticalLayoutWidget)
        self.ScanButton.setObjectName('ScanButton')
        self.ScanButton.setFont(font1)
        self.ScanButton.setStyleSheet('')

        self.ScanButtonContainer.addWidget(self.ScanButton)

        self.ButtonHSpacer = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.ScanButtonContainer.addItem(self.ButtonHSpacer)

        self.ClearButton = QPushButton(self.verticalLayoutWidget)
        self.ClearButton.setObjectName('ClearButton')
        self.ClearButton.setFont(font1)

        self.ScanButtonContainer.addWidget(self.ClearButton)

        self.ButtonHSpacerRight = QSpacerItem(125, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.ScanButtonContainer.addItem(self.ButtonHSpacerRight)


        self.ScanActionContainer.addLayout(self.ScanButtonContainer)

        self.ScanInput = QLineEdit(self.verticalLayoutWidget)
        self.ScanInput.setObjectName('ScanInput')
        self.ScanInput.setFont(font1)
        self.ScanInput.setStyleSheet('')

        self.ScanActionContainer.addWidget(self.ScanInput)

        self.ScanActionVFxdSpacer = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Maximum)

        self.ScanActionContainer.addItem(self.ScanActionVFxdSpacer)

        self.SearchByContainer = QHBoxLayout()
        self.SearchByContainer.setObjectName('SearchByContainer')
        self.SearchByContainer.setContentsMargins(10, -1, 5, -1)
        self.SearchByLabel = QLabel(self.verticalLayoutWidget)
        self.SearchByLabel.setObjectName('SearchByLabel')
        self.SearchByLabel.setFont(font1)

        self.SearchByContainer.addWidget(self.SearchByLabel)

        self.ValueRadioButton = QRadioButton(self.verticalLayoutWidget)
        self.ValueRadioButton.setObjectName('ValueRadioButton')
        self.ValueRadioButton.setFont(font1)
        self.ValueRadioButton.setChecked(True)

        self.SearchByContainer.addWidget(self.ValueRadioButton)

        self.NameRadioButton = QRadioButton(self.verticalLayoutWidget)
        self.NameRadioButton.setObjectName('NameRadioButton')
        self.NameRadioButton.setFont(font1)

        self.SearchByContainer.addWidget(self.NameRadioButton)

        self.SearchByHSpacer = QSpacerItem(50, 20, QSizePolicy.Maximum, QSizePolicy.Minimum)

        self.SearchByContainer.addItem(self.SearchByHSpacer)


        self.ScanActionContainer.addLayout(self.SearchByContainer)

        self.ScanActionVSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.ScanActionContainer.addItem(self.ScanActionVSpacer)

        self.FoundLabel = QLabel(self.verticalLayoutWidget)
        self.FoundLabel.setObjectName('FoundLabel')
        self.FoundLabel.setFont(font1)

        self.ScanActionContainer.addWidget(self.FoundLabel)


        self.ScanWidgetsContainer.addLayout(self.ScanActionContainer, 0, 1, 1, 1)

        self.ResultTab = QTreeWidget(self.verticalLayoutWidget)
        QTreeWidgetItem(self.ResultTab)
        QTreeWidgetItem(self.ResultTab)
        QTreeWidgetItem(self.ResultTab)
        QTreeWidgetItem(self.ResultTab)
        QTreeWidgetItem(self.ResultTab)
        QTreeWidgetItem(self.ResultTab)
        QTreeWidgetItem(self.ResultTab)
        QTreeWidgetItem(self.ResultTab)
        QTreeWidgetItem(self.ResultTab)
        QTreeWidgetItem(self.ResultTab)
        QTreeWidgetItem(self.ResultTab)
        QTreeWidgetItem(self.ResultTab)
        QTreeWidgetItem(self.ResultTab)
        QTreeWidgetItem(self.ResultTab)
        QTreeWidgetItem(self.ResultTab)
        self.ResultTab.setObjectName('ResultTab')
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ResultTab.sizePolicy().hasHeightForWidth())
        self.ResultTab.setSizePolicy(sizePolicy)
        self.ResultTab.setMinimumSize(QSize(700, 0))
        self.ResultTab.setFont(font1)
        self.ResultTab.setStyleSheet('')
        self.ResultTab.setEditTriggers(QAbstractItemView.DoubleClicked)
        self.ResultTab.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.ResultTab.setIndentation(0)
        self.ResultTab.setItemsExpandable(False)
        self.ResultTab.setExpandsOnDoubleClick(False)
        self.ResultTab.header().setMinimumSectionSize(100)
        self.ResultTab.header().setDefaultSectionSize(200)

        self.ScanWidgetsContainer.addWidget(self.ResultTab, 0, 0, 1, 1)

        self.ScanWidgetsContainer.setColumnStretch(0, 1)

        self.ScanActionBaseContainer.addLayout(self.ScanWidgetsContainer)

        self.ActionsSection.addTab(self.ScanTab, '')
        self.TemplateTab = QWidget()
        self.TemplateTab.setObjectName('TemplateTab')
        self.verticalLayoutWidget_4 = QWidget(self.TemplateTab)
        self.verticalLayoutWidget_4.setObjectName('verticalLayoutWidget_4')
        self.verticalLayoutWidget_4.setGeometry(QRect(0, 0, 1101, 361))
        self.VLayoutContainer = QVBoxLayout(self.verticalLayoutWidget_4)
        self.VLayoutContainer.setObjectName('VLayoutContainer')
        self.VLayoutContainer.setContentsMargins(0, 0, 0, 0)
        self.TemplateWidget = QTreeWidget(self.verticalLayoutWidget_4)
        QTreeWidgetItem(self.TemplateWidget)
        self.TemplateWidget.setObjectName('TemplateWidget')
        self.TemplateWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.TemplateWidget.header().setDefaultSectionSize(300)

        self.VLayoutContainer.addWidget(self.TemplateWidget)

        self.ActionsSection.addTab(self.TemplateTab, '')
        self.MetadataTab = QWidget()
        self.MetadataTab.setObjectName('MetadataTab')
        self.horizontalLayoutWidget = QWidget(self.MetadataTab)
        self.horizontalLayoutWidget.setObjectName('horizontalLayoutWidget')
        self.horizontalLayoutWidget.setGeometry(QRect(0, 0, 1101, 361))
        self.HLayoutBaseContainer = QHBoxLayout(self.horizontalLayoutWidget)
        self.HLayoutBaseContainer.setObjectName('HLayoutBaseContainer')
        self.HLayoutBaseContainer.setContentsMargins(0, 0, 0, 0)
        self.MSpacerLeft = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.HLayoutBaseContainer.addItem(self.MSpacerLeft)

        self.MVLayoutContainer = QVBoxLayout()
        self.MVLayoutContainer.setObjectName('MVLayoutContainer')
        self.MSpacerTop = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.MVLayoutContainer.addItem(self.MSpacerTop)

        self.MetadataContainer = QGridLayout()
        self.MetadataContainer.setObjectName('MetadataContainer')
        self.SlotsPerTabInput = QSpinBox(self.horizontalLayoutWidget)
        self.SlotsPerTabInput.setObjectName('SlotsPerTabInput')
        self.SlotsPerTabInput.setFont(font1)

        self.MetadataContainer.addWidget(self.SlotsPerTabInput, 3, 1, 1, 1)

        self.GameExecPath = QLineEdit(self.horizontalLayoutWidget)
        self.GameExecPath.setObjectName('GameExecPath')
        self.GameExecPath.setFont(font1)

        self.MetadataContainer.addWidget(self.GameExecPath, 1, 1, 1, 1)

        self.GameLabel = QLabel(self.horizontalLayoutWidget)
        self.GameLabel.setObjectName('GameLabel')
        self.GameLabel.setFont(font1)

        self.MetadataContainer.addWidget(self.GameLabel, 0, 0, 1, 1)

        self.SaveTabsLabel = QLabel(self.horizontalLayoutWidget)
        self.SaveTabsLabel.setObjectName('SaveTabsLabel')
        self.SaveTabsLabel.setFont(font1)

        self.MetadataContainer.addWidget(self.SaveTabsLabel, 2, 0, 1, 1)

        self.SlotStyleInput = QComboBox(self.horizontalLayoutWidget)
        self.SlotStyleInput.addItem('')
        self.SlotStyleInput.addItem('')
        self.SlotStyleInput.setObjectName('SlotStyleInput')
        self.SlotStyleInput.setFont(font1)
        self.SlotStyleInput.setEditable(True)

        self.MetadataContainer.addWidget(self.SlotStyleInput, 4, 1, 1, 1)

        self.GameExecutableLabel = QLabel(self.horizontalLayoutWidget)
        self.GameExecutableLabel.setObjectName('GameExecutableLabel')
        self.GameExecutableLabel.setFont(font1)

        self.MetadataContainer.addWidget(self.GameExecutableLabel, 1, 0, 1, 1)

        self.LocateGameButton = QPushButton(self.horizontalLayoutWidget)
        self.LocateGameButton.setObjectName('LocateGameButton')
        self.LocateGameButton.setFont(font1)

        self.MetadataContainer.addWidget(self.LocateGameButton, 1, 2, 1, 1)

        self.GameInput = QLineEdit(self.horizontalLayoutWidget)
        self.GameInput.setObjectName('GameInput')
        self.GameInput.setFont(font1)

        self.MetadataContainer.addWidget(self.GameInput, 0, 1, 1, 1)

        self.SlotsPerTabLabel = QLabel(self.horizontalLayoutWidget)
        self.SlotsPerTabLabel.setObjectName('SlotsPerTabLabel')
        self.SlotsPerTabLabel.setFont(font1)

        self.MetadataContainer.addWidget(self.SlotsPerTabLabel, 3, 0, 1, 1)

        self.SaveTabsInput = QSpinBox(self.horizontalLayoutWidget)
        self.SaveTabsInput.setObjectName('SaveTabsInput')
        self.SaveTabsInput.setFont(font1)

        self.MetadataContainer.addWidget(self.SaveTabsInput, 2, 1, 1, 1)

        self.SlotStyleLabel = QLabel(self.horizontalLayoutWidget)
        self.SlotStyleLabel.setObjectName('SlotStyleLabel')
        self.SlotStyleLabel.setFont(font1)

        self.MetadataContainer.addWidget(self.SlotStyleLabel, 4, 0, 1, 1)


        self.MVLayoutContainer.addLayout(self.MetadataContainer)

        self.MSpacerBottom = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.MVLayoutContainer.addItem(self.MSpacerBottom)


        self.HLayoutBaseContainer.addLayout(self.MVLayoutContainer)

        self.MSpacerRight = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.HLayoutBaseContainer.addItem(self.MSpacerRight)

        self.ActionsSection.addTab(self.MetadataTab, '')
        self.ConfigTab = QWidget()
        self.ConfigTab.setObjectName('ConfigTab')
        self.horizontalLayoutWidget_2 = QWidget(self.ConfigTab)
        self.horizontalLayoutWidget_2.setObjectName('horizontalLayoutWidget_2')
        self.horizontalLayoutWidget_2.setGeometry(QRect(0, 0, 1101, 361))
        self.CHLayoutBaseContainer = QHBoxLayout(self.horizontalLayoutWidget_2)
        self.CHLayoutBaseContainer.setObjectName('CHLayoutBaseContainer')
        self.CHLayoutBaseContainer.setContentsMargins(0, 0, 0, 0)
        self.CLVBaseContainer = QVBoxLayout()
        self.CLVBaseContainer.setObjectName('CLVBaseContainer')
        self.ExcludedLabel = QLabel(self.horizontalLayoutWidget_2)
        self.ExcludedLabel.setObjectName('ExcludedLabel')
        self.ExcludedLabel.setFont(font1)

        self.CLVBaseContainer.addWidget(self.ExcludedLabel)

        self.ExcludedCharacterList = QListWidget(self.horizontalLayoutWidget_2)
        QListWidgetItem(self.ExcludedCharacterList)
        QListWidgetItem(self.ExcludedCharacterList)
        QListWidgetItem(self.ExcludedCharacterList)
        self.ExcludedCharacterList.setObjectName('ExcludedCharacterList')
        self.ExcludedCharacterList.setStyleSheet('')

        self.CLVBaseContainer.addWidget(self.ExcludedCharacterList)


        self.CHLayoutBaseContainer.addLayout(self.CLVBaseContainer)

        self.CButtonContainer = QVBoxLayout()
        self.CButtonContainer.setObjectName('CButtonContainer')
        self.CBSpacerTop = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.CButtonContainer.addItem(self.CBSpacerTop)

        self.AddButton = QPushButton(self.horizontalLayoutWidget_2)
        self.AddButton.setObjectName('AddButton')
        self.AddButton.setFont(font1)

        self.CButtonContainer.addWidget(self.AddButton)

        self.EditButton = QPushButton(self.horizontalLayoutWidget_2)
        self.EditButton.setObjectName('EditButton')
        self.EditButton.setFont(font1)

        self.CButtonContainer.addWidget(self.EditButton)

        self.RemoveButton = QPushButton(self.horizontalLayoutWidget_2)
        self.RemoveButton.setObjectName('RemoveButton')
        self.RemoveButton.setFont(font1)

        self.CButtonContainer.addWidget(self.RemoveButton)

        self.CBSpacerBottom = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.CButtonContainer.addItem(self.CBSpacerBottom)

        self.CBWidthControl = QSpacerItem(120, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.CButtonContainer.addItem(self.CBWidthControl)


        self.CHLayoutBaseContainer.addLayout(self.CButtonContainer)

        self.CSpacerRight = QSpacerItem(300, 20, QSizePolicy.Maximum, QSizePolicy.Minimum)

        self.CHLayoutBaseContainer.addItem(self.CSpacerRight)

        self.ActionsSection.addTab(self.ConfigTab, '')

        self.MainContainer.addWidget(self.ActionsSection)

        self.SVSpacerMiddle = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.MainContainer.addItem(self.SVSpacerMiddle)

        self.ValueListsSection = QTabWidget(self.verticalLayoutWidget_2)
        self.ValueListsSection.setObjectName('ValueListsSection')
        self.ValueListsSection.setFont(font1)
        self.ValueListTabAction = QWidget()
        self.ValueListTabAction.setObjectName('ValueListTabAction')
        self.verticalLayoutWidget_3 = QWidget(self.ValueListTabAction)
        self.verticalLayoutWidget_3.setObjectName('verticalLayoutWidget_3')
        self.verticalLayoutWidget_3.setGeometry(QRect(0, 0, 1111, 411))
        self.VLVLayoutContainer = QVBoxLayout(self.verticalLayoutWidget_3)
        self.VLVLayoutContainer.setObjectName('VLVLayoutContainer')
        self.VLVLayoutContainer.setContentsMargins(0, 0, 0, 0)
        self.ValueListTab = QTreeWidget(self.verticalLayoutWidget_3)
        __qtreewidgetitem = QTreeWidgetItem(self.ValueListTab)
        QTreeWidgetItem(__qtreewidgetitem)
        __qtreewidgetitem1 = QTreeWidgetItem(self.ValueListTab)
        QTreeWidgetItem(__qtreewidgetitem1)
        QTreeWidgetItem(self.ValueListTab)
        self.ValueListTab.setObjectName('ValueListTab')
        self.ValueListTab.header().setDefaultSectionSize(300)

        self.VLVLayoutContainer.addWidget(self.ValueListTab)

        self.ValueListsSection.addTab(self.ValueListTabAction, '')
        self.RawListTabAction = QWidget()
        self.RawListTabAction.setObjectName('RawListTabAction')
        self.verticalLayoutWidget_6 = QWidget(self.RawListTabAction)
        self.verticalLayoutWidget_6.setObjectName('verticalLayoutWidget_6')
        self.verticalLayoutWidget_6.setGeometry(QRect(0, 0, 1111, 411))
        self.RLVLayoutContainer = QVBoxLayout(self.verticalLayoutWidget_6)
        self.RLVLayoutContainer.setObjectName('RLVLayoutContainer')
        self.RLVLayoutContainer.setContentsMargins(0, 0, 0, 0)
        self.RLStackedWidgets = QStackedWidget(self.verticalLayoutWidget_6)
        self.RLStackedWidgets.setObjectName('RLStackedWidgets')
        self.RLStackedWidgets.setEnabled(True)
        self.RLStackedWidgets.setStyleSheet('')
        self.page = QWidget()
        self.page.setObjectName('page')
        self.verticalLayoutWidget_7 = QWidget(self.page)
        self.verticalLayoutWidget_7.setObjectName('verticalLayoutWidget_7')
        self.verticalLayoutWidget_7.setGeometry(QRect(0, 0, 1101, 411))
        self.RLLVLayoutContainer = QVBoxLayout(self.verticalLayoutWidget_7)
        self.RLLVLayoutContainer.setObjectName('RLLVLayoutContainer')
        self.RLLVLayoutContainer.setContentsMargins(0, 0, 0, 0)
        self.LoadProgressBar = QProgressBar(self.verticalLayoutWidget_7)
        self.LoadProgressBar.setObjectName('LoadProgressBar')
        self.LoadProgressBar.setStyleSheet('')
        self.LoadProgressBar.setValue(24)
        self.LoadProgressBar.setTextVisible(False)

        self.RLLVLayoutContainer.addWidget(self.LoadProgressBar)

        self.LBVLayoutContainer = QGridLayout()
        self.LBVLayoutContainer.setObjectName('LBVLayoutContainer')
        self.LBSpacerLeft = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.LBVLayoutContainer.addItem(self.LBSpacerLeft, 1, 0, 1, 1)

        self.LBSpacerRight = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.LBVLayoutContainer.addItem(self.LBSpacerRight, 1, 3, 1, 1)

        self.LoadButton = QPushButton(self.verticalLayoutWidget_7)
        self.LoadButton.setObjectName('LoadButton')
        self.LoadButton.setFont(font1)
        self.LoadButton.setStyleSheet('')

        self.LBVLayoutContainer.addWidget(self.LoadButton, 1, 1, 1, 1)

        self.LBSpacerBottom = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.LBVLayoutContainer.addItem(self.LBSpacerBottom, 2, 1, 1, 1)

        self.LBSpacerTop = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.LBVLayoutContainer.addItem(self.LBSpacerTop, 0, 1, 1, 1)


        self.RLLVLayoutContainer.addLayout(self.LBVLayoutContainer)

        self.RLStackedWidgets.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName('page_2')
        self.verticalLayoutWidget_8 = QWidget(self.page_2)
        self.verticalLayoutWidget_8.setObjectName('verticalLayoutWidget_8')
        self.verticalLayoutWidget_8.setGeometry(QRect(0, 0, 1111, 411))
        self.TRLVLayoutContainer = QVBoxLayout(self.verticalLayoutWidget_8)
        self.TRLVLayoutContainer.setObjectName('TRLVLayoutContainer')
        self.TRLVLayoutContainer.setContentsMargins(0, 0, 0, 0)
        self.UnloadButton = QPushButton(self.verticalLayoutWidget_8)
        self.UnloadButton.setObjectName('UnloadButton')
        self.UnloadButton.setFont(font1)

        self.TRLVLayoutContainer.addWidget(self.UnloadButton)

        self.RawListTab = QTreeWidget(self.verticalLayoutWidget_8)
        self.RawListTab.setObjectName('RawListTab')
        self.RawListTab.setExpandsOnDoubleClick(False)
        self.RawListTab.header().setDefaultSectionSize(300)

        self.TRLVLayoutContainer.addWidget(self.RawListTab)

        self.RLStackedWidgets.addWidget(self.page_2)

        self.RLVLayoutContainer.addWidget(self.RLStackedWidgets)

        self.ValueListsSection.addTab(self.RawListTabAction, '')

        self.MainContainer.addWidget(self.ValueListsSection)

        self.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(self)
        self.menubar.setObjectName('menubar')
        self.menubar.setGeometry(QRect(0, 0, 1111, 26))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName('menuFile')
        self.menuSettings = QMenu(self.menubar)
        self.menuSettings.setObjectName('menuSettings')
        self.setMenuBar(self.menubar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menuFile.addAction(self.actionOpen_file)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionLoad_Template)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave_Save_File)
        self.menuFile.addAction(self.actionExport_Save_File)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_as)
        self.menuSettings.addAction(self.actionAuto_Load_Template)

        self.retranslate_ui()

        self.ActionsSection.setCurrentIndex(0)
        self.SlotStyleInput.setCurrentIndex(0)
        self.ValueListsSection.setCurrentIndex(0)
        self.RLStackedWidgets.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(self)
    # setupUi

    def retranslate_ui(self):
        self.setWindowTitle('Tyrano Browser')
        self.actionOpen_file.setText('Open...')
        self.actionSave.setText('Save Template')
        self.actionSave_as.setText('Save Template As...')
        self.actionLoad_Template.setText('Load Template...')
        self.actionAuto_Load_Template.setText('Auto Load Template')
        self.actionSave_Save_File.setText('Save Save File')
        self.actionExport_Save_File.setText('Export Save File...')
        self.InfoLabel.setText('No save loaded (Template - None)')
        self.ScanButton.setText('Scan')
        self.ClearButton.setText('Clear')
        self.SearchByLabel.setText('Search by')
        self.ValueRadioButton.setText('Value')
        self.NameRadioButton.setText('Name')
        self.FoundLabel.setText('Found: 0')
        ___qtreewidgetitem = self.ResultTab.headerItem()
        ___qtreewidgetitem.setText(2, 'Path');
        ___qtreewidgetitem.setText(1, 'Value');
        ___qtreewidgetitem.setText(0, 'Variable');

        __sortingEnabled = self.ResultTab.isSortingEnabled()
        self.ResultTab.setSortingEnabled(False)
        ___qtreewidgetitem1 = self.ResultTab.topLevelItem(0)
        ___qtreewidgetitem1.setText(2, 'x.y.z.pah.money');
        ___qtreewidgetitem1.setText(1, '500');
        ___qtreewidgetitem1.setText(0, 'money');
        ___qtreewidgetitem2 = self.ResultTab.topLevelItem(1)
        ___qtreewidgetitem2.setText(2, 'lmao.yeet');
        ___qtreewidgetitem2.setText(1, 'yes');
        ___qtreewidgetitem2.setText(0, 'yeet');
        ___qtreewidgetitem3 = self.ResultTab.topLevelItem(2)
        ___qtreewidgetitem3.setText(2, 'x.y.flower[4]');
        ___qtreewidgetitem3.setText(1, '23');
        ___qtreewidgetitem3.setText(0, 'flower[4]');
        ___qtreewidgetitem4 = self.ResultTab.topLevelItem(3)
        ___qtreewidgetitem4.setText(0, 'qwer');
        ___qtreewidgetitem5 = self.ResultTab.topLevelItem(4)
        ___qtreewidgetitem5.setText(0, 'qwer');
        ___qtreewidgetitem6 = self.ResultTab.topLevelItem(5)
        ___qtreewidgetitem6.setText(0, 'qwer');
        ___qtreewidgetitem7 = self.ResultTab.topLevelItem(6)
        ___qtreewidgetitem7.setText(0, 'qwer');
        ___qtreewidgetitem8 = self.ResultTab.topLevelItem(7)
        ___qtreewidgetitem8.setText(0, 'qwer');
        ___qtreewidgetitem9 = self.ResultTab.topLevelItem(8)
        ___qtreewidgetitem9.setText(0, 'qwer');
        ___qtreewidgetitem10 = self.ResultTab.topLevelItem(9)
        ___qtreewidgetitem10.setText(0, 'qwe');
        ___qtreewidgetitem11 = self.ResultTab.topLevelItem(10)
        ___qtreewidgetitem11.setText(0, 'rqw');
        ___qtreewidgetitem12 = self.ResultTab.topLevelItem(11)
        ___qtreewidgetitem12.setText(0, 'er');
        ___qtreewidgetitem13 = self.ResultTab.topLevelItem(12)
        ___qtreewidgetitem13.setText(0, 'qwer');
        ___qtreewidgetitem14 = self.ResultTab.topLevelItem(13)
        ___qtreewidgetitem14.setText(0, 'qwerr');
        ___qtreewidgetitem15 = self.ResultTab.topLevelItem(14)
        ___qtreewidgetitem15.setText(0, 'New Item');
        self.ResultTab.setSortingEnabled(__sortingEnabled)

        self.ActionsSection.setTabText(self.ActionsSection.indexOf(self.ScanTab), 'Scan')
        ___qtreewidgetitem16 = self.TemplateWidget.headerItem()
        ___qtreewidgetitem16.setText(1, 'Path');
        ___qtreewidgetitem16.setText(0, 'Description');

        __sortingEnabled1 = self.TemplateWidget.isSortingEnabled()
        self.TemplateWidget.setSortingEnabled(False)
        ___qtreewidgetitem17 = self.TemplateWidget.topLevelItem(0)
        ___qtreewidgetitem17.setText(1, '4');
        ___qtreewidgetitem17.setText(0, 'a');
        self.TemplateWidget.setSortingEnabled(__sortingEnabled1)

        self.ActionsSection.setTabText(self.ActionsSection.indexOf(self.TemplateTab), 'Template')
        self.GameExecPath.setText('')
        self.GameLabel.setText('Game:')
        self.SaveTabsLabel.setText('Save Tabs:')
        self.SlotStyleInput.setItemText(0, '{tab}-{tab_slot}')
        self.SlotStyleInput.setItemText(1, 'Save {slot}')

        self.GameExecutableLabel.setText('Game Executable:   ')
        self.LocateGameButton.setText('Locate...')
        self.GameInput.setText('')
        self.SlotsPerTabLabel.setText('Slots Per Tab:')
        self.SlotStyleLabel.setText('Slot Style:')
        self.ActionsSection.setTabText(self.ActionsSection.indexOf(self.MetadataTab), 'Metadata')
        self.ExcludedLabel.setText('Characters to Skip in Conversion')

        __sortingEnabled2 = self.ExcludedCharacterList.isSortingEnabled()
        self.ExcludedCharacterList.setSortingEnabled(False)
        ___qlistwidgetitem = self.ExcludedCharacterList.item(0)
        ___qlistwidgetitem.setText('+');
        ___qlistwidgetitem1 = self.ExcludedCharacterList.item(1)
        ___qlistwidgetitem1.setText('-');
        ___qlistwidgetitem2 = self.ExcludedCharacterList.item(2)
        ___qlistwidgetitem2.setText('@');
        self.ExcludedCharacterList.setSortingEnabled(__sortingEnabled2)

        self.AddButton.setText('Add')
        self.EditButton.setText('Edit')
        self.RemoveButton.setText('Remove')
        self.ActionsSection.setTabText(self.ActionsSection.indexOf(self.ConfigTab), 'Config')
        ___qtreewidgetitem18 = self.ValueListTab.headerItem()
        ___qtreewidgetitem18.setText(1, 'Value');
        ___qtreewidgetitem18.setText(0, 'Description');

        __sortingEnabled3 = self.ValueListTab.isSortingEnabled()
        self.ValueListTab.setSortingEnabled(False)
        ___qtreewidgetitem19 = self.ValueListTab.topLevelItem(0)
        ___qtreewidgetitem19.setText(0, 'Slot 1');
        ___qtreewidgetitem20 = ___qtreewidgetitem19.child(0)
        ___qtreewidgetitem20.setText(1, '500');
        ___qtreewidgetitem20.setText(0, 'Money');
        ___qtreewidgetitem21 = self.ValueListTab.topLevelItem(1)
        ___qtreewidgetitem21.setText(0, 'Slot 2');
        ___qtreewidgetitem22 = ___qtreewidgetitem21.child(0)
        ___qtreewidgetitem22.setText(1, '5000');
        ___qtreewidgetitem22.setText(0, 'Yes please');
        ___qtreewidgetitem23 = self.ValueListTab.topLevelItem(2)
        ___qtreewidgetitem23.setText(1, '300');
        ___qtreewidgetitem23.setText(0, 'lmao');
        self.ValueListTab.setSortingEnabled(__sortingEnabled3)

        self.ValueListsSection.setTabText(self.ValueListsSection.indexOf(self.ValueListTabAction), 'Value List')
        self.LoadButton.setText('Load')
        self.UnloadButton.setText('Unload')
        ___qtreewidgetitem24 = self.RawListTab.headerItem()
        ___qtreewidgetitem24.setText(1, 'Value');
        ___qtreewidgetitem24.setText(0, 'Description');
        self.ValueListsSection.setTabText(self.ValueListsSection.indexOf(self.RawListTabAction), 'Raw List')
        self.menuFile.setTitle('File')
        self.menuSettings.setTitle('Settings')
    # retranslateUi

