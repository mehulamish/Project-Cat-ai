# Gradio Job Inspection Form

## Overview

This project is a Gradio-based web application designed for job inspection reporting. It allows users to input various inspection data related to trucks, batteries, tyres, brakes, engines, and exterior conditions. The data can include text entries, images, audio recordings, and other multimedia elements. The application also supports generating JSON representations of the inspection data.

## Features

- **Data Collection**: Capture and submit detailed inspection data including images, text, and audio inputs.
- **Tabbed Interface**: Navigate between different sections of the job inspection form.
- **Customizable Theme**: Provides a custom theme and CSS for a personalized user experience.
- **Dynamic Image Handling**: Encode and display images in the interface.
- **AI Integration**: Use AI tools for processing image data.

## Installation

To get started with this project, you need to have Python installed on your system. You can then install the required dependencies using pip:

```bash
pip install gradio reportlab geocoder
```

## Usage

1. **Run the Application**:
   Execute the script to start the Gradio interface:

   ```bash
   python your_script_name.py
   ```

2. **Navigate the Interface**:
   - **Job Inspection**: Fill out the job inspection form with the required details.
   - **Tabs**: Use the tabs to navigate between different sections of the form.

3. **Image Handling**:
   Ensure that you have the `cat-logo.png` image file in the same directory as the script for the logo to display properly.

## Customization

You can customize the theme and CSS by modifying the `custom_theme` and `custom_css` variables in the script. Adjust these settings to fit your design preferences.

## Example

Here's how the form might look when filled out:

- **Header**: Input details like inspection ID, inspector name, and customer information.
- **Tyres**: Upload images and enter details related to tyre conditions.
- **Battery**: Upload battery-related images and enter battery specifications.
- **Exterior**: Upload exterior images and input details about rust and leaks.
- **Brakes**: Enter brake fluid levels, conditions, and other relevant details.
- **Engine**: Input engine-related data and upload engine images.
- **Customer**: Upload customer audio recordings and input additional customer-related information.

## Development

For development purposes, you may want to:
- Modify the form fields and data structure.
- Integrate additional AI tools or services.
- Adjust the PDF generation settings for customized reports.

## Contributing

Feel free to fork the repository and contribute to the project. Please make sure to follow the existing code style and provide clear commit messages.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
