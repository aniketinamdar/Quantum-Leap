import subprocess
import os
import time
import threading
import requests
import sys

curr = os.getcwd()

frontend_dir = os.path.join(curr, 'qlfrontend')
backend_dir = os.path.join(curr, 'qlbackend')
backend_script = 'main.py'

npm_path = 'C:\\Program Files\\nodejs\\npm.cmd'
python_path = sys.executable  

def create_virtualenv(venv_path):
    print("Creating virtual environment...")
    subprocess.run([python_path, '-m', 'venv', venv_path], cwd=backend_dir)

def install_backend_requirements(venv_path):
    print("Installing backend requirements...")
    pip_executable = os.path.join(venv_path, 'Scripts', 'pip')
    subprocess.run([pip_executable, 'install', '-r', os.path.join(backend_dir,'requirements.txt')], cwd=backend_dir)

def install_frontend_dependencies():
    print("Installing frontend dependencies...")
    subprocess.run([npm_path, 'install'], cwd=frontend_dir)

def start_frontend():
    print("Starting frontend...")
    frontend_process = subprocess.Popen([npm_path, 'run', 'dev'], cwd=frontend_dir)
    return frontend_process

def start_backend(venv_path):
    print("Starting backend...")
    python_executable = os.path.join(venv_path, 'Scripts', 'python')
    backend_process = subprocess.Popen([python_executable, backend_script], cwd=backend_dir)
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
    venv_path = os.path.join(backend_dir, 'venv')
    
    create_virtualenv(venv_path)
    install_backend_requirements(venv_path)
    install_frontend_dependencies()
    
    backend_process = start_backend(venv_path)
    
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
