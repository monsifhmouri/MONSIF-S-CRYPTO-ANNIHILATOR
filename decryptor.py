import os  
import json  
import base64  
from cryptography.fernet import Fernet, InvalidToken  
from Crypto.Cipher import AES, DES3  
from Crypto.Util.Padding import unpad  
from Crypto.Random import get_random_bytes  
from itertools import product  

# --- CONFIG ---  
ENCRYPTED_FILE = os.path.join(os.environ['USERPROFILE'], 'Desktop', 'annihilated_data.json')  
OUTPUT_FILE = os.path.join(os.environ['USERPROFILE'], 'Desktop', 'decrypted_plunder.txt')  

# Nuclear option dictionary  
COMMON_KEYS = [  
    "WO39vdwwmkeYpB5KOSmfu28mW7e1sIQV9BoBDRs22wI=",  # Original key  
    "U2VjcmV0S2V5MTIzNDU2Nzg5MDEyMzQ1Njc4OTA=",      # Base64 common  
    "password", "admin", "certinia", "12345678",      # Bruteforce candidates  
    "Th1sIsN0tAP@ssw0rd"  
]  

def fernet_decrypt(encrypted_data, key):  
    try:  
        fernet = Fernet(key)  
        return fernet.decrypt(encrypted_data).decode()  
    except (InvalidToken, ValueError):  
        return None  

def aes_decrypt(encrypted_data, key):  
    try:  
        iv = encrypted_data[:16]  
        cipher = AES.new(key, AES.MODE_CBC, iv)  
        return unpad(cipher.decrypt(encrypted_data[16:]), AES.block_size).decode()  
    except:  
        return None  

def tripledes_decrypt(encrypted_data, key):  
    try:  
        iv = encrypted_data[:8]  
        cipher = DES3.new(key, DES3.MODE_CFB, iv)  
        return cipher.decrypt(encrypted_data[8:]).decode()  
    except:  
        return None  

def nuclear_bruteforce(encrypted_data):  
    # Try all known encryption protocols  
    print("[!] Launching cryptocalypse...")  
    
    # Fernet first  
    for key in COMMON_KEYS:  
        if len(key) < 32:  
            key_padded = base64.urlsafe_b64encode(key.ljust(32, '#')[:32].encode())  
        else:  
            key_padded = base64.urlsafe_b64encode(key.encode())  
        
        decrypted = fernet_decrypt(encrypted_data, key_padded)  
        if decrypted:  
            return decrypted  
    
    # AES brute  
    for key in COMMON_KEYS:  
        key_bytes = key.encode().ljust(16, b'\0')[:16]  
        decrypted = aes_decrypt(encrypted_data, key_bytes)  
        if decrypted:  
            return decrypted  
    
    # 3DES hail mary  
    for key in COMMON_KEYS:  
        key_bytes = key.encode().ljust(24, b'\0')[:24]  
        decrypted = tripledes_decrypt(encrypted_data, key_bytes)  
        if decrypted:  
            return decrypted  
    
    return "FAIL: No key matched. Time for GPU brute force?"  

def main():  
    with open(ENCRYPTED_FILE, "rb") as f:  
        encrypted_blob = f.read()  
    
    result = nuclear_bruteforce(encrypted_blob)  
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:  
        f.write(result if result else "Decryption failed. Better luck next apocalypse.")  
    
    print(f"[!] Decrypted loot → {OUTPUT_FILE}")  

if __name__ == "__main__":  
    print(r"""  
     ██████╗██████╗ ██╗   ██╗██████╗ ████████╗  
    ██╔════╝██╔══██╗╚██╗ ██╔╝██╔══██╗╚══██╔══╝  
    ██║     ██████╔╝ ╚████╔╝ ██████╔╝   ██║     
    ██║     ██╔═══╝   ╚██╔╝  ██╔═══╝    ██║     
    ╚██████╗██║        ██║   ██║        ██║     
     ╚═════╝╚═╝        ╚═╝   ╚═╝        ╚═╝     
    """)  
    main()  
