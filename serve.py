from flask import Flask, request
import pandas as pd #Thao tác tạo file csv theo cấu trúc
import utils
import json
import re
import base64

global model
model = None
app = Flask(__name__)

@app.route("/", methods=["GET"])
def hello():
    return 'GET active'

@app.route("/predict", methods=["POST"])
def _predict():
    F1 = []
    F2 = []
    F3 = []
    F4 = []
    F5 = []
    F6 = []
    F7 = []
    F8 = []
    F9 = []
    F10 = []
    F11 = []
    F12 = []
    F13 = []
    F14 = []
    F15 = []
    F16 = []
    
    def_arr = ['eval']
    faf_arr = ['wget', 'curl', 'lynx', 'get', 'fetch']
    rcf_arr = ['perl', 'python', 'gcc', 'chmod', 'nohup', 'nc ']
    icf_arr = ['uname', 'id', 'ver', 'sysctl', 'whoami', '$OSTYPE', 'pwd']
    word = ['$_GET', '$_POST', '$_COOKIE', '$_REQUEST', '$_FILES', '$_SESSION']

    temp = list()
    temp2 = list()
    file_content =  request.files["file"].read().decode('latin-1')
    
    if not file_content.strip():  # Loại bỏ khoảng trắng để kiểm tra chuỗi rỗng
        result = {
            "result": 0, 
        }
    else:
        sample = utils.process(file_content)
        temp = utils.count_word(sample, word)
        temp2 = utils.cal_loop_ratio(sample)

        # Gộp mảng lại
        F1.append(temp[0])
        F2.append(temp[1])
        F3.append(temp[2])
        F4.append(temp[3])
        F5.append(temp[4])
        F6.append(temp[5])
        F7.append(temp2[0])
        F8.append(temp2[1])
        F9.append(temp2[2])
        F10.append(utils.cal_mal_func(sample, def_arr))
        F11.append(utils.cal_mal_func(sample, faf_arr))
        F12.append(utils.cal_mal_func(sample, rcf_arr))
        F13.append(utils.cal_mal_func(sample, icf_arr))
        F14.append(utils.count_max_len_word(sample))
        F15.append(utils.count_max_len_line(sample))
        F16.append(utils.calculate_entropy(sample))

        data = {
            'GET': F1,
            'POST': F2,
            'COOKIE': F3,
            'REQUEST': F4,
            'FILES': F5,
            'SESSION': F6,
            'elseif': F7,
            'for': F8,
            'foreach': F9,
            'DEF': F10,
            'FAF': F11,
            'RCF': F12,
            'ICF': F13,
            'maxWordLen': F14,
            'maxLineLen': F15,
            'entropy': F16,
        }

        target = pd.DataFrame(data)
        temp = model.predict(target)
    

        result = {
            "result": int(temp[0]), 
        }
    
    return json.dumps(result)

@app.route("/sync", methods=["GET"])
def parse_signature_file_safe():
    file_path = 'sign.txt'
    signature_data = {"signature": []}

    with open(file_path, 'r', encoding="utf-8") as file:
        for line in file:
            if not line.strip():
                continue
            
            if line.startswith("#"):
                # Tách dữ liệu bằng '#|||#'
                parts = line.strip().split("#|||#")
                if len(parts) != 2:
                    continue  # Bỏ qua dòng không đúng định dạng
                
                # Lấy mẫu regex và số thứ tự
                regex_pattern = parts[0].strip()
                try:
                    number = int(parts[1].strip())  # Mẫu webshell sau '#|||#'
                except ValueError:
                    number = None  # Nếu có lỗi, gán giá trị là None

                # Encode thành base64 để gửi dữ liệu
                escaped_pattern = base64.b64encode(regex_pattern.encode('utf-8')).decode('utf-8')

                # Thêm vào dữ liệu signature
                signature_data["signature"].append({
                    str(number): escaped_pattern
                })

    # Chuyển đổi thành JSON
    return json.dumps(signature_data)

if __name__ == '__main__':
    print("App run!")
    # Load model
    model = utils._load_model()
    app.run(host='0.0.0.0', port=8080)