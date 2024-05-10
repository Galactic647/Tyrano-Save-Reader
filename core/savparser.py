from __future__ import annotations

from core import get_hash_sig

from colorama import Fore, Style

from typing import Optional, Union
from pathlib import Path
from urllib import parse
import pathlib
import difflib
import regex
import json
import os

RE_NON_ASCII = regex.compile(r'%u[0-9A-F]{4,6}')
RE_NON_ASCII_CAP = regex.compile(r'[^\x00-\x7F]')
EXCLUDED = list('')
TEMP_INTREGITY_CHECK_FILENAME = 'temp_integrity_check.json'


def _temp_file_gen(input_file: Path) -> SavParser:
    output = f'{input_file.parent}/{TEMP_INTREGITY_CHECK_FILENAME}'
    parser = SavParser(input_file, output=output, overwrite_source=False)
    parser.unpack()
    parser.pack()
    return parser


def parser_integrity_check(input_file: Path) -> tuple[bool, str, str]:
    try:
        parser = _temp_file_gen(input_file)
    except UnicodeDecodeError:
        return False, 'N/A', 'N/A'
    source_sig = get_hash_sig(parser.source)
    true_source_sig = get_hash_sig(parser.true_source)

    valid = source_sig == true_source_sig
    if valid:
        os.remove(parser.output)
        os.remove(parser.source)
    return valid, true_source_sig, source_sig


def _recursive_binary_diff_check(a, b, max_diff: Optional[int] = None) -> int:
    diff_idx = 0
    min_idx = 0
    if max_diff is not None:
        max_idx = max_diff
    else:
        max_idx = min(len(a), len(b)) - 1
        
    while min_idx < max_idx:
        mid_idx = (min_idx + max_idx) // 2
        if mid_idx + 1 == max_idx:
            mid_idx = max_idx
        check_margin = min(50, mid_idx)

        if a[mid_idx - check_margin: mid_idx + 1] != b[mid_idx - check_margin: mid_idx + 1]:
            diff_idx = mid_idx
            break
        min_idx = mid_idx
    if diff_idx != max_diff:
        return _recursive_binary_diff_check(a, b, diff_idx)
    return diff_idx

def difference_check(input_file: Path) -> tuple[int, str, str]:
    output = f'{input_file.parent}/{TEMP_INTREGITY_CHECK_FILENAME}'
    parser = SavParser(input_file, output=output, overwrite_source=False)

    with open(parser.true_source, 'r', encoding='utf-8') as file:
        true_source = file.readlines()[0]
        file.close()
    with open(parser.source, 'r', encoding='utf-8') as file:
        repack_source = file.readlines()[0]
        file.close()
    os.remove(parser.output)
    os.remove(parser.source)

    min_idx = _recursive_binary_diff_check(true_source, repack_source, None)
    return min_idx, true_source[min_idx - 3: min_idx + 10], repack_source[min_idx - 3: min_idx + 10]


def _highlight(text, diff_range, colour) -> str:
    highlight = []
    splitter = [text[r[0]:r[1] + 1] for r in diff_range]
    splitter = [regex.escape(s) for s in splitter]
    text_parts = regex.split(f'({"|".join(splitter)})', text)
    
    idx_cursor = 0
    range_idx = 0
    for tp in text_parts:
        if range_idx < len(diff_range):
            idx_range = diff_range[range_idx]
        if idx_range[0] <= idx_cursor <= idx_range[1]:
            range_idx += 1
            highlight.append(f'{colour}{tp}{Style.RESET_ALL}')
        else:
            highlight.append(tp)
        idx_cursor += len(tp)
    return ''.join(highlight)


def difference_highlight(a: str, b: str) -> tuple:
    if len(a) != len(b):
        raise ValueError('a and b must be of same length')

    source_diffs = []
    comp_diffs = []
    found_diff = False
    diff_type = None
    low_idx = 0
    
    differ = list(difflib.ndiff(a, b))
    for idx, diff in enumerate(differ):
        if diff_type != diff[0] and diff_type is not None:
            if diff_type == '-':
                idx_offset = sum(d[1] - d[0] + 1 for d in comp_diffs)
                source_diffs.append((low_idx - idx_offset, idx - idx_offset - 1))
            else:
                idx_offset = sum(d[1] - d[0] + 1 for d in source_diffs)
                comp_diffs.append((low_idx - idx_offset, idx - idx_offset - 1))
            found_diff = False
            diff_type = None
        
        if not found_diff and diff[0] != ' ':
            found_diff = True
            diff_type = diff[0]
            low_idx = idx
        if idx == len(differ) - 1 and found_diff:
            if diff_type == '-':
                idx_offset = sum(d[1] - d[0] + 1 for d in comp_diffs)
                source_diffs.append((low_idx - idx_offset, idx - idx_offset))
            else:
                idx_offset = sum(d[1] - d[0] + 1 for d in source_diffs)
                comp_diffs.append((low_idx - idx_offset, idx - idx_offset))
    
    ha = _highlight(a, source_diffs, Fore.GREEN)
    hb = _highlight(b, comp_diffs, Fore.LIGHTRED_EX)
    return ''.join(ha), ''.join(hb)


def unquote(text: str) -> str:
    search = RE_NON_ASCII.findall(text)

    if search is not None:
        filtered = []
        for s in search:
            trimmed = s[2:]
            unc = int(trimmed, 16)
            if unc > 1114111:  # Max unicode character
                trimmed = trimmed[:-1]
                unc = int(trimmed, 16)
            filtered.append((trimmed, chr(unc)))
        filtered = dict((f'%u{f[0]}', f[1]) for f in filtered)
        for k, v in filtered.items():
            text = text.replace(k, v)
    return parse.unquote(text)


def quote(text: str) -> str:
    search = RE_NON_ASCII_CAP.findall(text)
    text = parse.quote(text)

    excluded = dict((parse.quote(k), k) for k in EXCLUDED)
    if search:
        search = dict((parse.quote(k), f'%u{ord(k):0X}') for k in set(search))
        excluded.update(search)
    for k, v in excluded.items():
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
        with open(self.true_source, 'r', encoding='utf-8') as file:
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
        with open(self.source, 'w', encoding='utf-8') as file:
            file.write(data)
            file.close()
