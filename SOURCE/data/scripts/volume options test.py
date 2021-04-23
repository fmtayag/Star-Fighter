# test code for the volume options
if event.key == pygame.K_p:
    pygame.mixer.music.set_volume(self.manager.p_prefs.music_vol)
    self.manager.p_prefs.music_vol -= 0.01