from PySide2.QtCore import QMetaObject, QRect, QSize, Qt
from PySide2.QtWidgets import (QMainWindow, QAction, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QTreeWidget,
                               QTreeWidgetItem, QProgressBar, QSizePolicy, QAbstractItemView, QPushButton, QLineEdit,
                               QSpacerItem, QRadioButton, QTabWidget, QGridLayout, QComboBox, QSpinBox, QMenuBar, QMenu)

class TyranoBrowserUI(QMainWindow):
    def __init__(self, parent=None):
        super(TyranoBrowserUI, self).__init__(parent=parent)
        if self.objectName():
            self.setObjectName('self')
        self.resize(1107, 861)
        
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

        self.VerticalLayoutWidget = QWidget(self.centralwidget)
        self.VerticalLayoutWidget.setObjectName('VerticalLayoutWidget')
        self.VerticalLayoutWidget.setGeometry(QRect(0, 10, 1111, 831))
        self.MainContainer = QVBoxLayout(self.VerticalLayoutWidget)
        self.MainContainer.setObjectName('MainContainer')
        self.MainContainer.setContentsMargins(0, 0, 0, 0)
        self.InfoContainer = QVBoxLayout()
        self.InfoContainer.setObjectName('InfoContainer')
        self.InfoContainer.setContentsMargins(5, -1, 5, -1)
        self.InfoLabel = QLabel(self.VerticalLayoutWidget)
        self.InfoLabel.setObjectName('InfoLabel')
        self.InfoLabel.setAlignment(Qt.AlignCenter)

        self.InfoContainer.addWidget(self.InfoLabel)

        self.ScanProgressBar = QProgressBar(self.VerticalLayoutWidget)
        self.ScanProgressBar.setObjectName('ScanProgressBar')
        self.ScanProgressBar.setValue(24)
        self.ScanProgressBar.setTextVisible(False)

        self.InfoContainer.addWidget(self.ScanProgressBar)


        self.MainContainer.addLayout(self.InfoContainer)

        self.ScanContainer = QHBoxLayout()
        self.ScanContainer.setObjectName('ScanContainer')
        self.ScanContainer.setContentsMargins(-1, 5, -1, 30)
        self.ResultTab = QTreeWidget(self.VerticalLayoutWidget)
        QTreeWidgetItem(self.ResultTab)
        QTreeWidgetItem(self.ResultTab)
        QTreeWidgetItem(self.ResultTab)
        self.ResultTab.setObjectName('ResultTab')
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ResultTab.sizePolicy().hasHeightForWidth())
        self.ResultTab.setSizePolicy(sizePolicy)
        self.ResultTab.setMinimumSize(QSize(750, 0))
        self.ResultTab.setEditTriggers(QAbstractItemView.DoubleClicked)
        self.ResultTab.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.ResultTab.setIndentation(0)
        self.ResultTab.setItemsExpandable(False)
        self.ResultTab.setExpandsOnDoubleClick(False)
        self.ResultTab.header().setMinimumSectionSize(100)
        self.ResultTab.header().setDefaultSectionSize(200)

        self.ScanContainer.addWidget(self.ResultTab)

        self.ScanActionContainer = QVBoxLayout()
        self.ScanActionContainer.setObjectName('ScanActionContainer')
        self.ScanScannerActionContainer = QHBoxLayout()
        self.ScanScannerActionContainer.setObjectName('ScanScannerActionContainer')
        self.ScanScannerActionContainer.setContentsMargins(5, -1, 5, -1)
        self.ScanButton = QPushButton(self.VerticalLayoutWidget)
        self.ScanButton.setObjectName('ScanButton')

        self.ScanScannerActionContainer.addWidget(self.ScanButton)

        self.ScanInput = QLineEdit(self.VerticalLayoutWidget)
        self.ScanInput.setObjectName('ScanInput')

        self.ScanScannerActionContainer.addWidget(self.ScanInput)


        self.ScanActionContainer.addLayout(self.ScanScannerActionContainer)

        self.ScanActionVFxdSpacer = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Maximum)

        self.ScanActionContainer.addItem(self.ScanActionVFxdSpacer)

        self.SearchByContainer = QHBoxLayout()
        self.SearchByContainer.setObjectName('SearchByContainer')
        self.SearchByContainer.setContentsMargins(10, -1, 5, -1)
        self.SearchByLabel = QLabel(self.VerticalLayoutWidget)
        self.SearchByLabel.setObjectName('SearchByLabel')

        self.SearchByContainer.addWidget(self.SearchByLabel)

        self.ValueRadioButton = QRadioButton(self.VerticalLayoutWidget)
        self.ValueRadioButton.setObjectName('ValueRadioButton')

        self.SearchByContainer.addWidget(self.ValueRadioButton)

        self.NameRadioButton = QRadioButton(self.VerticalLayoutWidget)
        self.NameRadioButton.setObjectName('NameRadioButton')

        self.SearchByContainer.addWidget(self.NameRadioButton)

        self.SearchByHSpacer = QSpacerItem(50, 20, QSizePolicy.Maximum, QSizePolicy.Minimum)

        self.SearchByContainer.addItem(self.SearchByHSpacer)


        self.ScanActionContainer.addLayout(self.SearchByContainer)

        self.ScanActionVSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.ScanActionContainer.addItem(self.ScanActionVSpacer)


        self.ScanContainer.addLayout(self.ScanActionContainer)


        self.MainContainer.addLayout(self.ScanContainer)

        self.ActionsSection = QTabWidget(self.VerticalLayoutWidget)
        self.ActionsSection.setObjectName('ActionsSection')
        self.ValueListTabAction = QWidget()
        self.ValueListTabAction.setObjectName('ValueListTabAction')
        self.ValueListTab = QTreeWidget(self.ValueListTabAction)
        self.ValueListTab.setObjectName('ValueListTab')
        self.ValueListTab.setGeometry(QRect(0, 0, 1101, 381))
        self.ValueListTab.header().setDefaultSectionSize(300)
        self.ActionsSection.addTab(self.ValueListTabAction, '')
        self.MetadataTabAction = QWidget()
        self.MetadataTabAction.setObjectName('MetadataTabAction')
        self.gridLayoutWidget = QWidget(self.MetadataTabAction)
        self.gridLayoutWidget.setObjectName('gridLayoutWidget')
        self.gridLayoutWidget.setGeometry(QRect(10, 0, 621, 201))
        self.MetadataContainer = QGridLayout(self.gridLayoutWidget)
        self.MetadataContainer.setObjectName('MetadataContainer')
        self.MetadataContainer.setContentsMargins(0, 0, 0, 0)
        self.GameExecPath = QLabel(self.gridLayoutWidget)
        self.GameExecPath.setObjectName('GameExecPath')

        self.MetadataContainer.addWidget(self.GameExecPath, 1, 1, 1, 1)

        self.GameLabel = QLabel(self.gridLayoutWidget)
        self.GameLabel.setObjectName('GameLabel')

        self.MetadataContainer.addWidget(self.GameLabel, 0, 0, 1, 1)

        self.SaveTabsLabel = QLabel(self.gridLayoutWidget)
        self.SaveTabsLabel.setObjectName('SaveTabsLabel')

        self.MetadataContainer.addWidget(self.SaveTabsLabel, 2, 0, 1, 1)

        self.GameExecutableLabel = QLabel(self.gridLayoutWidget)
        self.GameExecutableLabel.setObjectName('GameExecutableLabel')

        self.MetadataContainer.addWidget(self.GameExecutableLabel, 1, 0, 1, 1)

        self.LocateGameButton = QPushButton(self.gridLayoutWidget)
        self.LocateGameButton.setObjectName('LocateGameButton')

        self.MetadataContainer.addWidget(self.LocateGameButton, 1, 2, 1, 1)

        self.GameInput = QLineEdit(self.gridLayoutWidget)
        self.GameInput.setObjectName('GameInput')

        self.MetadataContainer.addWidget(self.GameInput, 0, 1, 1, 1)

        self.SlotsPerTabLabel = QLabel(self.gridLayoutWidget)
        self.SlotsPerTabLabel.setObjectName('SlotsPerTabLabel')

        self.MetadataContainer.addWidget(self.SlotsPerTabLabel, 3, 0, 1, 1)

        self.SlotStyleLabel = QLabel(self.gridLayoutWidget)
        self.SlotStyleLabel.setObjectName('SlotStyleLabel')

        self.MetadataContainer.addWidget(self.SlotStyleLabel, 4, 0, 1, 1)

        self.SlotStyleInput = QComboBox(self.gridLayoutWidget)
        self.SlotStyleInput.addItem('')
        self.SlotStyleInput.addItem('')
        self.SlotStyleInput.setObjectName('SlotStyleInput')
        self.SlotStyleInput.setEditable(True)

        self.MetadataContainer.addWidget(self.SlotStyleInput, 4, 1, 1, 1)

        self.SaveTabsInput = QSpinBox(self.gridLayoutWidget)
        self.SaveTabsInput.setObjectName('SaveTabsInput')

        self.MetadataContainer.addWidget(self.SaveTabsInput, 2, 1, 1, 1)

        self.SlotsPerTabInput = QSpinBox(self.gridLayoutWidget)
        self.SlotsPerTabInput.setObjectName('SlotsPerTabInput')

        self.MetadataContainer.addWidget(self.SlotsPerTabInput, 3, 1, 1, 1)

        self.MetadataContainer.setColumnStretch(1, 1)
        self.ActionsSection.addTab(self.MetadataTabAction, '')
        self.TemplateTabActiion = QWidget()
        self.TemplateTabActiion.setObjectName('TemplateTabActiion')
        self.TemplateTab = QTreeWidget(self.TemplateTabActiion)
        QTreeWidgetItem(self.TemplateTab)
        self.TemplateTab.setObjectName('TemplateTab')
        self.TemplateTab.setGeometry(QRect(0, 0, 1101, 381))
        self.TemplateTab.setContextMenuPolicy(Qt.CustomContextMenu)
        self.TemplateTab.header().setDefaultSectionSize(300)
        self.ActionsSection.addTab(self.TemplateTabActiion, '')
        self.RawJSONTabAction = QWidget()
        self.RawJSONTabAction.setObjectName('RawJSONTabAction')
        self.RawJSONTab = QTreeWidget(self.RawJSONTabAction)
        self.RawJSONTab.setObjectName('RawJSONTab')
        self.RawJSONTab.setGeometry(QRect(0, 0, 1101, 381))
        self.RawJSONTab.header().setDefaultSectionSize(300)
        self.ActionsSection.addTab(self.RawJSONTabAction, '')

        self.MainContainer.addWidget(self.ActionsSection)

        self.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(self)
        self.menubar.setObjectName('menubar')
        self.menubar.setGeometry(QRect(0, 0, 1107, 26))
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

        self.ActionsSection.setCurrentIndex(3)
        self.SlotStyleInput.setCurrentIndex(0)

        QMetaObject.connectSlotsByName(self)

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
        self.ResultTab.setSortingEnabled(__sortingEnabled)

        self.ScanButton.setText('Scan')
        self.SearchByLabel.setText('Search by')
        self.ValueRadioButton.setText('Value')
        self.NameRadioButton.setText('Name')
        ___qtreewidgetitem4 = self.ValueListTab.headerItem()
        ___qtreewidgetitem4.setText(2, 'Value');
        ___qtreewidgetitem4.setText(1, 'Description');
        ___qtreewidgetitem4.setText(0, 'Action');
        self.ActionsSection.setTabText(self.ActionsSection.indexOf(self.ValueListTabAction), 'Value List')
        self.GameExecPath.setText('None')
        self.GameLabel.setText('Game:')
        self.SaveTabsLabel.setText('Save Tabs:')
        self.GameExecutableLabel.setText('Game Executable:   ')
        self.LocateGameButton.setText('Locate...')
        self.GameInput.setText('')
        self.SlotsPerTabLabel.setText('Slots Per Tab:')
        self.SlotStyleLabel.setText('Slot Style:')
        self.SlotStyleInput.setItemText(0, '{tab}-{tab_slot}')
        self.SlotStyleInput.setItemText(1, 'Save {slot}')

        self.ActionsSection.setTabText(self.ActionsSection.indexOf(self.MetadataTabAction), 'Metadata')
        ___qtreewidgetitem5 = self.TemplateTab.headerItem()
        ___qtreewidgetitem5.setText(1, 'Path');
        ___qtreewidgetitem5.setText(0, 'Description');

        __sortingEnabled1 = self.TemplateTab.isSortingEnabled()
        self.TemplateTab.setSortingEnabled(False)
        ___qtreewidgetitem6 = self.TemplateTab.topLevelItem(0)
        ___qtreewidgetitem6.setText(1, '4');
        ___qtreewidgetitem6.setText(0, 'a');
        self.TemplateTab.setSortingEnabled(__sortingEnabled1)

        self.ActionsSection.setTabText(self.ActionsSection.indexOf(self.TemplateTabActiion), 'Template')
        ___qtreewidgetitem7 = self.RawJSONTab.headerItem()
        ___qtreewidgetitem7.setText(2, 'Value');
        ___qtreewidgetitem7.setText(1, 'Description');
        ___qtreewidgetitem7.setText(0, 'Action');
        self.ActionsSection.setTabText(self.ActionsSection.indexOf(self.RawJSONTabAction), 'Raw JSON')
        self.menuFile.setTitle('File')
        self.menuSettings.setTitle('Settings')
