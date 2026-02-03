


---

##  Step 1 — Add Your Code to GitHub

### If you *haven’t* added files yet …

In your local project folder (the one with `game.py` and assets), run:

```bash
git init
git add .
git commit -m "Initial commit - OpenGL Assignment 2"
git branch -M main
git remote add origin https://github.com/kashishjoshi13/opengl_assingnment2.git
git push -u origin main
```

This will upload your code to the currently empty repo.

---

##  Step 2 — Add a Good README

A good **README.md** gives context to your project — what it is, how to run it, and why it’s cool. Projects with well-written READMEs are easier to understand and more impressive.([arXiv][2])

Here’s a **ready-to-paste README** for your game:

````markdown
# OpenGL Assignment 2 — 2D Platformer Game

A 2D platformer game built in Python using OpenGL as part of a Computer Graphics course.

##  About the Game

This project implements:
- Player movement and gravity
- Collision detection with clouds/platforms
- Enemy interaction and physics
- Key and door mechanics
- Camera movement and shaders

##  How to Run

Make sure you have Python installed, then install dependencies:

```bash
pip install PyOpenGL PyOpenGL_accelerate numpy
````

Then run the game:

```bash
python game.py
```

## Features

* Smooth player movement
* Level design using objects & clouds
* Key collection and door unlocking
* Collision physics
* Camera follow on player

## Controls

* `W / Up`: Jump
* `A / Left`: Move left
* `D / Right`: Move right
* `Esc`: Quit

##  Structure

```
game.py
assets/
utils/
...
```

## 📌
Author

👤
**Kashish Joshi**
GitHub: [https://github.com/kashishjoshi13](https://github.com/kashishjoshi13)

````

---

## 📌
 Step 3 — Push README to GitHub

Save it as `README.md` in your project folder, then:

```bash
git add README.md
git commit -m "Add README"
git push
````

---

---



