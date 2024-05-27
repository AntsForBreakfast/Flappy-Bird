from random import randint

import pygame

from assets_manager import AssetsManager
from state_machine import StateMachine, State
from score_counter import ScoreCounter
from assets.objects.pipe import Pipe
from assets.objects.bird import Bird
from assets.objects.platform import Platform


class Game(State):
    def __init__(
        self, state_machine: StateMachine, assets_manager: AssetsManager
    ) -> None:
        self.state_machine: StateMachine = state_machine
        self.assets_manager: AssetsManager = assets_manager

        self.pipe_gap: pygame.Vector2 = pygame.math.Vector2(100, 100)
        self.score_counter = ScoreCounter(sprites=self.assets_manager.sprites["digits"])

        # Sprites
        self.sprite_backgroud_day: pygame.Surface = self.assets_manager.sprites[
            "background-day"
        ]
        self.sprites_pipe: dict[str : pygame.Surface] = self.assets_manager.sprites[
            "pipes"
        ]
        self.sprites_bird: dict[str : dict[str : pygame.Surface]] = (
            self.assets_manager.sprites["birds"]
        )
        self.sprite_platform: pygame.Surface = self.assets_manager.sprites["base"]

        # Objects
        self.pipe_group: pygame.sprite.Group = pygame.sprite.Group()
        _platform_1 = Platform(
            position=pygame.math.Vector2(0, 400),
            sprite=self.sprite_platform,
            velocity=pygame.math.Vector2(100, 0),
        )
        _platform_2 = Platform(
            position=pygame.math.Vector2(self.sprite_platform.get_width(), 400),
            sprite=self.sprite_platform,
            velocity=pygame.math.Vector2(100, 0),
        )
        self.platform_group: pygame.sprite.Group = pygame.sprite.Group(
            (_platform_1, _platform_2)
        )
        self.collision_group: pygame.sprite.Group = pygame.sprite.Group()
        self.bird = Bird(sprites=self.sprites_bird["blue"])

        # Test
        self.game_state = "running"

    def process_event(self, event: pygame.Event) -> None:
        self.bird.process_event(event=event)

    def update(self, delta_time: float) -> None:
        screen = pygame.display.get_surface().get_rect()

        self.pipe_group.update(delta_time=delta_time)
        self.platform_group.update(delta_time=delta_time)

        # For first launching since the pipe_group is empty
        try:
            last_pipe_fully_visible = (
                list(self.pipe_group)[-1].rect.right + self.pipe_gap.x < screen.right
            )
        except IndexError:
            last_pipe_fully_visible = 1

        if len(self.pipe_group) == 0 or last_pipe_fully_visible:
            sprite_pipe = self.sprites_pipe["green"]
            min_h = sprite_pipe.get_height()
            max_h = screen.h - sprite_pipe.get_height()

            pipe_obj_1 = Pipe(
                position=pygame.math.Vector2(screen.w, randint(max_h, min_h)),
                velocity=pygame.math.Vector2(100, 0),
                sprite=sprite_pipe,
            )

            pipe_2_h = pipe_obj_1.rect.top - min_h - self.pipe_gap.y
            pipe_obj_2 = Pipe(
                position=pygame.math.Vector2(screen.w, pipe_2_h),
                velocity=pygame.math.Vector2(100, 0),
                sprite=pygame.transform.flip(
                    surface=sprite_pipe, flip_x=False, flip_y=True
                ),
            )

            self.pipe_group.add([pipe_obj_1, pipe_obj_2])

        removed = 0
        for pipe in self.pipe_group:
            if pipe.rect.right <= 0:
                self.pipe_group.remove(pipe)
                removed += 1
        self.score_counter.add_to_counter(round(removed / 2))

        self.collision_group = pygame.sprite.Group(
            (self.platform_group, self.pipe_group)
        )

        # Bird logic
        self.bird.update(delta_time=delta_time)

        if pygame.sprite.spritecollideany(sprite=self.bird, group=self.collision_group):
            self.game_state = "Lost"

        self.score_counter.update()

    def render(self, screen: pygame.Surface) -> None:
        screen.blit(self.sprite_backgroud_day, (0, 0))

        self.pipe_group.draw(surface=screen)
        self.score_counter.render(screen=screen)
        self.bird.render(screen=screen)
        self.platform_group.draw(surface=screen)
