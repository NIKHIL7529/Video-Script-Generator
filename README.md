# Video Script Generator - README

## Overview

This is a **Video Script Generator** web application built using **Django**, **Tailwind CSS**, **Python**, **HTML**, and **JavaScript**. The application allows users to generate, save, and export video scripts. The user can input prompts in any language, and the app will generate scripts in that language. It also supports file uploads (e.g., .txt, .pdf) to extract and append content to the generated script. For images, optional OCR (Optical Character Recognition) is used to extract text. The generated scripts can be saved, retrieved, and exported as `.txt` or `.pdf` files. The app is fully responsive, working well on both mobile and desktop devices.

---

## Known Issues

- **OCR for Images**: The OCR feature relies on an external API for image text extraction. If the image quality is poor or the text is unclear, the OCR may not work as expected. For this reason I ahve used Tesseract OCR. But I have also written commented external OCR API code.
- **Multi-Language Generation**: The script generation may not always be perfect for all languages, depending on the quality of the input.

---

## Features

- **Multi-Language Support**: You can input prompts in any language, and the generated script will be in the same language.
- **File Handling**: Extracts and appends text from uploaded `.txt` and `.pdf` files. For images, it uses Tesseract OCR to extract text.
- **Save and Retrieve Scripts**: Users can save generated scripts and retrieve previously saved scripts from the `/saved-scripts` URL.
- **Export Options**: Download generated scripts in `.txt` or `.pdf` format.
- **Responsive Design**: The application is designed using Tailwind CSS to be fully responsive, working well on both mobile and desktop devices.

---

## Prerequisites

1. **Python 3.8+**  
   Ensure that you have Python installed on your local machine. You can download it from [here](https://www.python.org/downloads/).

2. **Django 3.x+**  
   The web application is built on Django. You can install it using pip:

   ```bash
   pip install django
   ```

3. **Tesseract OCR**  
   The application uses **Tesseract OCR** for text extraction from images. To install it on Windows, follow these steps:
   
   - Download the Tesseract installer from [here](https://github.com/UB-Mannheim/tesseract/wiki).
   - Install Tesseract.
   - After installation, add the Tesseract binary path (e.g., `C:\Program Files\Tesseract-OCR`) to your system's PATH.

4. **XAI API Key**  
   This project uses the **XAI API** for generating scripts. You will need an API key from XAI. Follow their API documentation to obtain the key.

---

## Setting Up the Project Locally

### 1. Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/your-username/video-script-generator.git
cd video-script-generator
```

### 2. Set Up a Virtual Environment

It's recommended to use a virtual environment to manage project dependencies. To create and activate a virtual environment:

```bash
# Install virtualenv if you don't have it
pip install virtualenv

# Create a virtual environment
virtualenv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Project Dependencies

With the virtual environment activated, install the required dependencies:

```bash
pip install -r requirements.txt
```

The `requirements.txt` file contains all the necessary dependencies, including Django, Tailwind, and Tesseract.

### 4. Set Up the `.env` File

Create a `.env` file in the root of the project directory and add your **XAI API key** and other necessary configurations. Example:

```plaintext
XAI_API_KEY=your-xai-api-key
TESSERACT_PATH=C:\Program Files\Tesseract-OCR\tesseract.exe  # Adjust if needed
```

Make sure to replace `your-xai-api-key` with your actual API key from XAI and specify the correct path to Tesseract if needed.

### 5. Run Database Migrations

Before running the application, make sure to apply the database migrations:

```bash
python manage.py migrate
```

This will set up the necessary database tables.

### 6. Start the Development Server

Now you can run the Django development server:

```bash
python manage.py runserver
```

Your application will be running at `http://127.0.0.1:8000/`. You can open this URL in your web browser.

---

## Application Usage

### 1. **Home Page**

The home page contains a form where you can enter a prompt for the video script. You can also optionally provide an external link or upload files (.txt, .pdf, .jpg, .png). The script will be generated based on your input.

- **Language Support**: The prompt can be in any language. The app will detect and respond in that language.
- **File Handling**: Upload `.txt` or `.pdf` files, or an image (JPEG/PNG). The text will be extracted and appended to the generated script.

### 2. **Saved Scripts**

To access previously saved scripts, navigate to the `/saved-scripts` URL:

```
http://127.0.0.1:8000/saved-scripts/
```

This page allows users to view and manage previously saved scripts.

### 3. **Export Options**

Once a script is generated, you can download it in two formats:

- **Download as `.txt`**: Saves the script as a plain text file.
- **Download as `.pdf`**: Saves the script as a PDF file.

### 4. **OCR**

If you upload an image (JPEG/PNG), the application will use Tesseract OCR to extract text from the image and append it to the generated script.

---

## Project Structure

```
video-script-generator/
│
├── manage.py                   # Django project management script
├── video_script_generator/      # Django app containing the project logic
│   ├── __init__.py
│   ├── settings.py              # Django settings file
│   ├── urls.py                  # URL routing for the app
│   ├── views.py                 # Views for handling requests
│   ├── models.py                # Models for the application (e.g., saved scripts)
│   └── static/                  # Static files (e.g., Tailwind CSS, JS)
│
├── requirements.txt             # List of Python dependencies
├── .env                         # Environment variables (API keys, paths, etc.)
└── README.md                    # Project documentation (this file)
```

---


## Contributing

Feel free to fork the repository, create an issue, or submit a pull request if you have improvements or bug fixes. Please follow the standard GitHub pull request process.


---

## Acknowledgments

- **Django**: The backend framework used to build the application.
- **Tailwind CSS**: A utility-first CSS framework for building modern, responsive UIs.
- **Tesseract OCR**: Used for extracting text from images.
- **XAI API**: Used for generating the video scripts.

---

This README provides a step-by-step guide for setting up, running, and using the Video Script Generator project locally. Follow the instructions carefully, and you'll be able to generate, save, and export video scripts efficiently.
