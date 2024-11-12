from flask import jsonify
import requests
from datetime import datetime, timedelta
import uuid
import os
import urllib.parse
import hashlib
import hmac

vnp_tmn_code = os.getenv("VNP_TMN_CODE")
vnp_return_url = os.getenv("RETURN_URL")
vnp_hash_secret = os.getenv("VNP_HASH_SECRET")
vnp_endpoint = os.getenv("VNP_ENDPOINT")

def hmacsha512(key, data):
    byteKey = key.encode('utf-8')
    byteData = data.encode('utf-8')
    return hmac.new(byteKey, byteData, hashlib.sha512).hexdigest()


def create_payment_vnpay(amount: int, client_ip: str, description: str):
    vnp_Amount = int(amount) * 100
    vnp_IpAddr = client_ip
    vnp_TxnRef = str(uuid.uuid4())
    vnp_CreateDate = datetime.now().strftime('%Y%m%d%H%M%S')
    vnp_ExpireDate = (datetime.now() + timedelta(minutes=10)).strftime('%Y%m%d%H%M%S')
    inputData = {
        'vnp_Version': '2.1.0',
        'vnp_Command': 'pay',
        'vnp_TmnCode': vnp_tmn_code,
        'vnp_Amount': vnp_Amount,
        'vnp_CurrCode': 'VND',
        'vnp_TxnRef': vnp_TxnRef,
        'vnp_OrderInfo': description,
        'vnp_OrderType': 'other',
        'vnp_Locale': 'vn',
        'vnp_ReturnUrl': vnp_return_url,
        'vnp_IpAddr': vnp_IpAddr,
        'vnp_CreateDate': vnp_CreateDate,
        'vnp_ExpireDate': vnp_ExpireDate
    }
    sortedData = sorted(inputData.items())
    
    # Build the query string
    queryString = '&'.join([f"{k}={urllib.parse.quote_plus(str(v))}" for k, v in sortedData])
    
    # Calculate the secure hash
    secureHash = hmacsha512(vnp_hash_secret, queryString)
    # Build the full URL
    vnp_PayUrl = f"{vnp_endpoint}?{queryString}&vnp_SecureHash={secureHash}"
    
    # Debug statements
    print("Input Data:", inputData)
    print("Query String:", queryString)
    print("Secure Hash:", secureHash)
    print("VNPAY URL:", vnp_PayUrl)
    
    return jsonify({
        'status': 'success',
        'url': vnp_PayUrl,
        'method': 'vnpay'
    })