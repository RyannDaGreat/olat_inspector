from http.server import SimpleHTTPRequestHandler, HTTPServer
import traceback
import os
import json

class CustomHandler(SimpleHTTPRequestHandler):

    @staticmethod
    def load_image(path):
        """Load an image from a given path."""
        image = load_image(path)  # Assuming load_image is defined elsewhere
        image = rotate_image(image, 45)  # Assuming rotate_image is defined elsewhere
        image = blend_images(image, cv_inpaint_image(image))  # Assuming blend_images and cv_inpaint_image are defined
        return image

    def send_head(self):
        path = self.translate_path(self.path)
        if is_image_file(path):  # Use the provided is_image_file function to check if it's an image
            try:
                image = self.load_image(path)  # Load the image from file
                encoded_image = encode_image_to_bytes(image, filetype='png')  # Encode image as PNG
                self.send_response(200)
                self.send_header("Content-type", 'image/png')
                self.send_header("Content-Length", str(len(encoded_image)))
                self.end_headers()
                return encoded_image
            except Exception as e:
                error_message = f"ERROR: {traceback.format_exc()}"
                self.send_error(500, error_message)
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
        elif self.path == '/listdir':
            try:
                listing = os.listdir('.')  # Get directory listing of the current directory
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(listing).encode())
            except Exception as e:
                error_message = f"ERROR: {traceback.format_exc()}"
                self.send_error(500, error_message)
        else:
            f = self.send_head()
            if f:
                try:
                    self.wfile.write(f)
                except Exception as e:
                    print(f"Failed to send file: {e}")

HTTPServer(('', 8000), CustomHandler).serve_forever()
