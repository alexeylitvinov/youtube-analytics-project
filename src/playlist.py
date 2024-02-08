import isodate

from src.channel import Channel
import datetime


class PlayList:
    def __init__(self, playlist_id):
        self.__playlist_id = playlist_id
        self.__playlist = Channel.get_service().playlists().list(id=self.__playlist_id, part='snippet').execute()
        self.title = self.__playlist['items'][0]['snippet']['title']
        self.url = 'https://www.youtube.com/playlist?list=' + self.__playlist_id
        self.__playlist_item = Channel.get_service().playlistItems().list(playlistId=self.__playlist_id,
                                                                          part='contentDetails').execute()

    @property
    def playlist_id(self):
        return self.__playlist_id

    def get_list_video_id(self):
        """Формирование списка из id video по id плейлиста"""
        video_ids = [video['contentDetails']['videoId'] for video in self.__playlist_item['items']]
        return video_ids

    @property
    def video_response(self):
        """Запрос по списку из id video, возвращаем словарь со всеми данными видео"""
        video_response = Channel.get_service().videos().list(part='contentDetails,statistics',
                                                             id=','.join(self.get_list_video_id())
                                                             ).execute()
        return video_response

    @property
    def total_duration(self):
        """Общее время продолжительности всех видео из плейлиста"""
        time_list = []
        for video in self.video_response['items']:
            iso_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_duration)
            time_list.append(duration)
        return sum(time_list, datetime.timedelta())

    def show_best_video(self):
        """Лучшее видео в плейлисте"""
        all_videos = {}
        for video in self.video_response['items']:
            all_videos[int(video['statistics']['likeCount'])] = video['id']
        return f'https://youtu.be/{all_videos[max(all_videos)]}'
