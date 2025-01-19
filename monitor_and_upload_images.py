import os
import time
import shutil
import subprocess

WATCH_FOLDER = r"C:\WATCH"
UPLOADED_FOLDER = r"C:\UPLOADS"

UPLOAD_URL = "https://projects.benax.rw/f/o/r/e/a/c/h/p/r/o/j/e/c/t/s/4e8d42b606f70fa9d39741a93ed0356c/iot_testing_202501/upload.php"

os.makedirs(UPLOADED_FOLDER, exist_ok=True)

def upload_file(file_path):
    
    try:
        result = subprocess.run(
            ["curl", "X", "POST", "-F", f"imageFile=@{file_path}", UPLOAD_URL],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
             print(f"Successfully uploaded: {file_path}")
             return True
        else:
            print(f"Failed to upload: {file_path}\nError: {result.stderr}")
            return False
    except Exception as e:
        print(f"Error during upload: {e}")
        return False
    
def monitor_and_upload():
    print("Monitoring folder for new images...")
    processed_files = set()
    
    while True:
        try:
            files = [
            f for f in os.listdir(WATCH_FOLDER)
            if os.path.isfile(os.path.join(WATCH_FOLDER,f)) and f not in processed_files
        ]
            for file_name in files:
                file_path = os.path.join(WATCH_FOLDER, file_name)
                
                if not file_name.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                    continue
                
                print(f"New file detected: {file_path}, waiting 30 seconds before upload...")
                time.sleep(30)
                
                if upload_file(file_path):
                    shutil.move(file_path, os.path.join(UPLOADED_FOLDER, file_name))
                    print(f"Moved {file_name} to uploaded folder.")
                    processed_files.add(file_name)
                else:
                    print(f"Failed to process {file_name}, retry later.")
                    
            time.sleep(5)
        except KeyboardInterrupt:
            print("Monitoring stopped.")
            break
        except Exception as e:
            print(f"Error: {e}")   
            
if __name__ == "__main__":
    monitor_and_upload()     