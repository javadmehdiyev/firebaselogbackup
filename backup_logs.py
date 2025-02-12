import os
import datetime
import tarfile
from firebase_admin import credentials, initialize_app, storage
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_backup(log_directory, backup_name):
    """Create a tar.gz archive of the log directory"""
    try:
        with tarfile.open(backup_name, "w:gz") as tar:
            tar.add(log_directory, arcname=os.path.basename(log_directory))
        return True
    except Exception as e:
        print(f"Error creating backup: {str(e)}")
        return False

def upload_to_firebase(backup_file, bucket_name):
    """Upload the backup file to Firebase Storage"""
    try:
        # Initialize Firebase with your credentials
        cred = credentials.Certificate(os.getenv('FIREBASE_CREDENTIALS_PATH'))
        initialize_app(cred, {'storageBucket': bucket_name})
        
        bucket = storage.bucket()
        current_date = datetime.datetime.now().strftime('%Y-%m-%d')
        
        # Create a new blob with the backup file
        blob = bucket.blob(f'logs_backup/{current_date}/{os.path.basename(backup_file)}')
        
        # Upload the file
        blob.upload_from_filename(backup_file)
        
        print(f"Successfully uploaded {backup_file} to Firebase Storage")
        return True
    except Exception as e:
        print(f"Error uploading to Firebase: {str(e)}")
        return False

def cleanup(backup_file):
    """Remove the local backup file after successful upload"""
    try:
        os.remove(backup_file)
        print(f"Successfully removed local backup file: {backup_file}")
    except Exception as e:
        print(f"Error removing local backup: {str(e)}")

def main():
    # Configuration
    log_directory = os.getenv('LOG_DIRECTORY', '/var/log')  # Default log directory
    bucket_name = os.getenv('FIREBASE_BUCKET_NAME')
    
    if not bucket_name:
        print("Error: FIREBASE_BUCKET_NAME not set in environment variables")
        return
    
    # Create backup filename with timestamp
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_name = f"logs_backup_{timestamp}.tar.gz"
    
    # Create backup
    if create_backup(log_directory, backup_name):
        # Upload to Firebase
        if upload_to_firebase(backup_name, bucket_name):
            # Cleanup local backup file
            cleanup(backup_name)
        else:
            print("Failed to upload backup to Firebase")
    else:
        print("Failed to create backup")

if __name__ == "__main__":
    main() 