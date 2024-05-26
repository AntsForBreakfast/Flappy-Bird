import pygame


class Bird:
    def __init__(self, sprites: dict[str : pygame.Surface]) -> None:
        self.sprites: list[pygame.Surface] = list(sprites.values())
        self.position: pygame.Vector2 = pygame.math.Vector2(20, 200)

        self.GRAVITY: float = 1000
        self.FLAP_FORCE: int = 300
        self.velocity: float = 0

        self.animation_speed: float = 8
        self.animation_index: int = 0
        self.sprite: pygame.Surface = self.sprites[self.animation_index]
        self.rect: pygame.Rect = self.sprite.get_rect(center=self.position)

        self.angle = 0
        self.rotation_velocity = 150

    def animate(self, delta_time):
        self.animation_index += self.animation_speed * delta_time
        self.animation_index %= len(self.sprites)
        self.sprite = self.sprites[int(self.animation_index)]
        self.sprite = pygame.transform.rotate(self.sprite, self.angle)

    def rotating(self, delta_time: float):
        if self.angle > -90:
            self.angle -= self.rotation_velocity * delta_time

    def flap(self):
        self.velocity = -self.FLAP_FORCE
        self.angle = 60

    def falling(self, delta_time: float):
        self.position.y += self.velocity * delta_time
        self.velocity += self.GRAVITY * delta_time

    def process_event(self, event: pygame.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.flap()

    def update(self, delta_time: float) -> None:
        self.falling(delta_time=delta_time)
        self.rotating(delta_time=delta_time)
        self.animate(delta_time=delta_time)
        self.rect = self.sprite.get_rect(center=self.position)

    def render(self, screen: pygame.Surface) -> None:
        screen.blit(self.sprite, self.rect)
