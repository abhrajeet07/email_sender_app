import os
import pandas as pd
from django.conf import settings
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from .forms import EmailForm
from django.contrib import messages

def send_email(request):
    if request.method == 'POST':
        form = EmailForm(request.POST, request.FILES)
        if form.is_valid():
            email_file = form.cleaned_data['email_file']
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['body']
            
            # Ensure MEDIA_ROOT directory exists
            if not os.path.exists(settings.MEDIA_ROOT):
                os.makedirs(settings.MEDIA_ROOT)

            # Save the uploaded file
            email_file_path = os.path.join(settings.MEDIA_ROOT, email_file.name)

            with open(email_file_path, 'wb+') as destination:
                for chunk in email_file.chunks():
                    destination.write(chunk)

            try:
                # Read emails from Excel file
                df = pd.read_excel(email_file_path)
                if 'Email' not in df.columns:
                    messages.error(request, "The uploaded file does not contain an 'Email' column.")
                    return redirect('send_email')
                
                emails = df['Email'].dropna().tolist()

                for recipient_email in emails:
                    email = EmailMessage(
                        subject,
                        body,
                        settings.EMAIL_HOST_USER,
                        [recipient_email]
                    )
                    email.send()
                
                messages.success(request, "Emails sent successfully!")
            except Exception as e:
                messages.error(request, f"An error occurred: {e}")
            finally:
                # Remove the uploaded file after processing
                if os.path.exists(email_file_path):
                    os.remove(email_file_path)

            return redirect('send_email')
    else:
        form = EmailForm()

    return render(request, 'email_app/send_email.html', {'form': form})
