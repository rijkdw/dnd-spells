import pprint
import json


def load_json_spells():
    return json.loads('\n'.join(open('files/spells.json', 'r+', encoding='utf-8').readlines())[1:])


if __name__ == '__main__':
    spells_list = load_json_spells()

    print(list(spells_list[0].keys()))

    # top level key inspection
    private_sanctum = [sp for sp in spells_list if sp['name'].lower()[0:6] == 'morden'][2]
    pprint.pprint(private_sanctum)
