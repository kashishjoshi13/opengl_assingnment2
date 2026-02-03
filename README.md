
---

#  OpenGL Assignment 2 — 2D Platformer Game

A 2D platformer game built using **Python + OpenGL** as part of a Computer Graphics assignment.

This project demonstrates real-time rendering, object transformations, collision physics, camera handling, shaders, and gameplay logic such as **key–door unlocking** and **cloud/platform collisions**.

---

##  Game Features

*  Player movement with gravity and jumping
*  Collision detection with clouds (platforms)
*  Enemy interaction
*  Key collection and door unlocking mechanic
*  Camera that follows the player
*  Shader-based rendering
*  Object-oriented game structure

---

##  Controls

| Key          | Action     |
| ------------ | ---------- |
| A            | Move Left  |
| D            | Move Right |
| W / Up Arrow | Jump       |
| ESC          | Exit Game  |

---

##  Tech Used

* Python
* OpenGL (PyOpenGL)
* NumPy
* Custom shaders
* Object and camera abstractions

---

##  Project Structure

```
game.py                # Main game loop and logic
assets/
   ├── shaders/        # Vertex & fragment shaders
   └── objects/        # Object property definitions
utils/
   ├── graphics.py     # Object, Camera, Shader classes
```

---

##  How to Run

### 1️ Install dependencies

```bash
pip install PyOpenGL PyOpenGL_accelerate numpy
```

### 2️ Run the game

```bash
python game.py
```

---

##  Gameplay Logic Implemented

* Platform (cloud) collision physics
* Gravity and velocity based motion
* State-based game progression
* Key pickup detection
* Door unlock condition
* Enemy and player interaction
* Scene update using delta time

---

## Academic Context

This project was developed as part of a **Computer Graphics OpenGL Assignment** to demonstrate understanding of:

* Rendering pipeline
* Transformations
* Shader usage
* Real-time interaction
* Physics simulation in games

---

##  Author

**Kashish Joshi**
GitHub: [https://github.com/kashishjoshi13](https://github.com/kashishjoshi13)

---

## Notes

This is an academic assignment focused on learning OpenGL concepts through game development.
