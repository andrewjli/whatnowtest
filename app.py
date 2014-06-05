from flask import Flask, request, render_template
from constants import SITENAME
import urllib2

def configure_sitename(app):
    @app.context_processor
    def inject_sitename():
        return dict(SITENAME=SITENAME)

app = Flask(__name__)
app.debug = True
configure_sitename(app)

@app.route('/', methods=['GET', 'POST'])
def search():
    data = {
        'url': '',
        'word': '',
        'counter': 0
    }
    counter = 0
    if request.method == 'GET':
        data['url'] = request.args.get('url', '')
        data['word'] = request.args.get('word', '')
    if request.method == 'POST':
        data['url'] = request.form['url']
        data['word'] = request.form['word']
    else:
        return render_template('400.html')

    page = urllib2.urlopen(data['url'])
    content = page.read()
    data['counter'] = content.count(data['word'].encode('ascii','ignore'))

    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run()
