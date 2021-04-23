class PlayerPrefs:
    def __init__(self):
        self.is_fullscreen = False
        self.music_vol = 1.0
        self.sfx_vol = 1.0
        self.game_difficulty = 0

        self.score = 0 # should just pass this from the game scene to the game over scene
        self.title_selected = 0 # this too