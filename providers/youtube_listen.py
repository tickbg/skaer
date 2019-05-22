import os
import requests


class YouTubeListenProvider(object):

    def __init__(self):
        self._language = 'en'
        self._region = 'BG'
        self._max_results = 50
        self.req_headers = {
            'Host': 'www.googleapis.com',
            'User-Agent': 'Mozilla/5.0 Firefox/66.0',
            'Accept-Encoding': 'gzip, deflate'
        }
        self.api_url = 'https://www.googleapis.com/youtube/v3/'

    def get_info(self):
        """ Public API call. """
        return {
            'name'        : 'YouTube Listen',
            'description' : 'Media provider to listen youtube music content',
            'cover_image' : 'http://localhost:8080/res/images/y-music.jpeg',
            'category'    : 'Music'
        }

    def entries(self):
        """ Public API call,
            return all entries (popular music videos and user's playlists). """

        plists = self._v3_get_request(path='playlists',
                                      params={
                                         'part': 'snippet',
                                         'mine': 'true',
                                         'maxResults': str(self._max_results),
                                         'hl': self._language}
                                     )
        # Merge results from the popular music videos and user's playlists.
        max_results = self._max_results - plists['pageInfo']['totalResults']
        items, total_res, next_page = self._get_popular_music_videos(max_results=max_results)
        for pl in plists['items']:
            print(pl)
            items.append({
                    'id': pl['id'],
                    'title': pl['snippet']['title'],
                    'url': pl['snippet']['thumbnails']['medium']['url'],
                    'type': 'playlist item'
                    })
        return items


    def search(self, q, search_type=['video', 'channel', 'playlist'],
               channel_id='', order='relevance', safe_search='moderate',
               page_token=''):
        """
        Public API call,
        Returns a collection of search results that match the query parameters.
        By default, a search result set identifies matching 
        video, channel, and playlist resources.
        One can also configure queries to only retrieve a specific type of resource.
        :param q: search string.
        :param search_type: acceptable values: 'video' | 'channel' | 'playlist'.
        :param channel_id: limit search to channel id
        :param order: one of: 'date', 'rating', 'relevance',
                              'title', 'videoCount', 'viewCount'
        :param safe_search: one of: 'moderate', 'none', 'strict'
        :param page_token: can be ''
        :return:

        """
        # prepare search type
        if not search_type:
            search_type = ''
        if isinstance(search_type, list):
            search_type = ','.join(search_type)

        # prepare page token
        if not page_token:
            page_token = ''

        # prepare params
        params = {
            'q': q,
            'part': 'snippet',
            'regionCode': self._region,
            'hl': self._language,
            'relevanceLanguage': self._language,
            'maxResults': str(self._max_results)
        }
        if search_type:
            params['type'] = search_type
        if channel_id:
            params['channelId'] = channel_id
        if order:
            params['order'] = order
        if safe_search:
            params['safeSearch'] = safe_search
        if page_token:
            params['pageToken'] = page_token

        video_only_params = [
            'eventType', 'videoCaption', 'videoCategoryId', 'videoDefinition',
            'videoDimension', 'videoDuration', 'videoEmbeddable', 'videoLicense',
            'videoSyndicated', 'videoType', 'relatedToVideoId', 'forMine'
        ]
        for key in video_only_params:
            if params.get(key) is not None:
                params['type'] = 'video'
                break
        res = self.v3_get_request(path='search', params=params)
        return res


    def _v3_get_request(self, headers=None, path=None, params=None):
        access_token = os.environ.get('access_token', '')
        req_params = { 'access_token': access_token }
        if params:
            req_params.update(params)
        req_headers = self.req_headers
        url = self.api_url + path.strip('/')
        if headers:
            req_headers.update(headers)
        r = requests.get(url, params=req_params, headers=req_headers)
        assert r.status_code == requests.codes.ok
        if r.headers.get('content-type', '').startswith('application/json'):
            return r.json()
        else:
            return r.content.decode('utf-8')

    def _get_music_category_id(self):
        params = {
            'part': 'snippet',
            'regionCode': self._region,
            'hl': 'en'
        }
        json_result = self._v3_get_request(path='videoCategories',
                                                  params=params)
        for item in json_result['items']:
            if item['snippet']['title'].startswith('Music'):
                category_id = int(item['id'])
                break
        return category_id

    def _get_popular_music_videos(self, page_token=None, max_results=None):
        """
        Returns a list of the most popular music videos for that region.
        :param page_token: fetch a concrete page
        :max_results: max results to return
        :return play items, total results, next page token:
        """
        category_id = self._get_music_category_id()
        if max_results:
            maxres = max_results
        else:
            maxres = self._max_results

        params = {
            'part': 'snippet',
            'maxResults': str(maxres),
            'regionCode': self._region,
            'hl': self._language,
            'videoCategoryId': category_id,
            'chart': 'mostPopular'
        }
        if page_token:
            params['pageToken'] = page_token
        res = self._v3_get_request(path='videos', params=params)
        if 'nextPageToken' in res:
            next_page = res['nextPageToken']
        else:
            next_page = None

        play_items = []
        for item in res['items']:
            play_items.append({
                        'id': item['id'],
                        'title': item['snippet']['title'],
                        'url': item['snippet']['thumbnails']['medium']['url'],
                        'type': 'music item'
                    })
        return play_items, res['pageInfo']['totalResults'], next_page


