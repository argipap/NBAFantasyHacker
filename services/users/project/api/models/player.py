from project import db


class Player(db.Model):
    __tablename__ = "players"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    player_id = db.Column(db.Integer, unique=True, nullable=False)
    first_name = db.Column(db.String(128), unique=False, nullable=False)
    last_name = db.Column(db.String(128), unique=False, nullable=False)

    def __init__(self, player_id, first_name, last_name):
        self.player_id = player_id
        self.first_name = first_name
        self.last_name = last_name

    def to_json(self):
        return {
            'id': self.id,
            'player_id': self.player_id,
            'first_name': self.first_name,
            'last_name': self.last_name
        }

    @classmethod
    def get_player_id_by_full_name(cls, first_name, last_name):
        player = cls.query.filter_by(first_name=first_name).\
            filter_by(last_name=last_name).\
            first()
        if player:
            return player.player_id
