import os
import stripe

from dotenv import load_dotenv
from flask import Flask, request, render_template, jsonify

load_dotenv()

app = Flask(__name__,
  static_url_path='',
  template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), "views"),
  static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), "public"))

# Configure Stripe API
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

# Home route
@app.route('/', methods=['GET'])
def index():
  return render_template('index.html')

# Checkout route
@app.route('/checkout', methods=['GET'])
def checkout():
  # Just hardcoding amounts here to avoid using a database
  item = request.args.get("item", default=None)
  amount = request.args.get("amount", default=0, type=int)
  
  title = None
  error = None

  if item == '1':
    title = 'The Art of Doing Science and Engineering'
    
  elif item == '2':
    title = 'The Making of Prince of Persia: Journals 1985-1993'
   
  elif item == '3':
    title = 'Working in Public: The Making and Maintenance of Open Source'

  else:
    error = 'No item selected'

  if not amount or amount <= 0:
    error = 'Invalid amount'

# ✅ Debug log
  print(f"📝 DEBUG: Sending item: {item}, amount: {amount}")

  return render_template('checkout.html', title=title, amount=amount, error=error)

# Success route
@app.route('/success', methods=['GET'])
def success():
  return render_template('success.html')

# Create Payment Intent Route
@app.route('/create-payment-intent', methods=['POST'])
def create_payment():
    """Create a Stripe Payment Intent"""
    try:
        data = request.json
        amount = int(data.get("amount", 0))  # Ensure amount is received

        if amount <= 0:
            return jsonify({"error": "Invalid amount"}), 400  # Prevent invalid payments

        payment_intent = stripe.PaymentIntent.create(
            amount=amount,
            currency="usd",
            automatic_payment_methods={"enabled": True}
        )

        print(f"Payment Intent Created: {payment_intent.id}, Client Secret: {payment_intent.client_secret}")

        return jsonify({
            "clientSecret": payment_intent.client_secret
        })
    except Exception as e:
        return jsonify(error=str(e)), 400

# Get Stripe Publishable Key Route
@app.route('/config', methods=['GET'])
def get_config():
    """Send the Stripe Publishable Key to the frontend"""
    return jsonify({"publishableKey": os.getenv("STRIPE_PUBLISHABLE_KEY")})

if __name__ == '__main__':
  app.run(port=5000, host='0.0.0.0', debug=True)