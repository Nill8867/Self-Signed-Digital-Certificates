#!/usr/bin/env python3

import ssl
import socket
import sys
import os
import time
import curses
from threading import Thread, Event
import colorama
from colorama import init
init()

os.environ.setdefault('ESCDELAY', '25')  # Reduce ESC key delay

class TLSClient:
    def __init__(self, host='localhost', port=8443):
        self.host = host
        self.port = port
        # Fix certificate path
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.cert_path = os.path.join(script_dir, "..", "certs", "server.crt")  # Using server.crt instead of client.crt
        print(f"Looking for certificate at: {self.cert_path}")
        self.secure_socket = None
        self.screen = None
        self.stop_event = Event()
        self.reconnect_attempts = 3
        self.reconnect_delay = 2

    def setup_ui(self):
        try:
            self.screen = curses.initscr()
            if not self.screen:
                raise Exception("Failed to initialize curses screen")
            curses.start_color()
            curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
            curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
            curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
            curses.noecho()
            curses.cbreak()
            self.screen.keypad(True)
            self.screen.scrollok(True)
            self.screen.clear()
        except Exception as e:
            print(f"Failed to setup UI: {e}")
            raise

    def cleanup_ui(self):
        if self.screen:
            self.screen.keypad(False)
            curses.nocbreak()
            curses.echo()
            curses.endwin()

    def check_certificate(self):
        try:
            if not os.path.exists(self.cert_path):
                print(f"Error: Certificate not found at {self.cert_path}")
                print("Current directory:", os.getcwd())
                print("Please ensure the certificate exists in the certs directory")
                return False
            print(f"Found certificate at {self.cert_path}")
            return True
        except Exception as e:
            print(f"Error checking certificate: {e}")
            return False

    def connect_to_server(self):
        for attempt in range(self.reconnect_attempts):
            try:
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.settimeout(10)

                # Create an unverified context for testing
                context = ssl._create_unverified_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE

                self.secure_socket = context.wrap_socket(client_socket)

                self.log_message(f"Connecting to {self.host}:{self.port}... (Attempt {attempt + 1})", 2)
                self.secure_socket.connect((self.host, self.port))
                self.log_message("Connected successfully!", 1)
                return True

            except (ssl.SSLError, ConnectionRefusedError, socket.timeout) as e:
                self.log_message(f"Connection attempt {attempt + 1} failed: {str(e)}", 3)
                if attempt < self.reconnect_attempts - 1:
                    self.log_message(f"Retrying in {self.reconnect_delay} seconds...", 2)
                    time.sleep(self.reconnect_delay)
                else:
                    self.log_message("Maximum reconnection attempts reached.", 3)
        return False

    def log_message(self, message, color_pair=0):
        if self.screen:
            max_y, max_x = self.screen.getmaxyx()
            y, x = self.screen.getyx()
            if y >= max_y - 1:
                self.screen.scroll(1)
                y = max_y - 2
            self.screen.addstr(y, 0, message + "\n", curses.color_pair(color_pair))
            self.screen.refresh()

    def receive_messages(self):
        while not self.stop_event.is_set():
            try:
                data = self.secure_socket.recv(1024)
                if not data:
                    self.log_message("Server disconnected.", 3)
                    break
                if data.decode() == "ping":
                    continue
                self.log_message(f"Server: {data.decode()}", 1)
            except socket.timeout:
                continue
            except (ssl.SSLError, socket.error) as e:
                if not self.stop_event.is_set():
                    self.log_message(f"Error receiving message: {e}", 3)
                    break

    def send_message(self, message):
        try:
            self.secure_socket.send(message.encode())
        except (socket.error, ssl.SSLError) as e:
            self.log_message(f"Error sending message: {e}", 3)
            return False
        return True

    def interactive_session(self):
        try:
            receiver_thread = Thread(target=self.receive_messages)
            receiver_thread.daemon = True
            receiver_thread.start()

            while not self.stop_event.is_set():
                try:
                    self.screen.addstr(curses.LINES - 1, 0, "> ")
                    self.screen.clrtoeol()
                    curses.echo()
                    message = self.screen.getstr(curses.LINES - 1, 2).decode()
                    curses.noecho()

                    if message.lower() == 'exit':
                        break
                    if not self.send_message(message):
                        break
                except curses.error:
                    continue
        finally:
            self.stop_event.set()
            receiver_thread.join(timeout=1.0)

    def run(self):
        try:
            print("Setting up UI...")  # Debug message
            self.setup_ui()
            
            print("Checking certificate...")  # Debug message
            if not self.check_certificate():
                print("Certificate check failed!")  # Debug message
                return
                
            print(f"Connecting to {self.host}...")  # Debug message
            if not self.connect_to_server():
                print("Connection failed!")  # Debug message
                return
                
            print("Starting interactive session...")  # Debug message
            self.interactive_session()
        except Exception as e:
            print(f"Fatal error: {e}")  # Debug message
        finally:
            if self.secure_socket:
                self.secure_socket.close()
            self.cleanup_ui()
            print("Connection closed")  # Debug message

if __name__ == "__main__":
    # Allow IP input from command-line
    if len(sys.argv) > 1:
        ip_address = sys.argv[1]
    else:
        ip_address = input("Enter server IP address (e.g., 172.17.8.200): ")

    client = TLSClient(host=ip_address)
    client.run()