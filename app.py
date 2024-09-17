import gradio as gr
import random
import string
from datetime import datetime
import geocoder
import base64
import ai
import json
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

global_data = {}
import os

def collect_inspection_data(
    inspection_id_input, Inspector_name_input, Inspector_employee_id,
    geo_input, serial_number_input, truck_model_input, truck_odometer_input,
    Customer_name_input, Cat_customer_id,
    left_front_image, left_front_pressure, right_front_image, right_front_pressure,
    left_rear_image, left_rear_pressure, right_rear_image, right_rear_pressure,
    left_front_condition_image, left_front_condition, right_front_condition_image,
    right_front_condition, left_rear_condition_image, left_rear_condition,
    right_rear_condition_image, right_rear_condition, tyre_audio_input, summary_text_tyre,
    battery_image, battery_make, battery_voltage, battery_water_level, battery_damage,
    battery_damage_image, leak_rust, battery_audio_input, summary_text_battery,
    capture_image, image_gallery, rust, oil_leak_suspension, exterior_audio_input,
    summary_text_exterior, brake_fluid_level, emergency_brake, front_brake_condition,
    rear_brake_condition, brakes_audio_input, summary_text_brakes, capture_image_brakes,
    image_gallery_brakes, engine_damage, engine_oil_condition, engine_oil_color,
    brake_fluid_condition, brake_fluid_color, engine_oil_leak, capture_image_engine,
    image_gallery_engine, engine_audio_input, summary_text_engine, customer_audio_input,
    summary_text_customer
):
    
    updated_dictionary={
        "Header": {
            "inspection_id": inspection_id_input,
            "Inspector_name": Inspector_name_input,
            "Inspector_employee_id": Inspector_employee_id,
            "geo_input": geo_input,
            "serial_number_input": serial_number_input,
            "truck_model_input": truck_model_input,
            "truck_odometer_input": truck_odometer_input,
            "Customer_name_input": Customer_name_input,
            "Cat_customer_id": Cat_customer_id,
            "Summary": "Will be updated",
        },
        "Tyres": {
            "left_front_image": left_front_image,
            "left_front_pressure": left_front_pressure,
            "right_front_image": right_front_image,
            "right_front_pressure": right_front_pressure,
            "left_rear_image": left_rear_image,
            "left_rear_pressure": left_rear_pressure,
            "right_rear_image": right_rear_image,
            "right_rear_pressure": right_rear_pressure,
            "left_front_condition_image": left_front_condition_image,
            "left_front_condition": left_front_condition,
            "right_front_condition_image": right_front_condition_image,
            "right_front_condition": right_front_condition,
            "left_rear_condition_image": left_rear_condition_image,
            "left_rear_condition": left_rear_condition,
            "right_rear_condition_image": right_rear_condition_image,
            "right_rear_condition": right_rear_condition,
            "tyre_audio_input": tyre_audio_input,
            "summary_text_tyre": summary_text_tyre,
        },
        "Battery": {
            "battery_image": battery_image,
            "battery_make": battery_make,
            "battery_voltage": battery_voltage,
            "battery_water_level": battery_water_level,
            "battery_damage": battery_damage,
            "battery_damage_image": battery_damage_image,
            "leak_rust": leak_rust,
            "battery_audio_input": battery_audio_input,
            "summary_text_battery": summary_text_battery,
        },
        "Exterior": {
            "capture_image": capture_image,
            "image_gallery": image_gallery,
            "rust": rust,
            "oil_leak_suspension": oil_leak_suspension,
            "exterior_audio_input": exterior_audio_input,
            "summary_text_exterior": summary_text_exterior,
        },
        "Brakes": {
            "brake_fluid_level": brake_fluid_level,
            "emergency_brake": emergency_brake,
            "front_brake_condition": front_brake_condition,
            "rear_brake_condition": rear_brake_condition,
            "brakes_audio_input": brakes_audio_input,
            "summary_text_brakes": summary_text_brakes,
            "capture_image_brakes": capture_image_brakes,
            "image_gallery_brakes": image_gallery_brakes,
        },
        "Engine": {
            "engine_damage": engine_damage,
            "engine_oil_condition": engine_oil_condition,
            "engine_oil_color": engine_oil_color,
            "brake_fluid_condition": brake_fluid_condition,
            "brake_fluid_color": brake_fluid_color,
            "engine_oil_leak": engine_oil_leak,
            "capture_image_engine": capture_image_engine,
            "image_gallery_engine": image_gallery_engine,
            "engine_audio_input": engine_audio_input,
            "summary_text_engine": summary_text_engine,
        },
        "Customer": {
            "customer_audio_input": customer_audio_input,
            "summary_text_customer": summary_text_customer,
        }
    }
    
    return updated_dictionary


# Read the image file and encode it
with open("cat-logo.png", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode()

# Custom theme and CSS
custom_theme = gr.themes.Base().set(
    body_background_fill="#FFFFFF",
    block_title_text_color="#A17917",
    block_label_text_color="#333333",
    input_background_fill="#F0F4F8",
    button_primary_background_fill="#F6D000",
    button_primary_background_fill_hover="#E6C000",
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

# Create the Gradio interface with Tabs for navigation
with (gr.Blocks(theme=custom_theme, css=custom_css) as demo):
    # Tabs for navigation
    
     # Navigation bar
    with gr.Row(elem_id="navbar", visible=True):
        with gr.Column(scale=1):
           gr.HTML(f"<img src='data:image/png;base64,{encoded_string}' alt='Company Logo' style='width: 100px; height: auto;'/>")  # Relative path for the logo
    
    summary_display = gr.JSON(visible=False)
    
    
    with gr.Tabs() as tabs:
        with gr.TabItem("Job Inspection",id=1) as tab1:
            # Job Inspection Form
            gr.Markdown("<h1 style='text-align: center; color: #A17917;'>Job Inspection Form</h1>")
            

            async def image_upload_truck(image):
                out = await ai.get_ai_response(0, image)
                return out['sno'], out['model']


            async def image_upload_odometer(image):
                out = await ai.get_ai_response(1, image)
                return out['reading']

            def generate_inspection_id():
                return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

            def fetch_geo_location():
                try:
                    # Use geocoder to get the IP-based location
                    g = geocoder.ip('me')
                    if g.latlng:
                        latitude, longitude = g.latlng
                        return f"Latitude: {latitude}, Longitude: {longitude}"
                    else:
                        return "Location not found"
                except Exception as e:
                    return f"Error: {str(e)}"
            
            # Generate 10-digit inspection id
            inspection_id = generate_inspection_id()
            inspection_id_input = gr.Textbox(label="Inspection ID", value=inspection_id, interactive=False)
            # Get current date and time
            current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            with gr.Row():
                with gr.Column():
                    Inspector_name_input = gr.Textbox(label="Inspector Name", value="Name", interactive=False)
                with gr.Column():
                    Inspector_employee_id = gr.Textbox(label="CAT. Employee ID", value="ID", interactive=False)

            # Date and Time with Pickers
            gr.HTML('''
            <label for="date-picker">Date:</label>
            <input type="date" id="date-picker" value="{current_date}"><br>
            <label for="time-picker">Time:</label>
            <input type="time" id="time-picker" value="{current_time}">
            '''.format(current_date=datetime.now().strftime("%Y-%m-%d"), 
                    current_time=datetime.now().strftime("%H:%M")))

            # Geo Coordinates with Reload Icon
            with gr.Row(elem_id="geo-container"):
                with gr.Column(scale=20):
                    geo_input = gr.Textbox(label="Geo Coordinates", value=fetch_geo_location(), interactive=False, elem_id="geo-input")
                with gr.Column(scale=1, min_width=50):
                    reload_icon = gr.Button("🔄", elem_id="reload-icon")

            with gr.Row():
                # Image upload column
                with gr.Column():
                    image_input_truck = gr.Image(label="Upload an Image of Truck's Serial Number Plate", type="filepath")
                with gr.Column(elem_id="truck-info-container"):
                    with gr.Row(elem_id="serial-number-container"):
                        serial_number_input = gr.Textbox(label="Truck Serial Number", placeholder="Enter Serial Number", interactive=True)
                    with gr.Row(elem_id="truck-model-container"):
                        truck_model_input = gr.Textbox(label="Truck Model", placeholder="Enter Truck Model", interactive=True)

            with gr.Row():    
                with gr.Column():
                    image_input_odometer = gr.Image(label="Upload an Image of Odometer", type="filepath")
                # Text input column
                with gr.Column():
                    truck_odometer_input = gr.Textbox(label="Odometer Reading", placeholder="Enter Odometer Reading", interactive=True)
            
            image_input_truck.change(
                image_upload_truck,
                inputs=image_input_truck,
                outputs=[serial_number_input, truck_model_input]
            )
            
            image_input_odometer.change(
                image_upload_odometer,
                inputs=image_input_odometer,
                outputs=[truck_odometer_input]
            )

            with gr.Row():
                inspector_signature = gr.Sketchpad(label="Inspector Signature", height=400, width=300)

            with gr.Row():
                with gr.Column():
                    Customer_name_input = gr.Textbox(label="Customer/Company Name", placeholder="Enter Name", interactive=True)
                with gr.Column():
                    Cat_customer_id = gr.Textbox(label="CAT. Customer ID", placeholder="Enter Customer ID", interactive=True)

            def reload_location():
                return fetch_geo_location()

            reload_icon.click(
                reload_location,
                inputs=[],
                outputs=[geo_input]
            )

            def change_tab():
                return gr.Tabs(selected=2)
            btn= gr.Button(value="Next")
            btn.click(change_tab,None,tabs)

        with gr.TabItem("Tyre Inspection",id=2) as tab2:
            # tyre Pressure Section
            # Functions to process uploaded images

            async def process_and_summarize_audio_tyre(audio):
                out = await ai.get_ai_response(3, audio)
                return out['content']

            
            async def process_tyre_pressure_image_left_front(image):
                out = await ai.get_ai_response(2, image)
                return out['content']

            async def process_tyre_pressure_image_right_front(image):
                out = await ai.get_ai_response(2, image)
                return out['content']

            async def process_tyre_pressure_image_left_rear(image):
                out = await ai.get_ai_response(2, image)
                return out['content']

            async def process_tyre_pressure_image_right_rear(image):
                out = await ai.get_ai_response(2, image)
                return out['content']

            # Default tyre data
            default_tyre_data = {
                "left_front": {
                    "pressure": "32",
                    "condition": "Good"
                },
                "right_front": {
                    "pressure": "30",
                    "condition": "Ok"
                },
                "left_rear": {
                    "pressure": "34",
                    "condition": "Good"
                },
                "right_rear": {
                    "pressure": "31",
                    "condition": "Needs Replacement"
                }
            }
            

            # tyre Pressure Section
            gr.Markdown("<h1 style='text-align: center; color: #A17917;'>Tyre Pressure</h1>")
            with gr.Row():
                with gr.Column():
                    left_front_image = gr.Image(label="Left Front tyre Pressure", type="filepath",mirror_webcam=False)
                    left_front_pressure = gr.Textbox(label="Left Front Pressure", value=default_tyre_data["left_front"]["pressure"], interactive=True)
                with gr.Column():
                    right_front_image = gr.Image(label="Right Front tyre Pressure", type="filepath")
                    right_front_pressure = gr.Textbox(label="Right Front Pressure", value=default_tyre_data["right_front"]["pressure"], interactive=True)
            
            with gr.Row():
                with gr.Column():
                    left_rear_image = gr.Image(label="Left Rear tyre Pressure", type="filepath",mirror_webcam=False)
                    left_rear_pressure = gr.Textbox(label="Left Rear Pressure", value=default_tyre_data["left_rear"]["pressure"], interactive=True)
                with gr.Column():
                    right_rear_image = gr.Image(label="Right Rear tyre Pressure", type="filepath",mirror_webcam=False)
                    right_rear_pressure = gr.Textbox(label="Right Rear Pressure", value=default_tyre_data["right_rear"]["pressure"], interactive=True)
                
            # Automatically extract tyre pressure when an image is uploaded
            left_front_image.change(fn=process_tyre_pressure_image_left_front, inputs=left_front_image, outputs=left_front_pressure)
            right_front_image.change(fn=process_tyre_pressure_image_right_front, inputs=right_front_image, outputs=right_front_pressure)
            left_rear_image.change(fn=process_tyre_pressure_image_left_rear, inputs=left_rear_image, outputs=left_rear_pressure)
            right_rear_image.change(fn=process_tyre_pressure_image_right_rear, inputs=right_rear_image, outputs=right_rear_pressure)

            # tyre Condition Section
            gr.Markdown("<br><h2 style='text-align: center; color: #A17917;'>Tyre Condition</h2>")
            with gr.Row():
                with gr.Column():
                    left_front_condition_image = gr.Image(label="Left Front Tyre", type="filepath")
                    left_front_condition = gr.Radio(choices=["Good", "Ok", "Needs Replacement"], label="Left Front Condition", value=default_tyre_data["left_front"]["condition"], interactive=True)
                with gr.Column():
                    right_front_condition_image = gr.Image(label="Right Front Tyre", type="filepath")
                    right_front_condition = gr.Radio(choices=["Good", "Ok", "Needs Replacement"], label="Right Front Condition", value=default_tyre_data["right_front"]["condition"], interactive=True)
            
            with gr.Row():
                with gr.Column():
                    left_rear_condition_image = gr.Image(label="Left Rear Tyre", type="filepath")
                    left_rear_condition = gr.Radio(choices=["Good", "Ok", "Needs Replacement"], label="Left Rear Condition", value=default_tyre_data["left_rear"]["condition"], interactive=True)
                with gr.Column():
                    right_rear_condition_image = gr.Image(label="Right Rear Tyre", type="filepath")
                    right_rear_condition = gr.Radio(choices=["Good", "Ok", "Needs Replacement"], label="Right Rear Condition", value=default_tyre_data["right_rear"]["condition"], interactive=True)

            # Overall tyre Summary and Audio Input
            gr.Markdown("<h2 style='text-align: center; color: #A17917;'>Overall Tyre Summary</h2>")
            with gr.Row():
                tyre_audio_input = gr.Audio(label="Record Overall tyre Summary", type="filepath")
    
            # Exterior Summary (Initially hidden)
            summary_text_tyre = gr.Textbox("Summary will be displayed here after audio is recorded.", lines=5, visible=False)

            # Update the summary text and make the summary row visible after audio input
            async def update_summary_tyre(audio):
                result = await process_and_summarize_audio_tyre(audio)
                return gr.update(value=result, visible=True)

            tyre_audio_input.change(fn=update_summary_tyre, inputs=tyre_audio_input, outputs=summary_text_tyre)

            def change_tab_2():
                return gr.Tabs(selected=3)
            btn= gr.Button(value="Next")
            btn.click(change_tab_2,None,tabs)
             
        with gr.TabItem("Battery Inspection",id=3) as tab3:
            # Battery Inspection Section
            # Functions to process uploaded images for Battery details
            async def process_battery_image(image):
                out = await ai.get_ai_response(4, image)
                return out['make'], out['voltage']

            async def process_and_summarize_audio_battery(audio):
                out = await ai.get_ai_response(3, audio)
                return out['content']


            def battery_damage_change(damage_choice):
                # This function determines if the damage image and leak/rust options should be shown
                if damage_choice == "Yes":
                    return gr.update(visible=True), gr.update(visible=True)
                else:
                    return gr.update(visible=False), gr.update(visible=False)
            # Header
            gr.Markdown("<h1 style='text-align: center; color: #A17917;'>Battery Inspection</h1>")

            # Battery Details
            with gr.Row():
                with gr.Column():
                    battery_image = gr.Image(label="Battery Image", type="filepath", mirror_webcam=False)
                with gr.Column():
                    battery_make, battery_voltage = gr.Textbox(label="Battery Make", interactive=False), gr.Textbox(label="Battery Voltage", interactive=False)
            battery_image.change(process_battery_image, inputs=battery_image, outputs=[battery_make, battery_voltage])

            with gr.Row():
                with gr.Column():
                    gr.HTML('''
                    <label for="date-picker">Battery Replacement Date:</label>
                    <input type="date" id="date-picker"; style="width: 100%; padding: 10px; box-sizing: border-box;"/>
                    ''')
                with gr.Column():
                    battery_water_level = gr.Radio(choices=["Good", "Ok", "Low"], label="Battery Water Level", interactive=True)
                with gr.Column():
                    battery_damage = gr.Radio(choices=["Yes", "No"], label="Battery Damage", interactive=True)
            
            with gr.Row(visible=False) as damage_details_row:
                with gr.Column():
                    battery_damage_image = gr.Image(label="Attach Image if Damaged", type="filepath", mirror_webcam=False)
                with gr.Column():
                    leak_rust = gr.Radio(choices=["Yes", "No"], label="Leak/Rust in Battery", interactive=True)

            battery_damage.change(
                battery_damage_change,
                inputs=battery_damage,
                outputs=[damage_details_row, leak_rust]
            )

            # Battery Summary
            with gr.Row():
                battery_audio_input = gr.Audio(label="Record Battery Summary", type="filepath")
                
                # Exterior Summary (Initially hidden)
                summary_text_battery = gr.Textbox("Summary will be displayed here after audio is recorded.", lines=5, visible=False)

                # Update the summary text and make the summary row visible after audio input
                async def update_summary_battery(audio):
                    result = await process_and_summarize_audio_battery(audio)
                    return gr.update(value=result, visible=True)

                battery_audio_input.change(fn=update_summary_battery, inputs=battery_audio_input, outputs=summary_text_battery)
            def change_tab_3():
                return gr.Tabs(selected=4)
            btn= gr.Button(value="Next")
            btn.click(change_tab_3,None,tabs)

        with gr.TabItem("Exterior Inspection",id=4) as tab4:
            async def process_and_summarize_audio_exterior(audio):
                out = await ai.get_ai_response(3, audio)
                return out['content']

            def check_images_and_mark(images):
                # Mark "Rust/Dent/Damage" as "Yes" if images are uploaded
                return "Yes" if images else "No"

            # Global list to store gallery images
            gallery_images = []

            def capture_and_store_images(image):
                # Add the captured image to the gallery
                if image:
                    gallery_images.append(image)
                return gallery_images

            # Header
            gr.Markdown("<h1 style='text-align: center; color: #A17917;'>Exterior Inspection</h1>")
            
            # Image capture and gallery
            with gr.Row():
                with gr.Column():
                    capture_image = gr.Image(label="Capture Image", type="filepath", mirror_webcam=False)
                with gr.Column():
                    image_gallery = gr.Gallery(label="Captured Images", type="filepath", interactive=False)

            # Function to update gallery
            capture_image.change(
                fn=capture_and_store_images, 
                inputs=capture_image, 
                outputs=image_gallery
            )

            # Rust/Dent/Damage marking
            with gr.Row():
                with gr.Column():
                    rust = gr.Radio(choices=["Yes", "No"], label="Rust/Dent/Damage", value="No", interactive=False)
                    image_gallery.change(fn=check_images_and_mark, inputs=image_gallery, outputs=rust)

                with gr.Column():
                    oil_leak_suspension = gr.Radio(choices=["Yes", "No"], label="Oil Leak in Suspension", interactive=True)
            
            # Audio input and summary generation
            with gr.Row():
                exterior_audio_input = gr.Audio(label="Record Exterior Summary", type="filepath")
            
            # Exterior Summary (Initially hidden)
            summary_text_exterior = gr.Textbox("Summary will be displayed here after audio is recorded.", lines=5, visible=False)

            # Update the summary text and make the summary row visible after audio input
            async def update_summary_exterior(audio):
                result = await process_and_summarize_audio_exterior(audio)
                return gr.update(value=result, visible=True)

            exterior_audio_input.change(fn=update_summary_exterior, inputs=exterior_audio_input, outputs=summary_text_exterior)     
            def change_tab_4():
                return gr.Tabs(selected=5)
            btn= gr.Button(value="Next")
            btn.click(change_tab_4,None,tabs)     
            
        with gr.TabItem("Brakes Inspection",id=5) as tab5:
            async def process_and_summarize_audio_brakes(audio):
                out = await ai.get_ai_response(3, audio)
                return out['content']

            # Global list to store gallery images
            gallery_images_brakes = []

            def capture_and_store_brakes(image):
                # Add the captured image to the gallery
                if image:
                    gallery_images_brakes.append(image)
                return gallery_images_brakes
            # Header
            gr.Markdown("<h1 style='text-align: center; color: #A17917;'>Brakes Inspection</h1>")

            # Brake Details
            with gr.Row():
                with gr.Column():
                    brake_fluid_level = gr.Radio(choices=["Good", "Ok", "Low"], label="Brake Fluid Level", interactive=True)
                with gr.Column():
                    emergency_brake = gr.Radio(choices=["Good", "Ok", "Low"], label="Emergency Brake", interactive=True)
                    
            with gr.Row():
                with gr.Column():
                    front_brake_condition = gr.Radio(choices=["Good", "Ok", "Needs Replacement"], label="Front Brake Condition", interactive=True)
                with gr.Column():    
                    rear_brake_condition = gr.Radio(choices=["Good", "Ok", "Needs Replacement"], label="Rear Brake Condition", interactive=True)

            # Brakes Summary
            with gr.Row():
                    brakes_audio_input = gr.Audio(label="Record Brakes Summary", type="filepath")
                    
                    # Exterior Summary (Initially hidden)
                    summary_text_brakes = gr.Textbox("Summary will be displayed here after audio is recorded.", lines=5, visible=False)

                    # Update the summary text and make the summary row visible after audio input
                    async def update_summary_brakes(audio):
                        result = await process_and_summarize_audio_brakes(audio)
                        return gr.update(value=result, visible=True)

                    brakes_audio_input.change(fn=update_summary_brakes, inputs=brakes_audio_input, outputs=summary_text_brakes)


          
            with gr.Row():
                    with gr.Column():
                        capture_image_brakes = gr.Image(label="Add Images for Reference", type="filepath")
                    with gr.Column():
                        image_gallery_brakes = gr.Gallery(label="Captured Images", type="filepath", interactive=False)
                    
                    capture_image_brakes.change(
                        fn=capture_and_store_brakes, 
                        inputs=capture_image_brakes, 
                        outputs=image_gallery_brakes
                    )
            def change_tab_4():
                return gr.Tabs(selected=6)
            btn= gr.Button(value="Next")
            btn.click(change_tab_4,None,tabs)
            
        with gr.TabItem("Engine Inspection",id=6)as tab6:
            async def process_and_summarize_audio_engine(audio):
                out = await ai.get_ai_response(3, audio)
                return out['content']

            gallery_images_engine = []

            def capture_and_store_images_engine(image):
                # Add the captured image to the gallery
                if image:
                    gallery_images_engine.append(image)
                return gallery_images_engine
          
          # Header
            gr.Markdown("<h1 style='text-align: center; color: #A17917;'>Engine Inspection</h1>")

          # Engine Details
            with gr.Row():
                engine_damage = gr.Radio(choices=["Yes", "No"], label="Rust/Dents/Damage", interactive=True)
              
            with gr.Row():
                with gr.Column():
                    capture_image_engine = gr.Image(label="Get Images", type="filepath", mirror_webcam=False)
                with gr.Column():
                   image_gallery_engine = gr.Gallery(label="Captured Images", type="filepath", interactive=False)

          # Function to update gallery
            capture_image_engine.change(
                fn=capture_and_store_images_engine, 
                inputs=capture_image_engine, 
                outputs=image_gallery_engine
          )
            with gr.Row():
                with gr.Column():
                    engine_oil_condition = gr.Radio(choices=["Good", "Bad"], label="Engine Oil Condition", interactive=True)
                with gr.Column():
                    engine_oil_color = gr.Radio(choices=["Clean", "Brown", "Black"], label="Engine Oil Color", interactive=True)

            with gr.Row():
                brake_fluid_condition = gr.Radio(choices=["Good", "Bad"], label="Brake Fluid Condition", interactive=True)
                brake_fluid_color = gr.Radio(choices=["Clean", "Brown", "Black"], label="Brake Fluid Color", interactive=True)
                engine_oil_leak = gr.Radio(choices=["Yes", "No"], label="Any Oil Leak in Engine", interactive=True)

          # Engine Summary
            with gr.Row():
                engine_audio_input = gr.Audio(label="Record Engine Summary", type="filepath")
            
            # Exterior Summary (Initially hidden)
            summary_text_engine = gr.Textbox("Summary will be displayed here after audio is recorded.", lines=5, visible=False)

            # Update the summary text and make the summary row visible after audio input
            async def update_summary_engine(audio):
                result = await process_and_summarize_audio_engine(audio)
                return gr.update(value=result, visible=True)

            engine_audio_input.change(fn=update_summary_engine, inputs=engine_audio_input, outputs=summary_text_engine)
            def change_tab_5():
                return gr.Tabs(selected=7)
            btn= gr.Button(value="Next")
            btn.click(change_tab_5,None,tabs)

        with gr.TabItem("Customer Ack",id=7)as tab7 :
            async def process_and_summarize_audio_cust(audio):
                out = await ai.get_ai_response(5, audio)
                return out['content']

            gallery_images_customer = []

            def capture_and_store_images_customer(image):
                # Add the captured image to the gallery
                if image:
                    gallery_images_customer.append(image)
                return gallery_images_customer   
            gr.Markdown("<h1 style='text-align: center; color: #A17917;'>Customer Specifications & Acknowledgement</h1>")

            # Voice Feedback from customer
            with gr.Row():
                customer_audio_input = gr.Audio(label="Feedback from customer", type="filepath")
            
            # Exterior Summary (Initially hidden)
            summary_text_customer = gr.Textbox("Summary will be displayed here after audio is recorded.", lines=5, visible=False)

            # Update the summary text and make the summary row visible after audio input
            async def update_summary_customer(audio):
                result = await process_and_summarize_audio_cust(audio)
                return gr.update(value=result, visible=True)

            customer_audio_input.change(fn=update_summary_customer, inputs=customer_audio_input, outputs=summary_text_customer)

            with gr.Row():
                with gr.Column():
                    capture_image_customer = gr.Image(label="Additional Images by Customer", type="filepath")
                with gr.Column():
                    image_gallery_customer = gr.Gallery(label="Captured Images", type="filepath", interactive=False)

            # Function to update gallery
            capture_image_customer.change(
                fn=capture_and_store_images_customer, 
                inputs=capture_image_customer, 
                outputs=image_gallery_customer
            )
            
            with gr.Row():
                customer_signature = gr.Sketchpad(label="Customer Signature", height=400, width=300)  

            def change_tab_6():
                return gr.Tabs(selected=8)
            btn= gr.Button(value="Next")
            btn.click(change_tab_6,None,tabs)

        with gr.TabItem("Summary", id=8, visible=True) as tab8:
            gr.Markdown("<h1 style='text-align: center; color: #A17917;'>Summary of Inspection</h1>")
            
            pdf_output = gr.File(label="Download Inspection Report", visible=False)
            def copy(inspection_data):
                global global_data
                global_data = inspection_data.copy()

         
            def add_text_with_line_breaks(c, x, y, text, max_width):
                # Create a text object for the content
                text_object = c.beginText(x, y)
                text_object.setFont("Helvetica", 10)
                text_object.setTextOrigin(x, y)
                text_object.setWordSpace(1)
                text_object.setLeading(12)  # Adjust leading to control line spacing
                
                # Add line breaks for long text
                words = text.split()
                line = ""
                for word in words:
                    test_line = f"{line} {word}".strip()
                    # Measure text width using pdfmetrics
                    if pdfmetrics.stringWidth(test_line, "Helvetica", 10) > max_width:
                        text_object.textLine(line)
                        line = word
                    else:
                        line = test_line
                text_object.textLine(line)
                
                c.drawText(text_object)

            def generate_pdf(data):
                # Set the file path for the PDF
                file_path = f"inspection_report_{data['Header']['inspection_id']}.pdf"
                
                # Create a canvas object for the PDF
                c = canvas.Canvas(file_path, pagesize=letter)
                
                # Load and display the logo image
                logo_path = "report_logo.png"  # Path to your logo image
                if os.path.isfile(logo_path):
                    c.drawImage(logo_path, 40, 690, width=300, height=70)  # Adjust position and size
                
                # Line separator under the header
                c.setLineWidth(4)
                c.line(40, 770, 570, 770)
                
                # Add a gap between the logo and the dictionary contents
                y_position = 640  # Starting position after the logo
                
                # Header Section
                c.setFont("Helvetica-Bold", 16)
                c.setFillColor(colors.HexColor("#A17917"))
                c.drawString(40, y_position, "Inspection Report")
                c.setFillColor(colors.black)
                y_position -= 30
                
                # Job Inspection Details with Aliases
                header_aliases = {
                    "inspection_id": "Inspection ID",
                    "Inspector_name": "Inspector Name",
                    "Inspector_employee_id": "Inspector Employee ID",
                    "geo_input": "Geo Location",
                    "serial_number_input": "Serial Number",
                    "truck_model_input": "Truck Model",
                    "truck_odometer_input": "Odometer",
                    "Customer_name_input": "Customer Name",
                    "Cat_customer_id": "Customer ID",
                }
                
                c.setFont("Helvetica", 12)
                for key, alias in header_aliases.items():
                    c.setFont("Helvetica-Bold", 12)
                    c.drawString(40, y_position, f"{alias}:")
                    c.setFont("Helvetica", 12)
                    if key == "Summary":
                        # Skip summary here, will add it later
                        continue
                    c.drawString(180, y_position, data['Header'].get(key, ""))
                    y_position -= 30

                # Define initial Y position for sections
                y_position -= 20

                def add_overall_summary(summary_text):
                    nonlocal y_position
                    # Check if there's enough space to draw the summary content
                    if y_position < 200:
                        c.showPage()
                        y_position = 750

                    # Draw "Overall Summary" heading
                    c.setFont("Helvetica-Bold", 14)
                    c.setFillColor(colors.HexColor("#A17917"))
                    c.drawString(40, y_position, "Overall Summary")
                    c.setFillColor(colors.black)
                    y_position -= 15  # Reduce the gap between the header and the content
                    
                    # Draw the summary text
                    c.setFont("Helvetica", 10)
                    add_text_with_line_breaks(c, 40, y_position, summary_text, 520)
                    y_position -= 60  # Adjust for space used by the summary

                # Add Overall Summary
                overall_summary = data['Header'].get("Summary", "No summary provided.")
                add_overall_summary(overall_summary)

                # Helper function to add a section
                def add_section(title, content, aliases):
                    nonlocal y_position
                    # Check if there's enough space to draw the section title
                    if y_position < 100:
                        c.showPage()
                        y_position = 750
                    
                    # Draw section title
                    c.setFont("Helvetica-Bold", 14)
                    c.setFillColor(colors.HexColor("#A17917"))
                    c.drawString(40, y_position, title)
                    c.setFillColor(colors.black)
                    y_position -= 30

                    # Add section content
                    c.setFont("Helvetica", 10)
                    for key, alias in aliases.items():
                        value = content.get(key, "")
                        # Draw alias (key name)
                        c.setFont("Helvetica-Bold", 10)
                        c.drawString(60, y_position, f"{alias}:")
                        y_position -= 15

                        if isinstance(value, str):
                            # Check if the value is a path to an image
                            if os.path.isfile(value) and value.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                                # Load and draw the image
                                c.drawImage(value, 80, y_position - 100, width=100, height=75)  # Adjust position and size
                                y_position -= 100  # Adjust for image height
                            else:
                                # Handle long text wrapping
                                add_text_with_line_breaks(c, 80, y_position, value, 460)
                        else:
                            c.drawString(80, y_position, "[Image/Audio Data]")
                            
                        y_position -= 20
                        # Check if we need to create a new page
                        if y_position < 50:
                            c.showPage()
                            y_position = 750
                            # Redraw the title on the new page
                            c.setFont("Helvetica-Bold", 14)
                            c.setFillColor(colors.HexColor("#A17917"))
                            c.drawString(40, y_position, title)
                            c.setFillColor(colors.black)
                            y_position -= 30

                # Add Sections
                add_section("Tyres", data['Tyres'], {
                    "left_front_image": "Left Front Image",
                    "left_front_pressure": "Left Front Pressure",
                    "right_front_image": "Right Front Image",
                    "right_front_pressure": "Right Front Pressure",
                    "left_rear_image": "Left Rear Image",
                    "left_rear_pressure": "Left Rear Pressure",
                    "right_rear_image": "Right Rear Image",
                    "right_rear_pressure": "Right Rear Pressure",
                    "left_front_condition_image": "Left Front Condition Image",
                    "left_front_condition": "Left Front Condition",
                    "right_front_condition_image": "Right Front Condition Image",
                    "right_front_condition": "Right Front Condition",
                    "left_rear_condition_image": "Left Rear Condition Image",
                    "left_rear_condition": "Left Rear Condition",
                    "right_rear_condition_image": "Right Rear Condition Image",
                    "right_rear_condition": "Right Rear Condition",
                    "tyre_audio_input": "Tyre Audio",
                    "summary_text_tyre": "Summary (Tyres)"
                })

                add_section("Battery", data['Battery'], {
                    "battery_image": "Battery Image",
                    "battery_make": "Battery Make",
                    "battery_voltage": "Battery Voltage",
                    "battery_water_level": "Battery Water Level",
                    "battery_damage": "Battery Damage",
                    "battery_damage_image": "Battery Damage Image",
                    "leak_rust": "Leak/Rust",
                    "battery_audio_input": "Battery Audio",
                    "summary_text_battery": "Summary (Battery)"
                })

                add_section("Exterior", data['Exterior'], {
                    "capture_image": "Capture Image",
                    "image_gallery": "Image Gallery",
                    "rust": "Rust",
                    "oil_leak_suspension": "Oil Leak Suspension",
                    "exterior_audio_input": "Exterior Audio",
                    "summary_text_exterior": "Summary (Exterior)"
                })

                add_section("Brakes", data['Brakes'], {
                    "brake_fluid_level": "Brake Fluid Level",
                    "emergency_brake": "Emergency Brake",
                    "front_brake_condition": "Front Brake Condition",
                    "rear_brake_condition": "Rear Brake Condition",
                    "brakes_audio_input": "Brakes Audio",
                    "summary_text_brakes": "Summary (Brakes)",
                    "capture_image_brakes": "Brakes Capture Image",
                    "image_gallery_brakes": "Brakes Image Gallery"
                })

                add_section("Engine", data['Engine'], {
                    "engine_damage": "Engine Damage",
                    "engine_oil_condition": "Engine Oil Condition",
                    "engine_oil_color": "Engine Oil Color",
                    "brake_fluid_condition": "Brake Fluid Condition",
                    "brake_fluid_color": "Brake Fluid Color",
                    "engine_oil_leak": "Engine Oil Leak",
                    "capture_image_engine": "Engine Capture Image",
                    "image_gallery_engine": "Engine Image Gallery",
                    "engine_audio_input": "Engine Audio",
                    "summary_text_engine": "Summary (Engine)"
                })

                add_section("Customer", data['Customer'], {
                    "customer_audio_input": "Customer Audio",
                    "summary_text_customer": "Summary (Customer)"
                })
                # Save the PDF
                c.save()
                print(f"PDF generated: {file_path}")
                return file_path
            
            async def on_submit_button_click(*inputs):
                # Collect inspection data
                inspection_data = collect_inspection_data(*inputs)
                copy(inspection_data)
                
                #Overall Summary 

                out = await ai.get_ai_response(6, str(global_data))
                global_data['Header']['Summary']=out['content']

                pdf_path = generate_pdf(global_data)
                return {
                    tab1: gr.update( visible=False),
                    tab2: gr.update( visible=False),
                    tab3: gr.update( visible=False),
                    tab4: gr.update( visible=False),
                    tab5: gr.update( visible=False),
                    tab6: gr.update( visible=False),
                    tab7: gr.update( visible=False),
                    
                    pdf_output: gr.update(value=pdf_path, visible=True)
                    
                }

            btn= gr.Button(value="Submit")
            btn.click(on_submit_button_click, 
                    inputs=[
                        inspection_id_input, Inspector_name_input, Inspector_employee_id,
                        geo_input, serial_number_input, truck_model_input, truck_odometer_input,
                        Customer_name_input, Cat_customer_id,
                        left_front_image, left_front_pressure, right_front_image, right_front_pressure,
                        left_rear_image, left_rear_pressure, right_rear_image, right_rear_pressure,
                        left_front_condition_image, left_front_condition, right_front_condition_image,
                        right_front_condition, left_rear_condition_image, left_rear_condition,
                        right_rear_condition_image, right_rear_condition, tyre_audio_input, summary_text_tyre,
                        battery_image, battery_make, battery_voltage, battery_water_level, battery_damage,
                        battery_damage_image, leak_rust, battery_audio_input, summary_text_battery,
                        capture_image, image_gallery, rust, oil_leak_suspension, exterior_audio_input,
                        summary_text_exterior, brake_fluid_level, emergency_brake, front_brake_condition,
                        rear_brake_condition, brakes_audio_input, summary_text_brakes, capture_image_brakes,
                        image_gallery_brakes, engine_damage, engine_oil_condition, engine_oil_color,
                        brake_fluid_condition, brake_fluid_color, engine_oil_leak, capture_image_engine,
                        image_gallery_engine, engine_audio_input, summary_text_engine, customer_audio_input,
                        summary_text_customer
                    ],
                    
                    outputs=[tab1,tab2,tab3,tab4,tab5,tab6,tab7,pdf_output])
        

demo.launch()