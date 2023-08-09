from flask import Flask, render_template, request


app = Flask(__name__, template_folder='templates', static_folder='static')


@app.route('/', methods=['GET'])
def index():
    answer = ''
    question = ''
    if request.method == 'GET':
        question = request.args.get("question")
        if question is None:
            question = ''
            return render_template('index.html', answer=answer, question=question)
        answer = get_answer(question)
    return render_template('index.html', answer=answer, question=question)


def get_answer(question):
    return 'Question "' + question + '" answered.'


if __name__ == '__main__':
    app.run()
