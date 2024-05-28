import pygame


class Pipe(pygame.sprite.Sprite):
    def __init__(
        self, position: pygame.Vector2, velocity: pygame.Vector2, sprite: pygame.Surface
    ) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.position: pygame.Vector2 = position
        self.velocity: pygame.Vector2 = velocity
        self.image: pygame.Surface = sprite

        self.rect: pygame.Rect = self.image.get_rect(topleft=self.position)

    def update(self, delta_time: float) -> None:
        # Pipe movement right to left
        self.position.x -= self.velocity.x * delta_time
        self.rect.x = self.position.x
