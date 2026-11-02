import socket
import base64
import binascii
import codext

encode_table = {
    "A": ".-",
    "B": "-...",
    "C": "-.-.",
    "D": "-..",
    "E": ".",
    "F": "..-.",
    "G": "--.",
    "H": "....",
    "I": "..",
    "J": ".---",
    "K": "-.-",
    "L": ".-..",
    "M": "--",
    "N": "-.",
    "O": "---",
    "P": ".--.",
    "Q": "--.-",
    "R": ".-.",
    "S": "...",
    "T": "-",
    "U": "..-",
    "V": "...-",
    "W": ".--",
    "X": "-..-",
    "Y": "-.--",
    "Z": "--..",
    "0": "-----",
    "1": ".----",
    "2": "..---",
    "3": "...--",
    "4": "....-",
    "5": ".....",
    "6": "-....",
    "7": "--...",
    "8": "---..",
    "9": "----.",
    ".": ".-.-.-",
    ",": "--..--",
    "?": "..--..",
    " ": "SPACE",
}
decode_table = {v: k for k, v in encode_table.items()}


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(("challenge01.root-me.org", 52017))
    for _ in range(100):
        data = s.recv(1024)
        enc = data.decode().splitlines()[-2].split("'")[1]
        if "/" in enc:
            dec = ""
            for char in enc.split('/'):
                dec += decode_table[char].lower()
            print(f"Morse: {dec}")
        else:
            try:
                dec = base64.b16decode(enc.upper(), casefold=False).decode('utf-8')
                print(f"Hex: {dec}")
            except binascii.Error:
                pass

            try:
                dec = base64.b32decode(enc).decode('utf-8')
                print(f"Base32: {dec}")
            except binascii.Error:
                pass

            try:
                dec = base64.b64decode(enc).decode('utf-8')
                print(f"Base64: {dec}")
            except (binascii.Error, UnicodeDecodeError):
                pass            


            try:
                dec = base64.b85decode(enc).decode('utf-8')
                print(f"Base85: {dec}")
            except (binascii.Error, ValueError):
                pass
                    
        s.sendall(dec.encode())
        s.sendall('\n'.encode())
    data = s.recv(1024)
    print(data.decode())
