import pygame

from assets_manager import AssetsManager
from state_machine import State, StateMachine
from states import game
from assets.objects.platform import Platform


class Menu(State):
    def __init__(
        self, state_machine: StateMachine, assets_manager: AssetsManager
    ) -> None:
        # Parameters
        self.state_machine: StateMachine = state_machine
        self.assets_manager: AssetsManager = assets_manager

        # Attributes
        _rect_screen: pygame.Rect = pygame.display.get_surface().get_rect()
        self.sprite_backgroud_day: pygame.Surface = self.assets_manager.sprites.get(
            "background-day"
        )
        self.sprite_message: pygame.Surface = self.assets_manager.sprites.get("message")
        self.rect_sprite_message: pygame.Rect = self.sprite_message.get_rect(
            center=_rect_screen.center
        )

        self.platform = Platform(
            position=pygame.math.Vector2(0, 400),
            sprite=self.assets_manager.sprites.get("base"),
        )

    def process_event(self, event: pygame.Event) -> None:
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.state_machine.switch(state=game.Game)

    def update(self, delta_time: float) -> int:
        return 1

    def render(self, screen: pygame.Surface) -> None:
        screen.blit(self.sprite_backgroud_day, (0, 0))
        self.platform.render(screen=screen)
        screen.blit(self.sprite_message, self.rect_sprite_message)
