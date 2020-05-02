from flask import Flask, render_template, redirect, url_for
import flask_wtf
import wtforms
from config import Config
from json_inspector import *
from utils import *
from database_handler import *

app = Flask(__name__)
app.config.from_object(Config)

inf = inflect.engine()

# Startup sequence

# generate clean json spells
generate_clean_json()
startup_database_init()


class QueryForm(flask_wtf.FlaskForm):

    global inf

    name_field = wtforms.StringField('Name')

    level_choices = [(0, 'Cantrip')]+[(x, inf.ordinal(x)) for x in list(range(1, 10))]
    level_checkbox = wtforms.SelectMultipleField('Level', choices=level_choices, option_widget=wtforms.widgets.CheckboxInput())

    school_choices = [(school, school) for school in school_list]
    school_checkbox = wtforms.SelectMultipleField('School', choices=school_choices, option_widget=wtforms.widgets.CheckboxInput())

    class_choices = [(c, c) for c in ['Bard', 'Cleric', 'Druid', 'Paladin', 'Ranger', 'Sorcerer', 'Warlock', 'Wizard']]
    class_checkbox = wtforms.SelectMultipleField('Class', choices=class_choices, option_widget=wtforms.widgets.CheckboxInput())

    submit_button = wtforms.SubmitField('Search')

    @timer
    def generate_query(self):

        name_fragment = self.name_field.data

        levels = [int(x) for x in self.level_checkbox.data]
        level_query = ' OR '.join([f'level = {level}' for level in levels])

        schools = self.school_checkbox.data
        schools_query = ' OR '.join([f'school = \"{school}\"' for school in schools])

        classes = self.class_checkbox.data
        classes_query = ' OR '.join([f'classes LIKE \'%{c}%\'' for c in classes])

        queries = [level_query, schools_query, classes_query]

        print(level_query, schools_query, classes_query)

        query = 'SELECT name FROM spells'
        if queries != ['']*len(queries):
            query += ' WHERE ' + ' AND '.join([f'({q})' for q in queries]).replace(' AND ()', '').replace(' () AND','')

        print(query)
        return query


@app.route('/home', methods=['GET', 'POST'])
@timer
def render_home():
    form = QueryForm()
    if form.is_submitted():
        query = form.generate_query()
        results = query_spell_table(query)[1]
        spell_names = [result[0] for result in results]
        spells = get_spells_with_names(spell_names)
        if len(spells) == 1:
            return redirect(url_for('render_spell_page', spell_name=spells[0]['name']))
        return render_template('home.html', title='D&D Spells 5th Edition', form=form, spells=spells)
    spells = load_clean_json_spells()
    return render_template('home.html', title='D&D Spells 5th Edition', form=form, spells=spells)


@app.route('/spell:<string:spell_name>')
def render_spell_page(spell_name):
    spell = get_spell_with_name(spell_name)
    spell_name = spell['name']
    return render_template('spell.html', title=f'{spell_name} – D&D Spells 5e', spell=spell)


@app.route('/about')
def render_about():
    return render_template('about.html', title='About – D&D Spells 5e')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
