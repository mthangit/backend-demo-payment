from flask import jsonify
import requests
from datetime import datetime, timedelta
import uuid
import os
import json
import urllib.parse
import hashlib
import hmac

MOMO_ACCESS_KEY = os.getenv("MOMO_ACCESS_KEY")
MOMO_SECRET_KEY = os.getenv("MOMO_SECRET_KEY")
MOMO_IPN_URL = os.getenv("MOMO_IPN_URL")
MOMO_PARTNER_CODE = os.getenv("MOMO_PARTNER_CODE")
MOMO_RETURN_URL = os.getenv("RETURN_URL")
MOMO_ENDPOINT = os.getenv("MOMO_ENDPOINT")


def create_momo_payment_url(amount: int, description: str):
    amount = str(amount)
    order_id = str(uuid.uuid4())
    orderInfo = description
    print(orderInfo)
    request_id = str(uuid.uuid4())
    requestType = "payWithMethod"
    storeId = "Test Store"
    orderGroupId = ""
    autoCapture = True
    lang = "vi"
    orderGroupId = ""
    extraData = ""  
    rawSignature = "accessKey=" + MOMO_ACCESS_KEY + "&amount=" + amount + "&extraData=" + extraData + "&ipnUrl=" + MOMO_IPN_URL + "&orderId=" + order_id \
               + "&orderInfo=" + orderInfo + "&partnerCode=" + MOMO_PARTNER_CODE + "&redirectUrl=" + MOMO_RETURN_URL\
               + "&requestId=" + request_id + "&requestType=" + requestType

    h = hmac.new(bytes(MOMO_SECRET_KEY, 'ascii'), bytes(rawSignature, 'ascii'), hashlib.sha256)
    signature = h.hexdigest()
    data = {
		'partnerCode': MOMO_PARTNER_CODE,
		'partnerName': "Test",
		'storeId': storeId,
		'requestId': request_id,
		'amount': amount,
		'orderId': order_id,
		'orderInfo': orderInfo,
		'redirectUrl': MOMO_RETURN_URL,
		'ipnUrl': MOMO_IPN_URL,
		'lang': lang,
		'extraData': extraData,
		'requestType': requestType,
		'signature': signature,
        'orderGroupId': orderGroupId,
        'autoCapture': autoCapture
        
	}
    print(data)
    data = json.dumps(data)
    clen = len(data)
    response = requests.post(MOMO_ENDPOINT, data=data, headers={'Content-Type': 'application/json', 'Content-Length': str(clen)})
    result = response.json()
    payURL = result.get('payUrl')
    print(result)
    return jsonify({
        'status': 'success',
        'url': payURL,
        'method': 'momo'
    })
