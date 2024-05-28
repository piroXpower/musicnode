from MahakMusic.core.bot import Anony
from MahakMusic.core.dir import dirr
from MahakMusic.core.git import git
from MahakMusic.core.userbot import Userbot
from MahakMusic.misc import dbb, heroku

from .logging import LOGGER

dirr()
git()
dbb()
heroku()

app = Anony()
userbot = Userbot()


from .platforms import *

Apple = AppleAPI()
Carbon = CarbonAPI()
SoundCloud = SoundAPI()
Spotify = SpotifyAPI()
Resso = RessoAPI()
Telegram = TeleAPI()
YouTube = YouTubeAPI()
