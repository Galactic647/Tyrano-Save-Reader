from core.thread import KillableThread
from ui.ui import TyranoBrowserUI

from PySide2.QtMultimedia import QSound
from PySide2.QtCore import Qt, QTimer
from PySide2.QtWidgets import QApplication, QFileDialog, QTreeWidgetItem, QMessageBox

import json
import time
import sys


class TyranoBrowser(TyranoBrowserUI):
    # TODO
    # 3. Need progress bar when loading a save.
    
    # TODO Complex Problem
    # 1. Need an algorithm to check the difference between loaded data and new data,
    #    while still keeping in mind of new variables that doesn't exist in the current loaded data.

    def __init__(self):
        super().__init__()

        self.save_file_path = None
        self.raw_data = dict()
        self.flattened_data = dict()
        self.scan_progress_bar_value = 0
        self.load_progress_bar_value = 0

        self.LocateGameButton.clicked.connect(self.locate_game_exec)

        self.actionOpen_file.triggered.connect(self.open_save_file)
        self.actionLoad_Template.triggered.connect(self.load_template_file)   

        self.actionSave.triggered.connect(self.save_file)
        self.actionExport_Save_File.triggered.connect(self.export_save_file)   

        self.actionSaveTemplate.triggered.connect(self.save_template)
        self.actionSaveTemplate_as.triggered.connect(self.save_template_as)

        self.ScanButton.clicked.connect(self.scan_function)
        self.ClearButton.clicked.connect(self.clear_result)
        self.UndoButton.clicked.connect(self.undo_result)

        self.LoadButton.clicked.connect(self.load_raw_list)
        self.UnloadButton.clicked.connect(self.unload_raw_list)

        self.scan_progress_bar_check_interval = QTimer()
        self.scan_progress_bar_check_interval.timeout.connect(self.update_progress_bar)
        self.scan_progress_bar_check_interval.start(50)

        # Scan Cache
        self.result_cache = None
        self.prev_result_cache = None

        # SFXs
        self.warning = QSound("C:/Windows/Media/Windows Foreground.wav")
        self.scan_complete = QSound("C:/Windows/Media/Windows Background.wav")

        # Threads
        self.load_raw_thread: KillableThread
        self.flattening_thread: KillableThread

    def change_progress_bar_state(self, state):
        if state.lower() == 'normal':
            self.ScanProgressBar.setObjectName('ScanProgressBar')
        elif state.lower() == 'process':
            self.ScanProgressBar.setObjectName('ProcessProgressBar')
        self.ScanProgressBar.style().unpolish(self.ScanProgressBar)
        self.ScanProgressBar.style().polish(self.ScanProgressBar)

    def update_progress_bar(self):
        self.ScanProgressBar.setValue(self.scan_progress_bar_value)
        self.LoadProgressBar.setValue(self.load_progress_bar_value)
    
    def unload_raw_list(self):
        self.RawListActionContainerWidget.setCurrentIndex(0)
        KillableThread(target=self.RawListWidget.clear, daemon=True).start()

    def load_raw_list(self):
        if self.LoadButton.text() == 'Load':
            self.LoadButton.setText('Cancel')
            self.LoadButton.setEnabled(False)
            self.display_raw_list()
        else:
            self.LoadButton.setEnabled(False)

            KillableThread(target=self.load_raw_thread.kill, daemon=True).start()
            self.load_progress_bar_value = 0
            self.LoadProgressBar.setValue(0)
            self.RawListWidget.clear()

            self.LoadButton.setText('Load')
            self.LoadButton.setEnabled(True)
    
    def display_raw_list(self):
        self.load_raw_thread = KillableThread(target=self._create_raw_list_slot, daemon=True)            
        self.load_raw_thread.start()
        self.LoadButton.setEnabled(True)

    def _create_raw_list_slot(self):
        self.LoadProgressBar.setMaximum(len(self.raw_data['data']))
        slots = []
        for idx, slot in enumerate(self.raw_data['data'], start=1):
            item = QTreeWidgetItem([f'Slot {idx}'])

            for name, path in slot.items():
                self._add_items_to_raw_list(name, path, item)

            slots.append(item)
            self.load_progress_bar_value = idx
        for slot in slots:
            self.RawListWidget.addTopLevelItem(slot)

        self.load_progress_bar_value = 0
        self.LoadProgressBar.setValue(0)
        self.LoadButton.setText('Load')
        self.RawListActionContainerWidget.setCurrentIndex(1)

    def _add_items_to_raw_list(self, name, data, parent):
        if isinstance(data, dict):
            item = QTreeWidgetItem(parent, [name])
            for k, v in data.items():
                self._add_items_to_raw_list(k, v, item)
        elif isinstance(data, list):
            item = QTreeWidgetItem(parent, [name])
            for idx, i in enumerate(data):
                self._add_items_to_raw_list(f'{name}[{idx}]', i, item)
        else:
            item = QTreeWidgetItem(parent, [name, str(data)])

    def display_result(self, data):
        pattern = self.SlotStyleInput.currentText()
        slots_per_tabs = self.SlotsPerTabInput.value()
        tab = tab_slot = 0

        for d in data:
            for path, value in d.items():
                name = path.split('.')[-1]
                slot, *pth = path.split('.')
                slot = int(slot[5:-1])

                if slots_per_tabs:
                    tab, tab_slot = divmod(slot, slots_per_tabs)
                    if not tab_slot:
                        tab -= 1
                        tab_slot = slots_per_tabs

                QTreeWidgetItem(self.ResultTab, [
                    name,
                    str(value),
                    pattern.format(slot=slot + 1, tab=tab + 1, tab_slot=tab_slot),
                    '.'.join(pth)
                ])

    def clear_result(self):
        self.ResultTab.clear()
        self.prev_result_cache = None
        self.result_cache = None

        self.ClearButton.setEnabled(False)
        self.UndoButton.setEnabled(False)
        self.ScanButton.setText('Scan')
        self.FoundLabel.setText('Found: 0')

    def undo_result(self):
        if not self.prev_result_cache:
            return
        self.ResultTab.clear()
        self.display_result(list({n: self.flattened_data[n]} for n in self.prev_result_cache))
        self.UndoButton.setEnabled(False)
        self.FoundLabel.setText(f'Found: {len(self.prev_result_cache)}')

    def scan_function(self):
        self.ResultTab.clear()

        if self.ScanButton.text() == 'Cancel':
            self.flattening_thread.kill()
            self.ScanProgressBar.setValue(0)
            self.scan_progress_bar_value = 0
            self.change_progress_bar_state('normal')
            self.ScanButton.setText('Scan')
            return

        if not self.ScanInput.text():
            QMessageBox.critical(self, 'Error', 'Please enter a search query')
            return
        if not self.flattened_data:
            self.ScanButton.setText('Cancel')
            self.change_progress_bar_state('process')
            self.flattening_thread = KillableThread(target=self.create_flattened_data, daemon=True)
            self.flattening_thread.start()
            return
        
        self.ClearButton.setEnabled(False)
        self.ScanButton.setEnabled(False)
        if self.NameRadioButton.isChecked():
            target = self.search_by_name
        else:
            target = self.search_by_value

        search_slot = self.SearchLocationInput.currentIndex()
        if self.flattening_thread.is_alive():
            target(self.ScanInput.text(), search_slot)
        else:
            KillableThread(target=target, args=(self.ScanInput.text(), search_slot), daemon=True).start()

    def search_by_name(self, name, search_slot=None):
        start = time.perf_counter()

        data = self.flattened_data
        if self.result_cache:
            if search_slot:
                data = dict()

                for c in self.result_cache:
                    if int(c.partition(']')[0][5:]) != search_slot - 1:
                        continue
                    data[c] = self.flattened_data[c]
            else:
                data = {n: self.flattened_data[n] for n in self.result_cache}
        elif search_slot:
            data = self.raw_data['data'][search_slot - 1]
            data = self.flatten(data, prefix=f'slot[{search_slot - 1}].')

        found = []
        self.ScanProgressBar.setMaximum(len(data))
        for idx, k in enumerate(data, start=1):
            if name in k.rpartition('.')[-1].split('[')[0]:  # what the fuck is this mate
                found.append(k)
            self.scan_progress_bar_value = idx
        self.ScanProgressBar.setValue(0)
        self.scan_progress_bar_value = 0

        if self.result_cache:
           self.prev_result_cache = self.result_cache 
           self.UndoButton.setEnabled(True)
        self.result_cache = found
        end = time.perf_counter()

        self.FoundLabel.setText(f'Found: {len(found)} ({end - start:.3f}s)')
        self.display_result(list({n: data[n]} for n in found))

        self.ScanButton.setEnabled(True)
        self.ClearButton.setEnabled(True)
        self.scan_complete.play()

    def search_by_value(self, value, search_slot=None):
        start = time.perf_counter()
        if value.isdigit():
            value = int(value)
        else:
            try:
                value = float(value)
            except ValueError:
                pass

        data = self.flattened_data
        if self.result_cache:
            if search_slot:
                data = dict()

                for c in self.result_cache:
                    if int(c.partition(']')[0][5:]) != search_slot - 1:
                        continue
                    data[c] = self.flattened_data[c]
            else:
                data = {n: self.flattened_data[n] for n in self.result_cache}
        elif search_slot:
            data = self.raw_data['data'][search_slot - 1]
            data = self.flatten(data, prefix=f'slot[{search_slot - 1}].')

        found = []
        self.ScanProgressBar.setMaximum(len(data))
        for idx, d in enumerate(data.items(), start=1):
            k, v = d
            if value == v:
                found.append(k)
            self.scan_progress_bar_value = idx
        self.ScanProgressBar.setValue(0)
        self.scan_progress_bar_value = 0

        if self.result_cache:
           self.prev_result_cache = self.result_cache 
           self.UndoButton.setEnabled(True)
        self.result_cache = found
        end = time.perf_counter()
        
        self.FoundLabel.setText(f'Found: {len(found)} ({end - start:.3f}s)')
        self.display_result(list({n: data[n]} for n in found))

        self.ScanButton.setEnabled(True)
        self.ClearButton.setEnabled(True)
        self.scan_complete.play()

    def create_flattened_data(self):
        self.ScanProgressBar.setMaximum(len(self.raw_data['data']))
        data = dict()
        for idx, v in enumerate(self.raw_data['data']):
            data.update(self.flatten(v, prefix=f'slot[{idx}].'))
            self.scan_progress_bar_value = idx
        
        self.flattened_data = data
        self.ScanProgressBar.setValue(0)
        self.scan_progress_bar_value = 0
        self.change_progress_bar_state('normal')
        self.ScanButton.setText('Scan')

        self.scan_function()

    def flatten(self, d, prefix=None):
        result = dict()
        for k, v in d.items():
            if prefix:
                name = f'{prefix}{k}'
            else:
                name = k
            values = self._flatten(name, v)
            result.update(values)
        return result

    def _flatten(self, name, value):
        if isinstance(value, list):
            flat = dict()
            for i, v in enumerate(value):
                flat.update(self._flatten(f'{name}[{i}]', v))
            return flat
        elif isinstance(value, dict):
            flat = dict()
            for k, v in value.items():
                flat.update(self._flatten(f'{name}.{k}', v))
            return flat
        return {name: value}
    
    def open_save_file(self):
        sav_loc = QFileDialog.getOpenFileName(self, 'Open Save File', filter='Tyrano Save Files (*.sav)')[0]
        self.save_file_path = sav_loc

    def load_template_file(self):
        template_loc = QFileDialog.getOpenFileName(self, 'Load Template', filter='JSON Files (*.json)')[0]

    def save_file(self):
        pass

    def export_save_file(self):
        save_loc = QFileDialog.getSaveFileName(self, 'Export Save', filter='Tyrano Save Files (*.sav);;JSON Files (*.json)')[0]
        print(save_loc)

    def locate_game_exec(self):
        game_exec = QFileDialog.getOpenFileName(self, 'Locate Game Executable', filter='Executables (*.exe)')[0]
        self.GameExecPath.setText(game_exec)

    def save_template(self):
        save_loc = QFileDialog.getSaveFileName(self, 'Save Template', filter='JSON Files (*.json)')[0]
        print(save_loc)

    def save_template_as(self):
        save_loc = QFileDialog.getSaveFileName(self, 'Save Template As', filter='All Files (*.*)')
        print(save_loc)


def main():
    app = QApplication(sys.argv)
    window = TyranoBrowser()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

