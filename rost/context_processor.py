from rost.feedback_form import FeedbackForm

def FeedbackFormProcessor(request):
    return {'form':FeedbackForm()}