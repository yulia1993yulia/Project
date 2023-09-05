from map import Map
from pynput import keyboard
import time
import os #чтобы очищать консоль перед выводом
from helicopter import Helicopter as helico
from clouds import Clouds
import json

TICK_SLEEP=0.05
TREE_UPDATE=50
CLOUDS_UPDATE=100
FREE_UPDATE =50
MAP_W, MAP_H=20,10

field=Map(MAP_W,MAP_H)
clouds=Clouds(MAP_W,MAP_H)
helico=helico(MAP_W,MAP_H)

tick=1
    

MOVES = {'w':(-1,0), 'd':(0,1),'s':(1,0), 'a':(0,-1)}
def process_key(key):
        global helico, tick, clouds, field
        c=key.char.lower()
        if c in MOVES.keys():
             dx,dy=MOVES[c][0],MOVES[c][1]
             helico.move(dx,dy)
        elif c=="f":
             data={"helicopter":helico.data_export(),
                    "clouds":clouds.data_export(),
                    "field":field.data_export(),
                    "tick":tick}
             with open ("level.json", "w") as lvl:
                 json.dump(data, lvl)
        elif c=="g":
              with open ("level.json", "r") as lvl:
                 data=json.load(lvl)
                 tick=data["tick"] or 1
                 helico.import_data(data["helicopter"])
                 field.import_data(data["field"])
                 clouds.import_data(data["cloudsg"])
             


listener = keyboard.Listener(
    on_press=None,
    on_release=process_key)
listener.start()


while True:
    os.system("cls") #для удаления предыдущего кадра
    print(helico.x,helico.y)
    print("TICK", tick) #выводим кол-во тиков
    field.process_helicopter(helico, clouds)
    helico.print_stats()
    field.print_map(helico, clouds) #выводим карту
    tick+=1 #увеличиваем кол-во тиков
    time.sleep(TICK_SLEEP) #и ждали 50 милисекунд между тиками
    if (tick % TREE_UPDATE==0):
        field.generate_tree()
    if (tick % FREE_UPDATE==0):
        field.update_fires()    
    if (tick % CLOUDS_UPDATE==0):    
        clouds.update()