import pygame
from tools.sprite_editor.core.animation_player import AnimationPlayer


class PreviewWindow:

    def __init__(self, editor):

        self.editor = editor
        self.player = AnimationPlayer()

        self.screen = pygame.display.set_mode((600, 500))
        pygame.display.set_caption("Animation Preview")

        self.running = True
        self.clock = pygame.time.Clock()

    def run(self):

        anim = self.editor.state.get_current_animation()

        if anim:
            self.player.play(anim)

        while self.running:

            dt = self.clock.tick(60) / 1000

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

            self.player.update(dt)

            self.screen.fill((20,20,20))

            frame = self.player.get_frame()
            sheet = self.editor.canvas.sheet

            if frame and sheet:

                img = sheet.subsurface(frame.x, frame.y, frame.w, frame.h)
                img = pygame.transform.scale(img,(frame.w*3,frame.h*3))

                rect = img.get_rect(center=self.screen.get_rect().center)

                self.screen.blit(img,rect)

            pygame.display.flip()