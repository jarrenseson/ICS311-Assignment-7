from my_rsa import generate_keys, rsa_decrypt, rsa_encrypt

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

if __name__=="__main__":
    main()