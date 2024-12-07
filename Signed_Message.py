import random

# Checks if number is prime
def is_prime(n, k=5):
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
def create_phi(p, q):
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
    while True:
        p=random.randint(10**10, 10**20)
        q=random.randint(10**10, 10**20)
        if(is_prime(p) and is_prime(q)):
            break

    n=p*q

    phi=create_phi(p,q)

    e=65537
    d=modulo_inverse(e, phi)

    private_key=(e,n)
    public_key=(d,n)

    return public_key, private_key


# Function to sign message
def sign_message(message, private_key):
    hashed = hash(message)
    signature = pow(hashed, private_key[0], private_key[1])
    return signature

# Function to verify signed message
def verify_signed_message(message, signature, public_key):
    hashed = hash(message)
    decrypted_hash = pow(signature, public_key[0], public_key[1])
    return decrypted_hash == hashed

# Main / Testing
def main():
    # Generate RSA keys
    public_key, private_key = generate_keys()
    
    # Original message
    message = "This is a secret message."
    print(f"Original Message: {message}")
    
    # Sign the message
    signature = sign_message(message, private_key)
    print(f"Signature: {signature}")
    
    # Verify the signed message
    is_valid = verify_signed_message(message, signature, public_key)
    print(f"Is the signature valid? {is_valid}")

    # Tamper with the message
    message = "This is a tampered message!"
    print(f"Tampered Message: {message}")

    # Verify the tampered message
    is_valid = verify_signed_message(message, signature, public_key)
    print(f"Is the signature valid? {is_valid}")

if __name__ == "__main__":
    main()