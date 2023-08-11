from flask import Flask, render_template, request
from transformers import T5Tokenizer, T5ForConditionalGeneration


model_name = 'google/flan-t5-small'
model = T5ForConditionalGeneration.from_pretrained(model_name)
tokenizer = T5Tokenizer.from_pretrained(model_name)

app = Flask(__name__, template_folder='templates', static_folder='static')


@app.route('/', methods=['GET'])
def index():
    translation = ''
    phrase = ''
    if request.method == 'GET':
        phrase = request.args.get("question")
        if phrase is None:
            phrase = ''
            return render_template('index.html', answer=translation, question=phrase)
        translation = get_answer(phrase)
    return render_template('index.html', answer=translation, question=phrase)


def get_answer(phrase):
    input_phrase = 'Translate English to German: ' + phrase
    input_ids = tokenizer(input_phrase, return_tensors='pt').input_ids
    max_tokens = len(phrase) * 1.5
    outputs = model.generate(input_ids, max_new_tokens=max_tokens)
    translation = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return translation


if __name__ == '__main__':
    app.run(port=5000)
