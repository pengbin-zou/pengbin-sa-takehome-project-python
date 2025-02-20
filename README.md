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
- [Challenges Faced & How They Were Solved](#challenges-faced--how-they-were-solved) 
- [Future Enhancements](#future-enhancements)  



## Installation & Setup

### Prerequisites

- **Python 3.11**: Strongly recommended (Python 3.13 has compatibility issues with some dependencies, including older Stripe versions).
- **Flask**: Lightweight web framework used for rapid prototyping.
- **Stripe API Keys** (Create an account at [Stripe](https://dashboard.stripe.com/register)). Once registered, follow this [guide](https://docs.stripe.com/keys) to generate your **Secret** and **Publishable Keys**.

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
```
+---------------------+
|     Client (Browser)    |
|     (HTML + JS)       |
|                       |
|  1. POST /create-payment-intent  |
|     (checkout.html)    |
+---------------------+
          |
          | HTTP Request
          v
+---------------------+
|     Flask Backend   |
|     (app.py)        |
|                       |
|  2. Interact with    |
|     Stripe Payment Intents API   |
|     (app.py) |
|  3. Return clientSecret |
+---------------------+
          |
          | HTTP Response
          v
+---------------------+
|     Client (Browser)    |
|     (Payment Element)   |
|  4. Initialize Payment  |
|     Element with        |
|     clientSecret
|   (checkout.html)       |
+---------------------+
```
## Project Structure

```
PengBin SA Take-Home Project/
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

## Challenges Faced & How They Were Solved

### 1. **Amount Display Issue**  
**Happened at Step**: Displaying Total Amount in Checkout Page (`checkout.html`)  

**Issue**:  
- The total amount was displayed as $25.00 instead of $25 in the checkout page, which could confuse users during payment.  
- This occurred because Stripe returns the amount in cents (e.g., 2500 for $25), but the JavaScript initially formatted it as a floating-point value instead of an integer.  

**Cause**:  
- The frontend and backend both needed to convert the amount from cents to dollars by dividing by 100, but the initial implementation lacked consistent formatting.

**Solution**:  
- Applied `parseInt(amount) / 100` in the frontend JavaScript and Flask backend to ensure consistent conversion from cents to dollars.  
- Added validation in both layers to prevent incorrect formatting, improving reliability and user clarity during checkout.

```javascript
// Correcting amount formatting in checkout.html
document.getElementById("pay-button-amount").innerText = parseInt(amount) / 100;
```
### 2. **Stripe Elements Not Mounting**  
**Happened at Step**: Rendering Payment Element in Checkout (`checkout.html`)  

**Issue**:  
- The Payment Element failed to render, leaving users unable to enter payment details and complete purchases.  

**Cause**:  
- The `clientSecret` was undefined during mounting because the fetch request to `/create-payment-intent` completed asynchronously after the `elements.create("payment")` call.  

**Solution**:  
- Used `async/await` to ensure the `clientSecret` was fetched before calling `elements.create("payment")`.  
- Thoroughly tested the payment flow to confirm the Payment Element rendered reliably, improving the checkout experience.

```javascript
// Ensure clientSecret is received before initializing Stripe Elements
const paymentIntentResponse = await fetch("/create-payment-intent", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ amount: amount })
});
const paymentIntentData = await paymentIntentResponse.json();

if (!paymentIntentData.clientSecret) {
    document.getElementById("payment-message").innerText = "Error: Client Secret not received!";
    return;
}

const clientSecret = paymentIntentData.clientSecret;

// Initialize Stripe Elements after receiving clientSecret
const stripe = Stripe("your-publishable-key");
const elements = stripe.elements({ clientSecret });
const paymentElement = elements.create("payment");
paymentElement.mount("#payment-element");
```
**Verification**:  
- Added a debugging log to check if clientSecret was received before initializing Stripe Elements:

```javascript
console.log("Received clientSecret:", clientSecret);
```
### 3. **Payment Intent Not Initializing**  
**Happened at Step**: Fetching `clientSecret` from Backend (`/create-payment-intent in app.py`) 

**Issue**:  
- The `clientSecret` wasn’t reaching the frontend, causing payment confirmation to fail and preventing customers from completing transactions.  

**Cause**:  
- The JSON response from `/create-payment-intent` was missing the `clientSecret` due to an error in the Flask route, likely from improper error handling or response formatting.

**Solution**:
- Ensured `clientSecret` was explicitly included in the JSON response from Flask.
```python
# Corrected Flask route to return clientSecret
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
**Verification**:  
- Used Stripe’s test card (`4242 4242 4242 4242`) to confirm payment worked.
- Opened developer tools (Network tab) to inspect API responses and confirm clientSecret was received.

## Future Enhancements

- **Webhooks**: Add real-time payment status updates for improved reliability and user feedback.
- **Refund Functionality**: Integrate the Refund API to allow transaction reversals.
- **Database Integration**: Store transactions for order tracking and receipt generation.
- **Multiple Payment Methods**: Support Apple Pay, Google Pay, etc., for broader accessibility.

---

Thank you for reviewing my submission! I’ve aimed to create a clear, functional, and extensible solution that showcases Stripe’s payment capabilities.
