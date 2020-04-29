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
    level_checkbox = wtforms.SelectMultipleField('Level', choices=[(x,x) for x in list(range(0,10))],
                                                 option_widget=wtforms.widgets.CheckboxInput())
    select_field = wtforms.SelectField('aa', choices=[('1','A'),('2','B'),('3','C')])
    boolean = wtforms.BooleanField('Boolean')

    def get_query(self):
        levels = [int(x) for x in self.level_checkbox.data]
        print(levels)


@app.route('/home', methods=['GET', 'POST'])
def render_home():
    form = QueryForm()
    if form.is_submitted():
        print(form.get_query())
    spells = [spell_json_to_jinja(s) for s
              in load_json_spells()]
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