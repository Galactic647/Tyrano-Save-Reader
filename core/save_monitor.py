from core.savparser import SavParser
from core.logger import logger

from typing import Optional, Union

from datetime import datetime
from pathlib import Path
import threading
import shutil
import time
import os


def backup(input_file: Union[str, Path], backup_limit: int) -> None:
    if isinstance(input_file, str):
        input_file = Path(input_file)
    if not os.path.exists(f'{input_file.parent}/backup'):
        os.mkdir(f'{input_file.parent}/backup')

    backups = os.listdir(f'{input_file.parent}/backup')
    backups = sorted(backups, key=lambda x: x.split('.')[0][-17:], reverse=True)
    if len(backups) >= backup_limit:
        for backup in backups[backup_limit - 1:]:
            os.remove(f'{input_file.parent}/backup/{backup}')

    date_sig = datetime.strftime(datetime.now(), r'%Y-%m-%d@%H%M%S')
    name = f'{input_file.stem} {date_sig}{input_file.suffix}'
    shutil.copy(input_file, f'{input_file.parent}/backup/{name}')


class ParserWrapper(object):
    def __init__(self, file: Union[str, Path], output: Union[str, Path],
                 step_backup: Optional[bool] = False, backup_limit: Optional[int] = 5) -> None:
        if not os.path.exists(file):
            raise FileNotFoundError
        self.file = Path(file)
        self.parser = SavParser(file, output, overwrite_source=True)
        self.step_backup = step_backup
        if not backup_limit:
            backup_limit = 5
        self.backup_limit = backup_limit
        self.backup()
        self.unpack()

        self.save_event = False
        self.modified_event = False
    
    def backup(self) -> None:
        backup(self.parser.source, self.backup_limit)

    def unpack(self) -> None:
        self.parser.unpack()
    
    def pack(self) -> None:
        if self.step_backup:
            self.backup()
        self.parser.pack()

class WatcherMeta(object):
    def __init__(self, parser: ParserWrapper, buffer: float) -> None:
        self.parser = parser
        self.buffer = buffer

    def check(self):
        pass
    
    def on_modified(self) -> None:
        pass
    

class SavWatcher(WatcherMeta):
    def __init__(self, parser: ParserWrapper, buffer: float) -> None:
        super().__init__(parser, buffer)
        self.monitor = self.parser.file
        self._already_synced = False
    
    def check(self) -> float:
        return self.monitor.stat().st_mtime

    def on_modified(self) -> None:
        if self.parser.save_event:
            logger.info('Source synced!')
        else:
            logger.info('Source changed!')
            self.parser.modified_event = True
            
            start = time.perf_counter()
            self.parser.unpack()
            logger.info(f'Changes unpacked! in {time.perf_counter() - start:.3f}s')
            time.sleep(self.buffer)
            self.parser.modified_event = False

class JsonWatcher(WatcherMeta):
    def __init__(self, parser: ParserWrapper, buffer: float) -> None:
        super().__init__(parser, buffer)
        self.monitor = Path(self.parser.parser.output)
    
    def check(self) -> float:
        return self.monitor.stat().st_mtime
        
    def on_modified(self) -> None:
        if self.parser.modified_event:
            logger.info('Changes loaded!')
        else:
            logger.info('Json changed!')
            self.parser.save_event = True

            start = time.perf_counter()
            self.parser.pack()
            logger.info(f'Changed packed! in {time.perf_counter() - start:.3f}s')
            time.sleep(self.buffer)
            self.parser.save_event = False

class FileWatcher(object):
    def __init__(self, cps: Optional[int] = 5) -> None:
        self.running = False
        if not cps:
            cps = 5
        self.cps = cps

        self._watches = dict()
        self._threads = dict()

    @property
    def delay(self) -> float:
        return 1. / self.cps
    
    def add_source(self, watch_obj: WatcherMeta) -> None:
        self._watches['source'] = watch_obj

    def add_parsed(self, watch_obj: WatcherMeta) -> None:
        self._watches['parsed'] = watch_obj
    
    def _monitor(self, watch: WatcherMeta) -> None:
        checkpoint = watch.check()
        while True:
            check = watch.check()
            if checkpoint != check:
                checkpoint = check
                watch.on_modified()
            time.sleep(self.delay)
    
    def start(self) -> None:
        logger.info('Watching!')
        for s, w in self._watches.items():
            thread = threading.Thread(target=self._monitor, args=(w,), daemon=True)
            self._threads[s] = thread
        for th in self._threads.values():
            th.start()
        self.running = True
    
    def stop_monitor(self) -> None:
        if self.running:
            for th in self._threads.values():
                th.join(timeout=0)
            logger.info('Stopped watching!')
            self.running = False
        else:
            logger.info('Already stopped!')
