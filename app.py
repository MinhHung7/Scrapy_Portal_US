from flask import Flask, render_template, jsonify, request
from main_1 import login
from quickstart import main

app = Flask(__name__)
login_Obj = None

@app.route('/', methods=['GET', 'POST','PUT'])
def login_page():
    global login_Obj
    if request.method == 'POST' or request.method == 'PUT':
        if request.method == 'POST':
            data = request.get_json()
            event_list = []
            code = ''
            login_Obj = login(data['email'], data['password'], code, event_list)

            if(login_Obj.checkInfo() == False):
                return jsonify({'status': 'failLogin', 'message': 'failLogin'})

            login_Obj.postCode()
            return jsonify({'status': 'successSendCode', 'message': 'successSendCode'})

        if request.method == 'PUT':
            data = request.get_json()
            login_Obj.code = data['code']
            login_Obj.checkCode()
            login_Obj.accessPortal()
            print("YEAH")
            main(login_Obj.event_list, "Lịch thi")
            return jsonify({'status': 'OK', 'message': 'OK'})
    
    # Render the HTML template
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)