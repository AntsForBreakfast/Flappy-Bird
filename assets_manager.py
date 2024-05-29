import pygame

from assets import loader


class AssetsManager:
    def __init__(self) -> None:
        self.sprites: dict[str, pygame.Surface] = loader.load_sprites()
        self.audio: dict[str : pygame.mixer.Sound] = loader.load_audio()
