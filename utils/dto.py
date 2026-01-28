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


class ScoreDto:
    # def __init__(self, user1, user2, score1, score2):
    #     self.user1 = user1
    #     self.user2 = user2
    #     self.score1 = score1
    #     self.score2 = score2

    def set_user1(self, user):
        self.user1 = user
    def set_user2(self, user):
        self.user2 = user
    def set_score1(self, score):
        self.score1 = score
    def set_score2(self, score):
        self.score2 = score

    def get_user1(self):
        return self.user1
    def get_user2(self):
        return self.user2
    def get_score1(self):
        return self.score1
    def get_score2(self):
        return self.score2
