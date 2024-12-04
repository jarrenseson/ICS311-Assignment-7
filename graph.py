from rsa import RSA_encryption, RSA_decryption

class person:
    def __init__(self, identity, public_key=None, private_key=None, inbox=None): # inbox will contain the decrypted messages
        self.identity=identity
        self.public_key=public_key
        self.private_key=private_key
        self.metadata={}
        self.inbox=inbox
    
    def __str__(self):
        return self.identity

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

class message:
    def __init__(self, sender, reciever, body, metadata=None):
        self.sender=sender
        self.receiver=reciever
        self.body=body
        self.metadata=metadata