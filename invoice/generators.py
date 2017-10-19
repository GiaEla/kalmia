import os

import pdfkit
from django.conf import settings
from django.template.loader import render_to_string


def create_pdf(template, context, dir_name, file_name):

    html_string = render_to_string(template, context)

    relative_path = dir_name + '/' + file_name

    file_path = os.path.join(settings.BASE_DIR, relative_path)

    pdfkit.from_string(html_string, file_path)

    return file_path
