import pygame


class Bird:
    def __init__(self, sprites: dict[str : pygame.Surface]) -> None:
        # Parameters
        self.sprites: list[pygame.Surface] = list(sprites.values())

        # Attributes
        self.GRAVITY: float = 1000
        self.FLAP_FORCE: int = 300
        self.velocity_bird: float = 0
        self.animation_speed: float = 8
        self.animation_index: int = 0
        self.angle_bird = 0
        self.rotation_velocity = 150

        self.position_bird: pygame.Vector2 = pygame.math.Vector2(20, 200)
        self.sprite: pygame.Surface = self.sprites[self.animation_index]
        self.rect: pygame.Rect = self.sprite.get_rect(center=self.position_bird)

    def animate(self, delta_time) -> None:
        self.animation_index += self.animation_speed * delta_time
        self.animation_index %= len(self.sprites)
        self.sprite = self.sprites[int(self.animation_index)]

    def rotating(self, delta_time: float) -> None:
        min_angle, max_angle = 60, -90
        self.angle_bird -= self.rotation_velocity * delta_time
        self.angle_bird = min(min_angle, max(self.angle_bird, max_angle))
        self.sprite = pygame.transform.rotate(self.sprite, self.angle_bird)

    def flap(self) -> None:
        self.velocity_bird = -self.FLAP_FORCE
        self.angle_bird = 60

    def falling(self, delta_time: float) -> None:
        self.position_bird.y += self.velocity_bird * delta_time
        self.velocity_bird += self.GRAVITY * delta_time

    def process_event(self, event: pygame.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.flap()

    def update(self, delta_time: float) -> None:
        self.falling(delta_time=delta_time)
        self.rotating(delta_time=delta_time)
        self.animate(delta_time=delta_time)

        # Updating the bird center position
        self.rect = self.sprite.get_rect(center=self.position_bird)

    def render(self, screen: pygame.Surface) -> None:
        screen.blit(self.sprite, self.rect)
