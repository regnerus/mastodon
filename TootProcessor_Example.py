'''NLTK Downloads only need to be executed once!'''

import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

from TootProcessor import TootProcessor

toot = '<p>Some early thoughts on Fort Triumph, the tactical RPG with interactive environments. <a href="https://www.gamingonlinux.com/articles/some-early-thoughts-on-fort-triumph-the-tactical-rpg-with-interactive-environments.11849" rel="nofollow noopener" target="_blank"><span class="invisible">https://www.</span><span class="ellipsis">gamingonlinux.com/articles/som</span><span class="invisible">e-early-thoughts-on-fort-triumph-the-tactical-rpg-with-interactive-environments.11849</span></a> <a href="https://mastodon.social/tags/earlyaccess" class="mention hashtag" rel="nofollow noopener" target="_blank">#<span>EarlyAccess</span></a> <a href="https://mastodon.social/tags/strategy" class="mention hashtag" rel="nofollow noopener" target="_blank">#<span>Strategy</span></a> <a href="https://mastodon.social/tags/steam" class="mention hashtag" rel="nofollow noopener" target="_blank">#<span>Steam</span></a> <a href="https://mastodon.social/tags/rpg" class="mention hashtag" rel="nofollow noopener" target="_blank">#<span>RPG</span></a></p>'

processor = TootProcessor(lemmatize_words = True, remove_duplicates = False)

processor.processToot(toot)