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
    
    ip = request.args.get('IP')
    port = request.args.get('port')
    username = request.args.get('username')
    password = request.args.get('password')
    
    if not ip or not port or not username or not password:
        return jsonify({'error': 'Missing necessary parameters'}), 400
    
    try:
        qnap = QNAPStats(host=ip, port=port, username=username, password=password)
        system_stats = qnap.get_system_stats()
        system_health= qnap.get_system_health()
        
        # so it displays like: 'heath':'good'
        health_info = {'health': system_health}
        
        disk_info = qnap.get_smart_disk_health()
        response = {
            'cpu': system_stats['cpu'],
            'ram': system_stats['memory'],
            'health': health_info,
            'disk_info': disk_info
        }
        return jsonify(response), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
        


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
