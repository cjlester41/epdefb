from flask import Flask, render_template_string, send_file
from definitions import ROOT_DIR
import threading
import webbrowser
import traceback
import os


class flask_web:

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
                    return send_file(os.path.join(ROOT_DIR, 'ui_files/screen.png'), mimetype='image/png')
                except Exception as e:
                    traceback.print_exc()
                    return "Internal Server Error", 500

            threading.Thread(target=self.run_flask).start()

    def run_flask(self):
        webbrowser.open("http://127.0.0.1:5000/")
        self.app.run(port=5000, debug=False, use_reloader=False)