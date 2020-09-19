from django.shortcuts import render
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa
from root.models import Profile

def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None



#Opens up page as PDF
class ViewPDF(View):
	def get(self, request, *args, **kwargs):
		profile = Profile.objects.get(user_id=request.user.id)
		first = self.request.GET["first_name"]
		phone = self.request.GET["phone"]
		last = self.request.GET["last_name"]
		skills = self.request.GET["skills"]
		proposal = self.request.GET["proposal"]
		education_experience = self.request.GET["Education_and_Work_experience"]
		data = { "first": first, "last": last, "skills": skills, "Education_and_Work_experience": education_experience, "profile": profile, "proposal": proposal, "phone": phone } 
		pdf = render_to_pdf('job/pdf.html', data)
		return HttpResponse(pdf, content_type='application/pdf')


#Automaticly downloads to PDF file
# class DownloadPDF(View):
# 	def get(self, request, *args, **kwargs):
		
# 		pdf = render_to_pdf('app/pdf_template.html', data)

# 		response = HttpResponse(pdf, content_type='application/pdf')
# 		name = "my" 
# 		content = f"attachment; filename={name}_resume.pdf"
# 		response['Content-Disposition'] = content
# 		return response



def index(request):
	context = {}
	return render(request, 'app/index.html', context)