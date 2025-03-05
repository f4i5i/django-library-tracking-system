from celery import shared_task
from .models import Loan
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_loan_notification(loan_id):
    try:
        loan = Loan.objects.get(id=loan_id)
        member_email = loan.member.user.email
        book_title = loan.book.title
        send_mail(
            subject='Book Loaned Successfully',
            message=f'Hello {loan.member.user.username},\n\nYou have successfully loaned "{book_title}".\nPlease return it by the due date.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[member_email],
            fail_silently=False,
        )
    except Loan.DoesNotExist:
        pass

@shared_task
def check_overdue_loans():
    today = timezone.now().date()
    overdue_loans = Loan.objects.filter(due_date__lt=today, is_returned=False)
    for loan in overdue_loans:
        try:
            send_mail(
                subject='Overdue Book Reminder',
                message=f'Hello {loan.member.user.username},\n\nThis is a reminder that the book "{loan.book.title}" is overdue. Please return it as soon as possible.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[loan.member.user.email],
                fail_silently=False,
            )
        except Exception as e:
            print(f'Error sending overdue reminder for loan{loan.id}: {str(e)}')

