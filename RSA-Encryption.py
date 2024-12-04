import random

# Checks if number is prime
def is_prime(n):
    if n<= 1:
        return False
    for i in range(2,int(n*.5)+1):
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
    return x%phi

def RSA_encryption(message):
    p=0
    q=0
    while True:
        p=randomint(10**100,int('inf'))
        q=randomint(10**100,int('inf'))
        if(is_prime(p) and is_prime(q)):
            break
    print("p: " + p)
    print("q: " + q)

    n=p*q
    print("n: " + n)

    phi=euler_totient_function(p,q)
    print("phi: " + phi)

    e=3
    d=modulo_inverse(e, phi)
    print("d: " + d)

    private=(e,n)
    public=(d,n)

    encrypted_message_private=(int(message)^e)%n
    encrypted_message_public=(int(message)^d)%n

    return encrypted_message_private, encrypted_message_public