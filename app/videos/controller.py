from datetime import datetime


class VideoController(object):
    def __init__(self):
        self.video_object = None
        self.video_dict = {}

    def user_object_to_dict(self):
        self.video_dict = {
            "id": self.video_object.id,
            "closeDate": self.video_object.close_date,
            "title": self.video_object.title,
            "lastPosition": self.video_object.last_position,
            "duration": self.video_object.duration
        }

    @staticmethod
    def create_video(video_dict, user_obj):
        from .model import Video
        from application import db

        new_video_obj = Video(
            datetime.fromtimestamp(video_dict["closeTimeStamp"]),
            video_dict["title"],
            video_dict["lastPosition"],
            video_dict["duration"]
        )

        new_video_obj.children.append(user_obj)

        db.session.add(new_video_obj)
        db.session.commit()

    @staticmethod
    def delete_videos():
        from .model import Video
        from application import db

        Video.query.delete()
        db.session.commit()

    @staticmethod
    def video_obj_to_dict(video_obj):
        video_dict = {
            'closeDate': video_obj.close_date,
            'title': video_obj.title,
            'lastPosition': video_obj.last_position,
            'duration': video_obj.duration
        }
        return video_dict

    @staticmethod
    def get_videos_by_username(username):
        from .model import Video
        from app.authentication.model import User
        video_objs = Video.query.filter(Video.children).filter(User.username == username).all()
        return [VideoController.video_obj_to_dict(video_obj) for video_obj in video_objs]
