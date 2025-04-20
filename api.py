from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['POST'])
def echo_headers():
    headers = request.headers
    response_text = "Headers de la requête :\n"
    
    for header, value in headers.items():
        response_text += f"{header}: {value}\n"
    
    return response_text, 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
