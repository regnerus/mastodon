from mastodon import Mastodon
import getpass
import os.path

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
mastodon.toot('Tooting (again) from python using #mastodonpy !')
