import socket

def get_ipv4_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
    except Exception as e:
        print(f"Une erreur s'est produite: {e}")
        ip_address = None
    finally:
        s.close()
    return ip_address

def get_code_room():
    return get_ipv4_address().split('.')[-1]

def verif_code(code):
    if len(code) > 3:
        return False
    for i in range(len(code)):
        if not('0' <= code[i] <= '9'):
            return False
    if not(0 < eval(code) <256):
        return False
    return True

def connect_ipv4(code=None):
    if not(code):
        code = input("code du serveur:")
    code = code.lstrip('0')
    if not(verif_code(code)):
        while not(verif_code(code)):
            print("code impossible")
            code = input("code du serveur:")
            code = code.lstrip('0')
    adresse = get_ipv4_address()
    adresse = adresse.split('.')
    adresse.pop()
    adresse.append(code)
    adresse = '.'.join(adresse)
    return adresse
