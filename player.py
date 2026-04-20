from circleshape import *
from constants import *
import pygame
from shot import Shot

class Player(CircleShape):

    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.cooldown_timer = 0
    

    # in the Player class
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)
    
    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()
        
        self.cooldown_timer -= dt
    
    def move(self, dt):
        rotated_down = pygame.Vector2(0, 1).rotate(self.rotation)
        rotated_speed_down = PLAYER_SPEED * dt * rotated_down
        self.position += rotated_speed_down
    
    def shoot(self):
        if self.cooldown_timer > 0:
            return
        
        self.cooldown_timer = PLAYER_SHOOT_COOLDOWN_SECONDS
        new_shot = Shot(self.position.x, self.position.y, SHOT_RADIUS)
        start_vector = pygame.Vector2(0, 1)
        rotated_start_vector = start_vector.rotate(self.rotation)
        speed_rotated_vector = rotated_start_vector * PLAYER_SHOOT_SPEED
        new_shot.velocity = speed_rotated_vector
