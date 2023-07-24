from flask import Flask

app = Flask(__name__) # Use __name__ as the import_name argument

@app.route('/hello', methods=['GET'])
def hello():
	return "Hello, world!"

if __name__ == '__main__':
        app.run(debug=True, port=8000)

