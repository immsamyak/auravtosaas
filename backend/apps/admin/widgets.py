from django.forms.widgets import ClearableFileInput

class TailwindImageWidget(ClearableFileInput):
    template_name = 'admin/widgets/image_input.html'
