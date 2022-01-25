from django.shortcuts import render
from rest_framework.views import APIView
import datetime
from expenses.models import Expenses
from rest_framework.response import Response
from rest_framework import status

class ExpenseStarts(APIView):

    def get_category_amount(self, expense_list, category):
        # expenses = expense_list.filter(category=category)
        # amount = 0
        # for expense in expenses:
        #     amount += expense.amount
        # return {"amount": amount}
        ...



    def get_cat(self, expense):
        return expense.categories

    def get(self, request):
      todays_date = datetime.date.today()
      ayear = todays_date-datetime.timedelta(30*12)
      '''
      filtering expenses based on the owner and date gte(greater than or equal to), lte(less than or equal to)
      '''
      expenses = Expenses.objects.filter(owner=request.user)
      print(expenses)
      final = {}
      

      categories = list(set(map(self.get_cat, expenses)))

      for expense in expenses:
          print(expense)
          for category in categories:
              
              final.update[category]= self.get_category_amount(expense, category)
      print(final)
              
      return Response({"categories": final}, status=status.HTTP_200_OK)