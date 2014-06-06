from flask import Flask, request, render_template
from constants import SITENAME
import time, urllib2, html2text

def configure_sitename(app):
    @app.context_processor
    def inject_sitename():
        return dict(SITENAME=SITENAME)

app = Flask(__name__)
app.debug = True
configure_sitename(app)

@app.route('/', methods=['GET', 'POST'])
def search():
    t0 = time.time()
    t1 = time.time()
    debug = 0
    data = {
        'url': '',
        'word': '',
        'counter': 0,
        'time': time.time(),
        'size': 0
    }
    counter = 0
    if request.method == 'GET':
        data['url'] = request.args.get('url', '')
        data['word'] = request.args.get('word', '')
        if request.args.get('withdebug'):
            debug = int(request.args.get('withdebug'))
    elif request.method == 'POST':
        data['url'] = request.form['url']
        data['word'] = request.form['word']
        if request.form['withdebug']:
            debug = int(request.form['withdebug'])
    else:
        return render_template('400.html')

    if debug:
        t0 = time.time()

    try:
        page = urllib2.urlopen(data['url'], timeout = 5)
    except urllib2.URLError, e:
        return render_template('408.html')

    source = page.read()

    handler = html2text.HTML2Text()
    handler.ignore_links = True

    content = handler.handle(source.decode('utf8').encode('ascii','ignore'))
    data['counter'] = content.count(data['word'].encode('ascii','ignore'))

    if debug:
        t1 = time.time()-t0
        data['time'] = t1
        if page.info().getheader('Content-Length'):
            data['size'] = int(page.info().getheader("Content-Length"))
        return render_template('debug.html', data=data)
    else:
        return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run()
