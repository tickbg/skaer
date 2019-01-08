
class YesMoviesProvider(object):

    def __init__(self, app):
        self._app = app

    def get_info(self):
        return { 'description' : 'YesMovies media provider',
                 'cover_image' : 'images/yes-movies.jpg',
                 'category'    : 'Video' }