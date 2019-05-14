from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/data_query')
def get_contact():
    org_id = request.args.get("orgId")
    print "us1"
    return "processed by us1 backend"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
