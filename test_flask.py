from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Server is running!"

@app.route('/test')
def test():
    return {'status': 'ok'}

if __name__ == '__main__':
    print("Starting test server on http://localhost:5001")
    app.run(host='0.0.0.0', port=5001, debug=False)
