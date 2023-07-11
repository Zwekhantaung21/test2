import os
from flask import Flask, render_template, request, jsonify, send_file
from pystrich.datamatrix import DataMatrixEncoder
import shutil
from fpdf import FPDF
import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.form['barcode-data']
    encoded_data = data
    generate_ai_syntax_data_matrix_barcode(encoded_data)

    # Generate PDF
    pdf = generate_pdf(data)
    pdf_path = "static/GS1Myanmar_Verify.pdf"
    pdf.output(pdf_path)

    return jsonify({'image_path': 'static/GS1MM_Datamatrix.png', 'pdf_path': pdf_path})

@app.route('/download_zip')
def download_zip():
    # Create a temporary folder
    temp_folder = "static/temp"
    os.makedirs(temp_folder, exist_ok=True)

    # Copy the generated image to the temporary folder
    shutil.copy2("static/GS1MM_Datamatrix.png", temp_folder)

    # Copy the generated PDF to the temporary folder
    shutil.copy2("static/GS1Myanmar_Verify.pdf", temp_folder)

    # Copy additional files or images to the temporary folder (if needed)
    # shutil.copy2("path/to/file.ext", temp_folder)

    # Create the ZIP file including the files in the temporary folder
    shutil.make_archive("static/GS1MM_Datamatrix", 'zip', temp_folder)

    # Remove the temporary folder
    shutil.rmtree(temp_folder)

    return send_file("static/GS1MM_Datamatrix.zip", as_attachment=True)

def generate_ai_syntax_data_matrix_barcode(data):
    encoder = DataMatrixEncoder(data)
    encoder.save("static/GS1MM_Datamatrix.png")
    print("Data Matrix barcode with AI syntax generated successfully!")

def displayResult(data):
    pc = ""
    sn = ""
    lot = ""
    exp = ""

    if len(data) == 16:
        pc = "Product Code: " + data[2:]
        exp = "Expire Date: " + data[2:]  # Replace with actual expiration date format
        lot = "Lot: " + data[2:]
        sn = "SN: " + data[2:]
    else:
        pc = "Product Code: " + data[2:16]
        exp = "Expire Date(Year-Month-Date): " + data[18:20] + "-" + data[20:22] + "-" + data[22:24]
        lot = "Lot: " + data[26:32]
        sn = "SN: " + data[35:39]

    result_text = pc + "\n" + exp + "\n" + lot + "\n" + sn
    return result_text

def generate_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Add first logo image at the top-left side
    logo_path = "static/gs1_logo.png"
    logo_width = 60  # Adjust the width of the logo as needed
    logo_x = 10  # Adjust the x-coordinate for the left side placement
    pdf.image(logo_path, x=logo_x, y=10, w=logo_width)

    # Add second logo image at the top-right side
    logo_path_2 = "static/mba_logo.png"
    logo_width_2 = 60  # Adjust the width of the logo as needed
    logo_x_2 = pdf.w - logo_width_2 - 10  # Adjust the x-coordinate for the right side placement
    pdf.image(logo_path_2, x=logo_x_2, y=10, w=logo_width_2)

    # Display the user input data
    pdf.set_text_color(1, 45, 108)
    pdf.set_font("Arial", style='B')
    pdf.set_xy(10, pdf.get_y() + 40)  # Adjust the y-coordinate as needed
    pdf.cell(0, 10, "Your Input Data", ln=True)
    pdf.set_text_color(1, 45, 108)
    pdf.cell(0, 10, data)

    # Calculate the y-coordinate for the image
    image_y = pdf.get_y() + 10

    image_width = 45  # Adjust the width of the image as needed

    # Calculate the x-coordinate for the centered image
    image_x = (pdf.w - image_width) / 2

    pdf.image("static/GS1MM_Datamatrix.png", x=image_x, y=image_y, w=image_width)

    # Calculate the y-coordinate for the HRI text below the image
    hri_text_y = image_y + image_width + 10  # Adjust the spacing between the image and HRI text

    # HRI text
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pdf.set_font("Arial", style='B', size=10)
    pdf.set_text_color(1, 45, 108)  # Set text color to #012D6C
    pdf.set_xy(10, hri_text_y)
    pdf.cell(0, 10, "This Data Matrix is generated from GS1 Myanmar Generator", ln=True, align='C')
    pdf.cell(0, 10, f"Generated Date and Time: {current_datetime}", ln=True, align='C')

    # Calculate the y-coordinate for the additional text below the HRI text
    additional_text_y = hri_text_y + 10
     # Additional text
    pdf.set_font("Arial", size=10)
    pdf.set_text_color(1, 45, 108)  # Set text color to default (blue)
    pdf.set_xy(10, additional_text_y)
    text = '''
    This attachment is about Verifying your Data Matrix that was produced from GS1 Myanmar. You can use our Data Matrix in your Product, Website, Marketing, Healthcare, Events etc. If there is any issues related to 'YOUR DISTRIBUTIONS' of Data Matrix produced by GS1 Myanmar, we would like to inform you that we will not be responsible for solving it aspect an error of GS1 Myanmar Data Matrix Generator(Bad resolution, ECC error and Quietzone Error). If you had an error with our generator contact us as soon as possible.    '''
    pdf.multi_cell(0, 10, text, align='J')

     # Check if the input data starts with "http://" or "https://"
    if not data.startswith("http://") and not data.startswith("https://") and not data[0].isalpha():
        # Display the result data
        result_text = displayResult(data)
        pdf.set_font("Arial", style='B', size=10)
        pdf.set_text_color(242, 99, 53)  # Set text color to #F26335
        result_text_y = pdf.get_y() 
        pdf.set_xy(10, result_text_y-2)
        pdf.multi_cell(0, 10, result_text, align='C')



    # Additional text at the bottom
    pdf.set_text_color(0)  # Set text color to default (black)
    pdf.set_xy(10, hri_text_y+99)  # Adjust the y-coordinate for the bottom placement
    pdf.set_text_color(1, 45, 108)
    pdf.set_font("Arial", size=8)
    bottom_text = '''
    Address: UMFCCI 5 Floor, Min Ye KyawSwar Road, Lanmadaw Township, Yangon 
    Email: info@gs1myanmar.org, Phone: +959446868002, +959446868004'''
    pdf.multi_cell(0, 10, bottom_text, align='C')

   
    return pdf


if __name__ == '__main__':
    app.run(debug=True)
