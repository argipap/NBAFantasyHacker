from project import db


class Player(db.Model):
    __tablename__ = "players"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    player_id = db.Column(db.Integer, unique=True, nullable=False)
    first_name = db.Column(db.String(128), unique=False, nullable=False)
    last_name = db.Column(db.String(128), unique=False, nullable=False)
    statistics = db.relationship('Statistic', backref='player')
    fan_points = db.relationship('PlayerFanPoints', backref='player', uselist=False)

    def __init__(self, player_id, first_name, last_name):
        self.player_id = player_id
        self.first_name = first_name
        self.last_name = last_name

    def to_json(self):
        return {
            'player_id': self.player_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'fan_points': self.fan_points.total
        }

    @classmethod
    def get_player_id_by_full_name(cls, first_name, last_name):
        player = cls.query.filter_by(first_name=first_name).\
            filter_by(last_name=last_name).first()
        if player:
            return player.player_id


class PlayerFanPoints(db.Model):
    __tablename__ = "player_fanpoints"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    player_id = db.Column(db.Integer, db.ForeignKey('players.player_id'), unique=True, nullable=False)
    total = db.Column(db.Float, nullable=False)

    def __init__(self, player_id, total):
        self.player_id = player_id
        self.total = total
