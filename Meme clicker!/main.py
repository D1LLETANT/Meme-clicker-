# https://htmlcolorcodes.com/color-picker/
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.core.window import Window
from kivy.utils import platform
from kivy.core.audio import SoundLoader

from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.properties import StringProperty,NumericProperty
from random import shuffle, choice, randint
from kivy.clock import Clock
from kivy.storage.jsonstore import JsonStore
from kivy.uix.popup import Popup
from kivy.base import stopTouchApp


class SoundPlayer(BoxLayout):

    def play_sound(self):
        sound = SoundLoader.load('assets/Audio/audio.mp3')
        if sound:
            sound.play()
    
# class MyApp(App):
#     def build(self):
#         return SoundPlayer()
    
# MyApp().run
        


class MenuScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
    
    def on_enter(self, *args):
        app.save_prog

class LeaderScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
    
    def on_enter(self, *args):
        app.save_prog

class GLeaderScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
    
    def on_enter(self, *args):
        app.save_prog

class ShopScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
    
    def on_enter(self, *args):
        app.save_prog
       
class GameScreen(Screen):
    points = NumericProperty(0)
    
    def __init__(self, **kw):
        super().__init__(**kw)
        popup = Popup(title='Заголовок вікна',
                      content=Label(text='Текст Popup'))
        popup.open()

    def on_enter(self, *args):
        self.ids.meme.new_meme()
        return super().on_enter(*args)

class SettingsScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
    
    def on_enter(self, *args):
        app.save_prog

class Meme(Image):

    is_anim= False
    hp = None
    meme = None
    meme_index = 0
    points = 0
    mult = 1

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos) and not self.is_anim:
            
            self.parent.parent.parent.points += (1*self.mult)
            self.points += (1*self.mult)
            self.hp -= 1

            if self.hp <= 0:
                self.break_meme()
                app.storage.put('progress', meme=self.meme)
            else:
                x = self.x
                y = self.y
                size =self.size.copy()
                anim = Animation(
                    size=(size[0]*1.2, size[1]*1.2), t='out_back', d=0.1) + Animation(size=(size[0], size[1]), d=.1)
                anim.start(self)
                self.is_anim = True
                anim.on_complete = lambda *arg: setattr(self, 'is_anim', False)

        return super().on_touch_down(touch)

    def new_meme(self, *args):

        Meme.meme = self.meme = app.LEVELS[randint(0, len(app.LEVELS)-1)]
        self.source = app.MEMES[self.meme]['source']
        self.hp = app.MEMES[self.meme]['hp']
        self.size = app.MEMES[self.meme]['size']
        size = self.size.copy()
        self.size = size[0], size[1]
        self.center = self.parent.center
        anim = Animation(opacity = 1, d=0.3)
        anim &= Animation(
            size=(self.size[0]/1.5, self.size[1]/1.5), d=.2, t='out_back')
        anim &= Animation(center=self.parent.center, d=.3)
        anim.start(self)
        anim.on_complete = lambda *arg: setattr(self, 'is_anim', False)

    def break_meme(self):
        self.is_anim = True
        anim = Animation(size=(self.size[0]*2, self.size[1]*2), d=.2)
        anim &= Animation(center=self.parent.center, d=.2)
        anim &= Animation(opacity=0, d=.3)

        anim.start(self)
        anim.on_complete = Clock.schedule_once(self.new_meme, .5)


class MainApp(App):
    storage = None
    LEVELS = ['Goat', 'Pupsik', 'Cat', 'HUH', 'WHAT?', 'Lione', 'Olen', 'WOW', 'Suslik', 'pufic', 'POPCAT']
    
    MEMES = {
        'Goat': {"source": 'assets/images/1.png', 'hp': 10, "size": ("400dp", "400dp")},
        'Pupsik': {"source": 'assets/images/2.png', 'hp': 10, "size": ("400dp", "400dp")},
        'Cat': {"source": 'assets/images/3.png', 'hp': 10, "size": ("400dp", "400dp")},
        'HUH': {"source": 'assets/images/4.png', 'hp': 10, "size": ("400dp", "400dp")},
        'WHAT?': {"source": 'assets/images/5.png', 'hp': 10, "size": ("400dp", "400dp")},
        'Lione': {"source": 'assets/images/6.png', 'hp': 10, "size": ("400dp", "400dp")},
        'Olen': {"source": 'assets/images/7.png', 'hp': 10, "size": ("400dp", "400dp")},
        'WOW': {"source": 'assets/images/8.png', 'hp': 10, "size": ("400dp", "400dp")},
        'Suslik': {"source": 'assets/images/9.png', 'hp': 10, "size": ("400dp", "400dp")},
        'pufic': {"source": 'assets/images/10.png', 'hp': 10, "size": ("400dp", "400dp")},
        'POPCAT': {"source": 'assets/images/11.png', 'hp': 10, "size": ("400dp", "400dp")},
    }

    def save_prog(self):
        app.storage.put('progress', meme=Meme.meme,
                        hp=Meme.hp,
                        meme_index=Meme.meme_index,
                        mult=Meme.points)
        
    def build(self):
        global storage
        self.storage = JsonStore(self.user_data_dir+"storage.json")
        storage = self.storage
        sm = ScreenManager(transition=FadeTransition(duration=1))
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(GameScreen(name='game'))
        sm.add_widget(SettingsScreen(name='settings'))
        sm.add_widget(LeaderScreen(name='leader'))
        sm.add_widget(GLeaderScreen(name='gleader'))
        sm.add_widget(ShopScreen(name='shop'))
        return sm
    
    def load_prog(self):
        return self.storage.get("progress")

if platform != 'android':
    Window.size = (400, 800)
    Window.left = 750
    Window.top = 100


app = MainApp()
app.run()
