from flask import Flask, render_template, request
import flask_wtf, wtforms
import pprint
from query_utils import *
from config import Config

app = Flask(__name__)
app.config.from_object(Config)


class QueryForm(flask_wtf.FlaskForm):
    query_area = wtforms.StringField('SELECT * FROM spells')
    submit = wtforms.SubmitField('Perform query')


def generate_subtitle(spell_dict):
    import inflect
    level = inflect.engine().ordinal(int(spell_dict['level']))
    school = spell_dict['school']
    ritual = ' (ritual)' if spell_dict['ritual'].lower() == 'yes' else ''
    if level == '0th':
        return f'{school} cantrip{ritual}'.capitalize()
    else:
        return f'{level} level {school}{ritual}'


def generate_components(spell_dict):
    ret_str = ', '.join(list(spell_dict['components']))
    return ret_str


def generate_duration(spell_dict):
    concentration = 'Concentration, ' if spell_dict['concentration'].lower() == 'yes' else ''
    return f'{concentration}up to 1 minute'.capitalize()


def query_to_dict(result):

    dict_list = []

    for row in result[1]:
        dict_row = {}
        for key, val in zip(result[0], list(row)):
            dict_row[key] = val
        dict_row['subtitle'] = generate_subtitle(dict_row)
        dict_list.append(dict_row)

    return dict_list


@app.route('/home', methods=['GET', 'POST'])
def render_home():
    form = QueryForm()
    if form.is_submitted():
        connection = create_connection('C:\\Users\\Rijk\\PycharmProjects\\DatabasePlaying\\sm_app.sqlite')
        query = f'SELECT * FROM spells {str(form.query_area.data)} ORDER BY name'
        try:
            spells = query_to_dict(execute_read_query(connection, query))
            return render_template('home.html', title='D&D Spells 5th Edition', form=form, spells=spells,
                                   gen_sub_func=generate_subtitle, gen_comp_func=generate_components,
                                   gen_dur_func=generate_duration)
        except:
            print('Error in render_home()')
    return render_template('home.html', title='D&D Spells 5th Edition', form=form)


@app.route('/about')
def render_about():
    return render_template('about.html', title='D&D Spells - About')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
    # connection = create_connection('C:\\Users\\Rijk\\PycharmProjects\\DatabasePlaying\\sm_app.sqlite')
    # query = 'SELECT * FROM spells'
    # spells = query_to_dict(execute_read_query(connection, query))
    # pprint.pprint(spells)