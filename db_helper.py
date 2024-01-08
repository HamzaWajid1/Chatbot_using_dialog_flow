import mysql.connector

global connection
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Hamza.paracha1",
    database="pandeyji_eatery"
)


# Function to insert a record into the order_tracking table
def insert_order_tracking(order_id, status):
    cursor = connection.cursor()

    # Inserting the record into the order_tracking table
    insert_query = "INSERT INTO order_tracking (order_id, status) VALUES (%s, %s)"
    cursor.execute(insert_query, (order_id, status))

    # Committing the changes
    connection.commit()

    # Closing the cursor
    cursor.close()


def insert_order_item(food_item, quantity, order_id):
    try:
        cursor = connection.cursor()

        # Calling the stored procedure
        cursor.callproc('insert_order_item', (food_item, quantity, order_id))

        # Committing the changes
        connection.commit()

        # Closing the cursor
        cursor.close()

        print("Order item inserted successfully!")

        return 1

    except mysql.connector.Error as err:
        print(f"Error inserting order item: {err}")

        # Rollback changes if necessary
        connection.rollback()

        return -1

    except Exception as e:
        print(f"An error occurred: {e}")
        # Rollback changes if necessary
        connection.rollback()

        return -1


def get_total_order_price(order_id):
    cursor = connection.cursor()

    # Executing the SQL query to get the total order price
    query = f"SELECT get_total_order_price({order_id})"
    cursor.execute(query)

    # Fetching the result
    result = cursor.fetchone()[0]

    # Closing the cursor
    cursor.close()

    return result


# Function to get the next available order_id
def get_next_order_id():
    cursor = connection.cursor()

    # Executing the SQL query to get the next available order_id
    query = "SELECT MAX(order_id) FROM orders"
    cursor.execute(query)

    # Fetching the result
    result = cursor.fetchone()[0]
    print(result)
    # Closing the cursor
    cursor.close()

    # Returning the next available order_id
    if result is None:
        return 1
    else:
        return result + 1


def get_order_status(order_id):
    # Replace these values with your MySQL database credentials

    try:
        # Create a cursor
        cursor = connection.cursor()

        # Query to retrieve the status for a given order_id
        query = f"SELECT status FROM order_tracking WHERE order_id = {order_id}"
        print(order_id)

        # Execute the query with the provided order_id
        cursor.execute(query)

        # Fetch the result
        result = cursor.fetchone()
        cursor.close()
        if result:
            # If the result is not None, print the status
            print(f"Status for Order ID {order_id}: {result[0]}")
            return result[0]
        else:
            print(f"No record found for Order ID {order_id}")
            return None

    except mysql.connector.Error as err:
        print(f"Error: {err}")


if __name__ == "__main__":
    # Take order_id as input
    order_id_input = input("Enter Order ID: ")

    # Call the function to get the order status
    get_order_status(order_id_input)
