import stripe
import os
from flask import jsonify

SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
RETURN_URL = os.getenv('RETURN_URL')
CANCEL_URL = os.getenv('CANCEL_URL')

stripe.api_key = SECRET_KEY

def create_checkout_session(product_id):
    try:
        session = stripe.checkout.Session.create(
            # payment_method_types=['card', 'wallets'],
            line_items=[{
                'price': product_id,  # Thay bằng Price ID của bạn
                'quantity': 1,
            }],
            mode='payment',
            success_url=RETURN_URL,
            cancel_url=CANCEL_URL,
        )
        # Trả về URL thanh toán thay vì Session ID
        return jsonify({
			'status': 'success',
			'url': session.url,
			'method': 'stripe',
			'session_id': session.id
            })
    except Exception as e:
        return jsonify(error=str(e)), 403
	
def retrieve_payment(session_id):
    data = stripe.checkout.Session.retrieve(session_id)
    # convert data to json
    data = data.to_dict()
    return jsonify({
		'status': data['payment_status'],
		'timestampt': data['created'],
		'payment_method_type': data['payment_method_types'][0] + ' - Stripe',
		'amount': data['amount_total'],
        'description': 'Thanh toan thanh cong',
        'method': 'stripe' 
	})
