from datetime import datetime
from .image_scraper import ImageScraper


class VideoController(object):
    def __init__(self):
        self.video_object = None
        self.video_dict = {}
        self.image_scraper = ImageScraper()

    def create_video(self, video_dict, user_obj):
        from .model import Video
        from application import db

        new_video_obj = Video(
            datetime.fromtimestamp(video_dict["closeTimeStamp"]),
            video_dict["title"],
            video_dict["lastPosition"],
            video_dict["duration"],
            self.image_scraper.get_first_hit(video_dict["title"])
        )

        try:
            new_video_obj.children.append(user_obj)
            db.session.add(new_video_obj)
            db.session.commit()
        except:
            print("Fatal error")

    @staticmethod
    def delete_videos():
        from .model import Video
        from application import db

        try:
            Video.query.delete()
            db.session.commit()
        except:
            print("Fatal error")

    @staticmethod
    def video_obj_to_dict(video_obj):
        video_dict = {
            'imageUrl': video_obj.image_url,
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

        try:
            video_objs = Video.query.filter(Video.children).filter(User.username == username).all()
            return [VideoController.video_obj_to_dict(video_obj) for video_obj in video_objs]
        except:
            print("Fatal error")
