class PlayerPrefs:
    def __init__(self):
        self.is_fullscreen = True
        self.is_frameless = False
        self.music_vol = 0.15
        self.sfx_vol = 0.30
        self.game_difficulty = 0
        self.hp_pref = 0 # Turn this to an index number instead. Store the preferences to defines.py
        self.can_pause = False # For game options

        self.score = 0 # should just pass this from the game scene to the game over scene
        self.title_selected = 0 # this too
        self.options_scene_selected = 0