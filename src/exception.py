class InstantiateApiError:
    def __init__(self, message='InstantiateApiError: несуществующий video_id'):
        self.message = message
        raise Exception(self.message)
