from core.savparser import SavParser
from core.logger import logger
from core import MIN_BUFFER_DELAY

from typing import Optional, Union

from json.decoder import JSONDecodeError
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

    logger.debug('Listing backups')
    backups = os.listdir(f'{input_file.parent}/backup')
    backups = sorted(backups, key=lambda x: x.split('.')[0][-17:], reverse=True)
    if len(backups) >= backup_limit:
        logger.debug(f'Backup will be overlimit by {backup_limit - len(backups) + 1}')
        for backup in backups[backup_limit - 1:]:
            bkp_file = f'{input_file.parent}/backup/{backup}'
            logger.debug(f'Removing backup -> {bkp_file}')
            os.remove(bkp_file)

    date_sig = datetime.strftime(datetime.now(), r'%Y-%m-%d@%H%M%S')
    name = f'{input_file.parent}/backup/{input_file.stem} {date_sig}{input_file.suffix}'
    logger.debug(f'Creating backup -> {name}')
    shutil.copy(input_file, name)
    logger.debug('Backup completed!')


class ParserWrapper(object):
    def __init__(self, file: Union[str, Path], output: Union[str, Path], buffer: float,
                 step_backup: Optional[bool] = False, backup_limit: Optional[int] = 5) -> None:
        if not os.path.exists(file):
            raise FileNotFoundError
        self.file = Path(file)
        logger.debug('Creating sav parser')
        self.parser = SavParser(file, output, overwrite_source=True)
        self.step_backup = step_backup
        if not backup_limit:
            backup_limit = 5
        self.backup_limit = backup_limit

        self.save_event = False
        self.modified_event = False

        self._triggered_checkpoint = 0
        self._buffer = buffer

        self.backup()
        self.unpack()
    
    def backup(self) -> None:
        loc = os.path.abspath(os.path.dirname(self.parser.source))
        logger.debug(f'Creating backup at {loc}')
        backup(self.parser.source, self.backup_limit)

    def unpack(self) -> None:
        triggered = time.perf_counter()
        logger.debug('Unpacking source to json')
        self.parser.unpack()
        
        delta = triggered - self._triggered_checkpoint
        logger.debug(f'Unpack triggered {delta:.5f}s after last pack event\n'
                     f'Unpack triggered at {triggered:.5f}\n'
                     f'Last pack event triggered at {self._triggered_checkpoint:.5f}')
        if delta < max(self._buffer, MIN_BUFFER_DELAY):
            logger.warning('Unpacking process still detected by json watcher, buffer delay might be too short.\n'
                           'if this is not cause by an actual game save, '
                           'please increase the buffer delay (-b, --buffer).\n'
                           'if it was from a gave save then you can ignore this warning\n'
                           f'Triggered in {delta:.5f}s after Unpacking')
        self._triggered_checkpoint = time.perf_counter()
            
    def pack(self) -> None:
        triggered = time.perf_counter()
        logger.debug('Packing json to source')
        if self.step_backup:
            self.backup()
        self.parser.pack()
        
        delta = triggered - self._triggered_checkpoint
        logger.debug(f'Unpack triggered {delta:.5f}s after last pack event\n'
                     f'Unpack triggered at {triggered:.5f}\n'
                     f'Last pack event triggered at {self._triggered_checkpoint:.5f}')
        if delta < max(self._buffer, MIN_BUFFER_DELAY):
            logger.warning('Packing process still detected by sav watcher, buffer delay might be too short.\n'
                           'if you haven\'t save anything in the parsed json file, '
                           'please increase the buffer delay (-b, --buffer).\n'
                           'if it was from a gave save then you can ignore this warning\n',
                           'Triggered in {delta:.5f}s after Unpacking')
        self._triggered_checkpoint = time.perf_counter()

class WatcherMeta(object):
    def __init__(self, parser: ParserWrapper, buffer: float) -> None:
        self.parser = parser
        self.buffer = buffer

    @property
    def name(self):
        pass

    def check(self):
        pass
    
    def on_modified(self) -> None:
        pass
    

class SavWatcher(WatcherMeta):
    def __init__(self, parser: ParserWrapper, buffer: float) -> None:
        super().__init__(parser, buffer)
        self.monitor = self.parser.file

    @property
    def name(self) -> str:
        return Path(self.parser.parser.true_source).name
    
    def check(self) -> float:
        return self.monitor.stat().st_mtime

    def on_modified(self) -> None:
        if self.parser.save_event:
            logger.info('Json -> Source synced!')
        else:
            logger.info('Source changed!')
            logger.debug('Triggering modified event to surpress json watcher')
            self.parser.modified_event = True
            
            start = time.perf_counter()
            self.parser.unpack()
            logger.info(f'Changes unpacked! in {time.perf_counter() - start:.3f}s')
            logger.debug('Delay buffer after unpacking to compromise saving process')
            time.sleep(self.buffer)
            logger.debug('Deactivating modified event')
            self.parser.modified_event = False

class JsonWatcher(WatcherMeta):
    def __init__(self, parser: ParserWrapper, buffer: float) -> None:
        super().__init__(parser, buffer)
        self.monitor = Path(self.parser.parser.output)

    @property
    def name(self) -> str:
        return self.parser.parser.output.name
    
    def check(self) -> float:
        return self.monitor.stat().st_mtime
        
    def on_modified(self) -> None:
        if self.parser.modified_event:
            logger.info('Changes loaded!')
        else:
            logger.info('Json changed!')
            logger.debug('Triggering save event to surpress sav watcher')
            self.parser.save_event = True

            start = time.perf_counter()
            self.parser.pack()
            logger.info(f'Changed packed! in {time.perf_counter() - start:.3f}s')
            logger.debug('Delay buffer after packing to compromise saving process')
            time.sleep(self.buffer)
            logger.debug('Deactivating save event')
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
                logger.debug(f'Detected change in {watch.name}\n'
                             f'Checkpoint: {checkpoint}\n'
                             f'Checked:    {check}')
                checkpoint = check

                retries = 1
                success = False
                logger.debug('Trying to process event')
                while not success:
                    try:
                        watch.on_modified()
                        success = True
                    except JSONDecodeError:
                        if retries >= 5:
                            logger.critical(f'Unable to parse {watch.name}, json decode error')
                            return
                        logger.error(f'Failed to process {watch.name} '
                                     'possibly checking the save file before it finishes saving'
                                     f', retrying in 2s ({retries}/5)')
                        time.sleep(2)
                        retries += 1
                    except Exception as e:
                        if retries >= 5:
                            logger.critical(f'Unable to parse {watch.name}, unknown error'
                                         f'\n{"-" * 20}'
                                         f'\n{e}'
                                         f'\n{"-" * 20}')
                            return
                        logger.error(f'Failed to process {watch.name}, unknown error'
                                     f'{"-" * 20}'
                                     f'{e}'
                                     f'{"-" * 20}'
                                     f', retrying in 2s ({retries}/5)')
                        time.sleep(2)
                        retries += 1
            time.sleep(self.delay)
    
    def start(self) -> None:
        logger.debug('Creating threads...')
        for s, w in self._watches.items():
            thread = threading.Thread(target=self._monitor, args=(w,), daemon=True)
            self._threads[s] = thread
        logger.debug('Starting threads...')
        for th in self._threads.values():
            th.start()
        self.running = True
        logger.info('Watching!')
    
    def stop_monitor(self) -> None:
        if self.running:
            logger.debug('Stopping threads...')
            for th in self._threads.values():
                th.join(timeout=0)
            logger.info('Stopped watching!')
            self.running = False
        else:
            logger.info('Already stopped!')
