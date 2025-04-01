
# InvoiceExtractor_NLP

![Invoice Extraction Process](https://github.com/user-attachments/assets/264aee95-0f9f-4f64-9b16-88ae990653cf)


## Overview

**InvoiceExtractor_NLP** is a Gemini-based NLP project designed to automatically extract information from invoices and store it in an Excel file. This tool leverages advanced Natural Language Processing (NLP) techniques to parse and interpret invoice data, making it easier to manage financial records.

## Features

- **Automatic Invoice Extraction**: Automatically extracts relevant data from invoices with high accuracy.
- **Excel Export**: Stores extracted data in a structured Excel file for easy access and analysis.
- **NLP-Powered**: Uses state-of-the-art NLP algorithms to understand and process invoice content.
- **User-Friendly**: Simple and intuitive interface for easy operation.

![Invoice Extraction Results](https://github.com/user-attachments/assets/bfe34591-ffc3-44c6-af68-582d27d11d6f)


## Installation

To get started with InvoiceExtractor_NLP, follow these installation steps:

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/fairoz-539/InvoiceExtractor_NLP.git
    cd InvoiceExtractor_NLP
    ```

2. **Install Dependencies**:
    Ensure you have Python and pip installed. Then, install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. **Set Up the Environment**:
    Create a `.env` file in the root directory and add any necessary environment variables as specified in the project documentation.

## Usage

To use the InvoiceExtractor_NLP tool, follow these steps:

1. **Prepare Your Invoices**:
    Ensure your invoices are in a supported format (e.g., PDF, JPEG).

2. **Run the Extraction Script**:
    Execute the main script to start the extraction process:
    ```bash
    python app.py
    ```

3. **View the Results**:
    The extracted data will be saved in an Excel file in the `invoices_excel` directory. Open the file to view the structured invoice data.

![Invoice Extraction](https://github.com/user-attachments/assets/b0cb8b44-5041-4ef9-bba4-15ee7ab72eb7)


## How It Works

InvoiceExtractor_NLP uses a combination of NLP techniques to process and extract information from invoices:

1. **Text Extraction**: Extracts raw text from invoices using OCR (Optical Character Recognition) if needed.
2. **Text Parsing**: Parses the extracted text to identify key information such as invoice number, date, total amount, and line items.
3. **Data Structuring**: Structures the parsed data into a predefined format and stores it in an Excel file.

### Detailed Explanation of the Code

- **Flask Application**: The project uses Flask to create a web server that handles file uploads and data extraction.
- **Image Encoding**: Images are encoded to base64 format for processing.
- **NLP Processing**: The encoded images are sent to the Gemini API for NLP-based data extraction.
- **Data Parsing**: Extracted information is parsed and converted into a JSON object.
- **Data Flattening**: Nested data structures are flattened for easier storage in Excel.
- **Excel Management**: Extracted data is saved to an Excel file, with separate sheets for invoice details and items.

## Routes

- **Home Route (`/`)**: Renders the home page.
- **Upload Route (`/upload`)**: Handles file uploads and initiates data extraction.
- **Invoices Route (`/invoices`)**: Fetches and returns all extracted invoices and items in JSON format.

## Contributing

We welcome contributions from the community. If you'd like to contribute to InvoiceExtractor_NLP, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes.
4. Open a pull request with a detailed description of your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contact

If you have any questions or need further assistance, please feel free to contact us at [fairosahmed.ai@gmail.com](mailto:fairosahmed.ai@gmail.com).
