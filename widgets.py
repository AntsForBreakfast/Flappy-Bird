import pygame


class ScoreCounter:
    def __init__(self, sprites: dict[str : pygame.Surface]) -> None:
        # Parameters
        self.sprites: dict[str : pygame.Surface] = sprites

        # Attributes
        self.counter: int = 0
        self.position: pygame.Vector2 = pygame.math.Vector2(0, 20)
        self.sprite_size: pygame.Vector2 = pygame.math.Vector2(
            self.sprites["0"].get_size()
        )
        self.counter_surface: pygame.Surface = pygame.Surface((0, 0))

    def add_to_counter(self, digit: int = 1) -> None:
        self.counter += digit

    def update(self) -> None:
        screen_rect = pygame.display.get_surface().get_rect()

        # Center counter, center changes by the digit number
        self.position.x = screen_rect.centerx - (
            self.sprite_size.x * len(str(self.counter)) / 2
        )

        # Create counter surface
        counter_width = self.sprite_size.x * len(str(self.counter))
        counter_height = self.sprite_size.y
        self.counter_surface = pygame.Surface((counter_width, counter_height))

        # Positioning digits on counter surface
        counter_rect = self.counter_surface.get_rect()
        for n in str(self.counter):
            sprite = self.sprites[n]
            self.counter_surface.blit(sprite, counter_rect)
            counter_rect.x += 24

    def render(self, screen: pygame.Surface) -> None:
        screen.blit(self.counter_surface, self.position)
