class UserDto:
    def __init__(self, id, name, salt, password):
        self.id = id
        self.name = name
        self.salt = salt
        self.password = password

dtos = []
def get_dtos():
    return dtos
def add_dto(dto):
    dtos.append(dto)
def del_dto(dto):
    dtos.remove(dto)
def find_salt_among_dtos(user):
    for dto in dtos:
        if dto.name == user:
            return dto.salt
    return None

