from django import forms
from .models import Movie, ButtonBox # do we actually need movie?

class ButtonBoxForm(forms.ModelForm):
    class Meta:
        model = ButtonBox
        fields = [] # we aren't actually taking in any input; this form
        # is never actually being rendered

        #fields = ['movie', 'user', 'seen', 'favorite', 'watch']

# I think, for your purposes here, you list the model but leave fields empty;
# otherwise it will expect data for them on the is_valid() check, expecting that
# the situation is a POST request sent from the page where this 'form' is rendered,
# and then that data is assigned (by this model form here) to the corresponding
# fields (matching Model fields to Form input fields, which is the whole point really
# of the ModelForm), and the view does the is_valid() call to make sure the input
# was all of the correct type.

# BUT, for your 'invisible forms' purpose, you don't actually want any 'form field'
# for any value, nor any check on those (unwanted) values; the button click acts
# indirectly as the 'input' and then you just skip to updating attributes
# accordingly. There are no form fields, and no input data to verify; the 'input'
# was simply the click on the button.

# therefore, leaving fields blank above is like fields = [] in the generic CVB;
# you're saying "This is a form, process it as a form, but it actually has no
# input fields" -- the ModelForm is still useful, even without use of any input
# fields, because when you do instance = form.save() you will create an object
# instance of the Model that the ModelForm is tied to -- which, above, is ButtonBox

# without that, you'd have to manually create an instance of ButtonBox in the view
# by calling the Class constructor; in fact, that 'trial code' you wrote a while
# back where you did a function-based view to recreate the behavior of a CBV, to
# see for yourself what was going on, that's exactly what you did: you called
# the Model constructor and built the instance yourself, rather than it happening
# through a ModelForm. In that situation, you were still using a form, though,
# you just weren't using ModelForm. Your code took the results of the POST request
# taking the data directly from the form, cleaning it, and then building a new
# object instance from scratch using those values (the values taken from the form's
# input fields, that had been cleaned.) So that was not an 'invisible' form scenario;
# it was a case of writing a function-based view to process a form's data without
# using a ModelForm. It required, notably, figuring out the syntax for accessing
# the data stored in the form's fields. this work is what using a ModelForm takes
# care of for you. You did it to 'see' yourself the logic of both 1. the ModelForm
# but also 2. a CBV
