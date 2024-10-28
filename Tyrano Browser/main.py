from ui.ui import TyranoBrowserUI

from PySide2.QtCore import Qt, QTimer
from PySide2.QtWidgets import QApplication, QFileDialog, QTreeWidgetItem, QMessageBox

import threading
import json
import time
import sys


class TyranoBrowser(TyranoBrowserUI):
    # TODO
    # 3. Need progress bar when loading a save.

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

        self.LoadButton.clicked.connect(self.load_raw_list)
        self.UnloadButton.clicked.connect(self.unload_raw_list)

        self.scan_progress_bar_check_interval = QTimer()
        self.scan_progress_bar_check_interval.timeout.connect(self.update_progress_bar)
        self.scan_progress_bar_check_interval.start(50)
        with open('test/flattened.json', 'rb') as file:
            self.flattened_data = json.loads(file.read())
            file.close()

        # Threads
        self.load_raw_thread = None

    def update_progress_bar(self):
        self.ScanProgressBar.setValue(self.scan_progress_bar_value)
        self.LoadProgressBar.setValue(self.load_progress_bar_value)

    def clear_result(self):
        self.ResultTab.clear()
        self.FoundLabel.setText('Found: 0')
    
    def unload_raw_list(self):
        self.RawListActionContainerWidget.setCurrentIndex(0)
        threading.Thread(target=self.RawListWidget.clear, daemon=True).start()

    def load_raw_list(self):
        if self.LoadButton.text() == 'Load':
            self.LoadButton.setText('Cancel')
            self.LoadButton.setEnabled(False)
            self.display_raw_list()
        else:
            self.LoadButton.setEnabled(False)

            self.load_raw_thread.join(0)
            self.load_progress_bar_value = 0
            self.LoadProgressBar.setValue(0)
            self.RawListWidget.clear()

            self.LoadButton.setText('Load')
            self.LoadButton.setEnabled(True)
    
    def display_raw_list(self):
        self.load_raw_thread = threading.Thread(target=self._create_raw_list_slot, daemon=True)            
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
        for d in data:
            for path, value in d.items():
                name = path.split('.')[-1]
                slot, *pth = path.split('.')
                QTreeWidgetItem(self.ResultTab, [
                    name,
                    str(value),
                    f'Slot {slot[5:-1]}',
                    '.'.join(pth)
                ])

    def scan_function(self):
        # TODO needs caching for continuous search
        self.ResultTab.clear()
        if not self.ScanInput.text():
            QMessageBox.critical(self, 'Error', 'Please enter a search query')
            return
        if not self.flattened_data:
            # TODO Need threading for this too (blue progress bar)
            self.create_flattened_data()
        
        self.ScanButton.setEnabled(False)
        if self.NameRadioButton.isChecked():
            threading.Thread(target=self.search_by_name, args=(self.ScanInput.text(),), daemon=True).start()
        else:
            threading.Thread(target=self.search_by_value, args=(self.ScanInput.text(),), daemon=True).start()

    def search_by_name(self, name):
        start = time.perf_counter()

        found = []
        self.ScanProgressBar.setMaximum(len(self.flattened_data))
        for idx, k in enumerate(self.flattened_data, start=1):
            if name in k.split('.')[-1].split('[')[0]:  # what the fuck is this mate
                found.append(k)
            self.scan_progress_bar_value = idx
        self.ScanProgressBar.setValue(0)
        self.scan_progress_bar_value = 0
        end = time.perf_counter()

        self.FoundLabel.setText(f'Found: {len(found)} ({end - start:.3f}s)')
        self.display_result(list({n: self.flattened_data[n]} for n in found))

        self.ScanButton.setEnabled(True)

    def search_by_value(self, value):
        start = time.perf_counter()
        if value.isdigit():
            value = int(value)
        else:
            try:
                value = float(value)
            except ValueError:
                pass

        found = []
        self.ScanProgressBar.setMaximum(len(self.flattened_data))
        for idx, d in enumerate(self.flattened_data.items(), start=1):
            k, v = d
            if value == v:
                found.append(k)
            self.scan_progress_bar_value = idx
        self.ScanProgressBar.setValue(0)
        self.scan_progress_bar_value = 0
        end = time.perf_counter()
        
        self.FoundLabel.setText(f'Found: {len(found)} ({end - start:.3f}s)')
        self.display_result(list({n: self.flattened_data[n]} for n in found))

        self.ScanButton.setEnabled(True)

    def create_flattened_data(self):
        for idx, v in enumerate(self.raw_data['data']):
            self.flattened_data.update(self.flatten(v, prefix=f'slot[{idx}].'))

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

