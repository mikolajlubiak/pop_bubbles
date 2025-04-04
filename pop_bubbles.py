import pyxel

SCREEN_WIDTH = 256
SCREEN_HEIGHT = 256

MAX_BUBBLE_SPEED = 2.0
NUM_INIT_BUBBLES = 50
NUM_EXPLODE_BUBBLES = 8


class Vec2:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y


class Bubble:
    def __init__(self) -> None:
        self.r = pyxel.rndf(3, 10)

        self.pos = Vec2(
            pyxel.rndf(self.r, SCREEN_WIDTH - self.r),
            pyxel.rndf(self.r, SCREEN_HEIGHT - self.r),
        )

        self.vel = Vec2(
            pyxel.rndf(-MAX_BUBBLE_SPEED, MAX_BUBBLE_SPEED),
            pyxel.rndf(-MAX_BUBBLE_SPEED, MAX_BUBBLE_SPEED),
        )

        self.color = pyxel.rndi(1, 15)

    def update(self):
        self.pos.x += self.vel.x
        self.pos.y += self.vel.y

        #        next_pos = Vec2(
        #            self.pos.x + self.vel.x,
        #            self.pos.y + self.vel.y,
        #        )
        #
        #        if next_pos.x - self.r < 0 or next_pos.x + self.r > SCREEN_WIDTH:
        #            self.vel.x *= -1.0
        #
        #        if next_pos.y - self.r < 0 or next_pos.y + self.r > SCREEN_HEIGHT:
        #            self.vel.y *= -1.0

        if self.vel.x < 0 and self.pos.x < self.r:
            self.vel.x *= -1
        if self.vel.x > 0 and self.pos.x > SCREEN_WIDTH - self.r:
            self.vel.x *= -1
        if self.vel.y < 0 and self.pos.y < self.r:
            self.vel.y *= -1
        if self.vel.y > 0 and self.pos.y > SCREEN_HEIGHT - self.r:
            self.vel.y *= -1

    def draw(self):
        pyxel.circ(self.pos.x, self.pos.y, self.r, self.color)


class App:
    def __init__(self) -> None:
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="POP BUBBLES")
        pyxel.mouse(True)

        self.is_exploded = False
        self.bubbles = [Bubble() for _ in range(NUM_INIT_BUBBLES)]

        pyxel.run(self.update, self.draw)

    def clicked_bubble(self):
        for i in range(len(self.bubbles)):
            bubble = self.bubbles[i]

            dx = bubble.pos.x - pyxel.mouse_x
            dy = bubble.pos.y - pyxel.mouse_y

            if (dx * dx + dy * dy) < (bubble.r * bubble.r):
                return i

        return None

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        num_bubbles = len(self.bubbles)

        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            idx = self.clicked_bubble()

            if idx:
                bubble = self.bubbles[idx]
                self.is_exploded = True
                new_r = pyxel.sqrt(bubble.r * bubble.r / NUM_EXPLODE_BUBBLES)

                for j in range(NUM_EXPLODE_BUBBLES):
                    angle = 360 * j / NUM_EXPLODE_BUBBLES

                    new_bubble = Bubble()
                    new_bubble.r = new_r

                    new_bubble.pos.x = bubble.pos.x + (bubble.r + new_r) * pyxel.cos(
                        angle
                    )

                    new_bubble.pos.y = bubble.pos.y + (bubble.r + new_r) * pyxel.sin(
                        angle
                    )

                    new_bubble.vel.x = pyxel.cos(angle) * MAX_BUBBLE_SPEED
                    new_bubble.vel.y = pyxel.sin(angle) * MAX_BUBBLE_SPEED

                    self.bubbles.append(new_bubble)

                self.bubbles.pop(idx)

        if pyxel.btn(pyxel.MOUSE_BUTTON_RIGHT):
            idx = self.clicked_bubble()

            if idx:
                bubble = self.bubbles[idx]

                dx = bubble.pos.x - pyxel.mouse_x
                dy = bubble.pos.y - pyxel.mouse_y

                bubble.vel.x = -dx
                bubble.vel.y = -dy

        for i in range(num_bubbles - 1, -1, -1):
            bi = self.bubbles[i]
            bi.update()

            for j in range(i - 1, -1, -1):
                bj = self.bubbles[j]
                dx = bi.pos.x - bj.pos.x
                dy = bi.pos.y - bj.pos.y
                total_r = bi.r + bj.r

                if (dx * dx + dy * dy) < total_r:
                    new_bubble = Bubble()
                    new_bubble.r = pyxel.sqrt(bi.r * bi.r + bj.r * bj.r)

                    new_bubble.pos.x = (bi.pos.x * bi.r + bj.pos.x * bj.r) / total_r
                    new_bubble.pos.y = (bi.pos.y * bi.r + bj.pos.y * bj.r) / total_r

                    new_bubble.vel.x = (bi.vel.x * bi.r + bj.vel.x * bj.r) / total_r
                    new_bubble.vel.y = (bi.vel.y * bi.r + bj.vel.y * bj.r) / total_r

                    self.bubbles.append(new_bubble)

                    self.bubbles.pop(i)
                    self.bubbles.pop(j)
                    num_bubbles -= 1
                    break

    def draw(self):
        pyxel.cls(0)

        for bubble in self.bubbles:
            bubble.draw()

        if not self.is_exploded and pyxel.frame_count % 20 < 10:
            pyxel.text(80, 50, "CLICK BUBBLES (RPM OR LPM)", pyxel.frame_count % 15 + 1)


App()
