from mastodon import Mastodon, StreamListener
import getpass
import os.path
import time

# Register app - only once!

if not os.path.isfile('pytooter_clientcred.secret'):
    Mastodon.create_app(
         'pytooterapp',
         api_base_url = 'https://mastodon.utwente.nl',
         to_file = 'pytooter_clientcred.secret'
    )


# Log in - either every time, or use persisted
mastodon = Mastodon(
    client_id = 'pytooter_clientcred.secret',
    api_base_url = 'https://mastodon.utwente.nl'
)


if not os.path.isfile('pytooter_usercred.secret'):
    passwd = getpass.getpass("password: ")
    mastodon.log_in(
        'g.meijer@student.utwente.nl',
        passwd,
        to_file = 'pytooter_usercred.secret'
    )




# Create actual API instance
mastodon = Mastodon(
    client_id = 'pytooter_clientcred.secret',
    access_token = 'pytooter_usercred.secret',
    api_base_url = 'https://mastodon.utwente.nl'
)

class Tootbot(StreamListener):
    def __init__(self, mastodon_api):
        super().__init__()
        self.mastodon_api = mastodon_api

    def on_notification(self, notification):
        if 'type' in notification and notification['type'] == 'follow':
            print(notification['account']['acct'] + " has followed you!")
            self.mastodon_api.status_post("Hey @%s, this is an automatic message to thank you for following me!"%notification['account']['acct'])

mastodon.stream_user(Tootbot(mastodon))

