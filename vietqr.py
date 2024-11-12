from flask import jsonify
import requests
import os

client_id = os.getenv("VIETQR_CLIENT_ID")
client_api_key = os.getenv("VIETQR_API_KEY")
payment_url = os.getenv("VIETQR_PAYMENT_URL")

def get_viet_qr_api(amount: int, description: str):
	data = {
		"accountNo": 1028183606,
		"accountName": "HOANG MANH THANG",
		"acqId": 970436,
		"amount": amount,
		"addInfo": description,
		"format": "text",
		"template": "compact2"
	}

	headers = {
		"x-client-id":  client_id,
		"x-api-key": client_api_key,
		"Content-Type": "application/json"
	}

	response = requests.post(payment_url, json=data, headers=headers)

	if response.status_code == 200:
		return response.json()
	else:
		return None

def get_viet_qr(amount: int, description: str):
    response = get_viet_qr_api(amount, description)
    
    if not response:
        return jsonify({
            'status': 'error',
            'message': 'Không thể tạo mã QR',
            'method': 'qr_code'
        }), 500
    
    data = response.get('data')
    url = data.get('qrDataURL')
    return jsonify({
        'status': 'success',
        'url': url,
        'method': 'qr_code'
    })


