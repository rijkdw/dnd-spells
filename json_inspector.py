import pprint
import json
import inflect
from utils import *


dummy_spells = [{
            'name': 'Eldritch Blast',
            'subtitle': 'Evocation cantrip',
            'time': '1 action',
            'duration': 'Instantaneous',
            'components': 'VS',
            'classes': 'Warlock',
            'source': 'PHB',
            'description': ['spell yes']
        }]


@timer
def load_json_spells():
    return json.loads('\n'.join(open('files/spells.json', 'r+', encoding='utf-8').readlines())[1:])


@timer
def load_clean_json_spells():
    return json.loads('\n'.join(open('files/spells_clean.json', 'r+', encoding='utf-8').readlines()))


def get_spell_with_name(target_spell_name: str):
    for spell in load_clean_json_spells():
        if spell['name'].lower() == target_spell_name.lower():
            return spell


@timer
def get_spells_with_names(target_spell_names: list):
    spells_to_return = []
    for spell in load_clean_json_spells():
        if spell['name'] in target_spell_names:
            spells_to_return.append(spell)
    return spells_to_return

    for spell_name in target_spell_names:
        spells_to_return.append(get_spell_with_name(spell_name))
    return spells_to_return


@timer
def spell_json_to_jinja(json_spell):
    inf = inflect.engine()

    # casting time
    time_unit = json_spell['time'][0]['unit']
    time_num = json_spell['time'][0]['number']
    time = f'{time_num} {inf.plural(time_unit, time_num)}'
    ritual = 0
    if 'meta' in list(json_spell.keys()):
        ritual = 1
        time += ' (ritual)'

    # range
    if 'special' in json_spell['range'].values():
        s_range = 'special'
    else:
        range_unit = json_spell['range']['distance']['type']
        if range_unit == 'self':        s_range = 'self'
        elif range_unit == 'touch':     s_range = 'touch'
        elif range_unit == 'sight':     s_range = 'sight'
        elif range_unit == 'unlimited': s_range = 'unlimited'
        else:
            range_num = json_spell['range']['distance']['amount']
            s_range = f'{range_num} {range_unit}'

    # subtitle (level + school)
    school = school_dict[json_spell['school']]
    level = json_spell['level']
    subtitle = f'{school} cantrip' if level == 0 else f'{inf.ordinal(level)}-level {school.lower()}'

    # components
    components_list = [c.upper() for c in list(json_spell['components'].keys())]
    if 'M' in components_list:
        materials = json_spell['components']['m']
        if type(materials) == dict:
            materials = materials['text']
        components_list.remove('M')
        components_list.append(f'M ({materials})')
    components = ', '.join(components_list)

    # duration
    durations = []
    concentration = 0
    for duration_obj in json_spell['duration']:
        if duration_obj['type'] == 'instant':
            duration_i = 'instantaneous'
        elif duration_obj['type'] == 'permanent':
            duration_i = 'until dispelled'
        elif duration_obj['type'] == 'special':
            duration_i = 'special'
        else:
            duration_num = duration_obj['duration']['amount']
            duration_unit = duration_obj['duration']['type']
            duration_i = f'{duration_num} {inf.plural(duration_unit, duration_num)}'
        if 'concentration' in list(duration_obj.keys()):
            duration_i += ' (concentration)'
            concentration = 1
        durations.append(duration_i)
    duration = ' or '.join(durations).capitalize()

    # classes and subclasses
    class_names = []
    if 'fromClassList' in list(json_spell['classes'].keys()):
        class_names += [d['name'] for d in json_spell['classes']['fromClassList']]
    if 'fromSubclass' in list(json_spell['classes'].keys()):
        for class_subclass_dict in json_spell['classes']['fromSubclass']:
            class_name = class_subclass_dict['class']['name']
            subclass_name = class_subclass_dict['subclass']['name']
            # if '(UA)' not in subclass_name:
            class_names.append(f'{class_name} ({subclass_name})')
    classes = ', '.join(remove_duplicates(class_names))

    source = json_spell['source']
    if 'page' in list(json_spell.keys()):
        page = json_spell['page']
        source += f' (p{page})'

    # spell description (includes html)
    description = []
    for entry in json_spell['entries']:
        if type(entry) == str:
            description.append(entry)
        if type(entry) == dict:
            if entry['type'] == 'entries':  # ex:  Alter Self
                name = entry['name']
                text = '\n'.join(entry['entries'])
                description.append(f'<b><i>{name}.</i></b> {text}')
            if entry['type'] == 'table':    # ex:  Animate Objects
                table_string = '<table>\n'
                # headers
                headers = entry['colLabels']
                table_string += '  <tr>\n'
                for h in headers:
                    table_string += f'    <th>{h}</th>\n'
                table_string += '  </tr>\n'
                # rows
                rows = entry['rows']
                for row in rows:
                    table_string += '  <tr>\n'
                    for r in row:
                        table_string += f'    <td>{r}</td>\n'
                    table_string += '  </tr>\n'
                table_string += '</table'
                description.append(table_string)
            if entry['type'] == 'list':     # ex:  Augury
                list_string = '<br><ul>'
                for item in entry['items']:
                    list_string += f'\n<li>{item}</li>'
                list_string += '\n</ul>'
                description.append(list_string)

    jinja_spell = {
        'name': json_spell['name'],
        'subtitle': subtitle,
        'level': level,
        'school': school,
        'time': time.capitalize(),
        'range': s_range.capitalize(),
        'components': components,
        'duration': duration.capitalize(),
        'classes': classes,
        'source': source,
        'description': description,
        'ritual': ritual,
        'concentration': concentration
    }

    if 'entriesHigherLevel' in list(json_spell.keys()):
        jinja_spell['description_higher'] = []
        higher_level_entries = json_spell['entriesHigherLevel'][0]['entries']
        for higher_level_entry in higher_level_entries:
            jinja_spell['description_higher'].append(higher_level_entry)

    return jinja_spell


@timer
def all_spells_json_to_jinja():
    return [spell_json_to_jinja(s) for s in load_json_spells()]


@timer
def generate_clean_json():
    spells_list = [spell_json_to_jinja(s) for s in load_json_spells()]
    with open('files/spells_clean.json', 'w+') as file:
        file.write(json.dumps(spells_list, indent=4))


if __name__ == '__main__':
    generate_clean_json()
