import subprocess

def update_requirements():
    output = subprocess.run(['sh', 'update_requirements.sh'], capture_output=True)
    return output