from flask import Flask, jsonify
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
                result.append({"id": customer.id[0], "first_name": customer.first_name[1], "last_name": customer.last_name[2], "email": customer.email[3]})
            return jsonify(result)
        else:
            return jsonify({"error": f"Customers not found."}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/hello', methods=['GET'])
def hello():
	return "Hello, world!"

if __name__ == '__main__':
        app.run(debug=True, port=8000)

