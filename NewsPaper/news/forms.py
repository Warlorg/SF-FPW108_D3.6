from django import forms
from .models import Post
from django.core.exceptions import ValidationError


class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = [
			'author',
			'categoryType',
			'postCategory',
			'title',
			'text',
		]

	def clean_title(self):
		title = self.cleaned_data["title"]
		if title[0].islower():
			raise ValidationError(
				"Название должно начинаться с заглавной буквы!"
			)
		return title