from core.errors import TemplateNotFoundError, InvalidTemplateError

from typing import Union, Optional
from pathlib import Path
import regex
import glob
import json
import os


def load_template(template: Union[str, Path], auto_load: Optional[bool] = False, game_exec: Optional[str] = None) -> dict:
    if isinstance(template, str):
        if not template.endswith('.json'):
            template = f'{template}.json'
        template = Path(template)
    if not os.path.exists('templates'):
        os.mkdir('templates')

    if auto_load and not game_exec:
        raise ValueError('game_exec must be set if auto_load is True')
    elif auto_load and template != '.json':
        templates = glob.glob('templates/**/*.json', recursive=True)
        if not templates:
            raise TemplateNotFoundError('No template found')

        invalid_tmpl = []
        for t in templates:
            with open(t, 'r') as file:
                try:
                    config = json.load(file)
                except json.decoder.JSONDecodeError:
                    invalid_tmpl.append(t)
                    continue
                file.close()
            if config.get('game-executable') == game_exec:
                return config
        if invalid_tmpl:
            raise InvalidTemplateError(f'Found {len(invalid_tmpl)} invalid templates: \n * {{inv_tmpl}}'.format(inv_tmpl="\n * ".join(invalid_tmpl)))
        raise TemplateNotFoundError('No template found')

    if not template.exists():
        templates = glob.glob(f'templates/**/{template}', recursive=True)
        if not templates:
            raise TemplateNotFoundError(f'Template {template!r} not found')
        template = templates[0]
    with open(template, 'r') as file:
        try:
            config = json.load(file)
        except json.decoder.JSONDecodeError:
            raise InvalidTemplateError(f'Invalid template {template!r}')
        file.close()
    return config


def _get_val_from_tmpl(data, path):
    if isinstance(path, str):
        elements = regex.split(r'(\.\w+|\[\d+\])', path)
        elements = [el for el in elements if el and el != '.']

        current = data
        for el in elements:
            try:
                if el.startswith('[') and el.endswith(']'):
                    index = int(el[1:-1])
                    current = current[index]
                else:
                    current = current[el.lstrip('.')]
            except KeyError:
                return path
            except IndexError:
                return path
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
        translated_slots.append(slots_per_tabs * (tab - 1) + tab_slot - 1)
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

    if not slots_to_check:
        slots_to_check = list(range(len(data['data'])))

    for slot in slots_to_check:
        try:
            index = int(slot)
        except ValueError:
            raise ValueError('slots-to-check cannot be styled if style is not provided')
        
        if slot_style:
            key = slot_style.format(tab=curtab, slot=curslot, tab_slot=curtabslot)
        else:
            key = str(slot)
        saves[key] = _get_val_from_tmpl(data['data'][index], variables)

        if curtabslot < slots_per_tabs and save_tabs is not None is not slots_per_tabs:
            curtabslot += 1
        else:
            curtabslot = 1
            curtab += 1
        curslot += 1
    return saves


def _set_val_from_tmpl(data, value, path: Union[str, list, dict]):
    if isinstance(path, str):
        elements = regex.split(r'(\.\w+|\[\d+\])', path)
        elements = [el for el in elements if el and el != '.']
        
        current = data
        for i, el in enumerate(elements):
            if el.startswith('[') and el.endswith(']'):
                index = int(el[1:-1])
                if i == len(elements) - 1:
                    current[index] = value
                else:
                    current = current[index]
            else:
                key = el.lstrip('.')
                if i == len(elements) - 1:
                    current[key] = value
                else:
                    current = current[key]
        return data
    elif isinstance(path, list):
        for v, p in zip(value, path):
            data = _set_val_from_tmpl(data, v, p)
        return data
    elif isinstance(path, dict):
        for v, p in zip(value.values(), path.values()):
            data = _set_val_from_tmpl(data, v, p)
        return data
    else:
        raise TypeError('path must be a string, list, or dict')

def set_value_from_template(data: dict, value: dict, tmpl_config: dict) -> dict:
    save_tabs = tmpl_config.get('save-tabs', -1)
    slots_per_tabs = tmpl_config.get('save-slots-per-tab', -1)
    if slots_per_tabs != -1 == save_tabs:
        raise ValueError('save-tabs and save-slots-per-tab must be set together')
    
    slot_style = tmpl_config.get('parsed-slot-style', str())
    slots_to_check = tmpl_config.get('slots-to-check', list())
    variables = tmpl_config.get('variables', dict())

    if slot_style and slots_to_check:
        for s, d in value.items():
            for v, p in zip(d.values(), variables.values()):
                index = _translate_slots_from_style([s], slot_style, save_tabs, slots_per_tabs)[0]
                data['data'][index] = _set_val_from_tmpl(data['data'][index], v, p)
        return data
    for s, d in value.items():
        for v, p in zip(d.values(), variables.values()):
            if slot_style:
                index = _translate_slots_from_style([s], slot_style, save_tabs, slots_per_tabs)[0]
            else:
                index = int(s)
            try:
                data['data'][index] = _set_val_from_tmpl(data['data'][index], v, p)
            except IndexError:
                continue
            except KeyError:
                continue
    return data
