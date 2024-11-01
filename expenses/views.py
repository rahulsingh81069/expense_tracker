from django.db.models import Sum
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Expense, Split, User
from .serializers import ExpenseSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def get_permissions(self):
        # Allow any user (authenticated or not) to create a new user
        if self.action == 'create':
            return [AllowAny()]
        # Require authentication for all other actions
        return [IsAuthenticated()]

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='user-balance/(?P<user_id>[^/.]+)')
    def user_balance(self, request, user_id=None):
        # Amount owed by the user (equal, exact, or percentage)
        amount_owed_by_user = 0
        user_splits = Split.objects.filter(user_id=user_id).exclude(expense__payer_id=user_id)

        for split in user_splits:
            if split.expense.split_method == 'percentage':
                amount_owed_by_user += (split.percentage or 0) * split.expense.amount / 100
            else:
                amount_owed_by_user += split.amount or 0

        # Amount owed to the user as payer
        expenses_as_payer = Expense.objects.filter(payer_id=user_id)
        amount_owed_to_user = 0

        for expense in expenses_as_payer:
            splits = Split.objects.filter(expense=expense).exclude(user_id=user_id)
            for split in splits:
                if expense.split_method == 'percentage':
                    amount_owed_to_user += (split.percentage or 0) * expense.amount / 100
                else:
                    amount_owed_to_user += split.amount or 0

        # Calculate net balance
        net_balance = amount_owed_to_user - amount_owed_by_user

        return Response({
            "user_id": user_id,
            "amount_owed_by_user": amount_owed_by_user,
            "amount_owed_to_user": amount_owed_to_user,
            "net_balance": net_balance
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], url_path='balance-sheet')
    def balance_sheet(self, request):
        users = User.objects.all()
        balance_sheet = []

        for user in users:
            
            # Amount owed by the user (all splits where user is not the payer)
            amount_owed_by_user = 0
            user_splits = Split.objects.filter(user=user).exclude(expense__payer=user)
            
            for split in user_splits:
                if split.expense.split_method == 'percentage':
                    amount_owed_by_user += (split.percentage or 0) * split.expense.amount / 100
                else:
                    amount_owed_by_user += split.amount or 0

            # Amount owed to the user as payer (all splits for expenses where user is the payer)
            expenses_as_payer = Expense.objects.filter(payer=user)
            amount_owed_to_user = 0

            for expense in expenses_as_payer:
                splits = Split.objects.filter(expense=expense).exclude(user=user)
                for split in splits:
                    if expense.split_method == 'percentage':
                        amount_owed_to_user += (split.percentage or 0) * expense.amount / 100
                    else:
                        amount_owed_to_user += split.amount or 0

            # Calculate net balance
            net_balance = amount_owed_to_user - amount_owed_by_user
            
            # Calculate total expenses done by the user
            total_expenses_done = expenses_as_payer.aggregate(total=Sum('amount'))['total'] or 0

            # Add to balance sheet
            balance_sheet.append({
                "user_id": user.id,
                "username": user.username,
                "amount_owed_by_user": amount_owed_by_user,
                "amount_owed_to_user": amount_owed_to_user,
                "net_balance": net_balance,
                "total_expenses_done": total_expenses_done
            })

        return Response(balance_sheet, status=status.HTTP_200_OK)