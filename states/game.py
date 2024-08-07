from random import randint

import pygame

from assets_manager import AssetsManager
from state_machine import StateMachine, State
from states import menu
from widgets import ScoreCounter, Button
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
        self.running: int = 1
        self.states: dict[str, str] = {"running": "gameover"}
        self.state: str = "running"
        self.rect_screen: pygame.Rect = pygame.display.get_surface().get_rect()
        self.pipe_gap: pygame.Vector2 = pygame.math.Vector2(100, 100)
        self.button_restart: Button = Button(
            text="restart",
            font=pygame.font.SysFont("Arial", 20),
            position=pygame.math.Vector2(77, 460),
            size=pygame.math.Vector2(100, 30),
            elevation=6,
            text_color=(84, 52, 68),
            bg_color=(255, 136, 44),
            shadow_color=(228, 100, 20),
            method=self.reset,
            audio=self.assets_manager.audio["swoosh"],
        )
        self.button_exit: Button = Button(
            text="exit",
            font=pygame.font.SysFont("Arial", 20),
            position=pygame.math.Vector2(221, 460),
            size=pygame.math.Vector2(100, 30),
            elevation=6,
            text_color=(84, 52, 68),
            bg_color=(255, 136, 44),
            shadow_color=(228, 100, 20),
            method=self.exiting,
            audio=self.assets_manager.audio["swoosh"],
        )

        # Sprites
        self.sprite_backgroud_day: pygame.Surface = self.assets_manager.sprites[
            "background-day"
        ]
        self.sprites_pipe: dict[str, pygame.Surface] = self.assets_manager.sprites[
            "pipes"
        ]
        self.sprite_gameover: pygame.Surface = self.assets_manager.sprites["gameover"]
        sprites_bird: dict[str, dict[str, pygame.Surface]] = (
            self.assets_manager.sprites["birds"]
        )
        sprite_platform: pygame.Surface = self.assets_manager.sprites["base"]
        sprites_digit: dict[str, pygame.Surface] = self.assets_manager.sprites[
            "digits"
        ]

        # Sprite coordinates
        self.rect_sprite_gameover: pygame.Rect = self.sprite_gameover.get_rect(
            center=self.rect_screen.center
        )

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
        self.bird = Bird(
            sprites=sprites_bird["red"], audio=self.assets_manager.audio["wing"]
        )
        self.score_counter = ScoreCounter(
            sprites=sprites_digit, audio=self.assets_manager.audio["point"]
        )

        # Initalizing
        self.add_pipes_to_group()

    def add_pipes_to_group(self) -> None:
        sprite_pipe = self.sprites_pipe["green"]
        min_h = sprite_pipe.get_height()
        max_h = self.rect_screen.h - sprite_pipe.get_height()

        pipe_obj_1 = Pipe(
            position=pygame.math.Vector2(self.rect_screen.w, randint(max_h, min_h)),
            velocity=pygame.math.Vector2(100, 0),
            sprite=sprite_pipe,
        )

        pipe_2_h = pipe_obj_1.rect.top - min_h - self.pipe_gap.y
        pipe_obj_2 = Pipe(
            position=pygame.math.Vector2(self.rect_screen.w, pipe_2_h),
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

    def next_state(self) -> None:
        self.state = self.states[self.state]

    def reset(self) -> None:
        self.state_machine.switch(state=menu.Menu)

    def exiting(self) -> None:
        self.running = 0

    def process_event(self, event: pygame.Event) -> None:
        if self.state == "running":
            self.bird.process_event(event=event)
        else:
            self.button_restart.process_event(event=event)
            self.button_exit.process_event(event=event)

    def update(self, delta_time: float) -> int:
        self.bird.update(delta_time=delta_time)

        if self.state == "running":
            # Updating groups
            self.pipe_group.update(delta_time=delta_time)
            self.platform_group.update(delta_time=delta_time)

            # Add new pipe
            grp_sprites = self.pipe_group.sprites()
            if grp_sprites[-1].rect.right + self.pipe_gap.x < self.rect_screen.right:
                self.add_pipes_to_group()

            # Removes all the pipes of the screen
            self.remove_pipes_from_group()

            # Creating group for collision checking with a bird
            self.collision_group = pygame.sprite.Group(
                (self.platform_group, self.pipe_group)
            )

            # Collision logic
            if pygame.sprite.spritecollideany(
                sprite=self.bird, group=self.collision_group
            ):
                self.assets_manager.audio["hit"].play()
                self.assets_manager.audio["die"].play()
                self.next_state()

            # Add score
            if self.bird.rect.centerx == self.pipe_group.sprites()[0].rect.centerx:
                self.score_counter.add_to_counter()

            # Update score counter
            self.score_counter.update()
        else:
            self.button_restart.update()
            self.button_exit.update()

        # Making sure the bird is above platform
        for platform in self.platform_group:
            if self.bird.rect.bottom > platform.rect.top:
                self.bird.rect.bottom = platform.rect.top

        return self.running

    def render(self, screen: pygame.Surface) -> None:
        screen.blit(self.sprite_backgroud_day, (0, 0))

        self.pipe_group.draw(surface=screen)
        self.score_counter.render(screen=screen)
        self.bird.render(screen=screen)
        self.platform_group.draw(surface=screen)

        if self.state == "gameover":
            screen.blit(self.sprite_gameover, self.rect_sprite_gameover)
            self.button_restart.render(screen=screen)
            self.button_exit.render(screen=screen)
