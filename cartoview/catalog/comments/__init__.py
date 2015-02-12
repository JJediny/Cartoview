from cartoview2.catalog.comments.models import CommentWithRating
from cartoview2.catalog.comments.forms import CommentFormWithRating

def get_model():
    return CommentWithRating

def get_form():
    return CommentFormWithRating
