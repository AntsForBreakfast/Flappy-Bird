import pygame

import assets_manager
import state_machine

from states.menu import Menu

pygame.init()


class Main:
    def __init__(self) -> None:
        # 288, 512
        self.screen = pygame.display.set_mode((288, 512))
        pygame.display.set_caption("Flappy Bird")
        self.asset_manager = assets_manager.AssetsManager()
        self.state_machine = state_machine.StateMachine(Menu, self.asset_manager)
        self.clock = pygame.Clock()
        self.FPS = 60

        self.running = True

    def run(self) -> None:
        delta_time = self.clock.tick(self.FPS) / 1000

        while self.running:
            events = pygame.event.get()
            for event in events:
                self.state_machine.process_event(event=event)
                if event.type == pygame.QUIT:
                    self.running = False
            self.state_machine.update(delta_time=delta_time)
            self.state_machine.render(screen=self.screen)

            pygame.display.flip()
            self.clock.tick(self.FPS)

        pygame.quit()


if __name__ == "__main__":
    main = Main()
    main.run()
