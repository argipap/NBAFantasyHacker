from project import db


class Statistic(db.Model):
    __tablename__ = "statistics"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    statistic_id = db.Column(db.Integer, db.ForeignKey('stat_categories.category_id'), nullable=False)
    category = db.relationship('StatisticCategory', backref='statistic')
    player_id = db.Column(db.Integer, db.ForeignKey('players.player_id'), nullable=False)
    value = db.Column(db.Float, nullable=False)
    year = db.Column(db.Integer, nullable=False)

    def __init__(self, statistic_id, player_id, value, year):
        self.statistic_id = statistic_id
        self.player_id = player_id
        self.value = value
        self.year = year
        self.category_id = statistic_id

    def to_json(self):
        return {
            'statistic_id': self.statistic_id,
            'value': self.value,
            'player_id': self.player_id,
            'year': self.year
        }

    @classmethod
    def get_statistics_by_player_id(cls, player_id, year):
        return cls.query.filter((Statistic.player_id == player_id) & (Statistic.year == year))


class StatisticCategory(db.Model):
    __tablename__ = "stat_categories"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_id = db.Column(db.Integer, unique=True, nullable=False)
    stat_short_name = db.Column(db.String(128), unique=False, nullable=False)
    stat_full_name = db.Column(db.String(128), unique=False, nullable=False)
    stat_modifier = db.Column(db.String(128), unique=False, nullable=False)

    def __init__(self, category_id, stat_short_name, stat_full_name, stat_modifier):
        self.category_id = category_id
        self.stat_short_name = stat_short_name
        self.stat_full_name = stat_full_name
        self.stat_modifier = stat_modifier

    @classmethod
    def get_stat_name_by_id(cls, stat_id):
        return cls.query.filter_by(category_id=stat_id).first().stat_short_name

    @classmethod
    def get_stat_id_by_name(cls, stat_name):
        return cls.query.filter_by(stat_short_name=stat_name).first().category_id

    @classmethod
    def get_stat_modifier_by_name(cls, stat_name):
        return cls.query.filter_by(stat_short_name=stat_name).first().stat_modifier

    @classmethod
    def get_stat_modifier_by_id(cls, cat_id):
        return cls.query.filter_by(category_id=cat_id).first().stat_modifier

    def to_json(self):
        return {
            'id': self.id,
            'statistic_id': self.statistic_id,
            'stat_short_name': self.stat_short_name,
            'stat_full_name': self.stat_full_name,
            'stat_modifier': self.stat_modifier
        }
