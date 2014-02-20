from rost.feedback_form import FeedbackForm

def FeedbackFormProcessor(request):
    if 'admin' in request.path:
        return {}
    return {'form':FeedbackForm()}