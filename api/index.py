from flask import Flask, send_file, request
import io
from barcode import Code128
from barcode.writer import ImageWriter

app = Flask(__name__)

@app.route('/')
def home():
    return "Barcode API is running! Use /barcode?code=YOUR_VALUE&text=false"

@app.route('/barcode')
def generate_barcode():
    # Get the 'code' from the URL (e.g. ?code=12345)
    code_text = request.args.get('code')
    
    # Get the 'text' parameter (defaults to 'true' if not provided)
    show_text = request.args.get('text', 'true').lower() != 'false'

    if not code_text:
        return "Error: No code provided", 400

    try:
        # Create a virtual file in memory
        fp = io.BytesIO()

        # Configure the ImageWriter with text option
        writer_options = {
            'write_text': show_text,  # Controls whether text appears below barcode
            'text_distance': 5,        # Distance between barcode and text
            'module_height': 15.0,     # Height of the barcode bars
        }

        # Generate the barcode with custom writer options
        barcode_instance = Code128(code_text, writer=ImageWriter())

        # Write the barcode to our memory file with options
        barcode_instance.write(fp, options=writer_options)

        # Reset file pointer to the beginning
        fp.seek(0)

        # Return the image directly to the browser/Excel
        return send_file(fp, mimetype='image/png')

    except Exception as e:
        return f"Error generating barcode: {str(e)}", 500

# Required for Vercel to find the app
if __name__ == '__main__':
    app.run()
