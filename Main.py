import socket

import snap7
from snap7.util import set_bool
from snap7.type import Areas

PLC_IP = '192.168.1.91'
RACK = 0
SLOT = 1
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 8080))
server_socket.listen(5)


print("Serwer nasłuchuje...")
def write_to_m_area(data):
    if 'true' in data:
        what = True
    else:
        what = False
    byte = (data[data.index('.') + len('.'):])
    plc = snap7.client.Client()
    plc.connect(PLC_IP, RACK, SLOT)
    area = Areas.MK
    start = 0
    size = 1
    data = plc.read_area(area, 0, start, size)
    set_bool(data, 0, int(byte), what)
    plc.write_area(area, 0, start, data)
    plc.disconnect()
while True:
    conn, addr = server_socket.accept()
    print(f"Połączono z {addr}")

    while True:
        data = conn.recv(1024)
        if not data:
            break
        print("Otrzymano:", data.decode())
        write_to_m_area(str(data.decode()))
    conn.close()
    print(f"Połączenie z {addr} zostało zamknięte")




