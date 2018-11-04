class Field:
    def __init__(self, name, data_type, constraint=None):
        self.name = name
        self.data_type = data_type
        self.constraint = constraint or ''

    def __repr__(self):
        return '{name} {data_type} {constraint}'.\
            format(name=self.name, data_type=self.data_type, constraint=self.constraint)
