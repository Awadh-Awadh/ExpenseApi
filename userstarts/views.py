from django.shortcuts import render
from rest_framework.views import APIView
import datetime
from expenses.models import Expenses
from income.models import Income
from rest_framework.response import Response
from rest_framework import status

class ExpenseStarts(APIView):

    def get_category_amount(self, expense_list, category):
        '''
            Query sets can be reused. for eaxample:

            everyone = User.objects.filter(is_active=True)
            active_not_deleted = everyone.filter(is_deleted=False)
            active_is_deleted = everyone.filter(is_deleted=True)

            this is the exact way we are doing with the expense_list
        
        '''
        expenses = expense_list.filter(categories = category)
        amount = 0
        for expense in expenses:
            amount += expense.amount
        return {"amount": str(amount)}
        



    def get_cat(self, expense):
        return expense.categories

    def get(self, request):
      todays_date = datetime.date.today()
      ayear = todays_date-datetime.timedelta(30*12)
      '''
      filtering expenses based on the owner and date gte(greater than or equal to), lte(less than or equal to)
      '''
      expenses = Expenses.objects.filter(owner=request.user)
      final = {}
      

      categories = list(set(map(self.get_cat, expenses)))
      


      for expense in expenses:      
            for category in categories:              
                 final[category]= self.get_category_amount(expenses, category)
              
      return Response({"categories": final}, status=status.HTTP_200_OK)



class IncomeStartsAPI(APIView):

    
    def get_cat_amount(self, income_list, category):
        incomes = income_list.filter(categories = category)
        amount= 0
        for income in incomes:
            amount += income.amount
        return str(amount)


    def get_category(self, income):
        return income.categories


    def get(self, request):

        today_date = datetime.date.today()
        ayear = today_date - datetime.timedelta(364)
        incomes = Income.objects.filter(owner=request.user)
        print(incomes)
        categories = list(map(self.get_category, incomes))
        print(categories)

        final = {}

        for income in incomes:
            for cat in categories:
                final[cat] = self.get_cat_amount(incomes, cat)
        return Response({"Income Data": final}, status=status.HTTP_200_OK)
