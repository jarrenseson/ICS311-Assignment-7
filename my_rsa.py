import random

# Checks if number is prime
def miller_rabin(n, k=5):
    if n == 2 or n == 3:
        return True
    if n == 1 or n % 2 == 0:
        return False
    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

# Generates n
def euler_totient_function(p, q):
    phi=(p-1)*(q-1)
    return phi

# Generates d
def extended_euclidean_function(e,phi):
    if phi==0:
        return e, 1, 0
    g, x1, y1 = extended_euclidean_function(phi, e % phi)
    x=y1
    y=x1 - (e // phi) * y1
    return g, x, y

def modulo_inverse(e,phi):
    g, x, y = extended_euclidean_function(e,phi)
    if g!=1:
        raise ValueError("no modulo inverse")
    return x%phi

def generate_keys():
    p=0
    q=0
    while True:
        p=random.randint(10**10, 10**20)
        q=random.randint(10**10, 10**20)
        if(miller_rabin(p) and miller_rabin(q)):
            break

    n=p*q

    phi=euler_totient_function(p,q)

    e=65537
    d=modulo_inverse(e, phi)

    private_key=(e,n)
    public_key=(d,n)

    return public_key, private_key


def rsa_encrypt(message, public_key):
    message_bytes = message.encode()
    int_message = int.from_bytes(message_bytes, byteorder="big")
    if int_message >= public_key[1]:
        raise ValueError("message is too long")
    encrypted_message = pow(int_message, public_key[0], public_key[1])

    return encrypted_message

def rsa_decrypt(encrypted_message, private_key):
    decrypted_int_message = pow(encrypted_message, *private_key)
    decrypted_bytes = decrypted_int_message.to_bytes((decrypted_int_message.bit_length() + 7) // 8, byteorder="big")
    decrypted_message = decrypted_bytes.decode()
    
    return decrypted_message
def main():
    public_key, private_key = generate_keys()
    rsa_decrypt(rsa_encrypt("HEllo there", public_key), private_key)

if __name__ =="__main__":
    main()