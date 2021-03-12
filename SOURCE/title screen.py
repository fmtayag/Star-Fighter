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
