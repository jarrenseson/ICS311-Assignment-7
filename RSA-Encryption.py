import random
import math

# Checks if number is prime
def is_prime(n):
    if n<= 1:
        return False
    for i in range(2,math.sqrt(n)):
        if n%i==0:
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
        print("no modulo inverse")
        return
    return x%phi

def RSA(message):
    p=0
    q=0
    while True:
        p=random.randint(10**100, 10**1000)
        q=random.randint(10**100, 10**1000)
        if(is_prime(p) and is_prime(q)):
            break

    n=p*q

    phi=euler_totient_function(p,q)

    e=65537
    d=modulo_inverse(e, phi)

    private=(e,n)
    public=(d,n)

    encrypted_message=pow(int(message),e,n)
    print(f"encrypted message: {encrypted_message}")

    decrypted_message=pow(int(encrypted_message),d,n)
    print(f"decrypted message: {decrypted_message}")

    return encrypted_message, decrypted_message

def main():
    print(RSA("hello there"))

if __name__ =="__main__":
    main()