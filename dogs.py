# Randomly display dogs images from internet
# Use another thread to retrieve image list without waiting
import requests
from random import randint
from PIL import Image
from io import BytesIO
from matplotlib import pyplot as plt
from threading import Thread, Lock
from time import sleep

stop_loading_image = False
def get_dogs_images(breeds):
   for breed_name in breeds:
        if stop_loading_image:
            break
        try:
            response = requests.get(f"https://dog.ceo/api/breed/{breed_name}/images", timeout=10)
        except requests.exceptions.Timeout as e:
            print(e)
        dog_images_message = response.json()
        if dog_images_message['status']=='success':
            dog_images=dog_images_message['message']
            lock.acquire()
            for dog_image in dog_images:
                dogs.append(dog_image)
            lock.release()

def on_close(event):									# handle canvas close event
	global canvas_not_close
	canvas_not_close=False

# main
dogs = []
lock = Lock()
fig = plt.figure()
fig.canvas.mpl_connect('close_event', on_close)
canvas_not_close=True
try:
    response = requests.get(f"https://dog.ceo/api/breeds/list/all", timeout=10)
except requests.exceptions.Timeout as e:
    print(e)
dog_message = response.json()

if dog_message['status']=="success":
    breeds = dog_message['message']
    t = Thread(target=get_dogs_images, args=(breeds,))
    t.start()
    total=0   
    while canvas_not_close:
        lock.acquire()
        total = len(dogs)
        if total==0:
            lock.release()
            sleep(1)
            continue
        idx = randint(0,total-1)
        URL = dogs[idx]
        lock.release()

        print("Total number of dogs : ", total)
        print("Dog's random number  : ", idx)
        r = requests.get(URL)
        im = Image.open(BytesIO(r.content))
        plt.imshow(im)
        plt.pause(2)
        plt.clf()
    
    stop_loading_image=True
    # t.join()