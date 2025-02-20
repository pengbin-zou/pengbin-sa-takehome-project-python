# Stripe E-Commerce Payment Integration (SA Take-Home Project)

## 🏆 Project Overview

This project is a **simple e-commerce checkout system** that integrates **Stripe Payment Elements** for secure transactions. It enables users to select a book, proceed to checkout, and complete a payment seamlessly using Stripe’s API.

## ✨ Features

- ✅ Secure payment processing using **Stripe Payment Intents API**
- ✅ Dynamic total amount calculation & error handling
- ✅ Displays **Payment Intent ID** & **Total Charged Amount**
- ✅ Structured to **easily extend with additional features**



## 📌 Table of Contents

- [🔧 Installation & Setup](#-installation--setup)  
- [⚙️ How It Works](#%EF%B8%8F-how-it-works)  
- [🏗️ Project Structure](#%EF%B8%8F-project-structure)  
- [🔬 Technical Implementation](#-technical-implementation)  
- [🚧 Challenges & Learnings](#-challenges--learnings)  
- [🔮 Future Enhancements](#-future-enhancements)  



## 🔧 Installation & Setup

### **1️⃣ Prerequisites**

Ensure you have the following installed:

- **Python 3.x**
- **Flask**
- **Stripe API Keys** (Create an account at [Stripe](https://dashboard.stripe.com/register))

### **2️⃣ Setup Instructions**


Clone the repository
```sh
git clone https://github.com/your-github-username/pengbin-sa-takehome-project.git
cd pengbin-sa-takehome-project
```

Create a virtual environment
```sh
python -m venv venv
source venv/bin/activate  # On Windows use venv\Scripts\activate
```

Install dependencies
```sh
pip install -r requirements.txt
```

### **3️⃣ Configure Environment Variables**

1. **Rename** `sample.env` **to** `.env` in the project root.  
2. **Populate** the file with your Stripe test API keys, for example:

```env
STRIPE_SECRET_KEY=sk_test_xxxxxxxxxxxxxxxxx
STRIPE_PUBLISHABLE_KEY=pk_test_xxxxxxxxxxxxxxxxx

```

### **4️⃣ Running the Application**

```sh
flask run
```

Then, open [http://127.0.0.1:5000/](http://127.0.0.1:5000/) in your browser to access the application.


## ⚙️ How It Works

### 📌 Payment Flow

1. **User selects a book** → enter your email address and click **"Pay"**.
2. **Backend creates a Stripe Payment Intent** → `/create-payment-intent`.
3. **Stripe renders a secure payment form** via **Elements API**.

4. **Enter Dummy Payment Info for Testing**  
   For example, use Stripe’s test card:
   ```
   4242 4242 4242 4242
   ```
   with any future date for expiry and any 3-digit CVC.
5. **User submits payment** → Payment is processed & confirmed.
6. **Upon success**, user is redirected to `/success`, displaying:
   - ✅ **Payment Intent ID**
   - ✅ **Total Charged Amount**
7. **Verify the payment in Stripe Dashboard** → Check the transaction to ensure it was processed successfully.


## 🏗️ Project Structure

```
stripe-payment-integration/
│── app.py  # Main Flask application
│── templates/
│   ├── index.html  # Home page
│   ├── checkout.html  # Payment form
│   ├── success.html  # Payment confirmation
│── static/
│── .env.example  # Environment variables
│── requirements.txt  # Dependencies
│── README.md  # Documentation
```
---
### 🔬 Technical Implementation

#### **APIs Used**

- **[Payment Intents API](https://stripe.com/docs/payments/payment-intents)**: Creates a payment intent before checkout.
- **[Payment Element](https://docs.stripe.com/payments/payment-element)**: Renders a secure payment form.

#### **Key Backend Code (`app.py`)**

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

### 🚧 Challenges & Learnings

#### ✅ Challenges Faced & How They Were Solved

- **Issue**: Payment Intent not initializing → **Solution**: Ensured `clientSecret` was properly returned from the backend.
- **Issue**: Amount displayed as `25.00` instead of `25` → **Solution**: Used `parseInt(amount) / 100`.
- **Issue**: Stripe Elements not mounting → **Solution**: Ensured `clientSecret` was passed before calling `elements.create()`.


### 🔮 Future Enhancements

- ✅ **Enable Webhooks** → Handle real-time payment updates.
- ✅ **Implement Refund Functionality** → Use `Refund API`.
- ✅ **Store Transactions in a Database** → Track orders and receipts.
- ✅ **Support Multiple Payment Methods** → Add Apple Pay, Google Pay, Grab Pay, etc.
