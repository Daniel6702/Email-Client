import json
from cryptography.fernet import Fernet
from EmailService.models.user import User
from dataclasses import asdict
import keyring
from PyQt5.QtWidgets import QApplication, QMessageBox
import sys
import os

KEY_NAME = 'email_client_encryption_key'

'''Functions:
    - add_user
    - update_user
    - delete_user
    - get_users
'''
def restart_program():
    try:
        script = os.path.abspath(sys.argv[0])
        os.chdir(os.path.dirname(script))
        os.execl(sys.executable, sys.executable, '"' + script + '"', *sys.argv[1:])
    except Exception as e:
        print(f"Error during restart: {e}")

class UserDataManager:
    def __init__(self, file_path = 'Certificates\\users.bin'):
        self.file_path = file_path
        self.cipher_suite = Fernet(self.load_key())

    @staticmethod
    def generate_key():
        return Fernet.generate_key()

    @staticmethod
    def store_key(key):
        keyring.set_password('system', KEY_NAME, key.decode('utf-8'))

    @staticmethod
    def load_key():
        key = keyring.get_password('system', KEY_NAME)
        if key is None:
            key = UserDataManager.generate_key()
            UserDataManager.store_key(key)
            return key
        else:
            return key

    def encrypt_data(self, data):
        return self.cipher_suite.encrypt(data.encode('utf-8'))

    def decrypt_data(self, data):
        return self.cipher_suite.decrypt(data).decode('utf-8')

    def add_user(self, user: User):
        users = self.get_users()
        users.append(user)
        encrypted_users = self.encrypt_data(json.dumps([asdict(u) for u in users]))
        
        with open(self.file_path, 'wb') as file:
            file.write(encrypted_users)

    def update_user(self, user: User):
        users = self.get_users()
        for i, u in enumerate(users):
            if u.email == user.email:
                users[i] = user
                break
        encrypted_users = self.encrypt_data(json.dumps([asdict(u) for u in users]))
        
        with open(self.file_path, 'wb') as file:
            file.write(encrypted_users)

    def delete_user(self, user: User):
        users = self.get_users()
        users = [user for user in users if user.email != user.email]
        
        encrypted_users = self.encrypt_data(json.dumps([asdict(u) for u in users]))
        
        with open(self.file_path, 'wb') as file:
            file.write(encrypted_users)
        print(f"User {user.email} has been deleted.")

    def get_users(self) -> list[User]:
        try:
            with open(self.file_path, 'rb') as file:
                encrypted_data = file.read()
            decrypted_data = self.decrypt_data(encrypted_data)
            data = json.loads(decrypted_data)
            
            return [User(**user_data) for user_data in data]
        except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
            print(f"An error occurred: {str(e)}")
            return []
        
    def get_users(self) -> list[User]:
        try:
            with open(self.file_path, 'rb') as file:
                encrypted_data = file.read()

            if not encrypted_data:
                return []

            decrypted_data = self.cipher_suite.decrypt(encrypted_data).decode('utf-8')

            if not decrypted_data:
                return []

            data = json.loads(decrypted_data)

            users = []
            for user_data in data:
                if isinstance(user_data.get('credentials', {}), str):
                    credentials_str = user_data['credentials'].strip('"')
                    try:
                        user_data['credentials'] = json.loads(credentials_str)
                    except json.JSONDecodeError as e:
                        print(f"Error decoding credentials for user {user_data.get('email')}: {e}")
                        user_data['credentials'] = {}

                users.append(User(**user_data))

            return users

        except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
            print(f"An error occurred while loading users: {str(e)}")
            return []
        except Exception as e: 
            app = QApplication(sys.argv)
            response = QMessageBox.question(None, "Decryption Error", 
                                            "Unable to decrypt the file on this computer. Would you like to delete the user file and restart?",
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if response == QMessageBox.Yes:
                with open(self.file_path, 'w') as file:
                    file.write('')
                restart_program()
            else:
                sys.exit(0) 

        return []