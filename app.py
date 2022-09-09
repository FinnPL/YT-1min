from flask import Flask, render_template, request
import  scrap
app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')


@app.route("/list/video", methods=['GET'])
def search():
    video_id = request.args.get('id', None)
    if video_id:
        emptyList = []
        list = scrap.rabit("https://www.youtube.com/watch?v="+video_id, emptyList)
        src = "https://www.youtube.com/embed/" + video_id + "?playlist="
        for i in list:
            src += i + ","
        return render_template('list.html', src=src)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run()
