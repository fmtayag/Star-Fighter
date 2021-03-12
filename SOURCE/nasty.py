""" while running:

    # Initialize the game objects and variables ================================

    # Empty the sprites
    sprites.empty()
    enemies.empty()
    p_lasers.empty()
    e_lasers.empty()
    upgrades.empty()
    particles[:] = []
    bouncies[:] = []
    

    # Instantiate the player
    player = Player(WIN_RES, player_imgs, p_spr_supergroup, Laser, p_laser_img, laser_sfx)
    player_group.add(player)
    sprites.add(player)

    # Reset the scores, and others
    spawn_timer = 0
    score = 0
    name = str()
    fade_timer = pygame.time.get_ticks()
    ts_timer = pygame.time.get_ticks() # Title screen timer
    dev_logo_alpha = 256
    logo_alpha = 0
    has_faded = False # for menu

    spawn_bouncies(window, bouncies)

    while in_devlogo_screen:

         # Lock the FPS
        clock.tick(FPS)

        # Get input ============================================================
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                in_devlogo_screen = False
        
        # Draw processes =======================================================
        
        now = pygame.time.get_ticks()
        if now - ts_timer > 3000:
            now = pygame.time.get_ticks()
            if now - fade_timer > 1000:
                dev_logo_alpha -= 5
                dev_logo_img.set_alpha(dev_logo_alpha)
                window.fill(BLACK)
                draw_bouncies(bouncies)
                window.blit(dev_logo_img, ( (WIN_RES["w"] / 2) - (dev_logo_img.get_width() / 2) * 2.8, WIN_RES["h"] * 0.3) )
                pygame.display.flip()

            if dev_logo_alpha < 0: # If image has almost faded out
                # Play the soundtrack
                pygame.mixer.music.play(loops=-1)
                in_devlogo_screen = False
                menu = True
        else:
            window.fill(BLACK)
            draw_bouncies(bouncies)
            window.blit(dev_logo_img, ( (WIN_RES["w"] / 2) - (dev_logo_img.get_width() / 2) * 2.8, WIN_RES["h"] * 0.3) )
            draw_text(window, "a game by", 32, game_font, WIN_RES["w"] / 2.3, WIN_RES["h"] * 0.4, WHITE)
            draw_text(window, "zyenapz", 32, game_font, WIN_RES["w"] / 2.3, WIN_RES["h"] * 0.45, WHITE)
            draw_text(window, "(c) 2020 zyenapz. All rights reserved.", 14, game_font, WIN_RES["w"] / 2, WIN_RES["h"] * 0.97, WHITE, "centered")
                
        # Update the window
        pygame.display.flip()

    while menu:

        # Lock the FPS
        clock.tick(FPS)

        # Increment the background and parallax's ypos
        background_y += 2
        backgroundp_y += 4

        # Get input ============================================================
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                menu = False
            elif event.type == pygame.KEYDOWN and has_faded:
                if event.key == pygame.K_z:
                    menu = False
                    gaming = True
                    played_once = True
                elif event.key == pygame.K_s:
                    menu = False
                    in_scores = True
                elif event.key == pygame.K_x:
                    running = False
                    menu = False

        # Update processes =====================================================
        if not played_once:
            if logo_alpha < 255:
                logo_alpha += 3
                logo_img.set_alpha(logo_alpha)
        else:
            logo_alpha = 255
            
        if logo_alpha >= 255:
            has_faded = True

        # Draw objects =========================================================

        # Draw the background and the parallax
        draw_background(window, background_img, background_rect, background_y)
        draw_background(window, backgroundp_img, backgroundp_rect, backgroundp_y)

        # Draw the title screen texts and images
        window.blit(logo_img, (window_rect.centerx-240, -64))
        if has_faded:
            draw_text(window, "powered by pygame", 16, game_font, window_rect.centerx, window_rect.centery-32, GRAY, "centered")
            draw_text(window, "[Z] Play", 32, game_font, window_rect.centerx, window_rect.centery+64, WHITE, "centered")
            draw_text(window, "  [S] Scores", 32, game_font, window_rect.centerx, window_rect.centery+96, WHITE, "centered")
            draw_text(window, "[X] Exit", 32, game_font, window_rect.centerx, window_rect.centery+128, WHITE, "centered")
            draw_text(window, "(c) 2020 zyenapz.", 16, game_font, window_rect.centerx, window_rect.bottom-98, GRAY, "centered")
            draw_text(window, "All rights reserved.", 16, game_font, window_rect.centerx, window_rect.bottom-82, GRAY, "centered")
            draw_text(window, "Game & Art by zyenapz", 16, game_font, window_rect.centerx, window_rect.bottom-66, GRAY, "centered")
            draw_text(window, "Music by YoItsRion", 24, game_font, window_rect.centerx, window_rect.bottom-45, GRAY, "centered")

        # Update the window
        pygame.display.flip()

    while in_scores:

        # Lock the FPS
        clock.tick(FPS)

        # Increment the background and parallax's ypos
        background_y += 2
        backgroundp_y += 4

        # Get input ============================================================
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                in_scores = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    menu = True
                    in_scores = False

        # Draw objects =========================================================
        draw_background(window, background_img, background_rect, background_y)
        draw_background(window, backgroundp_img, backgroundp_rect, backgroundp_y)
        draw_text(window, "High Scores", 32, game_font, window_rect.centerx, window_rect.top+32, WHITE, "centered")
        draw_text(window, "[X] Back", 32, game_font, window_rect.centerx, window_rect.bottom-64, WHITE, "centered")

        # Draw highscores
        if hi_scores != []:
            for i in range(len(hi_scores[:8])):
                name = hi_scores[i][0].upper()
                score = str(hi_scores[i][1]).zfill(4)
                if i == 0:
                    if hi_scores[i][1] > LEGEND_SCORE:
                        draw_text(window, f"{name} L{score}", 40, game_font, window_rect.centerx, 156, PURPLE, "centered")
                    else:
                        draw_text(window, f"{name} {score}", 40, game_font, window_rect.centerx, 156, GOLD, "centered")
                else:
                    if hi_scores[i][1] > LEGEND_SCORE:
                        draw_text(window, f"{name:<6} L{score}", 40, game_font, window_rect.centerx, 156+(40*(i+1)), PURPLE, "centered")
                    else:
                        draw_text(window, f"{name} {score}", 40, game_font, window_rect.centerx, 156+(40*(i+1)), WHITE, "centered")
        else:
            draw_text(window, f"No scores yet", 32, game_font, window_rect.centerx, window_rect.centery, WHITE, "centered")

        # Update the window
        pygame.display.flip()

    while gaming:
        if not paused:

            if spawn_timer == 0:
                spawn_timer = pygame.time.get_ticks()

            # Lock the FPS
            clock.tick(FPS)

            # Increment the background and parallax's ypos
            background_y += 1
            backgroundp_y += 2

            # Get input ========================================================
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    gaming = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                        paused = True

            # Update objects ===================================================

            # Spawn an enemy
            now = pygame.time.get_ticks()
            if (now - spawn_timer > spawn_delay - sd_subtractor(score) and
                len(enemies) < max_enemy(score)):
                spawn_timer = now
                roll_spawn(score)

            # Check if enemy is hit by lasers
            hits = pygame.sprite.groupcollide(enemies, p_lasers, False, True)
            for hit in hits:
                hit.spdy = -6 # Knockback effect
                hit.health -= 1
                spawn_explosion(Explosion, explosion_data, hit.rect.centerx, hit.rect.bottom, sprites)
                if hit.health <= 0:
                    offset = shake(15, 5)
                    u = Upgrade(window, upgrade_imgs, hit.rect.center, score)
                    sprites.add(u)
                    upgrades.add(u)
                    spawn_particles(hit.rect.centerx, hit.rect.centery, random.randrange(10,16), particle_colors)

            # Check if the player collides with an enemy
            hits = pygame.sprite.spritecollide(player, enemies, True, pygame.sprite.collide_circle)
            for hit in hits:
                player.health -= 5
                spawn_explosion(Explosion, explosion_data, hit.rect.centerx, hit.rect.bottom, sprites)
                spawn_explosion(Explosion, explosion_data, player.rect.centerx, player.rect.bottom, sprites)
                offset = shake(20, 10)
                spawn_particles(hit.rect.centerx, hit.rect.centery, random.randrange(10,16), particle_colors)

            # Check if player is hit by enemy lasers
            hits = pygame.sprite.spritecollide(player, e_lasers, True, pygame.sprite.collide_circle)
            for hit in hits:
                player.health -= hit.damage
                spawn_explosion(Explosion, explosion_data, player.rect.centerx, player.rect.bottom, sprites)
                offset = shake(20, 10)

            # Check if player picks up an upgrade
            hits = pygame.sprite.spritecollide(player, upgrades, True, pygame.sprite.collide_circle)
            for hit in hits:
                if hit.type == "gun":
                    if player.cur_lvl < 2:
                        player.cur_lvl += 1
                        if player.cur_lvl >= 2:
                            player.cur_lvl = 2
                        player.lvl = player.lvls[player.cur_lvl]
                    else:
                        player.health += 1
                        if player.health >= 10:
                            player.health = 10
                    upgrade_sfx.play()
                elif hit.type == "hp":
                    player.health += 2
                    if player.health >= 10:
                        player.health = 10
                    upgrade_sfx.play()
                elif hit.type == "coin":
                    score += 1
                    coin_sfx.play()

            # Check if player has no health
            if player.health <= 0:
                spawn_particles(player.rect.centerx, player.rect.centery, 50, particle_colors)
                gaming = False
                game_over = True
                player.kill()

            sprites.update()

            # Draw objects =====================================================

            # Draw the background and the parallax
            draw_background(window, background_img, background_rect, background_y)
            draw_background(window, backgroundp_img, backgroundp_rect, backgroundp_y)

            # Draw the sprites
            sprites.draw(window)
            update_particles()

            # Draw the HUD
            window.blit(score_img, (score_rect.x, score_rect.y))
            if score > LEGEND_SCORE:
                draw_text(window, f"LEGEND", 24, game_font, score_rect.x*12, score_rect.y+4, GOLD, "centered")
            else:
                draw_text(window, f"{str(score).zfill(4)}", 24, game_font, score_rect.x*9.5, score_rect.y+4, WHITE, "centered")
            window.blit(upgrade_imgs["gun"][0], (score_rect.x, score_rect.y*1.8))
            draw_text(window, f"{player.cur_lvl+1}/3", 24, game_font, score_rect.x*8.5, score_rect.y*2, WHITE, "centered")
            draw_hp(window, 10, 10, player.health, RED, hp_bar_img)

            # Screen shake
            window.blit(window, next(offset))

            # Update the window
            pygame.display.flip()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    gaming = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                        paused = False
                    elif event.key == pygame.K_x:
                        paused = False
                        gaming = False
                        menu = True

            # Draw the pause texts
            draw_text(window, f"PAUSED", 32, game_font, window_rect.centerx, window_rect.centery-32, WHITE, "centered")
            draw_text(window, f"[ESC][P] Resume", 24, game_font, window_rect.centerx, window_rect.centery+32, WHITE, "centered")
            draw_text(window, f"   [X] Quit", 24, game_font, window_rect.centerx, window_rect.centery+66, WHITE, "centered")

            # Update the window
            pygame.display.flip()

    while game_over:
        # Lock the FPS
        clock.tick(FPS)

        # Increment the background and parallax's ypos
        background_y += 1
        backgroundp_y += 2

        # Get input ============================================================
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game_over = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    name = name[:-1] # Remove the last character
                elif event.key == pygame.K_RETURN:
                    if len(name) > 2:
                        menu = True
                        game_over = False
                        hi_scores.append([name, score])
                        hi_scores = sort(hi_scores)
                        write_savedata(hi_scores, scores_path)
                else:
                    if chr(event.key) in 'abcdefghijklmnopqrstuvwxyz0123456789':
                        if len(name) < 5:
                            name = name + chr(event.key) # Concatenate the letter to the string
                            typing_sfx.play()
                        else:
                            denied_sfx.play()

        # Update objects =======================================================

        sprites.update()

        # Draw objects =========================================================

        # Draw the background and the parallax
        draw_background(window, background_img, background_rect, background_y)
        draw_background(window, backgroundp_img, backgroundp_rect, backgroundp_y)

        # Draw the sprites
        sprites.draw(window)
        update_particles()

        # Draw the HUD
        window.blit(score_img, (10, 50))
        if score > LEGEND_SCORE:
            draw_text(window, f"LEGEND {score}", 24, game_font, score_rect.x*18, score_rect.y+4, GOLD, "centered")
        else:
            draw_text(window, f"{str(score).zfill(4)}", 24, game_font, score_rect.x*9.5, score_rect.y+4, WHITE, "centered")
        draw_hp(window, 10, 10, player.health, RED, hp_bar_img)
        window.blit(upgrade_imgs["gun"][0], (score_rect.x, score_rect.y*1.8))

        # Draw the Game Over texts
        draw_text(window, f"{player.cur_lvl+1}/3", 24, game_font, score_rect.x*8.5, score_rect.y*2, WHITE, "centered")
        draw_text(window, "GAME OVER", 64, game_font, window_rect.centerx, window_rect.centery-64, WHITE, "centered")
        draw_text(window, "Enter name", 32, game_font, window_rect.centerx, window_rect.centery+32, WHITE, "centered")
        draw_text(window, f"{name.upper()}", 32, game_font, window_rect.centerx, window_rect.centery+74, WHITE, "centered")
        if len(name) > 2:
            draw_text(window, "Press ENTER", 24, game_font, window_rect.centerx, window_rect.centery+132, WHITE, "centered")

        # Screen shake
        window.blit(window, next(offset))

        # Update the window
        pygame.display.flip()

 """