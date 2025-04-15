import psycopg2
from dotenv import load_dotenv
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import datetime

# load env
load_dotenv()

gemini_key = os.getenv("gemini_key")
today = datetime.date.today()

# configure api key
os.environ["GOOGLE_API_KEY"] = gemini_key
# database connection
conn = psycopg2.connect(
    dbname = os.getenv("DB__NAME"),
    user = os.getenv("DB_USER"),
    password = os.getenv("DB_PASSWORD"),
    host = os.getenv("DB_HOST"),
    port = os.getenv("DB_PORT"),
)


# use gemini for prompting
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

gemini = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

# create app instance

app = Flask(__name__)
CORS(app)

# app route
@app.route("/api/home", methods=['GET'])
def return_home():
    # welcome message
    prompt = "Please write one line welcome spaza owners to our spaza shop called 4IR"

    # create a cursor
    cur = conn.cursor()

    # Execute a simple query
    cur.execute("SELECT * FROM products")
    
    # fetch and print results
    data = cur.fetchall()

    # prompts
    quantities = "We have a stock threshold of 30, which products should we stock" + str(data)
    expiring_products = "From the following data, which products are expiring soon" + str(data) + "and today is " + str(today)

    # call llm
    get_quantities = gemini.invoke(quantities)
    get_expiring_products = gemini.invoke(expiring_products)
    response = gemini.invoke(prompt)

    return jsonify({
        "message": response.content,
        "expiring_products": get_expiring_products.content,
        "quantities": get_quantities.content
    })


@app.route("/api/products", methods=['GET'])
def return_products():
    # create a cursor
    cur = conn.cursor()
    insert = conn.cursor()
    delete = conn.cursor()

    # move expired products to expired table
    insert.execute("INSERT INTO expired_products (product_id, name, quantity, expiring_date) SELECT id, name, quantity, expiring_date FROM products WHERE expiring_date IS NOT NULL AND expiring_date < %s", (today,))
    # delete expired products from products table
    delete.execute("DELETE FROM products WHERE expiring_date < %s", (today,))

    # commit changes
    conn.commit() 

    # execute a simple query
    cur.execute("SELECT name, brand, price, quantity, expiring_date FROM products")

    # fetch reulusts
    data = cur.fetchall()


    # return data
    products = []
    for row in data:
        products.append({
            "name": row[0],
            "brand": row[1],
            "price": row[2],
            "quantity": row[3],
            "expiring_date": row[4]
        })

    return jsonify({
        "products": products
    })

# expiring products
@app.route("/api/expiring-products", methods=['GET'])
def return_expiring_products():
    # create a cursor
    cur = conn.cursor()
    expired = conn.cursor()
    expiring = conn.cursor()

    # execute a simple query
    cur.execute("SELECT name, brand, price, quantity, expiring_date FROM products")
    # Query to get products that have already expired
    expired.execute("SELECT name, brand, price, quantity, expiring_date FROM products WHERE expiring_date < %s", (today,))
    # Query to get products that are expiring soon (within the next 7 days)
    expiring.execute("SELECT name, brand, price, quantity, expiring_date FROM products WHERE expiring_date BETWEEN %s AND %s", (today, today + datetime.timedelta(days=7)))
    

    # fetch results
    expiring_data = expiring.fetchall()
    expired_data = expired.fetchall()
    

    # prepare prompt
    expiring_products_prompt = "Please make a list of the following products: " + str(expiring_data)
    expired_products_prompt = "Please make a list of the following products: " + str(expired_data)

    # call llm
    get_expiring_products = gemini.invoke(expiring_products_prompt)
    get_expired_products = gemini.invoke(expired_products_prompt)

    # close cursor
    #cur.close()
    expired.close()
    expiring.close()

    # return data
    return jsonify({
        "expiring_products": get_expiring_products.content,
        "expired_products": get_expired_products.content
    })

# products to stock
@app.route("/api/stock-products", methods=['GET'])
def return_stock_products():
    # create a cursor
    cur = conn.cursor()

    # execute a simple query
    cur.execute("SELECT * FROM products")

    # fetch results
    data = cur.fetchall()

    # prepare prompt
    stock_products_prompt = "We have a stock threshold of 30, which products should we stock: " + str(data)

    # call llm
    get_stock_products = gemini.invoke(stock_products_prompt)

    # close cursor
    cur.close()

    # return data
    return jsonify({
        "stock_products": get_stock_products.content
    })

# add product
@app.route("/api/add-product", methods=['POST'])
def add_product():
    # create a cursor
    cur = conn.cursor()

    # get product details from request
    product_details = request.get_json()

    # extract details
    product_name = product_details.get("name")
    product_price = product_details.get("price")
    product_quantity = product_details.get("quantity")
    product_expiry = product_details.get("expiry_date")

    # validate input
    if not all([product_name, product_price, product_quantity, product_expiry]):
        return jsonify({"error": "All product fields are required"}), 400

    try:
        # insert product into database
        cur.execute(
            "INSERT INTO products (name, price, quantity, expiry_date) VALUES (%s, %s, %s, %s)",
            (product_name, product_price, product_quantity, product_expiry)
        )
        conn.commit()

        # return success response
        return jsonify({"message": "Product added successfully"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        # close cursor
        cur.close()

# sell products
@app.route("/api/sell-product", methods=['POST'])
def sell_products():
    # create a cursor
    cur = conn.cursor()

    # get product details from request
    product_details = request.get_json()

    # extract details
    product_name = product_details.get("name")
    product_quantity = product_details.get("quantity")

    # validate input
    if not all([product_name, product_quantity]):
        return jsonify({"error": "Product name and quantity are required"}), 400

    try:
        # update product quantity in database
        cur.execute(
            "UPDATE products SET quantity = quantity - %s WHERE name = %s",
            (product_quantity, product_name)
        )
        conn.commit()

        # return success response
        return jsonify({"message": "Product sold successfully"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        # close cursor
        cur.close()



# run app
if __name__ == "__main__":
    app.run(debug=True, port=5000)