from sylfk import SYLFk

app = SYLFk()

@app.route('/index',methods=['GET'])
def index():
	return 'This is a route test page'

@app.route("/test/js")
def test_js():
	return '<script src="/static/test.js"></script>'
app.run()