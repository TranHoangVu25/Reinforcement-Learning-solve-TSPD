from src.alogorithms.Q_learning.Q_learning_truck import Q_Learning
from src.alogorithms.Greedy_Sarsa.Optimize_first.Sarsa_truck import SARSA
from flask import Flask, send_file,jsonify, send_from_directory,request
from read_data import result_q_truck,result_q_drone,result_sarsa_truck,result_sarsa_drone,emissions_q,emissions_sarsa
import subprocess
import os
import webbrowser
import threading
from chatbot import model

app = Flask(__name__,static_folder="static")

@app.route("/compare")
def compare_screen():
    return send_file("FE.html")

@app.route("/Homepage")
def home_page_screen():
    return send_file("homepage.html")

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

@app.route("/api/result_q", methods=['GET'])
def get_truck_route_q():
    result = result_q_truck()
    return jsonify({'result':result})

@app.route("/api/result_q_drone", methods=['GET'])
def get_drone_route_q():
    result = result_q_drone()
    return jsonify({'result':result})

@app.route("/api/emissions_q",methods=['GET'])
def get_emission_q():
    result = emissions_q()
    return jsonify({'result':result})

@app.route("/api/result_sarsa_drone", methods=['GET'])
def get_drone_route_sarsa():
    result = result_sarsa_drone()
    return jsonify({'result':result})

@app.route("/api/result_sarsa_truck", methods=['GET'])
def get_truck_route_sarsa():
    result = result_sarsa_truck()
    return jsonify({'result':result})

@app.route("/api/emissions_sarsa",methods=['GET'])
def get_emission_sarsa():
    result = emissions_sarsa()
    return jsonify({'result':result})

@app.route('/api/get_image/<filename>')
def get_image(filename):
    return send_from_directory('result/figure', filename)

python_file_path = "D:\\Tran Hoang Vu\\Lab\\VRDP\\Large Nearest Search (LNS)\\q_and_sarsa\\travelling-salesman-problem-tsp\\main.py"


@app.route("/api/run_program", methods=['POST'])
def restart_program():
    try:
        # Kiểm tra xem file Python có tồn tại không
        if not os.path.exists(python_file_path):
            return jsonify({'status': 'error', 'message': f'File không tồn tại: {python_file_path}'}), 400

        # Chạy lại file Python mà không mở terminal
        subprocess.Popen(
            ["python", python_file_path], 
            stdout=subprocess.DEVNULL,  # Không in output ra console
            stderr=subprocess.DEVNULL   # Không in lỗi ra console
        )

        return jsonify({'status': 'success', 'message': 'File Python đã được chạy lại!'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route("/api/chat_bot", methods=['POST'])
def get_chat_bot():
    try:
        data = request.get_json()  # Nhận dữ liệu từ yêu cầu POST
        user_text = data.get('user_text', '')
        model_id = model()
        response = model_id.generate_content(f'Give me the information of the content {user_text}')
        result = response.text
        return jsonify({'response': result})
    except Exception as e:
        return jsonify({'error': str(e)})
Q_Learning()
SARSA()

if __name__ == "__main__":
    # webbrowser.open('http://127.0.0.1:5000/compare',new=2, autoraise=False)
    app.run(debug=True)

    

    