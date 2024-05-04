from core import get_hash_sig

from typing import Optional, Union
from pathlib import Path
from urllib import parse
import pathlib
import regex
import json
import os

RE_NON_ASCII = regex.compile(r'%u[0-9A-F]{4}')
RE_NON_ASCII_CAP = regex.compile(r'[^\x00-\x7F]')
EXCLUDED = [
        '+',
        '*'
    ]
TEMP_INTREGITY_CHECK_FILENAME = 'temp_integrity_check.json'


def parser_integrity_check(input_file: Path) -> bool:
    output = f'{input_file.parent}/{TEMP_INTREGITY_CHECK_FILENAME}'
    parser = SavParser(input_file, output=output, overwrite_source=False)
    parser.unpack()
    parser.pack()

    source_sig = get_hash_sig(parser.source)
    true_source_sig = get_hash_sig(parser.true_source)

    os.remove(output)
    os.remove(parser.source)
    return source_sig == true_source_sig


def unquote(text: str) -> str:
    search = RE_NON_ASCII.findall(text)

    if search is not None:
        search = dict((k, chr(int(k[2:], 16))) for k in search)
        for k, v in search.items():
            text = text.replace(k, v)
    return parse.unquote(text)


def quote(text: str) -> str:
    search = RE_NON_ASCII_CAP.findall(text)
    text = parse.quote(text)

    if search:
        search = dict((parse.quote(k), f'%u{ord(k):0X}') for k in search)
        excluded = dict((parse.quote(k), k) for k in EXCLUDED)
        search.update(excluded)
        for k, v in search.items():
            text = text.replace(k, v)
    return text


class SavParser(object):
    def __init__(self, source: Union[str, Path], output: Optional[Union[str, Path]] = 'auto',
                 overwrite_source: Optional[bool] = False) -> None:
        if not os.path.exists(source):
            raise FileNotFoundError(f'File {source} does not exists')
        self._source = pathlib.Path(source)
        
        if not output:
            output = f'{self._source.parent}/parsed.json'
        self.output = pathlib.Path(output)
        self.overwrite_source = overwrite_source

    @property
    def source(self) -> str:
        if self.overwrite_source:
            return str(self._source)
        src_name = '.'.join(self._source.name.split('.')[:-1])
        src = pathlib.Path(f'{self._source.parent}/{src_name}-repack{self._source.suffix}')
        return str(src)
    
    @property
    def true_source(self) -> str:
        return str(self._source)

    def unpack(self) -> None:
        with open(self.true_source, 'r') as file:
            data = file.readline()
            file.close()

        data = unquote(data)
        data = json.loads(data)
        with open(self.output, 'wb') as file:
            d = json.dumps(data, indent=4, ensure_ascii=False)
            file.write(d.encode('utf-8'))
            file.close()

    def pack(self) -> None:
        with open(self.output, 'rb') as file:
            data = file.read()
            data = json.loads(data)
            file.close()
        
        data = json.dumps(data, separators=(',', ':'), ensure_ascii=False)
        data = quote(data)
        with open(self.source, 'w') as file:
            file.write(data)
            file.close()
