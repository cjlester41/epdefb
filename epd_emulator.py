from PIL import Image, ImageDraw
from flask import Flask, render_template_string, send_file
import io, os
import threading
import webbrowser
import traceback

currentdir = os.path.dirname(os.path.realpath(__file__)) 

class EPD:
    
    def __init__(self, update_interval=1): 
        
        self.load_config()          
        self.image_mode = '1'          

        self.frame_buf = Image.new(self.image_mode, (self.width, self.height), 255)        
        self.update_interval = update_interval * 1000         

        self.init_flask()
        self.draw = ImageDraw.Draw(self.frame_buf)

    def load_config(self):            
        self.width = 1404
        self.height = 1872
        self.color = 'white'
        self.text_color = 'black'
    
    def update_image_bytes(self):
        self.image_bytes = io.BytesIO()
        self.frame_buf.save(self.image_bytes, format='PNG')
        self.frame_buf.save(os.path.join(os.path.dirname(__file__), 'screen.png'))  

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

    def init_flask(self):
        self.app = Flask(__name__)

        @self.app.route('/')
        def index():
            return render_template_string(f'''
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <style>
                        #screenImage {{
                            width: 100%;
                            height: auto;
                        }}
                    </style>
                    <script>
                        function updateImage() {{
                            var image = document.getElementById("screenImage");
                            image.src = "screen.png?t=" + new Date().getTime(); // Prevent caching
                        }}

                        setInterval(updateImage, {self.update_interval}); 
                    </script>
                </head>
                <body onload="updateImage()">
                    <img id="screenImage" src="screen.png" alt="EPD Emulator">
                </body>
                </html>
            ''')

        @self.app.route('/screen.png')
        def display_image():
            try:
                return send_file(os.path.join(os.path.dirname(__file__), 'screen.png'), mimetype='image/png')
            except Exception as e:
                traceback.print_exc()
                return "Internal Server Error", 500

        threading.Thread(target=self.run_flask).start()

    def run_flask(self):
        webbrowser.open("http://127.0.0.1:5001/")
        self.app.run(port=5001, debug=False, use_reloader=False)