# Stripe E-Commerce Payment Integration (SA Take-Home Project)

## Project Overview

This project is a take-home assignment demonstrating a simple e-commerce checkout system integrated with **Stripe Payment Element** for secure transactions. It enables users to select a book, proceed to checkout, and complete a payment seamlessly using Stripe’s API. The application is built with **Flask** (Python) and demonstrates how to securely process payments using Stripe's **Payment Intents API**.

## Key Features

- Secure payment processing using **Stripe Payment Intents API**
- Checkout and pay for one item via the **Stripe Payment Element** form
- Display **Payment Intent ID** & **Total Charged Amount** upon successful payment



## Table of Contents

- [Installation & Setup](#installation--setup)  
- [How It Works](#how-it-works)  
- [Project Structure](#project-structure)  
- [Technical Implementation](#technical-implementation)  
- [Approach and Challenges](#approach-and-challenges) 
- [Future Enhancements](#future-enhancements)  



## Installation & Setup

### Prerequisites

- **Python 3.11**: Strongly recommended (Python 3.13 has compatibility issues with some dependencies, including older Stripe versions).
- **Flask**: Lightweight web framework used for rapid prototyping.
- **Stripe API Keys** (Create an account at [Stripe](https://dashboard.stripe.com/register))

### Setup Instructions


1. Clone the repository
```sh
git clone https://github.com/pengbin-zou/pengbin-sa-takehome-project-python.git
cd pengbin-sa-takehome-project-python
```

2. Create and activate a virtual environment using **Python 3.11**:
```sh
python3.11 -m venv newvenv
source newvenv/bin/activate  # Windows: newvenv\Scripts\activate
```

3. Install dependencies
```sh
pip install -r requirements.txt
```

4. Configure environment variables:

- Rename** `sample.env` to `.env` in the project root.  
- Populate the file with your Stripe test API keys, for example:

```env
STRIPE_SECRET_KEY=sk_test_xxxxxxxxxxxxxxxxx
STRIPE_PUBLISHABLE_KEY=pk_test_xxxxxxxxxxxxxxxxx

```

### Running the Application

1. Start the Flask server:
```sh
flask run
```
**Note:** If `flask run` uses Python 3.13 instead of 3.11, force the virtual environment:
```sh
python -m flask run
```
This ensures you’re using **Python 3.11** from your virtual environment.

2. Open [http://127.0.0.1:5000/](http://127.0.0.1:5000/) in your browser to access the application.

### Troubleshooting
- If the server doesn’t start, ensure the `.env` file is correctly configured and the virtual environment is activated.


## How It Works
### Payment Flow

1. User selects a book, enters your email address and clicks **"Pay"**.
2. Backend creates a Stripe Payment Intent via `/create-payment-intent`.
3. Stripe renders a secure payment form using **Payment Element**.
4. User enters dummy payment info (e.g., test card `4242 4242 4242 4242`, future expiration like `11/30`, and any 3-digit CVC like `192`).
5. Payment is processed; upon success, the user is redirected to `/success`, showing:
   - Payment Intent ID
   - Total Charged Amount
6. Verify the payment in [Stripe Dashboard](https://dashboard.stripe.com/).

### Architecture
This is a Flask-based server-side rendered application with client-side Stripe integration. The frontend sends POST requests to the backend (`app.py`), which interacts with Stripe APIs and returns a `clientSecret` to initialize the Payment Element.


## Project Structure

```
SA Take-Home Project/
├── app.py            # Main Flask application
├── views             # HTML templates
│   ├── index.html    # Home page
│   ├── checkout.html # Payment form
│   ├── success.html  # Payment confirmation
│   └── layouts/      # Layout templates
│       └── main.html # Base layout
├── public            # Static assets (e.g., CSS, JS)
├── sample.env        # Sample API keys
├── requirements.txt  # Python dependencies
├── README.md         # This documentation
```

## Technical Implementation

### Stripe Tools Used

- **[Payment Intents API](https://stripe.com/docs/payments/payment-intents)**: Create a payment intent with the amount and currency on the server side (`stripe.PaymentIntent.create`).
- **[Payment Element](https://docs.stripe.com/js/elements_object/create)**: Render a secure, customizable payment form on the client side (`elements.create("payment")`).

### Key Backend Code (`app.py`)

```python
@app.route('/create-payment-intent', methods=['POST'])
def create_payment_intent():
    data = request.json
    amount = data.get("amount")
    try:
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency='usd'
        )
        return jsonify({'clientSecret': intent.client_secret})
    except stripe.error.StripeError as e:
        return jsonify({'error': str(e)}), 500
```

## Approach and Challenges

### Approach
Aim to build a minimal e-commerce checkout system focusing on Stripe integration. Use Flask for its simplicity and paired it with Stripe’s Payment Intents and Payment Element for a secure, user-friendly payment experience.

### Challenges Faced

1. **Payment Intent Not Initializing**: The `clientSecret` wasn’t reaching the frontend. Fixed by ensuring the backend returned it correctly in the JSON response.
2. **Amount Display Issue**: Total showed as `25.00` instead of `25`. Resolved by dividing `amount` by 100 using `parseInt(amount) / 100`.
3. **Stripe Elements Not Mounting**: The Payment Element failed to render due to a timing issue. Fixed by ensuring `clientSecret` was available before calling `elements.create()`.


## Future Enhancements

- **Webhooks**: Add real-time payment status updates for improved reliability and user feedback.
- **Refund Functionality**: Integrate the Refund API to allow transaction reversals.
- **Database Integration**: Store transactions for order tracking and receipt generation.
- **Multiple Payment Methods**: Support Apple Pay, Google Pay, etc., for broader accessibility.

---

Thank you for reviewing my submission! I’ve aimed to create a clear, functional, and extensible solution that showcases Stripe’s payment capabilities.
