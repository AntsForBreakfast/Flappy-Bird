import pygame

from assets_manager import AssetsManager
from state_machine import State, StateMachine
from states.game import Game


class Menu(State):
    def __init__(
        self, state_machine: StateMachine, assets_manager: AssetsManager
    ) -> None:
        self.state_machine: StateMachine = state_machine
        self.assets_manager: AssetsManager = assets_manager

        # Sprites
        self.sprite_backgroud_day: pygame.Surface = self.assets_manager.sprites.get(
            "background-day"
        )
        self.sprite_base: pygame.Surface = self.assets_manager.sprites.get("base")
        self.sprite_message: pygame.Surface = self.assets_manager.sprites.get("message")

        # Sprites positions
        self.rect_screen: pygame.Rect = pygame.display.get_surface().get_rect()
        self.rect_sprite_base: pygame.Rect = self.sprite_base.get_rect().move(0, 400)
        self.rect_sprite_message: pygame.Rect = self.sprite_message.get_rect(
            center=self.rect_screen.center
        )

    def process_event(self, event: pygame.Event) -> None:
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.state_machine.switch(Game)

    def update(self, delta_time: float) -> None:
        pass

    def render(self, screen: pygame.Surface) -> None:
        screen.blit(self.sprite_backgroud_day, (0, 0))
        screen.blit(self.sprite_base, self.rect_sprite_base)
        screen.blit(self.sprite_message, self.rect_sprite_message)
