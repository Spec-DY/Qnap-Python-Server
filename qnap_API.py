from flask import Flask, request, jsonify, session
from qnapstats import QNAPStats
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = 'very_secret_key'



@app.route('/api/qnap_status/login', methods=['POST'])
def get_qnap_stats():
    data = request.get_json()
    ip = data.get('IP')
    port = data.get('port')
    username = data.get('username')
    password = data.get('password')
    
    qnap = QNAPStats(host=ip, port=port, username=username, password=password)
    
    
    try:
        system_stats = qnap.get_system_stats()
        model_info = system_stats['system']['model']
        session['ip'] = ip
        session['port'] = port
        session['username'] = username
        session['password'] = password
        print(f"login sucess session :{session}")
        return jsonify(model_info), 200
    except Exception as e:
        print(f"login failed session :{session}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/qnap_status/systemstatus', methods=['GET'])
def get_systemstatus():
    
    if (session):
        qnap = QNAPStats(host=session['ip'], port=session['port'], username=session['username'], password=session['password'])
    
    
    try:
        system_stats = qnap.get_system_stats()
        cpu_info = system_stats['cpu'], system_stats['memory']
        print(f"get status sucess session :{session}")
        return jsonify(cpu_info), 200
    except Exception as e:
        print(f"get status failed session :{session}")
        return jsonify({'error': str(e)}), 501
        


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
