from OpenGL.GL import *
from utils.window_manager import Window
from game import Game

class App:
    def __init__(self, width, height):
        self.window = Window(height, width)
        glClearColor(0, 0, 0, 1)
        self.game = Game(height, width)

    def RenderLoop(self):
        while self.window.IsOpen():
            inputs, time = self.window.StartFrame(0.2, 0.2, 0.2, 1.0)
            self.game.ProcessFrame(inputs, time)
            glDisable(GL_DEPTH_TEST)
            self.window.EndFrame()
        self.window.Close()

if __name__ == "__main__":
    app = App(1000, 1000)
    app.RenderLoop()
