# Not your father's roguelike

[![GitHub license](https://img.shields.io/github/license/mikolasan/pyroguelike)](https://github.com/mikolasan/pyroguelike/blob/master/LICENSE)

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/be99136b390a43e395e917190831647c)](https://www.codacy.com/manual/SaturdaysCode/pyroguelike/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=mikolasan/pyroguelike&amp;utm_campaign=Badge_Grade)
[![Maintainability](https://api.codeclimate.com/v1/badges/ec7ad611258839e926a7/maintainability)](https://codeclimate.com/github/mikolasan/pyroguelike/maintainability)

## Install

`Pygame` on **Arch / Manjaro**

```
sudo pacman -S python-pygame
```

`Pygame` in all other cases (**Ubuntu, Windows**, etc)

```
pip install pygame==1.9.6
```

Then install other dependencies

```
pip install -r requirements.txt
```

_Note_: `Pygame` is not included into requirements, because of specifics of Repl.it service when `Pygame` is selected as a framework.

## Run

```
python main.py
```

## Release

```
pip install pyinstaller
pyinstaller main.py
```

---

### Controls

* Movements: `w` `a` `s` `d` - move a hero up, left, down, or right
* Use mouse pointer and left button to shoot (when you have ammo).
* Dialog system: `Enter` - to select your answer, `w`/`s` - up and down to choose another answer.

### Game Intro

What a day it had been!

Jeff got fired from Burger Queen restaurant today.
This week he needs to pay mortgage loan for her grandmother house and for cable TV just before a baseball season.

Considering all this stuff together Jeff decides to go to a bar.
To watch the first game, drink some beer and think about future and where to get some cash.
Collect $500 or more this night and life will become less miserable.

### Preview

<img src="https://storage.googleapis.com/replit/images/1555560839579_d796ad540bdb72f9e5c95849ee6c2aa8.pn" width="500">

*Screen 1 - Jeff talks with barman Joe*

<img src="https://storage.googleapis.com/replit/images/1555560839888_fe9969e4ad98ab91f1e49d33ed248827.pn" width="500">

*Screen 2 - Clearing a base from strange yellow creatures with red eyes*

[![YouTube video is better than thousand screens](http://img.youtube.com/vi/VqfjrGS7Ukw/0.jpg)](https://www.youtube.com/watch?v=VqfjrGS7Ukw)

*Screenplay (with music!)*


### About Repl.it Gam Jam

I'd like to share my experience with pygame on [replit](https://repl.it/@stakanmartini/test-roguelike-11)
with other programmers. Here are my notes I made when started with this project.
They boosted my productivity with this project in the platform usage.

* Stop button usually does not work. To restart code with new changes use Ctrl+Enter. Make sure focus in the code editor.
* Also try Ctrl+C in console window.
* If first methods do not help, close a browser tab and open repl.it, go to your dashboard and open project again.
* Sometimes it still displays window from previous start or do not display an app at all.
  It happened to me when the package manager (pip) tells you who is the boss. Then fork a project.
  When I discovered that method I finished with 11 forks of my game.
* You cannot open just a game in new tab using *.run link. You have to play with editor layout a whole day.
* I recommend to run your app in fullscreen mode to prevent from clicking on close and minimize buttons of the app window
* Linter tells you about every whitespace error and very often covers real syntax errors.
  Do you know that there is auto-format button near to "saved" status?
  I want an option to make it automatic on save (merge it with my habit to press Ctrl+S every minute)
* pdb module does not work. I tried pdb_clone and it worked.
* Do not remove file if it is currently opened.


## Building community 

Ask me anything, leave a comment, suggest incredible feature

[![Gitter](https://badges.gitter.im/pyroguelike/community.svg)](https://gitter.im/pyroguelike/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)
[![YouTube](https://img.shields.io/badge/video-YouTube-critical)](https://www.youtube.com/watch?v=VqfjrGS7Ukw)
[![GitHub issues](https://img.shields.io/github/issues/mikolasan/pyroguelike)](https://github.com/mikolasan/pyroguelike/issues)
