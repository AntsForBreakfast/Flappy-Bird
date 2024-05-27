import pygame


class Platform(pygame.sprite.Sprite):
    def __init__(
        self,
        position: pygame.Vector2,
        sprite: pygame.Surface,
        velocity: pygame.Vector2 = pygame.math.Vector2(0, 0),
    ) -> None:
        pygame.sprite.Sprite.__init__(self)
        # Parameters
        self.position: pygame.Vector2 = position
        self.velocity: pygame.Vector2 = velocity
        self.image: pygame.Surface = sprite

        # Attributes
        self.rect: pygame.FRect = self.image.get_frect(topleft=self.position)

    def update(self, delta_time: float) -> None:
        self.rect.x -= self.velocity.x * delta_time

        # Changing platform pos if out of screen
        screen_width = pygame.display.get_surface().get_width()
        if self.rect.right <= 0:
            self.rect.x = screen_width

    def render(self, screen: pygame.Surface) -> None:
        screen.blit(self.image, self.rect)
