# Materia Engine
# Version: 1.0.0
#   > Release date: March 12th 2021
# A framework built on top of pygame to make development of games easier.
# Author: zyenapz
#   > Email: zyenapz@gmail.com
#   > Website: zyenapz.github.io
#   > GitHub: github.com/zyenapz
#   > Twitter: @zyenapz

import pygame
import os
import pickle

# SCENES & MANAGERS

class Scene():
    def __init__(self):
        pass
    
    def handle_events(self, events):
        raise NotImplementedError
    
    def update(self):
        raise NotImplementedError

    def draw(self, window):
        raise NotImplementedError

class SceneManager(object):
    def __init__(self, InitScene):
        self.go_to(InitScene)

    def go_to(self, scene):
        self.scene = scene
        self.scene.manager = self

# ASSET LOADING / SAVING

def load_sound(filename, sfx_dir, volume):
    path = os.path.join(sfx_dir, filename)
    snd = pygame.mixer.Sound(path)
    snd.set_volume(volume)
    return snd

def load_img(file, directory, scale, convert_alpha=False):
    try:
        path = os.path.join(directory, file)
        if not convert_alpha:
            img = pygame.image.load(path).convert_alpha()
        else:
            img = pygame.image.load(path).convert()
            transColor = img.get_at((0,0))
            img.set_colorkey(transColor)
        img_w = img.get_width()
        img_h = img.get_height()
        img = pygame.transform.scale(img, (img_w*scale, img_h*scale))
        return img
    except Exception as e:
        print(f"Error for {file}: {e} Loading default texture instead.")
        s = pygame.Surface((32,32))
        s.fill('red')
        return s

def read_savedata(path):
    with open(path, 'rb') as f:
        try:
            data = pickle.load(f)
            return data
        except EOFError:
            return list()

def write_savedata(data, path):
    with open(path, 'wb') as f:
        pickle.dump(data, f)

# UTILITIES

def sort(arr):
    n = len(arr)

    for i in range(n-1):
        for j in range(0, n-i-1):
            if arr[j] < arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]

    return arr

