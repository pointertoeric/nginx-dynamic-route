from flask import Flask
from flask import request
from flask import Response

app = Flask(__name__)

@app.route('/get_dc')
def get_dc():
    org_id = request.args.get("orgId")
    print org_id
    if org_id == "1":
        return Response(response="us", headers={"x-route": "us1"})
    else:
        return Response(response="us1", headers={"x-route": "us2"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

