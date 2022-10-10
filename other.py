import pygame

TILESIZE = 24


class Snake(pygame.sprite.Sprite):
    images = None

    def __init__(self, grp, pos, length, parent=None):
        super().__init__(grp)
        self.parent = parent
        self.child = None
        self.direction = "N"

        if not self.parent:
            self.image = Snake.images["HEAD_N"]
        elif length == 1:
            self.image = Snake.images["TAIL_N"]
        else:
            self.image = Snake.images["BODY_NN"]

        self.pos = pos
        self.rect = self.image.get_rect(
            x=self.pos[0] * TILESIZE, y=self.pos[1] * TILESIZE
        )
        if length > 1:
            self.child = Snake(grp, (pos[0], pos[1] + 1), length - 1, self)

    def move(self):
        # if we have a parent, let's look were it moves
        parent_direction = self.parent.direction if self.parent else None

        if self.direction == "N":
            self.pos = self.pos[0], self.pos[1] - 1
        elif self.direction == "S":
            self.pos = self.pos[0], self.pos[1] + 1
        elif self.direction == "E":
            self.pos = self.pos[0] - 1, self.pos[1]
        elif self.direction == "W":
            self.pos = self.pos[0] + 1, self.pos[1]

        self.rect = self.image.get_rect(
            x=self.pos[0] * TILESIZE, y=self.pos[1] * TILESIZE
        )

        # move the child
        if self.child:
            self.child.move()

        if not self.parent:
            self.image = Snake.images["HEAD_" + self.direction]
        elif not self.child:
            self.image = Snake.images["TAIL_" + parent_direction]
        else:
            self.image = Snake.images["BODY_" + parent_direction + self.direction]

        # follow the parent
        if parent_direction:
            self.direction = parent_direction

    def update(self):
        # no parent means we're the head of the snake
        # and we should move we a key is pressed
        if not self.parent:
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_w]:
                self.direction = "N"
            if pressed[pygame.K_s]:
                self.direction = "S"
            if pressed[pygame.K_a]:
                self.direction = "E"
            if pressed[pygame.K_d]:
                self.direction = "W"


def build_images():
    load = lambda part: pygame.image.load(part + ".png").convert_alpha()
    parts = ("head", "body", "tail", "L")
    head_img, body_img, tail_img, l_img = [load(p) for p in parts]

    return {
        "HEAD_N": head_img,
        "HEAD_S": pygame.transform.rotate(head_img, 180),
        "HEAD_E": pygame.transform.rotate(head_img, 90),
        "HEAD_W": pygame.transform.rotate(head_img, -90),
        "BODY_NN": body_img,
        "BODY_SS": body_img,
        "BODY_WW": pygame.transform.rotate(body_img, 90),
        "BODY_EE": pygame.transform.rotate(body_img, 90),
        "BODY_NE": pygame.transform.rotate(l_img, 180),
        "BODY_WS": pygame.transform.rotate(l_img, 180),
        "BODY_WN": pygame.transform.rotate(l_img, 90),
        "BODY_SE": pygame.transform.rotate(l_img, 90),
        "BODY_ES": pygame.transform.rotate(l_img, -90),
        "BODY_NW": pygame.transform.rotate(l_img, -90),
        "BODY_EN": pygame.transform.rotate(l_img, 0),
        "BODY_SW": pygame.transform.rotate(l_img, 0),
        "TAIL_N": tail_img,
        "TAIL_S": pygame.transform.rotate(tail_img, 180),
        "TAIL_E": pygame.transform.rotate(tail_img, 90),
        "TAIL_W": pygame.transform.rotate(tail_img, -90),
    }


def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 480))
    Snake.images = build_images()

    # let's trigger the MOVE event every 500ms
    MOVE = pygame.USEREVENT + 1
    pygame.time.set_timer(MOVE, 500)

    all_sprites = pygame.sprite.Group()
    snake = Snake(all_sprites, (4, 4), 8)
    clock = pygame.time.Clock()
    dt = 0
    while True:
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                return
            if e.type == MOVE:
                snake.move()

        screen.fill((30, 30, 30))

        all_sprites.update()
        all_sprites.draw(screen)

        dt = clock.tick(60)
        pygame.display.flip()


main()
