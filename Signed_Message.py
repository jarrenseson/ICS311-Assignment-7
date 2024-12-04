import hashlib
import random

# Generate RSA Keys
def generate_RSA_keys():
    p, q = random_prime_number() # Generate random prime numbers
    n = p * q # Calculate n
    phi = (p-1)*(q-1) # Calculate phi
    e = 17 # Public exponent
    while gcd(e, phi) != 1:
        e = random.randint(2, phi - 1)
    
    d = pow(e, -1, phi) # Private exponent, modular inverse of e and phi

    print(f"Generated keys: Public key (e={e}, n={n}), Private key (d={d}, n={n})")
    return (e, n), (d, n) # Return public and private keys

# Function to generate random prime number
def random_prime_number():
    p = random.randint(10**12, 10**13) # Random number between 10^10 and 10^11
    q = random.randint(10**12, 10**13) # Random number between 10^10 and 10^11

    while not is_prime(p): # If p is not prime, generate a new random number
        p = random.randint(10**12, 10**13)
    while not is_prime(q) or q == p: # If q is not prime or equal to p, generate a new random number
        q = random.randint(10**12, 10**13)
    return p, q

# Function to check if number is prime
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**.5) + 1):
        if n % i == 0:
            return False
    return True

# GCD Function
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

# Function to hash message
def hash_message(message):
    if not isinstance(message, str):
        message = str(message)
    # Use SHA-1 instead of SHA-256
    hashed = int(hashlib.sha1(message.encode()).hexdigest(), 16)
    print(f"Hashed message (SHA-1): {hashed}")
    return hashed


# Function to sign message
def sign_message(message, private_key):
    d, n = private_key
    hashed = hash_message(message)
    signature = pow(hashed, d, n)
    print(f"Signed message: {signature}")
    return signature

# Function to verify signed message
def verify_signed_message(message, signature, public_key):
    e, n = public_key
    hashed = hash_message(message)
    decrypted_hash = pow(signature, e, n)

    print(f"Original hash: {hashed}")
    print(f"Decrypted hash: {decrypted_hash}")
    return decrypted_hash == hashed

# Main / Testing
def main():
    # Generate RSA keys
    public_key, private_key = generate_RSA_keys()
    
    # Original message
    message = "This is a secret message."
    
    # Sign the message
    signature = sign_message(message, private_key)
    print(f"Signature: {signature}")
    
    # Verify the signed message
    is_valid = verify_signed_message(message, signature, public_key)
    print(f"Is the signature valid? {is_valid}")

if __name__ == "__main__":
    main()