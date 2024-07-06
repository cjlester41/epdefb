from PIL import Image, ImageDraw
from flask import Flask, render_template_string, send_file
from definitions import ROOT_DIR
from emulator.flask_web import flask_web
import io, os, logging
import webbrowser


log = logging.getLogger('werkzeug')    # turn off excess logging from flask
log.setLevel(logging.ERROR)

class EPD:    # similar methods of actual driver but not exact match. launches browser and provides display via flask (html)
              ##### must have cursor in termial to capture keyboard inputs ##### 
    #flask_web.init_flask(self)

    def __init__(self, update_interval=1): 
        
        self.load_config()          
        self.image_mode = '1'          

        self.frame_buf = Image.new(self.image_mode, (self.width, self.height), 255)        
        self.update_interval = update_interval * 1000         

        flask_web.init_flask(self)
        self.draw = ImageDraw.Draw(self.frame_buf)

    def load_config(self):            
        self.width = 1404
        self.height = 1872
        self.color = 'white'
        self.text_color = 'black'
    
    def update_image_bytes(self):
        self.image_bytes = io.BytesIO()
        self.frame_buf.save(self.image_bytes, format='PNG')
        self.frame_buf.save(os.path.join(ROOT_DIR, 'ui_files/screen.png'))  

    def clear(self):
        self.image = Image.new(self.image_mode, (self.width, self.height), "white")
        self.draw = ImageDraw.Draw(self.image)  
        self.display(self.getbuffer(self.image))
        
    def display(self, image_buffer):      
        self.update_image_bytes()

    def draw_partial(self, image_buffer):
        self.display(image_buffer)

    def draw_full(self, image_buffer):  
        self.display(image_buffer)

    def get_frame_buffer(self, draw):
        return self.getbuffer(self.image)

    def getbuffer(self, image):
        return image.tobytes()

    def run_flask(self):
        webbrowser.open("http://127.0.0.1:5000/")
        self.app.run(port=5000, debug=False, use_reloader=False)
    