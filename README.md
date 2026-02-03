

# CSL7450 — Computer Graphics Assignment 2

## 2D Game using PyOpenGL (Chuck Platformer)

This project is a 2D platformer game developed using Python and PyOpenGL as part of CSL7450: Computer Graphics under Dr. Hardik Jain.

The game is inspired by the Angry Birds character Chuck, who must travel from the left cliff to the right cliff using clouds as platforms while avoiding Bad Piggies, collecting keys, and interacting with cave doors.

Assignment details are taken directly from the official problem statement. 

---

## Assignment Objective

Chuck starts from a cave on the left cliff and must reach the cave on the right cliff by:

* Landing on clouds (platforms)
* Avoiding Bad Piggies
* Collecting keys placed on clouds
* Interacting correctly with cave doors
* Ending the game with a Game Over screen

---

## Tasks Given in Assignment and What I Implemented

### 1. Fix Chuck Falling from the Cliff (Gravity Issue)

Problem: Chuck was falling due to gravity even when standing on the cliff.
Fix Implemented:

* Checked Chuck’s x-coordinate with respect to cliff width
* Stopped gravity effect when Chuck is on the cliff surface
* Stabilized Chuck’s position on both cliffs

---

### 2. Fix Bad Piggies Color

Problem: Piggies were red instead of green.
Fix Implemented:

* Modified object color property in pig object definition
* Rendered piggies correctly in green color

---

### 3. Cloud Collision and Key Collection Logic

#### (i) Chuck not settling on clouds

Problem: Bounding box collision with clouds was incorrect.
Fix Implemented:

* Corrected bounding box interaction between Chuck and clouds
* Adjusted y-position when collision happens from top
* Prevented Chuck from passing through clouds

#### (ii) Key not disappearing after collection

Problem: Key remained visible after collection.
Fix Implemented:

* Detected collision between Chuck and key
* Removed that key object from render list
* Increased key score counter

---

### 4. Door Open–Close Logic for Caves

Problem: Doors were flying away instead of behaving like doors.

Fix Implemented using Model Matrix (translation):

* Left Cave:

  * Door opens (moves left)
  * Chuck comes out
  * Door closes back to original position

* Right Cave:

  * Door opens when Chuck reaches
  * Chuck enters cave and disappears (z-coordinate logic or skip draw)
  * Door closes

---

### 5. Game Over Scene

Problem: No proper ending after Chuck reaches right cave.
Fix Implemented:

* Once Chuck disappears into right cave
* Screen clears to an empty scene indicating Game Over

---

## Controls

| Key    | Action     |
| ------ | ---------- |
| A      | Move Left  |
| D      | Move Right |
| W / Up | Jump       |
| ESC    | Exit       |

---

## Concepts Applied

* OpenGL Rendering Pipeline
* Shader usage
* Model transformation matrices
* Bounding box collision detection
* Gravity and velocity physics using delta time
* Camera following player
* Object-oriented game structure

---

## Project Structure

```
game.py
assets/
   ├── shaders/
   └── objects/
utils/
   └── graphics.py
```

---

## How to Run

```bash
pip install PyOpenGL PyOpenGL_accelerate numpy
python game.py
```

---

## Deliverables Covered

* Neat documentation (this README)
* Working game demonstration
* Complete code structure as required

---

## Author

Kashish Joshi
GitHub: [https://github.com/kashishjoshi13](https://github.com/kashishjoshi13)

---

This project helped me practically understand collision handling, transformations, shader-based rendering, and game physics inside an OpenGL environment.
