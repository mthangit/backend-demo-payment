from flask import Flask, request, jsonify
from vietqr import get_viet_qr
from vnpay import create_payment_vnpay
from momo import create_momo_payment_url
from stripe_payment import create_checkout_session, retrieve_payment
from flask_cors import CORS
app = Flask(__name__)

CORS(app)

@app.route('/api/payment', methods=['POST'])
def payment():
    try:
        data = request.get_json()
        
        amount = data.get('amount')
        description = data.get("description")
        product_id = data.get("product_id")
        if description ==  "":
            description = "Thanh toan cho Hoang Manh Thang"
        print(description)
        payment_method = data.get('payment_method')
        client_ip = get_client_ip(request)

        print(payment_method)
        
        if not amount or not payment_method:
            return jsonify({'status': 'error', 'message': 'Thiếu thông tin'}), 400

        match payment_method:
            case "qr_code":
                return get_viet_qr(amount, description)
            case "vnpay":
                return create_payment_vnpay(amount, client_ip, description)
            case "momo":
                return create_momo_payment_url(amount, description)
            case "stripe":
                return create_checkout_session(product_id)
    
    except Exception as e:
        print(str(e))
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/payment-info', methods=['GET'])
def retrieve_payment_info():
    return retrieve_payment(request.args.get('session_id'))

def get_client_ip(request):
    x_forwarded_for = request.headers.get('X-Forwarded-For')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.remote_addr
    return ip


# API nhận yêu cầu GET (ví dụ, chỉ để kiểm tra server)
@app.route('/api/status', methods=['GET'])
def status():
    return jsonify({'status': 'server is running'})

@app.route('/api/confirm-payment', methods=['POST'])
def confirm_payment():
	data = request.get_json()
	print(data)
	return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
