from core import save_monitor as sm, savparser as sp, tmpl_loader as tl
from core.logger import logger
from core import MIN_BUFFER_DELAY, MIN_BACKUPS
from core import errors

from typing import Union

from pathlib import Path
import configparser
import argparse
import logging
import json
import time
import os

INTRO = """
Please open:

    {output}

on a text editor to edit the values, changes will be updated to source automatically.
DO NOT USE AUTO SAVE ON THE TEXT EDITOR.
"""


def _get_suffix(rank: int) -> str:
    if rank % 100 in [11, 12, 13]:
        return "th"
    elif rank % 10 == 1:
        return "st"
    elif rank % 10 == 2:
        return "nd"
    elif rank % 10 == 3:
        return "rd"
    else:
        return "th"


def main(input_file: Union[str, Path], output_file: Union[str, Path],
         cps: int, buffer: float, step_backup: bool, backup_limit: int, template: Union[str, Path]) -> None:
    if not os.path.exists(input_file):
        logger.critical(f'{input_file} does not exists')
        return
    if buffer < MIN_BUFFER_DELAY:
        logger.critical(f'Unable to start because buffer delay is too low {buffer}s, the minimum is {MIN_BUFFER_DELAY}')
        return
    if backup_limit < MIN_BACKUPS:
        logger.critical(f'Unable to start because backup limit is too low {backup_limit}, the minimum is {MIN_BACKUPS}')
        return
    
    try:
        tmpl = tl.load_template(template)
        logger.info(f'Loaded template for {tmpl["game"]!r}')
    except errors.TemplateNotFoundError as e:
        logger.critical(e.message)
        return

    if isinstance(input_file, str):
        input_file = Path(input_file)
    if isinstance(output_file, str):
        if output_file.lower() == 'auto':
            output_file = f'{input_file.parent}/parsed.json'
        output_file = Path(output_file)

    excs = get_excluded(input_file.parent)
    sp.EXCLUDED.extend(excs)

    logger.info('Checking integrity...')
    valid, true_sig, source_sig = sp.parser_integrity_check(input_file)
    if not valid:
        logger.error('Integrity check failed\n'
                     f'True source:     {true_sig}\n'
                     f'Repacked source: {source_sig}')
        logger.info('Running difference check...')

        start = time.perf_counter()
        diff_idx, *difference = sp.difference_check(input_file)
        logger.debug(f'Located difference at index {diff_idx} -> {difference[0]}|{difference[1]}')
        logger.debug(f'Highlighting difference')
        diff_highlight = sp.difference_highlight(*difference)
        end = time.perf_counter() - start
        suffix = _get_suffix(diff_idx)

        logger.info(f'Difference check completed in {end:.3f}s\n'
                    f'Difference located at the {diff_idx:,}{suffix} character\n'
                    f'True source:     {diff_highlight[0]}\n'
                    f'Repacked source: {diff_highlight[1]}')
        return
    logger.info('Parsing valid!\n'
                f'True source:     {true_sig}\n'
                f'Repacked Source: {source_sig}')

    logger.debug('Creating watcher objects')
    parser = sm.ParserWrapper(input_file, output_file, buffer, step_backup, backup_limit, tmpl)
    sav_watcher = sm.SavWatcher(parser, buffer)
    json_watcher = sm.JsonWatcher(parser, buffer)

    logger.debug('Creating monitor object')
    observer = sm.FileWatcher(cps)
    logger.debug(f'Adding {sav_watcher.monitor} as source')
    observer.add_source(sav_watcher)
    logger.debug(f'Adding {json_watcher.monitor} as parsed reference')
    observer.add_parsed(json_watcher)
    logger.debug('Starting monitor')
    observer.start()
    print(INTRO.format(output=os.path.abspath(output_file)))

    try:
        logger.debug('On main loop')
        while True:
            # Keep thread alive
            time.sleep(1e6)
    except KeyboardInterrupt:
        logger.debug('Keyboard interrupt detected')
        observer.stop_monitor()


def initialie() -> argparse.Namespace:
    argparser = argparse.ArgumentParser(prog='monitor',
                                        description='Monitor your saves', )
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
                              'increase the value if the program is going on parsing loop between source and json '
                              f'(min {MIN_BUFFER_DELAY} default 1s)')
    options.add_argument('-s',
                         '--step-backup',
                         action='store_true',
                         help='create backup every parsing')
    options.add_argument('-k',
                         '--backup-limit',
                         type=int,
                         default=5,
                         help='max number of backups to keep, old backup will be replaced with new ones'
                              '(min 2 default 5)')
    options.add_argument('-l',
                         '--log-level',
                         type=str,
                         default='info',
                         choices=['debug', 'info', 'warning', 'error', 'critical'],
                         help='log level (default info)')
    options.add_argument('-t',
                         '--template',
                         type=str,
                         default=str(),
                         help='use a template file for specific game to filter and edit important variables from the save data.')
    return argparser.parse_args()


def get_excluded(directory: Union[str, Path]) -> list:
    create_config(directory)
    parser = configparser.ConfigParser()
    parser.read(f'{directory}/monitor config.ini')
    return json.loads(parser.get('Settings', 'excluded'))


def create_config(directory: Union[str, Path]) -> None:
    if os.path.exists(f'{directory}/monitor config.ini'):
        return
    parser = configparser.ConfigParser()
    parser.add_section('Settings')
    parser.set('Settings', 'excluded', json.dumps(['*', '+']))

    with open(f'{directory}/monitor config.ini', 'w') as file:
        parser.write(file)
        file.close()


if __name__ == "__main__":
    try:
        args = initialie()
        arguments = [f'{s}: {getattr(args, s)!r}' for s in dir(args) if not s.startswith('_')]

        logger.setLevel(getattr(logging, args.log_level.upper()))
        logger.debug(f'Running with args:\n{{args}}'.format(args='\n'.join(arguments)))
        main(args.input, args.output, args.cps, args.buffer, args.step_backup, args.backup_limit, args.template)
    except KeyboardInterrupt:
        logger.info('Interrupted')
    except Exception as e:
        logger.critical(f'Critical error encountered'
                f'\n{"-" * 20}'
                f'\n{e}'
                f'\n{"-" * 20}')
