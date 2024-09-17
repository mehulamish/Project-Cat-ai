import gradio as gr
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

# Sample dictionary with conditions (for manual testing or as a default)
default_data = {
    'Header': {'inspection_id': 'YEQO4VFXH3', 'Inspector_name': 'Name'},
    'Tyres': {
        'left_front_condition': 'Needs Replacement', 
        'right_front_condition': 'Ok', 
        'left_rear_condition': 'Good', 
        'right_rear_condition': 'Needs Replacement'
    }
}

# Function to generate the 4-digit number based on conditions
def generate_condition_code(data):
    tyres = data.get('Tyres', {})
    conditions = [
        tyres.get('left_front_condition', ''),
        tyres.get('right_front_condition', ''),
        tyres.get('left_rear_condition', ''),
        tyres.get('right_rear_condition', '')
    ]
    
    # Generate the binary string
    binary_string = ''.join(['1' if 'Needs Replacement' in condition else '0' for condition in conditions])
    
    return binary_string

# Function to fetch the image based on the generated code
def check_and_fetch_image(data_json):
    # Convert the string input into a Python dictionary
    data = eval(data_json)
    binary_code = generate_condition_code(data)
    image_path = f"./{binary_code}.png"
    return image_path

# Function to generate the PDF with the selected image
def generate_pdf(data_json):
    # Convert the string input into a Python dictionary
    data = eval(data_json)
    binary_code = generate_condition_code(data)
    image_path = f"./{binary_code}.png"
    
    # Create the PDF
    pdf_path = f"./{binary_code}_report.pdf"
    c = canvas.Canvas(pdf_path, pagesize=A4)
    
    # Add some text to the PDF
    c.drawString(100, 800, f"Inspection Report: {data['Header']['inspection_id']}")
    c.drawString(100, 780, f"Inspector: {data['Header']['Inspector_name']}")
    
    # Add the image to the PDF
    try:
        img = ImageReader(image_path)
        c.drawImage(img, 100, 500, width=125, height=200)
    except FileNotFoundError:
        c.drawString(100, 500, "Image not found. Please make sure the image file exists.")
    
    c.save()
    
    return pdf_path

# Construct function that generates the PDF and returns it for download
def construct_pdf(data_json):
    pdf_path = generate_pdf(data_json)
    return pdf_path

# Gradio interface
custom_theme = gr.themes.Base().set(
    body_background_fill="#FFFFFF",
    block_title_text_color="#A17917",
    block_label_text_color="#333333",
    input_background_fill="#F0F4F8"
)

custom_css = """
body {
    background-color: #F0F4F8;
}
.gradio-container {
    max-width: 1000px !important;
    margin-left: auto !important;
    margin-right: auto !important;
}
"""

with gr.Blocks(theme=custom_theme, css=custom_css) as demo:
    gr.Markdown("<h1 style='text-align: center; color: #00509E;'>PDF Generation</h1>")
    
    # Textbox for inputting the dictionary data as a string
    data_input = gr.Textbox(label="Input Data", value=str(default_data), lines=10)
    
    # Button to trigger PDF generation
    generate_button = gr.Button("Generate PDF")
    
    # PDF output for download
    pdf_output = gr.File(label="Download PDF")

    # Button click triggers the PDF generation
    generate_button.click(fn=construct_pdf, inputs=data_input, outputs=pdf_output)

demo.launch(share=True)
