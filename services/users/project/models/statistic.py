from project import db


class Statistic(db.Model):
    __tablename__ = "statistics"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    statistic_id = db.Column(db.Integer, unique=True, nullable=False)
    stat_short_name = db.Column(db.String(128), unique=False, nullable=False)
    stat_full_name = db.Column(db.String(128), unique=False, nullable=False)
    stat_modifier = db.Column(db.String(128), unique=False, nullable=False)

    def __init__(self, statistic_id, stat_short_name, stat_full_name, stat_modifier):
        self.statistic_id = statistic_id
        self.stat_short_name = stat_short_name
        self.stat_full_name = stat_full_name
        self.stat_modifier = stat_modifier

    @classmethod
    def get_stat_name_by_id(cls, stat_id):
        return cls.query.filter_by(statistic_id=stat_id).first().stat_short_name

    @classmethod
    def get_stat_modifier_by_name(cls, stat_name):
        return cls.query.filter_by(stat_short_name=stat_name).first().stat_modifier

    def to_json(self):
        return {
            'id': self.id,
            'statistic_id': self.statistic_id,
            'stat_short_name': self.stat_short_name,
            'stat_full_name': self.stat_full_name,
            'stat_modifier': self.stat_modifier
        }
