from flask import Flask, send_file, request
import io
from barcode import Code128
from barcode.writer import ImageWriter

app = Flask(__name__)

@app.route('/')
def home():
    return "Barcode API is running! Use /barcode?code=YOUR_VALUE"

@app.route('/barcode')
def generate_barcode():
    # Get the 'code' from the URL (e.g. ?code=12345)
    code_text = request.args.get('code')

    if not code_text:
        return "Error: No code provided", 400

    try:
        # Create a virtual file in memory
        fp = io.BytesIO()

        # Generate the barcode as an image (Code128 is a standard generic format)
        # You can change Code128 to EAN13 if you have specific retail codes
        barcode_instance = Code128(code_text, writer=ImageWriter())

        # Write the barcode to our memory file
        barcode_instance.write(fp)

        # Reset file pointer to the beginning
        fp.seek(0)

        # Return the image directly to the browser/Excel
        return send_file(fp, mimetype='image/png')

    except Exception as e:
        return f"Error generating barcode: {str(e)}", 500

# Required for Vercel to find the app
if __name__ == '__main__':
    app.run()
