import pygame

from state_machine import StateMachine, State
from assets_manager import AssetsManager


class GameOver(State):
    def __init__(
        self, state_machine: StateMachine, assets_manager: AssetsManager
    ) -> None:
        self.state_machine: StateMachine = state_machine
        self.assets_manager: AssetsManager = assets_manager

    def process_event(self, event: pygame.Event) -> None: ...

    def update(self, delta_time: float) -> None: ...

    def render(self, screen: pygame.Surface) -> None: ...
