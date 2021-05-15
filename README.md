Super Giulio Bros Vol.30
=============

INSTALLATION GUIDE:

Download SGB folder. Copy commands below into Terminal.

1. xcode-select --install
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
2. brew install sdl2 sdl2_gfx sdl2_image sdl2_mixer sdl2_net sdl2_ttf
3. brew install Caskroom/cask/xquartz
4. brew install python@3.8
5. Go to SGB folder
6. python3.8 -m venv .venv; source .venv/bin/activate
7. pip install -r requirements.txt

RUN CODE:
1. Go to SGB folder
2. source .venv/bin/activate ## if virtual environment not active
3. python3.8 sgb.py
