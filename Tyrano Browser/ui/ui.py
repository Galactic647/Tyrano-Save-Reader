from ui.widget import CustomEditTreeWidget

from PySide2.QtCore import QMetaObject, QRect, QSize, Qt
from PySide2.QtGui import QFont
from PySide2.QtWidgets import (QMainWindow, QAction, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QTreeWidget, QLineEdit,
    QTreeWidgetItem, QProgressBar, QSizePolicy, QAbstractItemView, QPushButton, QSpacerItem, QRadioButton, QTabWidget,
    QGridLayout, QComboBox, QSpinBox, QMenuBar, QMenu, QListWidget, QStackedWidget)


class TyranoBrowserUI(QMainWindow):
    def __init__(self, parent=None):
        super(TyranoBrowserUI, self).__init__(parent)
        
        self.resize(1111, 874)
        font = QFont()
        font.setPointSize(9)
        self.setFont(font)

        with open('ui/theme/dark-style.qss') as file:
            self.setStyleSheet(file.read())

        self.centralwidget = QWidget(self)
        self.setCentralWidget(self.centralwidget)

        # ----- Menu Bar -----
        self.menubar = QMenuBar(self)
        self.menubar.setGeometry(QRect(0, 0, 1111, 26))
        self.menuFile = QMenu(self.menubar)
        self.menuSettings = QMenu(self.menubar)
        self.setMenuBar(self.menubar)

        self.actionOpen_file = QAction(self)
        self.actionSave = QAction(self)
        self.actionSave_as = QAction(self)
        self.actionLoad_Template = QAction(self)
        self.actionAuto_Load_Template = QAction(self)
        self.actionAuto_Load_Template.setCheckable(True)
        self.actionAuto_Load_Template.setChecked(True)
        self.actionSave_Save_File = QAction(self)
        self.actionExport_Save_File = QAction(self)

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
        
        self.BaseVLayoutWidget = QWidget(self.centralwidget)
        self.BaseVLayoutWidget.setGeometry(QRect(0, 10, 1111, 831))

        # ----- Main Widget Area -----
        self.MainContainer = QVBoxLayout(self.centralwidget)
        self.MainContainer.setContentsMargins(0, 0, 0, 0)
        self.MainContainer.addWidget(self.BaseVLayoutWidget)

        self.InfoLabel = QLabel(self.BaseVLayoutWidget)
        self.InfoLabel.setFont(font)
        self.InfoLabel.setAlignment(Qt.AlignCenter)
        self.MainContainer.addWidget(self.InfoLabel)

        # ----- Actions Section -----
        self.ActionsSection = QTabWidget(self.BaseVLayoutWidget)
        self.ActionsSection.setFont(font)
        
        # ----- Tab Widget - Scan Tab -----
        self.ScanTab = QWidget()
        self.ScanTabVLayoutWidget = QWidget(self.ScanTab)
        self.ScanTabVLayoutWidget.setGeometry(QRect(0, 0, 1101, 361))
        self.ScanActionBaseContainer = QVBoxLayout(self.ScanTabVLayoutWidget)
        self.ScanActionBaseContainer.setContentsMargins(0, 0, 0, 0)

        self.ScanProgressBar = QProgressBar(self.ScanTabVLayoutWidget)
        self.ScanProgressBar.setObjectName('ScanProgressBar')
        self.ScanProgressBar.setTextVisible(False)
        self.ScanActionBaseContainer.addWidget(self.ScanProgressBar)

        self.ScanButtonContainer = QHBoxLayout()
        self.ScanButtonContainer.setContentsMargins(5, -1, 5, -1)

        self.ScanButton = QPushButton(self.ScanTabVLayoutWidget)
        self.ScanButton.setFont(font)
        self.ScanButtonContainer.addWidget(self.ScanButton)

        self.ButtonHSpacerMiddle = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.ScanButtonContainer.addItem(self.ButtonHSpacerMiddle)

        self.ClearButton = QPushButton(self.ScanTabVLayoutWidget)
        self.ClearButton.setFont(font)
        self.ScanButtonContainer.addWidget(self.ClearButton)

        self.ButtonHSpacerRight = QSpacerItem(125, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.ScanButtonContainer.addItem(self.ButtonHSpacerRight)

        self.ScanActionContainer = QVBoxLayout()
        self.ScanActionContainer.addLayout(self.ScanButtonContainer)

        self.ScanInput = QLineEdit(self.ScanTabVLayoutWidget)
        self.ScanInput.setFont(font)
        self.ScanActionContainer.addWidget(self.ScanInput)

        self.ScanActionVSpacerMiddle = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Maximum)
        self.ScanActionContainer.addItem(self.ScanActionVSpacerMiddle)

        self.SearchByContainer = QHBoxLayout()
        self.SearchByContainer.setContentsMargins(10, -1, 5, -1)

        self.SearchByLabel = QLabel(self.ScanTabVLayoutWidget)
        self.SearchByLabel.setFont(font)
        self.SearchByContainer.addWidget(self.SearchByLabel)

        self.ValueRadioButton = QRadioButton(self.ScanTabVLayoutWidget)
        self.ValueRadioButton.setFont(font)
        self.ValueRadioButton.setChecked(True)
        self.SearchByContainer.addWidget(self.ValueRadioButton)

        self.NameRadioButton = QRadioButton(self.ScanTabVLayoutWidget)
        self.NameRadioButton.setFont(font)
        self.SearchByContainer.addWidget(self.NameRadioButton)

        self.SearchByHSpacerRight = QSpacerItem(50, 20, QSizePolicy.Maximum, QSizePolicy.Minimum)
        self.SearchByContainer.addItem(self.SearchByHSpacerRight)

        self.ScanActionContainer.addLayout(self.SearchByContainer)

        self.ScanActionVSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.ScanActionContainer.addItem(self.ScanActionVSpacer)

        self.FoundLabel = QLabel(self.ScanTabVLayoutWidget)
        self.FoundLabel.setFont(font)
        self.ScanActionContainer.addWidget(self.FoundLabel)

        self.ResultTab = QTreeWidget(self.ScanTabVLayoutWidget)
    
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ResultTab.sizePolicy().hasHeightForWidth())
        self.ResultTab.setSizePolicy(sizePolicy)

        self.ResultTab.setMinimumSize(QSize(700, 0))
        self.ResultTab.setFont(font)
        self.ResultTab.setEditTriggers(QAbstractItemView.DoubleClicked)
        self.ResultTab.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.ResultTab.setSortingEnabled(False)
        self.ResultTab.setIndentation(0)
        self.ResultTab.setItemsExpandable(False)
        self.ResultTab.setExpandsOnDoubleClick(False)
        
        self.ScanWidgetsContainer = QGridLayout()
        self.ScanWidgetsContainer.addWidget(self.ResultTab, 0, 0, 1, 1)
        self.ScanWidgetsContainer.setColumnStretch(0, 1)
        self.ScanWidgetsContainer.addLayout(self.ScanActionContainer, 0, 1, 1, 1)
        self.ScanActionBaseContainer.addLayout(self.ScanWidgetsContainer)

        self.ActionsSection.addTab(self.ScanTab, '')

        # ----- Tab Widget - Template Tab -----
        self.TemplateTab = QWidget()
        self.TemplateTabVLayoutWidget = QWidget(self.TemplateTab)
        self.TemplateTabVLayoutWidget.setGeometry(QRect(0, 0, 1101, 361))
        self.TemplateContainer = QVBoxLayout(self.TemplateTabVLayoutWidget)
        self.TemplateContainer.setContentsMargins(0, 0, 0, 0)

        # TODO
        # 1. Make a custom context menu for right clicking (add group, remove group, edit group, etc.)
        self.TemplateWidget = CustomEditTreeWidget([1], self.TemplateTabVLayoutWidget)
        self.TemplateWidget.setSortingEnabled(False)
        self.TemplateWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.TemplateContainer.addWidget(self.TemplateWidget)

        self.ActionsSection.addTab(self.TemplateTab, '')

        # ----- Tab Widget - Metadata Tab -----
        self.MetadataTab = QWidget()
        self.MetadataTabHLayoutWidget = QWidget(self.MetadataTab)
        self.MetadataTabHLayoutWidget.setGeometry(QRect(0, 0, 1101, 361))
        self.HLayoutBaseContainer = QHBoxLayout(self.MetadataTabHLayoutWidget)
        self.HLayoutBaseContainer.setContentsMargins(0, 0, 0, 0)

        self.MSpacerLeft = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.HLayoutBaseContainer.addItem(self.MSpacerLeft)

        self.MVLayoutContainer = QVBoxLayout()

        self.MSpacerTop = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.MVLayoutContainer.addItem(self.MSpacerTop)

        self.MetadataContainer = QGridLayout()

        self.SlotsPerTabInput = QSpinBox(self.MetadataTabHLayoutWidget)
        self.SlotsPerTabInput.setFont(font)
        self.MetadataContainer.addWidget(self.SlotsPerTabInput, 3, 1, 1, 1)

        self.GameExecPath = QLineEdit(self.MetadataTabHLayoutWidget)
        self.GameExecPath.setFont(font)
        self.MetadataContainer.addWidget(self.GameExecPath, 1, 1, 1, 1)

        self.GameLabel = QLabel(self.MetadataTabHLayoutWidget)
        self.GameLabel.setFont(font)
        self.MetadataContainer.addWidget(self.GameLabel, 0, 0, 1, 1)

        self.SaveTabsLabel = QLabel(self.MetadataTabHLayoutWidget)
        self.SaveTabsLabel.setFont(font)
        self.MetadataContainer.addWidget(self.SaveTabsLabel, 2, 0, 1, 1)

        self.SlotStyleInput = QComboBox(self.MetadataTabHLayoutWidget)
        # TODO deal with these two items
        self.SlotStyleInput.addItem('')
        self.SlotStyleInput.addItem('')
        self.SlotStyleInput.setFont(font)
        self.SlotStyleInput.setEditable(True)
        self.MetadataContainer.addWidget(self.SlotStyleInput, 4, 1, 1, 1)

        self.GameExecutableLabel = QLabel(self.MetadataTabHLayoutWidget)
        self.GameExecutableLabel.setFont(font)
        self.MetadataContainer.addWidget(self.GameExecutableLabel, 1, 0, 1, 1)

        self.LocateGameButton = QPushButton(self.MetadataTabHLayoutWidget)
        self.LocateGameButton.setFont(font)
        self.MetadataContainer.addWidget(self.LocateGameButton, 1, 2, 1, 1)

        self.GameInput = QLineEdit(self.MetadataTabHLayoutWidget)
        self.GameInput.setFont(font)
        self.MetadataContainer.addWidget(self.GameInput, 0, 1, 1, 1)

        self.SlotsPerTabLabel = QLabel(self.MetadataTabHLayoutWidget)
        self.SlotsPerTabLabel.setFont(font)
        self.MetadataContainer.addWidget(self.SlotsPerTabLabel, 3, 0, 1, 1)

        self.SaveTabsInput = QSpinBox(self.MetadataTabHLayoutWidget)
        self.SaveTabsInput.setFont(font)
        self.MetadataContainer.addWidget(self.SaveTabsInput, 2, 1, 1, 1)

        self.SlotStyleLabel = QLabel(self.MetadataTabHLayoutWidget)
        self.SlotStyleLabel.setFont(font)
        self.MetadataContainer.addWidget(self.SlotStyleLabel, 4, 0, 1, 1)

        self.MVLayoutContainer.addLayout(self.MetadataContainer)

        self.MSpacerBottom = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.MVLayoutContainer.addItem(self.MSpacerBottom)

        self.HLayoutBaseContainer.addLayout(self.MVLayoutContainer)

        self.MSpacerRight = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.HLayoutBaseContainer.addItem(self.MSpacerRight)

        self.ActionsSection.addTab(self.MetadataTab, '')

        # ----- Tab Widget - Config Tab -----
        self.ConfigTab = QWidget()
        self.ConfigTabLayoutWidget = QWidget(self.ConfigTab)
        self.ConfigTabLayoutWidget.setGeometry(QRect(0, 0, 1101, 361))
        self.ConfigHBaseContainer = QHBoxLayout(self.ConfigTabLayoutWidget)
        self.ConfigHBaseContainer.setContentsMargins(0, 0, 0, 0)

        self.ConfigListBaseContainer = QVBoxLayout()

        self.ExcludedLabel = QLabel(self.ConfigTabLayoutWidget)
        self.ExcludedLabel.setObjectName('ExcludedLabel')
        self.ExcludedLabel.setFont(font)
        self.ConfigListBaseContainer.addWidget(self.ExcludedLabel)

        self.ExcludedCharacterList = QListWidget(self.ConfigTabLayoutWidget)
        self.ExcludedCharacterList.setSortingEnabled(False)
        self.ExcludedCharacterList.setObjectName('ExcludedCharacterList')
        self.ConfigListBaseContainer.addWidget(self.ExcludedCharacterList)

        self.ConfigHBaseContainer.addLayout(self.ConfigListBaseContainer)

        self.ConfigButtonContainer = QVBoxLayout()

        self.CBSpacerTop = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.ConfigButtonContainer.addItem(self.CBSpacerTop)

        self.AddButton = QPushButton(self.ConfigTabLayoutWidget)
        self.AddButton.setFont(font)
        self.ConfigButtonContainer.addWidget(self.AddButton)

        self.EditButton = QPushButton(self.ConfigTabLayoutWidget)
        self.EditButton.setFont(font)
        self.ConfigButtonContainer.addWidget(self.EditButton)

        self.RemoveButton = QPushButton(self.ConfigTabLayoutWidget)
        self.RemoveButton.setFont(font)

        self.ConfigButtonContainer.addWidget(self.RemoveButton)

        self.CBSpacerBottom = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.ConfigButtonContainer.addItem(self.CBSpacerBottom)

        self.CBWidthControl = QSpacerItem(120, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.ConfigButtonContainer.addItem(self.CBWidthControl)

        self.ConfigHBaseContainer.addLayout(self.ConfigButtonContainer)

        self.CSpacerRight = QSpacerItem(300, 20, QSizePolicy.Maximum, QSizePolicy.Minimum)
        self.ConfigHBaseContainer.addItem(self.CSpacerRight)

        self.ActionsSection.addTab(self.ConfigTab, '')

        self.MainContainer.addWidget(self.ActionsSection)

        # ----- Intermediate Widget Area -----
        self.IntermediateSpacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.MainContainer.addItem(self.IntermediateSpacer)

        # ---- Value List Section -----
        self.ValueListsSection = QTabWidget(self.BaseVLayoutWidget)
        self.ValueListsSection.setFont(font)

        # ----- Tab Widget - Value List Tab -----
        self.ValueListTab = QWidget()
        self.ValueListTabVLayoutWidget = QWidget(self.ValueListTab)
        self.ValueListTabVLayoutWidget.setGeometry(QRect(0, 0, 1111, 411))
        self.ValueListContainer = QVBoxLayout(self.ValueListTabVLayoutWidget)
        self.ValueListContainer.setContentsMargins(0, 0, 0, 0)

        self.ValueListWidget = CustomEditTreeWidget([0], self.ValueListTabVLayoutWidget)
        self.ValueListWidget.setSortingEnabled(False)
        self.ValueListContainer.addWidget(self.ValueListWidget)

        self.ValueListsSection.addTab(self.ValueListTab, '')

        # ----- Tab Widget - Raw List Tab -----
        self.RawListTab = QWidget()
        self.RawListActionContainerVLayoutWidget = QWidget(self.RawListTab)
        self.RawListActionContainerVLayoutWidget.setGeometry(QRect(0, 0, 1111, 351))
        self.RawListActionContainer = QVBoxLayout(self.RawListActionContainerVLayoutWidget)
        self.RawListActionContainer.setContentsMargins(0, 0, 0, 0)
        
        self.RawListActionContainerWidget = QStackedWidget(self.RawListActionContainerVLayoutWidget)
        
        # ----- Manual Load Page -----
        self.ManualLoadPage = QWidget()
        self.ManualLoadPageLayoutWidget = QWidget(self.ManualLoadPage)
        self.ManualLoadPageLayoutWidget.setGeometry(QRect(0, 0, 1101, 351))
        self.ManualLoadContainer = QVBoxLayout(self.ManualLoadPageLayoutWidget)
        self.ManualLoadContainer.setContentsMargins(0, 0, 0, 0)

        self.LoadProgressBar = QProgressBar(self.ManualLoadPageLayoutWidget)
        self.LoadProgressBar.setObjectName('LoadProgressBar')
        self.LoadProgressBar.setTextVisible(False)
        self.ManualLoadContainer.addWidget(self.LoadProgressBar)

        self.LoadButtonContainer = QGridLayout()

        self.LoadButtonSpacerLeft = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.LoadButtonContainer.addItem(self.LoadButtonSpacerLeft, 1, 0, 1, 1)

        self.LoadButtonSpacerRight = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.LoadButtonContainer.addItem(self.LoadButtonSpacerRight, 1, 3, 1, 1)

        self.LoadButton = QPushButton(self.ManualLoadPageLayoutWidget)
        self.LoadButton.setObjectName('LoadButton')
        self.LoadButton.setFont(font)
        self.LoadButtonContainer.addWidget(self.LoadButton, 1, 1, 1, 1)

        self.LoadButtonSpacerBottom = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.LoadButtonContainer.addItem(self.LoadButtonSpacerBottom, 2, 1, 1, 1)

        self.LoadButtonSpacerTop = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.LoadButtonContainer.addItem(self.LoadButtonSpacerTop, 0, 1, 1, 1)

        self.ManualLoadContainer.addLayout(self.LoadButtonContainer)

        self.RawListActionContainerWidget.addWidget(self.ManualLoadPage)

        # ----- Raw List Page -----
        self.RawListPage = QWidget()
        self.RawListPageVLayoutWidget = QWidget(self.RawListPage)
        self.RawListPageVLayoutWidget.setGeometry(QRect(0, 0, 1111, 411))
        self.RawListContainer = QVBoxLayout(self.RawListPageVLayoutWidget)
        self.RawListContainer.setContentsMargins(0, 0, 0, 0)

        self.UnloadButton = QPushButton(self.RawListPageVLayoutWidget)
        self.UnloadButton.setObjectName('UnloadButton')
        self.UnloadButton.setFont(font)
        self.RawListContainer.addWidget(self.UnloadButton)

        self.RawListWidget = CustomEditTreeWidget([0], self.RawListPageVLayoutWidget)
        self.RawListWidget.setExpandsOnDoubleClick(False)
        self.RawListContainer.addWidget(self.RawListWidget)

        self.RawListActionContainerWidget.addWidget(self.RawListPage)

        self.RawListActionContainer.addWidget(self.RawListActionContainerWidget)

        self.ValueListsSection.addTab(self.RawListTab, '')

        self.MainContainer.addWidget(self.ValueListsSection)

        # ----- Set Indexes -----
        self.ActionsSection.setCurrentIndex(0)
        self.SlotStyleInput.setCurrentIndex(0)
        self.ValueListsSection.setCurrentIndex(0)
        self.RawListActionContainerWidget.setCurrentIndex(0)

        QMetaObject.connectSlotsByName(self)
        self.retranslate_ui()

    def retranslate_ui(self):
        self.setWindowTitle('Tyrano Browser')

        self.menuFile.setTitle('File')
        self.menuSettings.setTitle('Settings')

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

        self.GameExecPath.setText('')
        self.GameLabel.setText('Game:')
        self.SaveTabsLabel.setText('Save Tabs:')
        self.SlotStyleInput.setItemText(0, '{tab}-{tab_slot}')
        self.SlotStyleInput.setItemText(1, 'Save {slot}')

        self.GameExecutableLabel.setText('Game Executable:')
        self.LocateGameButton.setText('Locate...')
        self.GameInput.setText('')
        self.SlotsPerTabLabel.setText('Slots Per Tab:')
        self.SlotStyleLabel.setText('Slot Style:')
        self.ExcludedLabel.setText('Characters to Skip in Conversion')
        
        self.AddButton.setText('Add')
        self.EditButton.setText('Edit')
        self.RemoveButton.setText('Remove')

        self.LoadButton.setText('Load')
        self.UnloadButton.setText('Unload')

        self.ResultTab.setColumnCount(3)
        self.ResultTab.setHeaderLabels(['Variable', 'Value', 'Path'])

        for i in range(self.ResultTab.columnCount()):
            self.ResultTab.header().resizeSection(i, 200)

        self.TemplateWidget.setColumnCount(2)
        self.TemplateWidget.setHeaderLabels(['Description', 'Path'])

        for i in range(self.TemplateWidget.columnCount()):
            self.TemplateWidget.header().resizeSection(i, 300)

        self.ValueListWidget.setColumnCount(2)
        self.ValueListWidget.setHeaderLabels(['Description', 'Value'])

        for i in range(self.ValueListWidget.columnCount()):
            self.ValueListWidget.header().resizeSection(i, 300)

        self.RawListWidget.setColumnCount(2)
        self.RawListWidget.setHeaderLabels(['Description', 'Value'])

        for i in range(self.RawListWidget.columnCount()):
            self.RawListWidget.header().resizeSection(i, 300)

        self.ActionsSection.setTabText(self.ActionsSection.indexOf(self.ScanTab), 'Scan')
        self.ActionsSection.setTabText(self.ActionsSection.indexOf(self.TemplateTab), 'Template')
        self.ActionsSection.setTabText(self.ActionsSection.indexOf(self.MetadataTab), 'Metadata')
        self.ActionsSection.setTabText(self.ActionsSection.indexOf(self.ConfigTab), 'Config')

        self.ValueListsSection.setTabText(self.ValueListsSection.indexOf(self.ValueListTab), 'Value List')
        self.ValueListsSection.setTabText(self.ValueListsSection.indexOf(self.RawListTab), 'Raw List')
