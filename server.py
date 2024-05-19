from http.server import SimpleHTTPRequestHandler, HTTPServer
from PIL import Image
from io import BytesIO

class CustomHandler(SimpleHTTPRequestHandler):
    def send_head(self):
        path = self.translate_path(self.path)
        f = None
        if path.endswith(".jpg") or path.endswith(".png"):  # Add other image formats if needed
            try:
                # Open the image, flip it and save to buffer
                img = Image.open(path)
                img = img.transpose(Image.FLIP_TOP_BOTTOM)
                buffer = BytesIO()
                img_format = 'JPEG' if path.endswith('.jpg') else 'PNG'
                img.save(buffer, format=img_format)
                buffer.seek(0)
                f = buffer
                # Set the content type
                ctype = 'image/jpeg' if img_format == 'JPEG' else 'image/png'
                self.send_response(200)
                self.send_header("Content-type", ctype)
                self.send_header("Content-Length", str(len(buffer.getvalue())))
                self.end_headers()
                return f
            except IOError:
                self.send_error(404, "File not found")
                return None
        else:
            return super().send_head()

    def do_GET(self):
        if self.path == '/hello':
            print("Hello World")
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"Button clicked, check your server console!")
        else:
            f = self.send_head()
            if f:
                try:
                    self.copyfile(f, self.wfile)
                finally:
                    if isinstance(f, BytesIO):
                        f.close()

HTTPServer(('', 8000), CustomHandler).serve_forever()
