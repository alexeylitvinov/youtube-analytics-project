from src.channel import Channel


class Video:
    def __init__(self, video_id):
        self.video_id = video_id
        self.video = Channel.get_service().videos().list(part='snippet,statistics', id=self.video_id).execute()
        self.title = self.video['items'][0]['snippet']['title']
        self.url = 'https://www.youtube.com/watch?v=' + self.video_id
        self.video_count = self.video['items'][0]['statistics']['viewCount']
        self.like_count = self.video['items'][0]['statistics']['likeCount']

    def __str__(self):
        return f'{self.title}'


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id
        self.playlist = Channel.get_service().playlistItems().list(playlistId=self.playlist_id,
                                                                   part='snippet',
                                                                   videoId=self.video_id).execute()
        self.title = self.playlist['items'][0]['snippet']['title']
