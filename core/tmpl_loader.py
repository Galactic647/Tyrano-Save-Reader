from core.errors import TemplateNotFoundError

from typing import Union
from pathlib import Path
import regex
import json
import os


def load_template(template: Union[str, Path]) -> dict:
    if isinstance(template, str):
        if not template.endswith('.json'):
            template = f'{template}.json'
        template = Path(template)

    if not template.exists():
        if not os.path.exists(f'templates/{template}'):
            raise TemplateNotFoundError(str(template))
        template = f'templates/{template}'
    with open(template, 'r') as file:
        config = json.load(file)
    return config


def _get_val_from_tmpl(data, path):
    if isinstance(path, str):
        elements = regex.split(r'(\.\w+|\[\d+\])', path)
        elements = [el for el in elements if el and el != '.']

        current = data
        for el in elements:
            if el.startswith('[') and el.endswith(']'):
                index = int(el[1:-1])
                current = current[index]
            else:
                current = current[el.lstrip('.')]
        return current
    elif isinstance(path, list):
        return [_get_val_from_tmpl(data, p) for p in path]
    elif isinstance(path, dict):
        return {k: _get_val_from_tmpl(data, p) for k, p in path.items()}
    raise TypeError('path must be a string, list, or dict')


def _translate_slots_from_style(slots: list, style: str, save_tabs: int, slots_per_tabs: int) -> list:
    catcher = regex.findall(r'\{((?:tab|slot|tab_slot))\}', style)
    escaped = regex.escape(style)
    for c in catcher:
        escaped = escaped.replace(f'\\{{{c}\\}}', f'(?P<{c}>\\d+)')
    pattern = regex.compile(escaped, regex.VERBOSE | regex.IGNORECASE)
    
    translated_slots = []
    for s in slots:
        result = pattern.search(s)
        if result is None:
            raise ValueError('slots-to-check must have the same style as parsed-slot-style')
        
        result = result.groupdict() 
        tab = int(result.get('tab', -1))
        slot = int(result.get('slot', -1))
        tab_slot = int(result.get('tab_slot', -1))

        if slot > 0:
            translated_slots.append(slot - 1)
            continue
        if (tab_slot != -1 == tab) or (tab != -1 == tab_slot):
            raise ValueError('tab_slot must be used with tab and vice versa')
        elif tab > save_tabs:
            raise ValueError('tab must be less than or equal to save_tabs')
        elif tab_slot > slots_per_tabs:
            raise ValueError('tab_slot must be less than or equal to slot_per_tabs')
        translated_slots.append(save_tabs * (tab - 1) + tab_slot - 1)
    return translated_slots


def get_value_from_template(data: dict, tmpl_config: dict) -> dict:
    save_tabs = tmpl_config.get('save-tabs', -1)
    slots_per_tabs = tmpl_config.get('save-slots-per-tab', -1)
    if slots_per_tabs != -1 == save_tabs:
        raise ValueError('save-tabs and save-slots-per-tab must be set together')

    slot_style = tmpl_config.get('parsed-slot-style', str())
    slots_to_check = tmpl_config.get('slots-to-check', list())
    variables = tmpl_config.get('variables', dict())
    if not variables:
        return data

    saves = dict()

    if slot_style and slots_to_check:
        translated_slots = _translate_slots_from_style(slots_to_check, slot_style, save_tabs, slots_per_tabs)
        for idx, fmt in zip(translated_slots, slots_to_check):
            saves[fmt] = _get_val_from_tmpl(data['data'][idx], variables)
        return saves
    
    curtab = 1
    curslot = 1
    curtabslot = 1

    for idx, slots in enumerate(data['data'], start=1):
        saves[slot_style.format(tab=curtab, slot=curslot, tab_slot=curtabslot)] = _get_val_from_tmpl(slots, variables)
        
        if curtabslot < slots_per_tabs and save_tabs is not None is not slots_per_tabs:
            curtabslot += 1
        else:
            curtabslot = 1
            curtab += 1
        curslot += 1
    return saves
