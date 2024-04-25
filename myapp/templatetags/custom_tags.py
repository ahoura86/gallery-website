from django import template

register = template.Library()

@register.simple_tag
def custom_file_input(field):
    return field.as_widget(attrs={'class':'hidden', 'label':'انتخاب فایل'})

register.filter("custom_file_input", custom_file_input)
