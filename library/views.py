from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Author, Book, Member, Loan
from django.db.models import Count, Q
from .serializers import AuthorSerializer, BookSerializer, MemberSerializer, LoanSerializer
from rest_framework.decorators import action
from django.utils import timezone
from .tasks import send_loan_notification

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer

    @action(detail=True, methods=['post'])
    def loan(self, request, pk=None):
        book = self.get_object()
        if book.available_copies < 1:
            return Response({'error': 'No available copies.'}, status=status.HTTP_400_BAD_REQUEST)
        member_id = request.data.get('member_id')
        try:
            member = Member.objects.get(id=member_id)
        except Member.DoesNotExist:
            return Response({'error': 'Member does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
        loan = Loan.objects.create(book=book, member=member)
        book.available_copies -= 1
        book.save()
        send_loan_notification.delay(loan.id)
        return Response({'status': 'Book loaned successfully.'}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def return_book(self, request, pk=None):
        book = self.get_object()
        member_id = request.data.get('member_id')
        try:
            loan = Loan.objects.get(book=book, member__id=member_id, is_returned=False)
        except Loan.DoesNotExist:
            return Response({'error': 'Active loan does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
        loan.is_returned = True
        loan.return_date = timezone.now().date()
        loan.save()
        book.available_copies += 1
        book.save()
        return Response({'status': 'Book returned successfully.'}, status=status.HTTP_200_OK)

class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

    @action(detail=True, methods=['get'])
    def top_active(self, request):
        top_members = Member.objects.annotate(
            active_loans=Count(
                'loans',
                filter=F('loans__is_returned') == False
            )
        ).filter(
            active_loans__gt=0
        ).order_by(
            '-active_loans'
        )[:5]

        serializer = TopActiveMemberSerializer(top_members, many=True)
        return Response(serializer.data)

class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    @action(detail=True, methods=['post'])
    def extend_due_date(self, request, pk=None):
        today = timezone.now().date()
        loan = self.get_object()
        if loan.is_returned:
            return Response({'error': 'Loan has already been returned.'}, status=status.HTTP_400_BAD_REQUEST)

        if loan.due_date < today:
            return Response({'error': 'Due date has already passed.'}, status=status.HTTP_400_BAD_REQUEST)


        additional_days = request.data.get('additional_days', 7)
        try:
            additional_days = int(additional_days)
            if additional_days <=0:
                return Response({'error': 'Additional days must be a positive integer.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({'error': 'Additional days must be a positive integer.'}, status=status.HTTP_400_BAD_REQUEST)
        loan.due_date += timezone.timedelta(days=additional_days)
        loan.save()

        serializer = self.serializer_class(loan)
        return Response({
            'message': 'Due date extended successfully.',
            'data': serializer.data
        }, status=status.HTTP_200_OK)