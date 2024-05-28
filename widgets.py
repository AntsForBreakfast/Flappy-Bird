import pygame

type rgb = tuple[int, int, int]


class Button:
    def __init__(
        self,
        text: str,
        font: pygame.Font,
        position: pygame.Vector2,
        size: pygame.Vector2,
        elevation: int,
        text_color: rgb,
        bg_color: rgb,
        shadow_color: rgb,
        method: callable,
    ) -> None:
        self.text: str = text
        self.font: pygame.Font = font
        self.position: pygame.Vector2 = position
        self.size: pygame.Vector2 = size
        self.elevation: int = elevation
        self.text_color: rgb = text_color
        self.bg_color: rgb = bg_color
        self.shadow_color: rgb = shadow_color
        self.method: callable = method

        self.pressed: bool = False
        self.dynamic_elevation: int = elevation

        self.top_rect: pygame.Rect = pygame.Rect((0, 0), self.size).move_to(
            center=self.position
        )

        self.bottom_rect: pygame.Rect = pygame.Rect(
            self.top_rect.topleft,
            (self.size.x, self.elevation),
        )

        self.text_surface = self.font.render(
            text=self.text, antialias=True, color=self.text_color
        )
        self.text_rect = self.text_surface.get_rect(center=self.top_rect.center)

    def process_event(self, event: pygame.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.top_rect.collidepoint(event.pos):
                self.pressed = True
                self.dynamic_elevation = 0
        elif event.type == pygame.MOUSEBUTTONUP:
            if (
                event.button == 1
                and self.top_rect.collidepoint(event.pos)
                and self.pressed
            ):
                self.method()
            self.pressed = False
            self.dynamic_elevation = self.elevation

    def update(self) -> None:
        # Elevation logic
        self.top_rect.y = self.position.y - self.dynamic_elevation
        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation

        self.text_rect.center = self.top_rect.center

    def render(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(
            surface=screen,
            color=self.shadow_color,
            rect=self.bottom_rect,
            border_radius=2,
        )
        pygame.draw.rect(
            surface=screen, color=self.bg_color, rect=self.top_rect, border_radius=2
        )

        screen.blit(source=self.text_surface, dest=self.text_rect)


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
