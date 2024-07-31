from cryptography.fernet import Fernet

# key = Fernet.generate_key()
# with open("secret.key", "wb") as key_file:
#     key_file.write(key)
    
def load_key():
    return open("secret.key", "rb").read()
key=load_key()

def encrypt_message(message,key):

    f = Fernet(key)
    encrypted_message = f.encrypt(message.encode())
    return encrypted_message

def decrypt_message(encrypted_message,key):
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message).decode()
    return decrypted_message


# import mysql.connector
# from cryptography.fernet import Fernet

# config = {
#     'user': 'root',
#     'password': 'root',
#     'host': 'localhost',
#     'port': 3308,
#     'raise_on_warnings': True,
#     'database': 'agriguard'
# }

# cnx = mysql.connector.connect(**config)
# cursor = cnx.cursor()

# # Example user data
# username = "admin"
# email = "admin@example.com"
# password = "admin"

# encrypted_password = encrypt_message(password,key)

# cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, encrypted_password))
# cnx.commit()

# # Verifying user data
# cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
# stored_password = cursor.fetchone()[0]

# decrypted_password = decrypt_message(stored_password.encode(),key)
# print("Decrypted Password:", decrypted_password)

# cursor.close()
# cnx.close()
