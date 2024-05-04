from core import save_monitor as sm
from core import savparser as sp
from core.logger import logger

from typing import Union

from pathlib import Path
import argparse
import time
import os

INTRO = """
Please open:

    {output}

on a text editor to edit the values, changes will be updated to source automatically.
DO NOT USE AUTO SAVE ON THE TEXT EDITOR.
"""


def main(input_file: Union[str, Path], output_file: Union[str, Path],
         cps: int,buffer: float, step_backup: bool, backup_limit: int) -> None:
    if not os.path.exists(input_file):
        raise FileNotFoundError(f'{input_file} does not exists')
    
    if isinstance(input_file, str):
        input_file = Path(input_file)
    if isinstance(output_file, str):
        if output_file.lower() == 'auto':
            output_file = f'{input_file.parent}/parsed.json'
        output_file = Path(output_file)

    logger.info('Checking integrity...')
    if not sp.parser_integrity_check(input_file):
        logger.error('Integrity check failed')
        return
    logger.info('Parsing valid!')
    
    parser = sm.ParserWrapper(input_file, output_file, step_backup, backup_limit)
    sav_watcher = sm.SavWatcher(parser, buffer)
    json_watcher = sm.JsonWatcher(parser, buffer)

    observer = sm.FileWatcher(cps)
    observer.add_source(sav_watcher)
    observer.add_parsed(json_watcher)
    observer.start()
    print(INTRO.format(output=os.path.abspath(output_file)))

    try:
        while True:
            # Keep thread alive
            time.sleep(1e6)
    except KeyboardInterrupt:
        observer.stop_monitor()


def initialie() -> argparse.Namespace:
    argparser = argparse.ArgumentParser(prog='monitor',
                                        description='Monitor your saves',)
    argparser.add_argument('-i',
                           '--input',
                           type=str,
                           help='save file to monitor',
                           required=True)
    argparser.add_argument('-o',
                           '--output',
                           type=str,
                           default='auto',
                           help='parsed save output (default auto)')
    options = argparser.add_argument_group('additional options')
    options.add_argument('-c',
                           '--cps',
                           type=int,
                           default=5,
                           help='number of checks per second (default 5)')
    options.add_argument('-b',
                           '--buffer',
                           type=float,
                           default=1.0,
                           help='number of seconds of save buffer, '
                           'increase the value if the program is going on parsing loop (default 1s)')
    options.add_argument('-sb',
                           '--step-backup',
                           action='store_true',
                           help='create backup every parsing')
    options.add_argument('-bl',
                           '--backup-limit',
                           type=int,
                           default=5,
                           help='max number of backups to keep, old backup will be replaced with new ones (min 2 default 5)')
    return argparser.parse_args()


if __name__ == "__main__":
    args = initialie()
    main(args.input, args.output, args.cps, args.buffer, args.step_backup, args.backup_limit)
