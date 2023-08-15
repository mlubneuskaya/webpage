from flask import Flask, render_template, request, jsonify
from transformers import T5Tokenizer, T5ForConditionalGeneration
from flask_swagger_ui import get_swaggerui_blueprint
import json


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
    phrase = ''
    if request.method == 'GET':
        phrase = request.args.get("question")
        if phrase is None:
            phrase = ''
            return render_template('index.html', translation=translation, phrase=phrase)
        translation = get_answer(phrase)
    return render_template('index.html', translation=translation, phrase=phrase)


def get_answer(phrase):
    input_phrase = 'Translate English to German: ' + phrase
    input_ids = tokenizer(input_phrase, return_tensors='pt').input_ids
    max_tokens = len(phrase) * 1.5
    outputs = model.generate(input_ids, max_new_tokens=max_tokens)
    translation = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return translation


if __name__ == '__main__':
    app.run(port=5000)
