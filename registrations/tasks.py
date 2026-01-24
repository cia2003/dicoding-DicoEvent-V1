from celery import shared_task
from django.core.mail import EmailMultiAlternatives

@shared_task
def send_registration_confirmation_email(user_email, username, registration_id, time=None):
    subject = 'Konfirmasi Pemesanan Tiket di DicoEvent'

    # HTML formatted version
    if time == None:
        text_content = f'''Halo {username},

        Terima kasih telah melakukan pendaftaran di DicoEvent. Berikut adalah detail pendaftaran Anda:
        ID Pendaftaran: {registration_id}

        Segera selesaikan pembayaran untuk mengamankan tiket Anda.

        Terima kasih,
        Tim DicoEvent


        Pesan ini dibuat secara otomatis, mohon tidak membalas email ini.
        '''

        html_content = f"""
            <html>
            <body style="font-family: Arial, sans-serif; color: #333;">
                <div style="max-width: 600px; margin: auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
                    <h2 style="color: #E50914; text-align: center;">Konfirmasi Pemesanan Tiket di DicoEvent</h2>
                    <p>Halo <strong>{username}</strong>,</p>
                    <p>Terima kasih telah melakukan pendaftaran di <strong>DicoEvent</strong>. Berikut adalah <strong>detail pendaftaran Anda:</strong></p>
                    <p style="background-color: #f8f8f8; padding: 10px; border-radius: 5px;">
                        <strong>ID Pendaftaran:</strong> {registration_id}
                    </p>
                    <p><strong>Segera</strong> selesaikan pembayaran untuk mengamankan tiket Anda.</p>
                    <br>
                    <p style="font-size: 12px; color: #777; text-align: center;">
                        Pesan ini dikirim secara otomatis. Mohon tidak membalas pesan ini.
                    </p>
                    <p style="font-size: 12px; color: #777; text-align: center;">
                        <strong>Tim DicoEvent</strong>
                    </p>
                </div>
            </body>
            </html>
        """
    else:
        text_content = f'''Halo {username},

        Terima kasih telah melakukan pendaftaran di DicoEvent. Berikut adalah detail pendaftaran Anda:
        ID Pendaftaran: {registration_id}

        Anda memiliki waktu {time} jam. Segera selesaikan pembayaran untuk mengamankan tiket Anda.

        Terima kasih,
        Tim DicoEvent


        Pesan ini dibuat secara otomatis, mohon tidak membalas email ini.
        '''
        html_content = f"""
            <html>
            <body style="font-family: Arial, sans-serif; color: #333;">
                <div style="max-width: 600px; margin: auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
                    <h2 style="color: #E50914; text-align: center;">Konfirmasi Pemesanan Tiket di DicoEvent</h2>
                    <p>Halo <strong>{username}</strong>,</p>
                    <p>Terima kasih telah melakukan pendaftaran di <strong>DicoEvent</strong>. Berikut adalah <strong>detail pendaftaran Anda:</strong></p>
                    <p style="background-color: #f8f8f8; padding: 10px; border-radius: 5px;">
                        <strong>ID Pendaftaran:</strong> {registration_id}
                    </p>
                    <p>Anda memiliki waktu <strong>{time}</strong> jam. <strong>Segera</strong> selesaikan pembayaran untuk mengamankan tiket Anda.</p>
                    <br>
                    <p style="font-size: 12px; color: #777; text-align: center;">
                        Pesan ini dikirim secara otomatis. Mohon tidak membalas pesan ini.
                    </p>
                    <p style="font-size: 12px; color: #777; text-align: center;">
                        <strong>Tim DicoEvent</strong>
                    </p>
                </div>
            </body>
            </html>
            """
 
    email = EmailMultiAlternatives(subject, text_content, 'no-reply@dicoeventticket.com', [user_email])
    email.attach_alternative(html_content, "text/html")
    email.send()
    return f'Email sent to {user_email}'