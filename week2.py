import tkinter as tk
from tkinter import simpledialog,filedialog, messagebox
import paramiko
from cryptography.fernet import Fernet
import os

# Constants for SFTP server connection
HOST = 'your-sftp-host'  # Change this to your SFTP server address
PORT = 22
USERNAME = 'uday'  # Change this to your SFTP username
PASSWORD = '1234'  # Change this to your SFTP password

# File paths for key and directory (change these as needed)
KEY_FILE_PATH = 'encryption_key.txt'
REMOTE_DIRECTORY = '/remote/dir/'  # Remote directory path
def prompt_sftp_details():
    global HOST
    HOST = simpledialog.askstring('SFTP Server', 'Enter SFTP server address:')
# Function to generate a new encryption key if it doesn't exist
def generate_key():
    if not os.path.exists(KEY_FILE_PATH):
        key = Fernet.generate_key()
        with open(KEY_FILE_PATH, 'wb') as key_file:
            key_file.write(key)
    with open(KEY_FILE_PATH, 'rb') as key_file:
        key = key_file.read()
    return key

# Set up the encryption cipher
ENCRYPTION_KEY = generate_key()
cipher = Fernet(ENCRYPTION_KEY)

# Function to upload files
def upload_file():
    filename = filedialog.askopenfilename()
    if filename:
        try:
            # Encrypt the file data
            with open(filename, 'rb') as f:
                file_data = f.read()
            encrypted_data = cipher.encrypt(file_data)

            # Connect to SFTP server and upload the file
            with paramiko.Transport((HOST, PORT)) as transport:
                try:
                    transport.connect(username=USERNAME, password=PASSWORD)
                except paramiko.SSHException as e:
                    messagebox.showerror('Connection Error', f'Failed to connect to SFTP server: {e}')
                    return
                
                sftp = transport.open_sftp()
                
                # Get the remote file path
                remote_path = os.path.join(REMOTE_DIRECTORY, os.path.basename(filename))
                with sftp.file(remote_path, 'wb') as remote_file:
                    remote_file.write(encrypted_data)
            
            messagebox.showinfo('Success', 'File uploaded successfully.')
        except Exception as e:
            messagebox.showerror('Error', f'Failed to upload file: {e}')


# Function to download files
def download_file():
    # Let user choose where to save the downloaded file
    save_path = filedialog.asksaveasfilename()
    if save_path:
        try:
            # Connect to SFTP server and download the file
            with paramiko.Transport((HOST, PORT)) as transport:
                transport.connect(username=USERNAME, password=PASSWORD)
                sftp = transport.open_sftp()
                
                # Get the remote file path
                remote_path = filedialog.askopenfilename(title='Select file to download')
                
                with sftp.file(remote_path, 'rb') as remote_file:
                    encrypted_data = remote_file.read()
                
                # Decrypt the file data
                decrypted_data = cipher.decrypt(encrypted_data)
                
                # Save the decrypted file
                with open(save_path, 'wb') as f:
                    f.write(decrypted_data)
            
            messagebox.showinfo('Success', 'File downloaded successfully.')
        except Exception as e:
            messagebox.showerror('Error', f'Failed to download file: {e}')

# Function to handle file management (viewing, deleting)
def manage_files():
    # Implementation for file management goes here (viewing and deleting files)
    pass

# Function to handle user authentication
def login():
    # Implementation for login and authentication goes here
    pass

# Main application GUI setup
def main():
    prompt_sftp_details()
    root = tk.Tk()
    root.title('File Sharing App')
    
    # Create buttons for file operations
    upload_button = tk.Button(root, text='Upload File', command=upload_file)
    upload_button.pack(pady=5)
    
    download_button = tk.Button(root, text='Download File', command=download_file)
    download_button.pack(pady=5)
    
    manage_button = tk.Button(root, text='Manage Files', command=manage_files)
    manage_button.pack(pady=5)
    
    login_button = tk.Button(root, text='Login', command=login)
    login_button.pack(pady=5)
    
    # Run the application
    root.mainloop()

if __name__ == '__main__':
    main()
