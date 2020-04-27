import pprint
import json
import inflect


school_dict = {
    'A': 'Abjuration', 'C': 'Conjuration', 'D': 'Divination', 'V': 'Evocation',
    'E': 'Enchantment', 'I': 'Illusion', 'N': 'Necromancy', 'T': 'Transmutation'
}


def load_json_spells():
    return json.loads('\n'.join(open('files/spells.json', 'r+', encoding='utf-8').readlines())[1:])


def spell_json_to_jinja(json_spell):
    inf = inflect.engine()

    time_unit = json_spell['time'][0]['unit']
    time_num = json_spell['time'][0]['number']
    time = f'{time_num} {inf.plural(time_unit, time_num)}'

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

    school = school_dict[json_spell['school']]
    level = json_spell['level']
    subtitle = f'{school} cantrip' if level == 0 else f'{inf.ordinal(level)}-level {school.lower()}'

    components_list = [c.upper() for c in list(json_spell['components'].keys())]
    if 'M' in components_list:
        materials = json_spell['components']['m']
        components_list.remove('M')
        components_list.append(f'M ({materials})')
    components = ', '.join(components_list)

    durations = []
    for duration_obj in json_spell['duration']:
        if duration_obj['type'] == 'instant':
            durations.append('instantaneous')
        elif duration_obj['type'] == 'permanent':
            durations.append('until dispelled')
        elif duration_obj['type'] == 'special':
            durations.append('special')
        else:
            duration_num = duration_obj['duration']['amount']
            duration_unit = duration_obj['duration']['type']
            durations.append(f'{duration_num} {inf.plural(duration_unit, duration_num)}')
    duration = ' or '.join(durations).capitalize()

    class_names = []
    if 'fromClassList' in list(json_spell['classes'].keys()):
        class_names += [d['name'] for d in json_spell['classes']['fromClassList']]
    # if 'fromSubclass' in list(json_spell['classes'].keys()):
    #     class_names += [d['name'] for d in json_spell['classes']['fromSubclass']]
    classes = ', '.join(class_names)

    jinja_spell = {
        'name': json_spell['name'],
        'subtitle': subtitle,
        'time': time,
        'range': s_range,
        'components': components,
        'duration': duration,
        'classes': classes
    }

    return jinja_spell


if __name__ == '__main__':
    spells_list = load_json_spells()

    # top level key inspection
    private_sanctum = [sp for sp in spells_list if sp['name'].lower()[0:6] == 'morden'][2]
    # pprint.pprint(private_sanctum)

    pprint.pprint(private_sanctum)
    print('')
    pprint.pprint(spell_json_to_jinja(private_sanctum))

    for spell in spells_list:
        try:
            spell_json_to_jinja(spell)
        except KeyError as error:
            print(spell['name'], error)
