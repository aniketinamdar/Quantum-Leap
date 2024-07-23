import subprocess
import os
import time
import threading
import requests

curr = os.getcwd()

frontend_dir = os.path.join(curr, 'qlfrontend')
backend_dir = os.path.join(curr, 'qlbackend')
backend_script = 'main.py'

# Provide the full path to the npm executable
npm_path = 'C:\\Program Files\\nodejs\\npm.cmd'

def start_frontend():
    print("Starting frontend...")
    frontend_process = subprocess.Popen([npm_path, 'run', 'dev'], cwd=frontend_dir)
    return frontend_process

def start_backend():
    print("Starting backend...")
    backend_process = subprocess.Popen(['python', backend_script], cwd=backend_dir)
    return backend_process

def wait_for_process(proc, name):
    try:
        proc.wait()
    except KeyboardInterrupt:
        print(f"Terminating {name} process...")
        proc.terminate()
        proc.wait()

def is_backend_ready(url='http://localhost:5000'):
    try:
        response = requests.get(url)
        return response.status_code == 200
    except requests.ConnectionError:
        return False

if __name__ == "__main__":
    backend_process = start_backend()
    
    # Check if the backend is ready before starting the frontend
    backend_ready = False
    while not backend_ready:
        print("Model is too big to load, please wait for a while...")
        time.sleep(120)
        backend_ready = is_backend_ready()
    
    frontend_process = start_frontend()

    backend_thread = threading.Thread(target=wait_for_process, args=(backend_process, "backend"))
    frontend_thread = threading.Thread(target=wait_for_process, args=(frontend_process, "frontend"))
    
    backend_thread.start()
    frontend_thread.start()
    
    backend_thread.join()
    frontend_thread.join()
    
    print("Both processes terminated.")
