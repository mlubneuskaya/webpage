from flask import Flask, render_template, request, abort
from transformers import T5Tokenizer, T5ForConditionalGeneration
from flask_swagger_ui import get_swaggerui_blueprint
import psycopg2

app = Flask(__name__, template_folder='templates', static_folder='static')

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Sample API"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

model_name = 'google/flan-t5-small'
model = T5ForConditionalGeneration.from_pretrained(model_name)
tokenizer = T5Tokenizer.from_pretrained(model_name)


@app.route('/', methods=['GET'])
def index():
    translation = ''
    phrase = request.args.get("phrase")
    if phrase is not None:
        translation = get_answer(phrase)
    else:
        phrase = ''
    return render_template('index.html', translation=translation, phrase=phrase, language=language.upper())


host = '127.0.0.1'
try:
    conn = psycopg2.connect(database='settings', host=host, user='postgres', password='password', port=5432)
    cursor = conn.cursor()
except Exception:
    print('Cannot connect to database')
    quit()


cursor.execute('SELECT default_language FROM default_settings')
language = cursor.fetchall()[0][0]


@app.route('/settings/', methods=['POST'])
def update_default_language():
    new_language = request.json.lower()
    if new_language not in ["german", "french", "romanian"]:
        abort(400)
    command = "UPDATE default_settings SET default_language = '{}'".format(new_language)
    try:
        cursor.execute(command)
    except Exception:
        abort(500)
    conn.commit()
    return 'Default language updated to {}'.format(new_language)


def get_answer(phrase):
    input_phrase = 'Translate English to {}: {}'.format(language, phrase)
    input_ids = tokenizer(input_phrase, return_tensors='pt').input_ids
    max_tokens = len(phrase) * 1.5
    outputs = model.generate(input_ids, max_new_tokens=max_tokens)
    translation = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return translation


if __name__ == '__main__':
    app.run(host='localhost', port=8000)

cursor.close()
conn.close()
