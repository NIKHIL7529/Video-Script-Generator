import os
import requests
import json
from django.shortcuts import render
from django.http import JsonResponse
from .models import Script
import pytesseract
from PIL import Image
from PyPDF2 import PdfReader
from reportlab.lib.pagesizes import letter
from bs4 import BeautifulSoup
from openai import OpenAI
from dotenv import load_dotenv
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph

load_dotenv()
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
XAI_API_KEY = os.getenv("API_KEY")

client = OpenAI(
    api_key=XAI_API_KEY,
    base_url="https://api.x.ai/v1",
)

def home(request):
    scripts = Script.objects.all().order_by('-created_at')[:5]
    return render(request, 'generator/Home.html', {'scripts': scripts})

def generate_script_from_api(prompt):
    """
    Sends the prompt to the x.ai API and returns the generated script.
    """
    try:
        max_tokens = 500
        response = client.chat.completions.create(
            model="grok-2-1212",  
            messages=[
                {"role": "system", "content": "You are Grok, a chatbot inspired by the Hitchhiker's Guide to the Galaxy."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=max_tokens,
        )
        script = response.choices[0].message.content
        return script
    except Exception as e:
        print(f"Error generating script: {e}")
        return "Error generating script from the AI."

def generate_script(request):
    if request.method == "POST":
        try:                  
            prompt = request.POST.get('prompt', '')
            external_link = request.POST.get('external_link', '')
            files = request.FILES.getlist('files', [])
            extracted_text = ""

            if files:
                for file in files:
                    if file.name.endswith('.txt'):
                        extracted_text += file.read().decode('utf-8') 
                    elif file.name.endswith('.pdf'):
                        extracted_text += extract_text_from_pdf(file)
                    elif file.name.endswith('.jpg') or file.name.endswith('.png'):
                        extracted_text += extract_text_from_image(file)
                    else:
                        return JsonResponse({'error': 'Unsupported file type. Only .txt, .pdf, .jpg, and .png are allowed.'}, status=400)
                prompt += extracted_text

            if not prompt and not external_link:
                return JsonResponse({'error': 'Prompt is required'}, status=400)
            
            if external_link:
                prompt += extract_text_from_link(external_link)
            print(prompt)
            script = generate_script_from_api(prompt)

            return JsonResponse({"script": script, "prompt": prompt})
        except Exception as e:
            print(f"Error generating script: {e}")
            return JsonResponse({'error': 'Error generating script'}, status=500)
    return render(request, 'generator/Home.html')

def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# def extract_text_from_image(image):
#     OCR_API_KEY = os.getenv('OCR_API_KEY')
#     files = {'image': image.file.read()}
#     data = {
#         'apikey': OCR_API_KEY,
#         'language': 'eng',  # You can specify other languages as well
#     }

#     response = requests.post(OCR_SPACE_API_URL, files=files, data=data)

#     if response.status_code == 200:
#         result = response.json()
#         # Check if OCR returned any text
#         if result.get('ParsedResults'):
#             text = result['ParsedResults'][0]['ParsedText']
#             return text
#         else:
#             return "No text detected in image."
#     else:
#         raise Exception(f"Error from OCR API: {response.status_code} - {response.text}")
    
def extract_text_from_image(image):
    img = Image.open(image)
    text = pytesseract.image_to_string(img)
    return text

def extract_text_from_link(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    metas = soup.find_all('meta', attrs={'name': 'description'})
    if metas:
        return metas[0].attrs['content'] 
    else:
        return soup.get_text()

def download_script_txt(request):
    script_content = request.GET.get('script', '')

    if not script_content:
        return HttpResponse("No script content provided", status=400)

    response = HttpResponse(script_content, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="generated_script.txt"'
    return response

def download_script_pdf(request):
    script_content = request.GET.get('script', '')

    if not script_content:
        return HttpResponse("No script content provided", status=400)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="generated_script.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
    custom_style = ParagraphStyle(name='CustomStyle', fontSize=10, leading=12, spaceAfter=12, textColor=colors.black)

    paragraph = Paragraph(script_content, style=custom_style)
    doc.build([paragraph])
    return response

def save_script(request):
    if request.method == "POST":
        data = json.loads(request.body)
        prompt = data.get('prompt', '')
        script = data.get('script', '')

        if not prompt or not script:
            return JsonResponse({'error': 'Prompt and script are required'}, status=400)
        new_script = Script.objects.create(prompt=prompt, script=script)
        return JsonResponse({'message': 'Script saved successfully', 'id': new_script.id})
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def get_saved_scripts(request):
    page = int(request.GET.get('page', 1))
    scripts_per_page = 5
    scripts = Script.objects.all().order_by('-created_at')[(page - 1) * scripts_per_page:page * scripts_per_page]
    return render(request, 'generator/saved.html', {'scripts': scripts, 'page': page})
