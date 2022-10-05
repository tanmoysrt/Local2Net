import socket
from queue import Queue
import threading
from time import sleep
DEBUG = True

# rx -> receiving data from the channel
# tx -> sending data to the channel

class Adapter:
    def __init__(self, host="127.0.0.1", port=8005, forwarding_port=3000):
        global DEBUG
        self.DEBUG = DEBUG
        self.host = host
        self.port = port
        self.forwarding_port = forwarding_port
        self.rx_buffer = Queue() 
        self.tx_buffer = Queue() 

        # Events
        self.tx_channel_new_data_event = threading.Event()
        self.rx_channel_new_data_event = threading.Event()

        self.tx_channel_new_data_event.clear()
        self.rx_channel_new_data_event.clear()

        # Private variables
        self._killed_signal = False
        self._tx_exit = False
        self._rx_exit = False
        self._endpoint_socket_closed = False

    def connect(self): 
        self.endpoint_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.endpoint_sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.endpoint_sock.connect((self.host, int(self.port)))
        self.endpoint_sock.settimeout(5)

        self.backend_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.backend_sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.backend_sock.connect(("127.0.0.1", int(self.forwarding_port)))

        self.endpoint_rx_thread = threading.Thread(target=self._endpoint_rx_thread_func)
        self.endpoint_tx_thread = threading.Thread(target=self._endpoint_tx_thread_func)

        self.backend_rx_thread = threading.Thread(target=self._backend_rx_thread_func)
        self.backend_tx_thread = threading.Thread(target=self._backend_tx_thread_func)

        self.endpoint_rx_thread.start()
        self.endpoint_tx_thread.start()

        self.backend_rx_thread.start()
        self.backend_tx_thread.start()

        try:
            self.endpoint_rx_thread.join()
        except:
            if DEBUG: print("[DEBUG] Error while joining endpoint_rx_thread")
        try:
            self.endpoint_tx_thread.join()
        except:
            if DEBUG: print("[DEBUG] Error while joining endpoint_tx_thread")
        try:
            self.backend_rx_thread.join()
        except:
            if DEBUG: print("[DEBUG] Error while joining backend_rx_thread")

        try:
            self.backend_tx_thread.join()
        except:
            if DEBUG: print("[DEBUG] Error while joining backend_tx_thread")

        self._close_connection()

    def _endpoint_rx_thread_func(self):
        while True:
            try:
                data = self.endpoint_sock.recv(1024)
                if not data:
                    if DEBUG: print("[DEBUG] Invalid data received from system")
                else:
                    self.rx_buffer.put(data)
                    # Notify that new data is available
                    if not self.rx_channel_new_data_event.is_set():
                        self.rx_channel_new_data_event.set()
            except socket.timeout:
                if self._killed_signal:
                    self._tx_exit = True
                    break
            except socket.error:
                if DEBUG: print("[DEBUG] Socket error")
                break
            except Exception as e:
                if DEBUG: print("[DEBUG] Error while receiving data from system: {}".format(e))
                break

    def _endpoint_tx_thread_func(self):
        while True:
            while self.tx_buffer.empty():
                self.tx_channel_new_data_event.wait()
                self.tx_channel_new_data_event.clear()
            
            data = self.tx_buffer.get()
            self.endpoint_sock.sendall(data)

    def _backend_rx_thread_func(self):
        while True:
            data = self.backend_sock.recv(1024)
            if not data:
                if DEBUG: print("[DEBUG] Invalid data received from backend")
            else:
                self.tx_buffer.put(data)
                # Notify that new data is available
                if not self.tx_channel_new_data_event.is_set():
                    self.tx_channel_new_data_event.set()
    
    def _backend_tx_thread_func(self):
        while True:
            while self.rx_buffer.empty():
                self.rx_channel_new_data_event.wait()
                self.rx_channel_new_data_event.clear()
            
            data = self.rx_buffer.get()
            self.backend_sock.sendall(data)

    def close(self):
        self._send_kill_signal()
        self._close_connection()

    def _send_kill_signal(self, wait_for_exit_thread=True):
        self._killed_signal = True
        if wait_for_exit_thread:
            while self._tx_exit is False:
                if DEBUG: print("Waiting for tx thread to exit")
                sleep(0.1)
            while self._rx_exit is False:
                if DEBUG: print("Waiting for rx thread to exit")
                sleep(0.1)


    def _close_connection(self):
        if self._endpoint_socket_closed:
            return
        self.endpoint_sock.close()
        self._endpoint_socket_closed = True

# Driver code
if __name__ == "__main__":
    adapter = Adapter()
    try:
        adapter.connect()
    except KeyboardInterrupt:
        adapter.close()
    adapter.close()