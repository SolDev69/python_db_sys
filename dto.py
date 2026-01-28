class UserDto:
    def __init__(self, id, name, password):
        self.id = id
        self.name = name
        self.password = password

dtos = []
def get_dtos():
    return dtos
def add_dto(dto):
    dtos.append(dto)
def del_dto(dto):
    dtos.remove(dto)