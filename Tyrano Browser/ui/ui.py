from ui.widget import CustomEditTreeWidget, CustomCheckboxDelegate, TemplateTreeWidget

from PySide2.QtCore import QMetaObject, QRect, QSize, Qt
from PySide2.QtGui import QFont
from PySide2.QtWidgets import (QMainWindow, QAction, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QTreeWidget, QLineEdit,
    QTreeWidgetItem, QProgressBar, QSizePolicy, QAbstractItemView, QPushButton, QSpacerItem, QRadioButton, QTabWidget,
    QGridLayout, QComboBox, QSpinBox, QMenuBar, QMenu, QListWidget, QStackedWidget)

import regex


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
        self.actionSaveTemplate = QAction(self)
        self.actionSaveTemplate_as = QAction(self)
        self.actionLoad_Template = QAction(self)
        self.actionAuto_Load_Template = QAction(self)
        self.actionAuto_Load_Template.setCheckable(True)
        self.actionAuto_Load_Template.setChecked(True)
        self.actionAuto_Pick_Slot_To_Show = QAction(self)
        self.actionAuto_Pick_Slot_To_Show.setCheckable(True)
        self.actionAuto_Pick_Slot_To_Show.setChecked(True)
        self.actionSave = QAction(self)
        self.actionExport_Save_File = QAction(self)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menuFile.addAction(self.actionOpen_file)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionLoad_Template)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionExport_Save_File)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSaveTemplate)
        self.menuFile.addAction(self.actionSaveTemplate_as)
        self.menuSettings.addAction(self.actionAuto_Load_Template)
        self.menuSettings.addAction(self.actionAuto_Pick_Slot_To_Show)
        
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
        self.ActionsSection.currentChanged.connect(self.action_section_on_change)
        
        # ----- Tab Widget - Scan Tab -----
        self.ScanTab = QWidget()
        self.ScanTabVLayoutWidget = QWidget(self.ScanTab)
        self.ScanTabVLayoutWidget.setGeometry(QRect(0, 0, 1101, 361))
        self.ScanActionBaseContainer = QVBoxLayout(self.ScanTab)
        self.ScanActionBaseContainer.setContentsMargins(0, 0, 0, 0)

        self.ScanProgressBar = QProgressBar(self.ScanTabVLayoutWidget)
        self.ScanProgressBar.setObjectName('ScanProgressBar')
        self.ScanProgressBar.setTextVisible(False)
        self.ScanActionBaseContainer.addWidget(self.ScanProgressBar)

        self.ScanButtonContainer = QGridLayout()
        self.ScanButtonContainer.setHorizontalSpacing(15)
        self.ScanButtonContainer.setContentsMargins(5, -1, 8, -1)

        self.ScanButton = QPushButton(self.ScanTabVLayoutWidget)
        self.ScanButton.setFont(font)
        self.ScanButtonContainer.addWidget(self.ScanButton, 0, 0, 1, 1)

        self.ClearButton = QPushButton(self.ScanTabVLayoutWidget)
        self.ClearButton.setFont(font)
        self.ClearButton.setEnabled(False)
        self.ScanButtonContainer.addWidget(self.ClearButton, 0, 1, 1, 1)

        self.UndoButton = QPushButton(self.ScanTabVLayoutWidget)
        self.UndoButton.setFont(font)
        self.UndoButton.setEnabled(False)
        self.ScanButtonContainer.addWidget(self.UndoButton, 0, 2, 1, 1)

        self.ScanActionContainer = QVBoxLayout()
        self.ScanActionContainer.addLayout(self.ScanButtonContainer)

        self.ScanInput = QLineEdit(self.ScanTabVLayoutWidget)
        self.ScanInput.setFont(font)
        self.ScanActionContainer.addWidget(self.ScanInput)

        self.ScanActionVSpacerScan2SB = QSpacerItem(20, 8, QSizePolicy.Minimum, QSizePolicy.Maximum)
        self.ScanActionContainer.addItem(self.ScanActionVSpacerScan2SB)

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

        self.ScanActionVSpacerSearchBy2SI = QSpacerItem(20, 8, QSizePolicy.Minimum, QSizePolicy.Maximum)
        self.ScanActionContainer.addItem(self.ScanActionVSpacerSearchBy2SI)

        self.SearchConstraintContainer = QGridLayout()
        self.SearchConstraintContainer.setContentsMargins(10, -1, -1, -1)
        self.SearchLocationInput = QComboBox(self.ScanTabVLayoutWidget)
        self.SearchLocationInput.setFont(font)
        self.SearchConstraintContainer.addWidget(self.SearchLocationInput, 0, 1, 1, 1)

        self.SearchInLabel = QLabel(self.ScanTabVLayoutWidget)
        self.SearchInLabel.setObjectName(u"SearchInLabel")
        self.SearchInLabel.setFont(font)
        self.SearchConstraintContainer.addWidget(self.SearchInLabel, 0, 0, 1, 1)

        self.SearchInHSpacer = QSpacerItem(60, 20, QSizePolicy.Maximum, QSizePolicy.Minimum)
        self.SearchConstraintContainer.addItem(self.SearchInHSpacer, 0, 2, 1, 1)

        self.SearchConstraintContainer.setColumnStretch(1, 1)
        self.ScanActionContainer.addLayout(self.SearchConstraintContainer)

        self.ScanActionVSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.ScanActionContainer.addItem(self.ScanActionVSpacer)

        self.ScanActionWidthControl = QSpacerItem(350, 40, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.ScanActionContainer.addItem(self.ScanActionWidthControl)

        self.FoundLabel = QLabel(self.ScanTabVLayoutWidget)
        self.FoundLabel.setFont(font)
        self.ScanActionContainer.addWidget(self.FoundLabel)

        self.ResultTab = QTreeWidget(self.ScanTabVLayoutWidget)
    
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
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
        self.ResultTab.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ResultTab.doubleClicked.connect(self.result_tab_double_click)
        self.ResultTab.customContextMenuRequested.connect(self.result_tab_context_menu_open)
        
        self.ScanWidgetsContainer = QGridLayout()
        self.ScanWidgetsContainer.addWidget(self.ResultTab, 0, 0, 1, 1)
        self.ScanWidgetsContainer.addLayout(self.ScanActionContainer, 0, 1, 1, 1)
        self.ScanWidgetsContainer.setColumnStretch(0, 1)
        self.ScanActionBaseContainer.addLayout(self.ScanWidgetsContainer)

        self.ActionsSection.addTab(self.ScanTab, '')

        # ----- Tab Widget - Template Tab -----
        self.TemplateTab = QWidget()
        self.TemplateTabVLayoutWidget = QWidget(self.TemplateTab)
        self.TemplateTabVLayoutWidget.setGeometry(QRect(0, 0, 1101, 361))
        self.TemplateContainer = QVBoxLayout(self.TemplateTab)
        self.TemplateContainer.setContentsMargins(0, 0, 0, 0)

        self.TemplateWidget = TemplateTreeWidget(self.TemplateTabVLayoutWidget)
        self.TemplateWidget.setSortingEnabled(False)
        self.TemplateWidget.setDragEnabled(True)
        self.TemplateWidget.setAcceptDrops(True)
        self.TemplateWidget.setDropIndicatorShown(True)
        self.TemplateWidget.setDragDropMode(QAbstractItemView.InternalMove)
        self.TemplateWidget.setDefaultDropAction(Qt.MoveAction)
        self.TemplateWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.TemplateWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.TemplateWidget.itemChanged.connect(self.refresh_value_list)
        self.TemplateWidget.customContextMenuRequested.connect(self.template_tab_context_menu_open)
        self.TemplateContainer.addWidget(self.TemplateWidget)

        self.ActionsSection.addTab(self.TemplateTab, '')

        # ----- Tab Widget - Metadata Tab -----
        self.MetadataTab = QWidget()
        self.MetadataTabHLayoutWidget = QWidget(self.MetadataTab)
        self.MetadataTabHLayoutWidget.setGeometry(QRect(0, 0, 1101, 361))
        self.HLayoutBaseContainer = QHBoxLayout(self.MetadataTab)
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
        self.ConfigHBaseContainer = QHBoxLayout(self.ConfigTab)
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
        self.ValueListTab = QWidget(self)
        self.ValueListTabVLayoutWidget = QWidget(self.ValueListTab)
        self.ValueListTabVLayoutWidget.setGeometry(QRect(0, 0, 1111, 411))
        self.ValueListContainer = QVBoxLayout(self.ValueListTab)
        self.ValueListContainer.setContentsMargins(0, 0, 0, 0)

        self.SelectiveShowLayout = QGridLayout()
        self.SelectiveShowLayout.setContentsMargins(7, 7, -1, -1)
        self.ShowLabel = QLabel(self.ValueListTabVLayoutWidget)
        self.ShowLabel.setFont(font)
        self.SelectiveShowLayout.addWidget(self.ShowLabel, 0, 0, 1, 1)

        self.ShowInput = QComboBox()
        self.ShowInput.setFont(font)
        self.SelectiveShowLayout.addWidget(self.ShowInput, 0, 1, 1, 1)
        self.ShowInput.currentIndexChanged.connect(self.refresh_value_list)

        self.ShowHSpacer = QSpacerItem(850, 20, QSizePolicy.Maximum, QSizePolicy.Minimum)
        self.SelectiveShowLayout.addItem(self.ShowHSpacer, 0, 2, 1, 1)

        self.SelectiveShowLayout.setColumnStretch(1, 1)
        self.ValueListContainer.addLayout(self.SelectiveShowLayout)

        self.ValueListWidget = CustomEditTreeWidget([0], self.ValueListTabVLayoutWidget)
        self.ValueListWidget.setSortingEnabled(False)
        self.ValueListWidget.setItemDelegateForColumn(0, CustomCheckboxDelegate(20, self.ValueListWidget))
        self.ValueListContainer.addWidget(self.ValueListWidget)

        self.ValueListsSection.addTab(self.ValueListTab, '')

        # ----- Tab Widget - Raw List Tab -----
        self.RawListTab = QWidget()
        self.RawListActionContainerVLayoutWidget = QWidget(self.RawListTab)
        self.RawListActionContainerVLayoutWidget.setGeometry(QRect(0, 0, 1111, 351))
        self.RawListActionContainer = QVBoxLayout(self.RawListTab)
        self.RawListActionContainer.setContentsMargins(0, 0, 0, 0)
        
        self.RawListActionContainerWidget = QStackedWidget(self.RawListActionContainerVLayoutWidget)
        
        # ----- Manual Load Page -----
        self.ManualLoadPage = QWidget()
        self.ManualLoadPageLayoutWidget = QWidget(self.ManualLoadPage)
        self.ManualLoadPageLayoutWidget.setGeometry(QRect(0, 0, 1101, 351))
        self.ManualLoadContainer = QVBoxLayout(self.ManualLoadPage)
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
        self.RawListContainer = QVBoxLayout(self.RawListPage)
        self.RawListContainer.setContentsMargins(0, 0, 0, 0)

        self.UnloadButton = QPushButton(self.RawListPageVLayoutWidget)
        self.UnloadButton.setObjectName('UnloadButton')
        self.UnloadButton.setFont(font)
        self.RawListContainer.addWidget(self.UnloadButton)

        self.RawListWidget = CustomEditTreeWidget([0], self.RawListPageVLayoutWidget)
        self.RawListWidget.setExpandsOnDoubleClick(False)
        self.RawListWidget.setItemDelegateForColumn(0, CustomCheckboxDelegate(20, self.RawListPageVLayoutWidget))
        self.RawListContainer.addWidget(self.RawListWidget)

        self.RawListActionContainerWidget.addWidget(self.RawListPage)

        self.RawListActionContainer.addWidget(self.RawListActionContainerWidget)

        self.ValueListsSection.addTab(self.RawListTab, '')

        self.MainContainer.addWidget(self.ValueListsSection)

        QMetaObject.connectSlotsByName(self)
        self.retranslate_ui()

        self.set_shortcut()

    def retranslate_ui(self):
        self.setWindowTitle('Tyrano Browser')

        self.menuFile.setTitle('File')
        self.menuSettings.setTitle('Settings')

        self.actionOpen_file.setText('Open...')
        self.actionSaveTemplate.setText('Save Template')
        self.actionSaveTemplate_as.setText('Save Template As...')
        self.actionLoad_Template.setText('Load Template...')
        self.actionAuto_Load_Template.setText('Auto Load Template')
        self.actionSave.setText('Save')
        self.actionExport_Save_File.setText('Export Save...')
        
        self.InfoLabel.setText('No save loaded (Template - None)')
        
        self.ScanButton.setText('Scan')
        self.ClearButton.setText('Clear')
        self.UndoButton.setText('Undo')
        self.SearchByLabel.setText('Search by')
        self.ValueRadioButton.setText('Value')
        self.NameRadioButton.setText('Name')

        self.SearchInLabel.setText('Search In')
        self.SearchLocationInput.addItem('All')
        self.FoundLabel.setText('Found: 0')

        self.GameLabel.setText('Game:')
        self.SaveTabsLabel.setText('Save Tabs:')
        self.SlotStyleInput.addItem('{tab}-{tab_slot}')
        self.SlotStyleInput.addItem('Slot {slot}')
        self.SlotStyleInput.setCurrentIndex(1)

        self.GameExecutableLabel.setText('Game Executable:')
        self.LocateGameButton.setText('Locate...')
        self.SlotsPerTabLabel.setText('Slots Per Tab:')
        self.SlotStyleLabel.setText('Slot Style:')
        self.ExcludedLabel.setText('Characters to Skip in Conversion')
        
        self.AddButton.setText('Add')
        self.EditButton.setText('Edit')
        self.RemoveButton.setText('Remove')

        self.ShowLabel.setText('Show')
        self.ShowInput.addItem('All')

        self.LoadButton.setText('Load')
        self.UnloadButton.setText('Unload')

        self.ResultTab.setHeaderLabels(['Variable', 'Value', 'Slot', 'Path'])

        for i in range(self.ResultTab.columnCount()):
            self.ResultTab.header().resizeSection(i, 180)

        self.TemplateWidget.setHeaderLabels(['Description', 'Path'])

        for i in range(self.TemplateWidget.columnCount()):
            self.TemplateWidget.header().resizeSection(i, 300)

        self.ValueListWidget.setHeaderLabels(['Description', 'Value'])

        for i in range(self.ValueListWidget.columnCount()):
            self.ValueListWidget.header().resizeSection(i, 300)

        self.RawListWidget.setHeaderLabels(['Description', 'Value'])

        for i in range(self.RawListWidget.columnCount()):
            self.RawListWidget.header().resizeSection(i, 300)

        self.ActionsSection.setTabText(self.ActionsSection.indexOf(self.ScanTab), 'Scan')
        self.ActionsSection.setTabText(self.ActionsSection.indexOf(self.TemplateTab), 'Template')
        self.ActionsSection.setTabText(self.ActionsSection.indexOf(self.MetadataTab), 'Metadata')
        self.ActionsSection.setTabText(self.ActionsSection.indexOf(self.ConfigTab), 'Config')

        self.ValueListsSection.setTabText(self.ValueListsSection.indexOf(self.ValueListTab), 'Value List')
        self.ValueListsSection.setTabText(self.ValueListsSection.indexOf(self.RawListTab), 'Raw List')

    def set_shortcut(self):
        self.ScanInput.returnPressed.connect(self.ScanButton.click)

    def action_section_on_change(self, index):
        if index != 1:  # Template tab
            return
        self.ActionsSection.setTabText(1, 'Template')

    def result_tab_double_click(self, index):
        item = self.ResultTab.itemFromIndex(index)
        if item is None:
            return
        
        it = QTreeWidgetItem(self.TemplateWidget, [item.text(0), item.text(3)])
        it.setFlags(it.flags() & ~Qt.ItemIsDropEnabled | Qt.ItemIsEditable)

        self.ActionsSection.setTabText(1, 'Template*')
        self.refresh_value_list()

    def result_tab_context_menu_open(self, position):
        # TODO
        # needs to check if the item is list based or not (low priority)
        items = self.ResultTab.selectedItems()
        if not items:
            return
        
        menu = QMenu()
        add_to_template = menu.addAction('Add to Template')
        action = menu.exec_(self.ResultTab.viewport().mapToGlobal(position))

        if action != add_to_template:
            return
        for item in items:
            it = QTreeWidgetItem(self.TemplateWidget, [item.text(0), item.text(3)])
            it.setFlags(it.flags() & ~Qt.ItemIsDropEnabled | Qt.ItemIsEditable)
        
        self.ActionsSection.setTabText(1, 'Template*')
        self.refresh_value_list()

    def template_tab_context_menu_open(self, position):
        clicked_item = self.TemplateWidget.itemAt(position)

        if clicked_item is not None:
            self._template_tab_context_menu_at_item(position)
        else:
            self._template_tab_context_menu_at_empty_area(position)
    
    def _template_tab_context_menu_at_empty_area(self, position):
        menu = QMenu()

        add_item = menu.addAction('Add Item')

        action = menu.exec_(self.TemplateWidget.viewport().mapToGlobal(position))

        if action == add_item:
            item = QTreeWidgetItem(self.TemplateWidget, ['New Item'])
            item.setFlags(item.flags() | Qt.ItemIsEditable)

    def _template_tab_context_menu_at_item(self, position):
        menu = QMenu()

        add_item = menu.addAction('Add Item')
        delete_item = menu.addAction('Delete Item')

        action = menu.exec_(self.TemplateWidget.viewport().mapToGlobal(position))

        if action == add_item:
            item = QTreeWidgetItem(self.TemplateWidget, ['New Item'])
            item.setFlags(item.flags() | Qt.ItemIsEditable)
        elif action == delete_item:
            selected_items = self.TemplateWidget.selectedItems()

            for item in selected_items:
                parent = item.parent()

                if parent:
                    self.TemplateWidget.removeChildItem(parent, item)
                else:
                    self.TemplateWidget.takeTopLevelItem(self.TemplateWidget.indexOfTopLevelItem(item))

    def _get_value_from_path(self, data, path):
        elements = regex.split(r'(\.\w+|\[\d+\])', path)
        elements = [el for el in elements if el and el != '.']

        current = data
        for el in elements:
            try:
                if el.startswith('[') and el.endswith(']'):
                    index = int(el[1:-1])
                    current = current[index]
                else:
                    current = current[el.lstrip('.')]
            except KeyError:
                return path
            except IndexError:
                return path
        return current

    def _get_tree_data(self, root):
        data = dict()

        for i in range(root.childCount()):
            item = root.child(i)
            if item.childCount():
                data[item.text(0)] = self._get_tree_data(item)
            else:
                data[item.text(0)] = item.text(1)
        return data
    
    def add_item_to_value_list(self, data, name, path, parent):
        if isinstance(path, dict) or not path:
            item = QTreeWidgetItem(parent, [name])

            if not path:
                return
            for k, v in path.items():
                self.add_item_to_value_list(data, k, v, item)
        else:
            val = self._get_value_from_path(data, path)

            item = QTreeWidgetItem(parent, [name, str(val)])
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsEditable)
            item.setCheckState(0, Qt.Unchecked)

    def refresh_value_list(self):
        self.ValueListWidget.clear()
        root = self.TemplateWidget.invisibleRootItem()
        template_data = self._get_tree_data(root)

        show_slot = self.ShowInput.currentIndex()

        if not show_slot:
            for idx, slot in enumerate(self.raw_data['data'], start=1):
                item = QTreeWidgetItem(self.ValueListWidget, [f'Slot {idx}'])

                for name, path in template_data.items():
                    self.add_item_to_value_list(slot, name, path, item)
        else:
            slot_data = self.raw_data['data'][show_slot - 1]

            for name, path in template_data.items():
                self.add_item_to_value_list(slot_data, name, path, self.ValueListWidget)
