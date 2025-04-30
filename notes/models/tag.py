class Tag:
    def __init__(self, name):
        if not name.startswith('#'):
            self.name = f"#{name}" 
        else:
            self.name = name  

    def __str__(self):
        return f"{self.name}"