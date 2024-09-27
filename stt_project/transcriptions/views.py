from django.shortcuts import render
from django import forms
import assemblyai as aai


class UploadFileForm(forms.Form):
    audio_file = forms.FileField()


def index(request):
    context = None
    print("Path", request.path)
    print("Path", request.get_host())
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if not form.is_valid():
            context = {"error": "Provide a valid file"}
            return render(request, "transcriptions/index.html", context)

        try:
            # Get file
            file = request.FILES['audio_file']

            # Transcribe with AssemblyAI. You can submit file-type objects directly
            transcriber = aai.Transcriber()
            transcript = transcriber.transcribe(file.file)

            # Close file
            file.close()

            # Return transcript or error
            if transcript.error:
                context = {"error": transcript.error}
            else:
                context = {"transcript": transcript.text}
        except Exception as e:
            context = {"error": str(e)}

    return render(request, "transcriptions/index.html", context)
