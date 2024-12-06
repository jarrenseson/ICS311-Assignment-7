from my_rsa import generate_keys, rsa_decrypt, rsa_encrypt
from run_length_encoding import run_length_encode
from lossy_compression import FFTTransform

class message:
    def __init__(self, sender, receiver, body, metadata=None):
        self.sender=sender.identity
        self.receiver=receiver.identity
        self.body=body
        self.metadata=metadata
    
    def __str__(self):
        return(f"to: {self.receiver}\nfrom: {self.sender}\nbody: {self.body}\nmetadata: {self.metadata}")

class person:
    def __init__(self, identity, public_key=None, private_key=None, inbox=None): # inbox will contain the decrypted messages
        self.identity=identity
        self.public_key=public_key
        self.private_key=private_key
        self.inbox=[]

class graph:
    def __init__(self):
        self.nodes={}
        self.edges={}

    def add_person(self, person):
        self.nodes[person.identity]=person
        self.edges[person.identity]=[]

    def add_edge(self, person1, person2):
        if person1.identity in self.edges and person2.identity in self.edges:
            self.edges[person1.identity].append(person2)
            self.edges[person2.identity].append(person1)
    
    def send_rsa_message(self, sender, receiver, unencrypted_message, metadata=None):
        if sender.identity not in self.nodes or receiver.identity not in self.nodes:
            raise ValueError("sender or receiver not in graph.")
        public_key, private_key = generate_keys()
        self.nodes[sender.identity].public_key = public_key
        self.nodes[receiver.identity].public_key = public_key
        self.nodes[sender.identity].private_key = private_key 
        self.nodes[receiver.identity].private_key = private_key
        encrypted_message = rsa_encrypt(unencrypted_message, public_key)
        final_message = message(sender, receiver, encrypted_message, metadata)
        self.nodes[receiver.identity].inbox.append(final_message)
        return None
    
    def read_rsa_message(self, person):
        if person.identity not in self.nodes:
            raise ValueError("person not in graph")
        self.nodes[person.identity].inbox[0].body = rsa_decrypt(self.nodes[person.identity].inbox[0].body, self.nodes[person.identity].private_key)
        print(f"{self.nodes[person.identity].inbox[0]}")
        del self.nodes[person.identity].inbox[0]

    # Sends a compressed message from a sender to a receiver using Run-Length Encoding (RLE).
    def send_compressed_message(self, sender, receiver, uncompressed_message):
        # Validation of sender and receiver
        if sender.identity not in self.nodes or receiver.identity not in self.nodes:
            raise ValueError("Sender or receiver not in graph.")

        # Compress the message body
        compressed_message = run_length_encode(uncompressed_message)

        # Create metadata indicating the message is compressed
        metadata = {"compression": "RLE", "original_length": len(uncompressed_message)}

        # Create and send the message
        compressed_msg = message(sender, receiver, compressed_message, metadata)
        self.nodes[receiver.identity].inbox.append(compressed_msg)

        print(f"Compressed message sent from {sender.identity} to {receiver.identity}.")

    # Sends a lossy compressed message from sender to reciever using FFT
    def send_fft_message(self, sender, receiver, uncompressed_message, compression_level, metadata=None):
        if sender.identity not in self.nodes or receiver.identity not in self.nodes:
            raise ValueError("sender or receiver not in graph.")

        # Use FFTTransform to compress the message
        compressed_body, transformed_coefficients = FFTTransform.compress_message(uncompressed_message, compression_level)

        # Create metadata
        final_metadata = metadata or {}
        final_metadata['compression'] = 'fft'
        final_metadata['original_length'] = len(uncompressed_message)
        final_metadata['compression_level'] = compression_level
        final_metadata['coefficients'] = transformed_coefficients.tolist()

        # Send the message
        final_message = message(sender, receiver, compressed_body, final_metadata)
        self.nodes[receiver.identity].inbox.append(final_message)

    # Reads lossy compressed message
    def read_fft_message(self, person):
        if person.identity not in self.nodes:
            raise ValueError("person not in graph")

        # Read and reconstruct the first message in the inbox
        message_to_read = self.nodes[person.identity].inbox[0]
        transformed_coefficients = np.array(message_to_read.metadata['coefficients'], dtype=np.complex128)
        decompressed_body = FFTTransform.decompress_message(message_to_read.body, transformed_coefficients)

        print(f"Decompressed message: {decompressed_body}")

def main():
    network = graph()

    person1=person("alex")
    person2=person("grace")
    person3=person("ben")

    network.add_person(person1)
    network.add_person(person2)

    network.send_rsa_message(person1, person2, "Hellooooooo!")
    network.read_rsa_message(person2)
    network.send_rsa_message(person3, person2, "hehe")

    print("------------------------------Test for send compressed Message-----------------------------")

    #testing for run_length_encoding
    # Send a compressed message
    network.send_compressed_message(person1, person2, "aaaabbbccd")

    # Check the receiver's inbox
    for msg in person2.inbox:
        print(msg)

    print("------------------------------Test for lossy compressed message-----------------------------")

    # Send an FFT-compressed message
    network.send_fft_message(person1, person2, "Hellooooooo, how are you?", compression_level = 5)
    
    # Receiver reads the message
    network.read_fft_message(person2)

if __name__=="__main__":
    main()
