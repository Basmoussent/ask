from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['POST', "GET"])
def echo_request():
    headers = request.headers
    content_type = request.content_type

    response_text = "=== Headers ===\n"
    for header, value in headers.items():
        response_text += f"{header}: {value}\n"

    response_text += f"\n=== Content-Type ===\n{content_type}\n"

    response_text += "\n=== Body ===\n"
    if content_type and "application/json" in content_type:
        response_text += request.get_data(as_text=True)
    elif content_type and "application/x-www-form-urlencoded" in content_type:
        for key, value in request.form.items():
            response_text += f"{key} = {value}\n"
    else:
        response_text += request.get_data(as_text=True)

    return response_text, 200, {"Content-Type": "text/plain"}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
