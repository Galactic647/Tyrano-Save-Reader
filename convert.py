from core import savparser as sp

from typing import Union

from pathlib import Path
import argparse
import os


def main(input_file: Union[str, Path], output_file: Union[str, Path]) -> None:
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

    if input_file.suffix == '.sav':
        parser = sp.SavParser(input_file, output_file, overwrite_source=False)
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
    return argparser.parse_args()


if __name__ == '__main__':
    args = initialize()
    main(args.input, args.output)