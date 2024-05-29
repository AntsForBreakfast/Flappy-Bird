from dataclasses import dataclass
from abc import ABC, abstractmethod

import pygame

from assets_manager import AssetsManager


@dataclass
class State(ABC):
    state: "StateMachine"

    def switch(self, state: "State"):
        self.state.state = state(self)

    @abstractmethod
    def process_event(self, event: pygame.Event) -> None: ...

    @abstractmethod
    def update(self) -> None: ...

    @abstractmethod
    def render(self, screen: pygame.Surface) -> None: ...


class StateMachine:
    def __init__(self, starting_state: State, assets_manager: AssetsManager):
        self.assets_manager: AssetsManager = assets_manager
        self.state = starting_state(
            state_machine=self, assets_manager=self.assets_manager
        )

    def switch(self, state: State) -> None:
        self.state = state(self, self.assets_manager)

    def process_event(self, event: pygame.Event) -> None:
        self.state.process_event(event=event)

    def update(self, delta_time: float) -> int:
        running = self.state.update(delta_time)
        return running

    def render(self, screen: pygame.Surface) -> None:
        screen.fill("black")
        self.state.render(screen=screen)
