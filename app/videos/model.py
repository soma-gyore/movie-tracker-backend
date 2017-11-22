from application import db


users_videos = db.Table(
    'users_videos',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id', ondelete="CASCADE")),
    db.Column('video_id', db.Integer, db.ForeignKey('videos.id', ondelete="CASCADE"))
)


class Video(db.Model):
    __tablename__ = 'videos'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    close_date = db.Column(db.DateTime, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    last_position = db.Column(db.Integer, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    children = db.relationship("User", secondary=users_videos)

    def __init__(self, close_date, title, last_position, duration):
        self.close_date = close_date
        self.title = title
        self.last_position = last_position
        self.duration = duration
