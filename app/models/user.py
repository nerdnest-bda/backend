
class User:
    def __init__(self, uid, full_name, email, password, gpa, verbal_score, quant_score, awa_score  ):
        self.uid = uid
        self.full_name = full_name
        self.email = email
        self.gpa = gpa
        self.password = password
        self.verbal_score = verbal_score
        self.quant_score =  quant_score
        self.awa_score = awa_score

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    def to_dict(self):
        return {
            "uid": self.uid,
            "full_name": self.full_name,
            "email": self.email,
            "gpa": self.gpa,
            "password" : self.password,
            "verbal_score": self.verbal_score,
            "quant_score": self.quant_score,
            "awa_score": self.awa_score

        }
