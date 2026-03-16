from django.forms import ModelForm
from cats.models import Breed, Cat

# Форма для пород
class BreedForm(ModelForm):
    class Meta:
        model = Breed
        fields = '__all__'

# Форма для кошек (если решишь использовать её вместо полей в CreateView)
class CatForm(ModelForm):
    class Meta:
        model = Cat
        fields = '__all__'