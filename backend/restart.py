"""
Quick script to restart the backend server.
"""
import subprocess
import sys
import time

# Kill existing processes on port 8000
print("Stopping existing backend processes...")
result = subprocess.run(
    ['netstat', '-ano'],
    capture_output=True,
    text=True,
    shell=True
)

pids = set()
for line in result.stdout.split('\n'):
    if ':8000' in line and 'LISTENING' in line:
        parts = line.split()
        if parts:
            pid = parts[-1]
            try:
                pids.add(int(pid))
            except ValueError:
                pass

for pid in pids:
    print(f"Killing PID {pid}...")
    subprocess.run(['taskkill', '/F', '/PID', str(pid)], shell=True)

time.sleep(2)

# Start fresh backend
print("\nStarting fresh backend instance...")
print("Run: python main.py")
print("\nOr manually restart from your terminal.")
