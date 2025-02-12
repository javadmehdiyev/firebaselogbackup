import os
import datetime
import tarfile
import base64
from github import Github
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

def upload_to_github(backup_file):
    """Upload the backup file to GitHub repository"""
    try:
        # GitHub configuration
        github_token = os.getenv('GITHUB_TOKEN')
        repo_name = os.getenv('GITHUB_REPO')
        
        if not github_token or not repo_name:
            print("Error: GitHub configuration not set in environment variables")
            return False
        
        # Initialize GitHub
        g = Github(github_token)
        repo = g.get_user().get_repo(repo_name)
        
        # Create path with current date
        current_date = datetime.datetime.now().strftime('%Y-%m-%d')
        file_path = f'logs_backup/{current_date}/{os.path.basename(backup_file)}'
        
        # Read the backup file
        with open(backup_file, 'rb') as file:
            content = file.read()
        
        # Convert to base64
        content_base64 = base64.b64encode(content).decode()
        
        try:
            # Try to get the file first (to update if exists)
            existing_file = repo.get_contents(file_path)
            repo.update_file(
                file_path,
                f"Update log backup for {current_date}",
                content_base64,
                existing_file.sha
            )
        except:
            # File doesn't exist, create new
            repo.create_file(
                file_path,
                f"Add log backup for {current_date}",
                content_base64
            )
        
        print(f"Successfully uploaded {backup_file} to GitHub")
        return True
    except Exception as e:
        print(f"Error uploading to GitHub: {str(e)}")
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
    
    # Create backup filename with timestamp
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_name = f"logs_backup_{timestamp}.tar.gz"
    
    # Create backup
    if create_backup(log_directory, backup_name):
        # Upload to GitHub
        if upload_to_github(backup_name):
            # Cleanup local backup file
            cleanup(backup_name)
        else:
            print("Failed to upload backup to GitHub")
    else:
        print("Failed to create backup")

if __name__ == "__main__":
    main() 