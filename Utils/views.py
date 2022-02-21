from django.http import JsonResponse

def http_404(request, exception):
  message = ("endpoint is not found")
  response = JsonResponse(data = {"message": message})
  response.status_code=404
  return response

def http_500(request):
  message = ("Server crashed. the problem is on our end")
  response = JsonResponse(data = {"message": message})
  response.status_code=500
  return response