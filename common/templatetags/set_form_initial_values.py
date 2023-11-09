from django import template

register = template.Library()


@register.filter
def set_form_initial_values(form_field, obj):
    if not hasattr(form_field.form, "model"):
        raise ValueError(
            "Function cannot resolve form model. Set 'model' attribute for your form."
        )

    model = form_field.form.model
    model_obj = model.objects.get(id=obj["id"])
    form_field.initial = getattr(model_obj, form_field.name)
    return form_field
