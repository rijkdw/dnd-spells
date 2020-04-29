from flask import Flask, render_template
import flask_wtf, wtforms
import json
import pprint
from config import Config
from json_inspector import *

app = Flask(__name__)
app.config.from_object(Config)

spells_json_master = json.loads('\n'.join(open('files/spells.json', 'r+', encoding='utf-8').readlines())[1:])


class QueryForm(flask_wtf.FlaskForm):
    name_field = wtforms.StringField('Name')
    submit_button = wtforms.SubmitField('Search')
    class_radio = wtforms.RadioField('Levels', choices=list(range(0,10)))


@app.route('/home', methods=['GET', 'POST'])
def render_home():
    form = QueryForm()
    if form.is_submitted():
        pass
    spells = [spell_json_to_jinja(s) for s in load_json_spells()]
    return render_template('home.html', title='D&D Spells 5th Edition', form=form, spells=spells)
    return render_template('home.html', title='D&D Spells 5th Edition', form=form)


@app.route('/spell:<string:spell_name>')
def render_spell_page(spell_name):
    spell = spell_json_to_jinja([s for s in load_json_spells() if s['name'].lower() == spell_name.lower()][0])
    return render_template('spell.html', title=f'{spell_name} – D&D Spells 5e', spell=spell)


@app.route('/about')
def render_about():
    return render_template('about.html', title='About – D&D Spells 5e')


if __name__ == '__main__':
    app.run(debug=True, port=5000)