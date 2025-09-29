# pip install eel
import eel

eel.init('ui') # folder name

@eel.expose
def get_data():
    return 'Got data from python'

@eel.expose
def send_data(msg):
    print(msg)

eel.start('index.html') # Run app window