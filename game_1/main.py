import pygame

clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((720, 360))
pygame.display.set_caption('Бегущий')
icon = pygame.image.load('images/icon.png').convert_alpha()
pygame.display.set_icon(icon)

bg = pygame.image.load('images/bg.jpg').convert()

walk_left = [
    pygame.image.load('images/player_left/1.png'),
    pygame.image.load('images/player_left/2.png'),
    pygame.image.load('images/player_left/3.png'),
    pygame.image.load('images/player_left/4.png'),
]

walk_right = [
    pygame.image.load('images/player_right/5.png'),
    pygame.image.load('images/player_right/6.png'),
    pygame.image.load('images/player_right/7.png'),
    pygame.image.load('images/player_right/8.png'),
]

ghost = pygame.image.load('images/ghost.png').convert_alpha()
ghost_list_in_game = []

player_amin_count = 0
bg_x = 0

player_speed = 5
player_x = 150
player_y = 235

is_jump = False
jump_count = 8

pg_sound = pygame.mixer.Sound('sounds/sound_back.mp3')
pg_sound.play()

ghost_timer = pygame.USEREVENT + 1
pygame.time.set_timer(ghost_timer, 2500)

lable = pygame.font.Font('fonts/PlayfairDisplay-ExtraBold.ttf', 40)
lose_label = lable.render('Вы проиграли!', False, (233, 242, 228))
restart_label = lable.render('Играть заново', False, (165, 111, 171))
restart_label_rect = restart_label.get_rect(topleft=(230, 160))

bullets_left = 5
bullet = pygame.image.load('images/bullet.png').convert_alpha()
bullets = []

gameplay = True

running = True
while running:

    screen.blit(bg, (bg_x, 0))
    screen.blit(bg, (bg_x + 720, 0))

    if gameplay:
        player_rect = walk_left[0].get_rect(topleft=(player_x, player_y))

        if ghost_list_in_game:
            for (i, el) in enumerate(ghost_list_in_game):
                screen.blit(ghost, el)
                el.x -= 10

                if el.x < -10:
                    ghost_list_in_game.pop(i)

                if player_rect.colliderect(el):
                    gameplay = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            screen.blit(walk_left[player_amin_count], (player_x, player_y))
        else:
            screen.blit(walk_right[player_amin_count], (player_x, player_y))

        if keys[pygame.K_LEFT] and player_x > 50:
            player_x -= player_speed
        elif keys[pygame.K_RIGHT] and player_x < 300:
            player_x += player_speed

        if not is_jump:
            if keys[pygame.K_SPACE]:
                is_jump = True
        else:
            if jump_count >= -8:
                if jump_count > 0:
                    player_y -= (jump_count ** 2) / 2
                else:
                    player_y += (jump_count ** 2) / 2
                jump_count -= 1
            else:
                is_jump = False
                jump_count = 8

        if player_amin_count == 3:
            player_amin_count = 0
        else:
            player_amin_count += 1

        bg_x -= 2
        if bg_x == -618:
            bg_x = 0

        if bullets:
            for (i, el) in enumerate(bullets):
                screen.blit(bullet, (el.x, el.y))
                el.x += 6

                if el.x > 735:
                    bullets.pop(i)

                if ghost_list_in_game:
                    for (index, ghost_el) in enumerate(ghost_list_in_game):
                        if el.colliderect(ghost_el):
                            ghost_list_in_game.pop(index)
                            bullets.pop(i)
    else:
        screen.fill((61, 71, 138))
        screen.blit(lose_label, (230, 90))
        screen.blit(restart_label, restart_label_rect)

        mouse = pygame.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            player_x = 150
            ghost_list_in_game.clear()
            bullets.clear()
            bullets_left = 5

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == ghost_timer:
            ghost_list_in_game.append(ghost.get_rect(topleft=(722, 244)))
        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_z and bullets_left > 0:
            bullets.append(bullet.get_rect(topleft=(player_x + 30, player_y + 10)))
            bullets_left -= 1

    clock.tick(30)

