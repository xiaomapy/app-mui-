from flask import globals
from flask import Flask, render_template
from views.login import logning
from views.register import reg
from views.user_info import info
from views.get_file import getfile
from views.content_song import song_cont
from views.devices import devs
from views.toys import toy
from views.friend import fri
from views.chat import cht

app = Flask(__name__)

app.register_blueprint(logning)
app.register_blueprint(reg)
app.register_blueprint(info)
app.register_blueprint(getfile)
app.register_blueprint(song_cont)
app.register_blueprint(devs)
app.register_blueprint(toy)
app.register_blueprint(fri)
app.register_blueprint(cht)


@app.route('/')
def hello_world():
    return render_template("web页面模拟玩具.html")


if __name__ == '__main__':
    app.run('0.0.0.0', 8080, debug=True)

    app.__call__
