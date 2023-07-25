from flask import Flask, jsonify, request
import psycopg2

app = Flask(__name__) # Use __name__ as the import_name argument

# Database connection details
db_host = '0.0.0.0'  # Replace with your PostgreSQL container's IP or hostname
db_port = 5432  # Replace with the exposed port of your PostgreSQL container
db_name = 'ze_db'
db_user = 'postgres'
db_password = 'senha'

def get_db_connection():
    return psycopg2.connect(
        host=db_host,
        port=db_port,
        database=db_name,
        user=db_user,
        password=db_password
    )

@app.route('/api/data', methods=['GET'])
def get_data():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = 'SELECT * FROM public."customers";'
        cursor.execute(query)
        customers = cursor.fetchall()

        if customers:
            result = []
            for customer in customers:
                # Convert the tuple to a list using list()
                customer_list = list(customer)

                # Access data from the list using index positions
                result.append({
                    "id": customer_list[0],         # Access the first column (id)
                    "first_name": customer_list[1], # Access the second column (first_name)
                    "last_name": customer_list[2],  # Access the third column (last_name)
                    "email": customer_list[3]       # Access the fourth column (email)
                })
            return jsonify(result)
        else:
            return jsonify({"error": f"Customers not found."}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/hello', methods=['GET'])
def hello():
	return "Hello, world!"

@app.route('/create', methods=['POST'])
def create():
    # Get the first_name, last_name and email from the request body
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')

    try:
        # Insert the data into the database
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO public.\"customers\" (first_name, last_name, email) VALUES (%s, %s, %s)", 
            (first_name, last_name, email)
        )
        connection.commit()

        # Close the cursor and connection
        cursor.close()
        connection.close()

        return {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "message": f"Customer {first_name} created."
        }, 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
        app.run(debug=True, port=8000)