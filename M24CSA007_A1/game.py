import numpy as np
import ast

from utils.graphics import Object, Camera, Shader
from assets.shaders.shaders import object_shader
from assets.objects.objects import (
    playerProps, enemyProps, entryProps, exitProps,
    backgroundProps2, sunProps, cloudprops,
    keyProps, doorprops
)


class Game:
    def __init__(self, height, width):
        self.height = height
        self.width = width

        # Game state
        self.state = "GAME"
        self.screen = 0
        self._level_initialized = False

        # Rendering
        self.camera = Camera(height, width)
        self.shaders = [Shader(object_shader["vertex_shader"], object_shader["fragment_shader"])]

        # Gameplay vars
        self.player_health = 100
        self.player_lives = 3
        self.collect_key_check = [False] * 7  # Tracks which keys are collected

        # Task 4 & 5 tracking
        self.chuck_visible = True
        self.game_over_scene = False

        # time tracking
        self.elapsed_time = 0.0
        self._hud_print_accum = 0.0

        # physics flags
        self.is_on_platform = False

        # Physics tuning
        self.GRAVITY = 150.0           
        self.JUMP_V = 260.0
        self.MOVE_V = 140.0

        # Collision sizing heuristic
        self.BASE_UNIT = 10.0          
        self.key_points = 0


    # -----------------------------
    # Level init
    # -----------------------------
    def InitScreen(self, reset_keys=False):
        if reset_keys:
            self.collect_key_check = [False] * 7

        self.chuck_visible = True
        self.game_over_scene = False

        # Background & static props
        self.bg = Object(self.shaders[0], backgroundProps2)
        self.sun = Object(self.shaders[0], sunProps)

        # Entry / Exit
        self.entry = Object(self.shaders[0], entryProps)
        self.entry.properties["position"] = np.array([-460, 320, 0], dtype=np.float32)

        self.exit = Object(self.shaders[0], exitProps)
        self.exit.properties["position"] = np.array([460, -280, 0], dtype=np.float32)

        # Doors (Task 4)
        self.entrydoor = Object(self.shaders[0], doorprops)
        self.entrydoor.properties["position"] = self.entry.properties["position"] + np.array([0, 0, 20], dtype=np.float32)
        self.entrydoor_origin_x = self.entrydoor.properties["position"][0]

        self.exitdoor = Object(self.shaders[0], doorprops)
        self.exitdoor.properties["position"] = self.exit.properties["position"] + np.array([0, 0, 20], dtype=np.float32)
        self.exitdoor_origin_x = self.exitdoor.properties["position"][0]

        self.entry_closed_x = self.entrydoor.properties["position"][0]
        self.entry_open_x = self.entry_closed_x - 70
        self.entry_opening = True   # open at start so Chuck can come out

        self.exit_closed_x = self.exitdoor.properties["position"][0]
        self.exit_open_x = self.exit_closed_x - 70
        self.exit_opening = False


        # Player
        self.player = Object(self.shaders[0], playerProps)
        self.player.properties["position"] = self.entry.properties["position"] + np.array([0.0, 0.0, -50], dtype=np.float32)
        self.player.properties["velocity"] = np.array([0.0, 0.0, 0.0], dtype=np.float32)


        # Clouds + Keys
        self.cloud = []
        self.keys = []
        for i in range(7):
            cl = Object(self.shaders[0], cloudprops)
            cl.properties["position"] = np.array(
                [
                    (-self.width / 2) + (i + 1) * (self.width / 8),
                    (self.height / 2) - (self.height / 8) * (i + 1),
                    0,
                ],
                dtype=np.float32,
            )
            cl.properties["scale"] = np.array([2, 2, 1], dtype=np.float32)
            cl.properties["velocity"] = np.array([0, 125 + 4 * i, 0], dtype=np.float32)
            self.cloud.append(cl)

            key = Object(self.shaders[0], keyProps)
            # place key exactly on cloud top
            cloud_half_h = 0.5 * self.BASE_UNIT * float(cl.properties["scale"][1])
            key.properties["position"] = cl.properties["position"] + np.array([0, cloud_half_h + 5, 15], dtype=np.float32)

            key.properties["scale"] = np.array([3, 3, 1], dtype=np.float32)

            # If key was already collected in this level session, hide it
            if self.collect_key_check[i]:
                key.properties["scale"] = np.array([0, 0, 0], dtype=np.float32)

            self.keys.append(key)

        # Enemies
        self.enemies = []
        for _ in range(5):
            ene = Object(self.shaders[0], enemyProps)
            ene.properties["position"] = np.array(
                [
                    np.random.uniform(-(self.width / 2) + 200, (self.width / 2) - 200),
                    np.random.uniform(-self.height / 2 + 100, self.height / 2 - 100),
                    50,
                ],
                dtype=np.float32,
            )
            ene.properties["velocity"] = np.array([0.0, 0.0, 0.0], dtype=np.float32)
            self.enemies.append(ene)

        self._level_initialized = True

    # -----------------------------
    # Save / Load
    # -----------------------------
    def save_game(self):
        state_data = {
            "screen": int(self.screen),
            "player_lives": int(self.player_lives),
            "player_health": int(self.player_health),
            "collect_key_check": list(self.collect_key_check),
            "elapsed_time": float(self.elapsed_time),
        }
        with open("savegame.txt", "w") as f:
            f.write(repr(state_data))
        print("Saved game -> savegame.txt")

    def load_game(self):
        try:
            with open("savegame.txt", "r") as f:
                data = ast.literal_eval(f.read())

            self.screen = int(data.get("screen", 0))
            self.player_lives = int(data.get("player_lives", 3))
            self.player_health = int(data.get("player_health", 100))
            self.collect_key_check = list(data.get("collect_key_check", [False] * 7))
            self.elapsed_time = float(data.get("elapsed_time", 0.0))

            self.state = "GAME"
            self._level_initialized = False
            print("Loaded game from savegame.txt")

        except Exception as e:
            print("Load game failed:", e)

    # -----------------------------
    # Core loop
    # -----------------------------
    def ProcessFrame(self, inputs, time_dict):
        dt = time_dict["deltaTime"]

        if "1" in inputs:
            self.save_game()
        if "2" in inputs:
            self.load_game()

        if not self._level_initialized:
            self.InitScreen(reset_keys=False)

        if not hasattr(self, "player") or not hasattr(self, "bg"):
            self._level_initialized = False
            self.InitScreen(reset_keys=False)

        self.elapsed_time += dt

        self.UpdateScene(inputs, time_dict)
        self.DrawScene()
        self._print_hud_to_console(dt)

    def _print_hud_to_console(self, dt):
        self._hud_print_accum += dt
        if self._hud_print_accum >= 1.0:
            self._hud_print_accum = 0.0
            print(
                f"Lives={self.player_lives} | Health={self.player_health} | "
                f"Level={self.screen+1} | Keys={sum(self.collect_key_check)} | "
                f"Time={self.elapsed_time:.1f}s"
            )

    def _clamp_player_x_only(self):
        pos = self.player.properties["position"]
        pos[0] = np.clip(pos[0], -self.width / 2, self.width / 2)
        self.player.properties["position"] = pos


    def getAABB(self, obj):
        pos = obj.properties["position"]
        scale = obj.properties["scale"]

        half_w = 0.5 * self.BASE_UNIT * float(scale[0])
        half_h = 0.5 * self.BASE_UNIT * float(scale[1])

        left = pos[0] - half_w
        right = pos[0] + half_w
        bottom = pos[1] - half_h
        top = pos[1] + half_h

        return left, right, bottom, top


    # -----------------------------
    # Gameplay update
    # -----------------------------
    def UpdateScene(self, inputs, time_dict):
        if self.game_over_scene: return # Stop updates if game over
        dt = time_dict["deltaTime"]

        # Horizontal movement
        self.player.properties["velocity"][0] = 0.0
        if "A" in inputs:
            self.player.properties["velocity"][0] = -self.MOVE_V
        if "D" in inputs:
            self.player.properties["velocity"][0] = self.MOVE_V

        player_pos = self.player.properties["position"]
        player_vel = self.player.properties["velocity"]
        player_half_w = 0.5 * self.BASE_UNIT * float(self.player.properties["scale"][0])
        player_half_h = 0.5 * self.BASE_UNIT * float(self.player.properties["scale"][1])
        player_bottom = float(player_pos[1]) - player_half_h


        # -----------------------------
        # TASK 1: Cliff Steady Logic
        # -----------------------------
        self.is_on_platform = False
        
        # Left Cliff steady check
        if player_pos[0] < -350:
            self.is_on_platform = True
            player_pos[1] = 320 + player_half_h # entry height
            player_vel[1] = 0.0
        # Right Cliff steady check
        elif player_pos[0] > 350:
            self.is_on_platform = True
            player_pos[1] = -280 + player_half_h # exit height
            player_vel[1] = 0.0

        # -----------------------------
        # TASK 4: Door Animations
        # -----------------------------
        door_speed = 220 * dt
        player_x = player_pos[0]

        # -------- ENTRY DOOR --------
        entry_x = self.entrydoor.properties["position"][0]

        if self.entry_opening:
            if entry_x > self.entry_open_x:
                self.entrydoor.properties["position"][0] -= door_speed
            else:
                self.player.properties["position"][2] = 50
                if player_x > -380:
                    self.entry_opening = False
        else:
            if entry_x < self.entry_closed_x:
                self.entrydoor.properties["position"][0] += door_speed

        # -------- EXIT DOOR --------
        exit_x = self.exitdoor.properties["position"][0]

        if player_x > 400:
            self.exit_opening = True

        if self.exit_opening:
            if exit_x > self.exit_open_x:
                self.exitdoor.properties["position"][0] -= door_speed
            else:
                if player_x > 440:
                    self.player.properties["position"][2] = -200
                    self.exit_opening = False
                    self.game_over_scene = True
        else:
            if exit_x < self.exit_closed_x:
                self.exitdoor.properties["position"][0] += door_speed

        # -----------------------------
        # TASK 3: Clouds update + settle
        # -----------------------------
        for cloud in self.cloud:
            # 1. Move Cloud
            if cloud.properties["position"][1] > (self.height / 2) - 100 or \
               cloud.properties["position"][1] < (-self.height / 2) + 100:
                cloud.properties["velocity"][1] *= -1

            cloud.properties["position"] += cloud.properties["velocity"] * dt
            
            cloud_half_h = 0.5 * self.BASE_UNIT * float(cloud.properties["scale"][1])
            
            # 2. Make Keys Follow Cloud
            for key in self.keys:
                 if abs(key.properties["position"][0] - cloud.properties["position"][0]) < 5:
                      key.properties["position"] = cloud.properties["position"] + np.array([0, cloud_half_h + 5, 15], dtype=np.float32)

            # 3. Collision / Settle
            c_left, c_right, c_bottom, c_top = self.getAABB(cloud)
            p_left, p_right, p_bottom, p_top = self.getAABB(self.player)

            # Check overlap + falling + close enough to top
            if (p_right > c_left and 
                p_left < c_right and 
                player_vel[1] <= 0 and 
                p_bottom >= c_top - 15 and 
                p_bottom <= c_top + 25):

                self.is_on_platform = True
                
                # SNAP to top to prevent sinking
                player_pos[1] = c_top + player_half_h
                player_vel[1] = 0.0

        # -----------------------------
        # TASK 3: Key collection (CORRECTED)
        # -----------------------------
        for i in range(len(self.keys)):
            # If already collected, skip checking collision
            if self.collect_key_check[i]:
                continue

            key = self.keys[i]
            k_left, k_right, k_bottom, k_top = self.getAABB(key)
            p_left, p_right, p_bottom, p_top = self.getAABB(self.player)

            if (p_right > k_left and 
                p_left < k_right and 
                p_top > k_bottom and 
                p_bottom < k_top):

                # Update the persistent checklist
                self.collect_key_check[i] = True
                
                # Update simple points counter
                self.key_points += 1
                
                # Hide the key visually
                key.properties["scale"] = np.array([0, 0, 0], dtype=np.float32)

        # Gravity & Jump
        if not self.is_on_platform:
            player_vel[1] -= self.GRAVITY * dt
        if self.is_on_platform and "SPACE" in inputs:
            player_vel[1] = self.JUMP_V

        self.player.properties["position"] += self.player.properties["velocity"] * dt
        self._clamp_player_x_only()

        # OOB/Death Fall
        if self.player.properties["position"][1] < (-self.height / 2) - 200:
            self.player_lives -= 1
            self.player_health = 100
            self.player.properties["position"] = self.entry.properties["position"] + np.array([0.0, 0.0, 50], dtype=np.float32)
            self.player.properties["velocity"][:] = 0.0
            if self.player_lives <= 0:
                self._reset_game()

        # Enemy Hit
        for enemy in self.enemies:
            if np.linalg.norm(self.player.properties["position"] - enemy.properties["position"]) < 100:
                self.player_health -= 10
                if self.player_health <= 0:
                    self.player_lives -= 1
                    self.player_health = 100
                    self.player.properties["position"] = self.entry.properties["position"] + np.array([0.0, 0.0, 50], dtype=np.float32)
                    self.player.properties["velocity"][:] = 0.0
                    if self.player_lives <= 0:
                        self._reset_game()

        # Transition Logic
        if np.linalg.norm(self.player.properties["position"] - self.exit.properties["position"]) < 40:
            # Check collected keys using the boolean list sum
            if sum(self.collect_key_check) >= 3:
                self._next_level()

    def _reset_game(self):
        print("GAME OVER")
        self.player_lives = 3
        self.player_health = 100
        self.collect_key_check = [False] * 7
        self._level_initialized = False

    def _next_level(self):
        if self.screen < 2:
            self.screen += 1
            self.collect_key_check = [False] * 7
            self._level_initialized = False
            print(f"Moved to Level {self.screen+1}")
        else:
            print("YOU WON!")
            self.screen = 0
            self.collect_key_check = [False] * 7
            self._level_initialized = False

    # -----------------------------
    # Draw (Modified for Task 4 & 5)
    # -----------------------------
    def DrawScene(self):
        if self.game_over_scene:
            import OpenGL.GL as gl
            gl.glClearColor(0, 0, 0, 1) # Task 5: Empty scene
            gl.glClear(gl.GL_COLOR_BUFFER_BIT)
            return

        for shader in self.shaders:
            self.camera.Update(shader)

        self.bg.Draw()
        self.sun.Draw()
        self.entry.Draw()
        self.exit.Draw()
        self.entrydoor.Draw()
        self.exitdoor.Draw()
        
        if self.chuck_visible: # Task 4 ii
            self.player.Draw()

        for cl in self.cloud:
            cl.Draw()
        for ene in self.enemies:
            ene.Draw()
        for key in self.keys:
            key.Draw()