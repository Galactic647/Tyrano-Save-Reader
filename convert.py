from core import savparser as sp

from typing import Union, Optional

from pathlib import Path
import configparser
import argparse
import json
import os

DEFAULT_CONFIG = {
    'Settings': {
        'excluded': ['*', '+'],
        'included': ['~']
    }    
}


def main(input_file: Union[str, Path], output_file: Union[str, Path], first: Optional[bool] = False) -> None:
    if not os.path.exists(input_file):
        raise FileNotFoundError(f'{input_file} does not exists')

    if isinstance(input_file, str):
        input_file = Path(input_file)
    if isinstance(output_file, str):
        if output_file == 'auto' and input_file.suffix == '.sav':
            output_file = f'{input_file.parent}/parsed.json'
        elif output_file == 'auto' and input_file.suffix == '.json':
            output_file = f'{input_file.parent}/packed.sav'
        output_file = Path(output_file)
    if first and input_file.suffix == '.json':
        raise ValueError('Cannot use --first with .json file')

    sp.EXCLUDED.extend(get_excluded())
    sp.INCLUDED.extend(get_included())

    if input_file.suffix == '.sav':
        parser = sp.SavParser(input_file, output_file, overwrite_source=False)
        if first:
            parser.unpack_first_slot()
        else:
            parser.unpack()
    elif input_file.suffix == '.json':
        output_file.touch()
        parser = sp.SavParser(output_file, input_file, overwrite_source=True)
        parser.pack()
    else:
        raise ValueError(f'{input_file} is not a .sav or .json file')

def initialize() -> argparse.Namespace:
    argparser = argparse.ArgumentParser(prog='convert',
                                        description='Converts .sav to .json and vice versa')
    argparser.add_argument('-i',
                           '--input',
                           type=str,
                           help='.sav or .json input file',
                           required=True)
    argparser.add_argument('-o',
                           '--output',
                           type=str,
                           default='auto',
                           help='the output file (default auto)')
    argparser.add_argument('-f',
                           '--first',
                           action='store_true',
                           default=False,
                           help='only conver the first save slot instead of the entire file, '
                                'helpful if you want a reference to make a template')
    return argparser.parse_args()


def get_excluded() -> list:
    create_config()
    parser = configparser.ConfigParser()
    parser.read('convert config.ini')
    return json.loads(parser.get('Settings', 'excluded'))


def get_included() -> list:
    create_config()
    parser = configparser.ConfigParser()
    parser.read('convert config.ini')
    return json.loads(parser.get('Settings', 'included'))


def create_config() -> None:
    parser = configparser.ConfigParser()

    if os.path.exists('convert config.ini'):
        parser.read('convert config.ini')
    
    for section, data in DEFAULT_CONFIG.items():
        if section not in parser.sections():
            parser.add_section(section)
        
        for option, value in data.items():
            if not parser.has_option(section, option):
                parser.set(section, option, json.dumps(value))
    
    with open('convert config.ini', 'w') as file:
        parser.write(file)
        file.close()


if __name__ == '__main__':
    args = initialize()
    main(args.input, args.output, args.first)