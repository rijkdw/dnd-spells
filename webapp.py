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
    query_area = wtforms.StringField('SELECT * FROM spells')
    submit = wtforms.SubmitField('Perform query')


@app.route('/home', methods=['GET', 'POST'])
def render_home():
    form = QueryForm()
    if form.is_submitted():
        spells = [{
            'name': 'Eldritch Blast',
            'subtitle': 'Evocation cantrip',
            'casting_time': '1 action',
            'duration': 'Instantaneous',
            'components': 'VS',
            'spell_lists': 'Warlock',
            'source': 'PHB'
        }]
        return render_template('home.html', title='D&D Spells 5th Edition', form=form, spells=spells)
    return render_template('home.html', title='D&D Spells 5th Edition', form=form)


@app.route('/about')
def render_about():
    return render_template('about.html', title='D&D Spells - About')


if __name__ == '__main__':
    app.run(debug=True, port=5000)