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

def RSA(message):
    p=0
    q=0
    while True:
        p=random.randint(10**100, 10**200)
        q=random.randint(10**100, 10**200)
        if(miller_rabin(p) and miller_rabin(q)):
            break

    n=p*q

    phi=euler_totient_function(p,q)

    e=65537
    d=modulo_inverse(e, phi)

    private=(e,n)
    public=(d,n)
    int_message=int(''.join([str(ord(char)).zfill(3) for char in message]))

    encrypted_message=pow(int_message, e, n)
    print(f"encrypted message: {encrypted_message}")

    decrypted_int_message=pow(int(encrypted_message),d,n)
    decrypted_message=''.join([chr(int(str(decrypted_int_message)[i:i+3])) for i in range(0,len(str(decrypted_int_message)), 3)])
    print(f"decrypted message: {decrypted_message}")
    print("=" * 50)

    return encrypted_message, decrypted_message

def main():
    RSA("hello there")
    RSA("Hello there")
    RSA("hELLO THERE")
    RSA("HELLO THERE")
    RSA("heLlO ThErE")
    RSA("HeLlO ThErE")

if __name__ =="__main__":
    main()