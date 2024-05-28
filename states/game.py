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
        # Parameters
        self.state_machine: StateMachine = state_machine
        self.assets_manager: AssetsManager = assets_manager

        # Attributes
        self.screen_rect: pygame.Rect = pygame.display.get_surface().get_rect()
        self.pipe_gap: pygame.Vector2 = pygame.math.Vector2(100, 100)

        self.sprite_backgroud_day: pygame.Surface = self.assets_manager.sprites[
            "background-day"
        ]
        self.sprites_pipe: dict[str : pygame.Surface] = self.assets_manager.sprites[
            "pipes"
        ]
        sprites_bird: dict[str : dict[str : pygame.Surface]] = (
            self.assets_manager.sprites["birds"]
        )
        sprite_platform: pygame.Surface = self.assets_manager.sprites["base"]
        sprites_digit: dict[str : pygame.Surface] = self.assets_manager.sprites[
            "digits"
        ]

        # Groups
        self.pipe_group: pygame.sprite.Group = pygame.sprite.Group()
        self.collision_group: pygame.sprite.Group = pygame.sprite.Group()
        _platform_1 = Platform(
            position=pygame.math.Vector2(0, 400),
            sprite=sprite_platform,
            velocity=pygame.math.Vector2(100, 0),
        )
        _platform_2 = Platform(
            position=pygame.math.Vector2(sprite_platform.get_width(), 400),
            sprite=sprite_platform,
            velocity=pygame.math.Vector2(100, 0),
        )
        self.platform_group: pygame.sprite.Group = pygame.sprite.Group(
            (_platform_1, _platform_2)
        )

        # Objects
        self.bird = Bird(sprites=sprites_bird["blue"])
        self.score_counter = ScoreCounter(sprites=sprites_digit)

        # Initalizing
        self.add_pipes_to_group()

        # Test
        self.game_state = "running"

    def add_pipes_to_group(self) -> None:
        sprite_pipe = self.sprites_pipe["green"]
        min_h = sprite_pipe.get_height()
        max_h = self.screen_rect.h - sprite_pipe.get_height()

        pipe_obj_1 = Pipe(
            position=pygame.math.Vector2(self.screen_rect.w, randint(max_h, min_h)),
            velocity=pygame.math.Vector2(100, 0),
            sprite=sprite_pipe,
        )

        pipe_2_h = pipe_obj_1.rect.top - min_h - self.pipe_gap.y
        pipe_obj_2 = Pipe(
            position=pygame.math.Vector2(self.screen_rect.w, pipe_2_h),
            velocity=pygame.math.Vector2(100, 0),
            sprite=pygame.transform.flip(
                surface=sprite_pipe, flip_x=False, flip_y=True
            ),
        )

        self.pipe_group.add([pipe_obj_1, pipe_obj_2])

    def remove_pipes_from_group(self) -> None:
        for pipe in self.pipe_group:
            if pipe.rect.right <= 0:
                self.pipe_group.remove(pipe)

    def process_event(self, event: pygame.Event) -> None:
        self.bird.process_event(event=event)

    def update(self, delta_time: float) -> None:
        # Updating groups
        self.pipe_group.update(delta_time=delta_time)
        self.platform_group.update(delta_time=delta_time)

        # Add new pipe
        grp_sprites = self.pipe_group.sprites()
        if grp_sprites[-1].rect.right + self.pipe_gap.x < self.screen_rect.right:
            self.add_pipes_to_group()

        # Removes all the pipes of the screen
        self.remove_pipes_from_group()

        # Creating group for collision checking with a bird
        self.collision_group = pygame.sprite.Group(
            (self.platform_group, self.pipe_group)
        )

        # Updating the bird
        self.bird.update(delta_time=delta_time)

        # Collision logic
        if pygame.sprite.spritecollideany(sprite=self.bird, group=self.collision_group):
            self.game_state = "Lost"

        # Add score
        if self.bird.rect.centerx == self.pipe_group.sprites()[0].rect.centerx:
            self.score_counter.add_to_counter()

        # Update score counter
        self.score_counter.update()

    def render(self, screen: pygame.Surface) -> None:
        screen.blit(self.sprite_backgroud_day, (0, 0))

        self.pipe_group.draw(surface=screen)
        self.score_counter.render(screen=screen)
        self.bird.render(screen=screen)
        self.platform_group.draw(surface=screen)
