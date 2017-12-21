from OpenGL.GL import *
import glfw
from gameobjects import Platform, Background, Ball, Heart
from shader import Shader


class Window:
    TITLE = 'Catch the ball'
    WIDTH = 1280
    HEIGHT = 720
    MAX_FAIL = 5
    game_status_play = True
    fails = 0
    score = 0

    def reshape(self, window, width, height):
        angle = 85
        width, height = glfw.get_framebuffer_size(window)
        aspect_ratio = width / height
        self.ball.shader.use()
        self.ball.prep(self.ball.shader, aspect_ratio, 0.5, angle)

        self.platform.shader.use()
        self.platform.prep(self.platform.shader, aspect_ratio, 1.0, angle)

        for i in range(0, self.MAX_FAIL):
            self.hearts[i].shader.use()
            self.hearts[i].prep(self.hearts[i].shader, aspect_ratio, 0.3, angle)


        self.bg.shader.use()
        self.bg.prep(self.bg.shader, aspect_ratio, 11.0, angle)
        glViewport(0, 0, width, height)

    def __init__(self):
        if not glfw.init():
            return

        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 2)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)

        window = glfw.create_window(self.WIDTH, self.HEIGHT, self.TITLE, None, None)
        glfw.set_window_size_limits(window, 320, 480, glfw.DONT_CARE, glfw.DONT_CARE)
        if not window:
            glfw.terminate()
            return

        glfw.make_context_current(window)
        glfw.set_key_callback(window, self.key_callback)
        glfw.set_window_size_callback(window, self.reshape)

        width, height = glfw.get_framebuffer_size(window)
        glViewport(0, 0, width, height)
        aspect_ratio = width / height


        glClearColor(0.2, 0.3, 0.2, 1.0)
        glEnable(GL_DEPTH_TEST)

        self.ball = Ball('resources/tkan.jpg')
        ball_shader = Shader('shaders/vs.shader', 'shaders/fs.shader')
        self.ball.prep(ball_shader, aspect_ratio, 0.5, 85)

        self.platform = Platform('resources/yachik3.jpg')
        shader = Shader('shaders/vs.shader', 'shaders/fs.shader')
        self.platform.prep(shader, aspect_ratio, 1.0, 85)

        self.hearts = []
        for i in range(0, self.MAX_FAIL):
            heart = Heart([-3.0 + i * 0.5, 5.5, 0.0])
            heart_shader = Shader('shaders/vs', 'shaders/fs')
            heart.prep(heart_shader, aspect_ratio, 0.3, 85)
            self.hearts.append(heart)

        self.bg = Background('resources/bg-doski.jpg')
        bg_shader = Shader('shaders/vs.shader', 'shaders/fs.shader')
        self.bg.prep(bg_shader, aspect_ratio, 11.0, 85)

        while not glfw.window_should_close(window):
            glClearColor(0.0, 0.3, 0.3, 1.0)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            glDisable(GL_DEPTH_TEST)
            self.bg.draw()
            glEnable(GL_DEPTH_TEST)

            self.platform.draw(self.game_status_play)
            self.ball.draw(self.game_status_play)

            if self.collision_detect():
                if self.fails == self.MAX_FAIL:
                    self.game_status_play = False

            for heart in self.hearts:
                heart.draw()

            glfw.swap_buffers(window)
            glfw.poll_events()

        glfw.terminate()

    def key_callback(self, window, key, scancode, action, mode):
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(window, GL_TRUE)

        if key == glfw.KEY_SPACE and action == glfw.PRESS:
            self.reset_game(self.ball)

        if key == glfw.KEY_A:
            if action == glfw.PRESS:
                glfw.set_time(0)
                self.platform.curr_movement = self.platform.LEFT
            elif action == glfw.RELEASE:
                self.platform.curr_movement = self.platform.STOP
        if key == glfw.KEY_D:
            if action == glfw.PRESS:
                glfw.set_time(0)
                self.platform.curr_movement = self.platform.RIGHT
            elif action == glfw.RELEASE:
                self.platform.curr_movement = self.platform.STOP

    def reset_game(self, item):
        self.score = 0
        self.fails = 0
        self.game_status_play = True
        item.random_pos()
        item.speed = item.INITIAL_SPEED
        for heart in self.hearts:
            heart.pos[1] = 5.5

    def collision_detect(self):
        platform_edges = [self.platform.pos[0] - 0.5 * self.platform.scale, self.platform.pos[0] + 0.5 * self.platform.scale]
        item_edges = [self.ball.pos[0] - 0.5 * self.ball.scale, self.ball.pos[0] + 0.5 * self.ball.scale]
        if self.ball.pos[1]-0.5*self.ball.scale < self.platform.pos[1]+0.5*self.platform.scale:
            self.ball.random_pos()
            self.ball.speed = self.ball.speed * 1.1
            if item_edges[0] >= platform_edges[0] and item_edges[1] <= platform_edges[1]:
                self.score += 1
            else:
                self.fails += 1
                self.hearts[self.MAX_FAIL - self.fails].pos[1] = 20.0
            return True
        return False

if __name__ == '__main__':
    app = Window()
