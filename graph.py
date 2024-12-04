class person:
    def __init__(self, identity, public_key=none, private_key=none):
        self.identity=identity
        self.public_key=public_key
        self.private_key=private_key
        self.metadata={}
    
    def __str__(self):
        return self.identity

class graph:
    def __init__(self):
        self.nodes={}
        self.edges={}