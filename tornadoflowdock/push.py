from  tornado.httpclient import HTTPRequest, AsyncHTTPClient
import json

class Flow(object):
    def __init__(self, id, token, external_user_name=None):
        self.id = id
        self.token = token
        self.external_user_name = external_user_name
        self.http_client = AsyncHTTPClient()

    def _post(self, push_type, body, callback=None):
        request = HTTPRequest("https://api.flowdock.com/v1/messages/%s/%s" % (push_type, self.token), **{
            'headers': {
                'Content-Type': 'application/json'
            },
            'method': "POST",
            'body':  json.dumps(body)
        })

        self.http_client.fetch(request, callback)

    def chat(self, content, external_user_name=None, callback=None, message_id=None, tags=None):
        self._post("chat", {
            'event': 'message',
            'content': content,
            'external_user_name': external_user_name or self.external_user_name,
            'message_id': message_id,
            'tags': tags or []
        }, callback=callback)

    def team_inbox(self, source, from_address, subject, content, from_name=None, reply_to=None, project=None, format=None, callback=None, tags=None, link=None):
        self._post("team_inbox", {
            'source': source,
            'from_address': from_address,
            'subject': subject,
            'content': content,
            'from_name': from_name,
            'reply_to': reply_to,
            'project': project,
            'format': format,
            'tags': tags or [],
            'link': link,
        }, callback=callback)
