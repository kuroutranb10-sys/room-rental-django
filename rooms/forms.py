from django import forms
from .models import Room


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    widget = MultipleFileInput

    def clean(self, data, initial=None):
        single_file_clean = super().clean

        if isinstance(data, (list, tuple)):
            result = []

            for item in data:
                result.append(single_file_clean(item, initial))

            return result

        return single_file_clean(data, initial)

class RoomForm(forms.ModelForm):
    images = MultipleFileField(
        required=False)

    class Meta:
        model = Room

        fields = [
            'name',

            'city',
            'ward',

            'address',

            'price',
            'area',

            'electricity_price',
            'water_price',
            'deposit',

            'floor',
            'max_people',

            'has_wifi',
            'has_air_conditioner',
            'has_bed',
            'has_tv',
            'has_refrigerator',

            'image',
            'status',
        ]

        widgets = {

            'city': forms.Select(
                attrs={
                    'id': 'id_city'
                }
            ),

            'ward': forms.Select(
                attrs={
                    'id': 'id_ward'
                }
            ),

            'price': forms.TextInput(
                attrs={
                    'id': 'id_price',
                    'inputmode': 'numeric',
                    'autocomplete': 'off',
                }
            ),

            'electricity_price': forms.TextInput(
                attrs={
                    'id': 'id_electricity_price',
                    'inputmode': 'numeric',
                    'autocomplete': 'off',
                }
            ),

            'water_price': forms.TextInput(
                attrs={
                    'id': 'id_water_price',
                    'inputmode': 'numeric',
                    'autocomplete': 'off',
                }
            ),

            'deposit': forms.TextInput(
                attrs={
                    'id': 'id_deposit',
                    'inputmode': 'numeric',
                    'autocomplete': 'off',
                }
            ),
        }


    def clean(self):

        cleaned_data = super().clean()


        # =========================
        # KIỂM TRA CÁC GIÁ TRỊ DƯƠNG
        # =========================

        positive_fields = [
            'price',
            'area',
            'electricity_price',
            'water_price',
            'deposit',
            'floor',
            'max_people',
        ]


        for field_name in positive_fields:

            value = cleaned_data.get(field_name)


            if value is not None and value <= 0:

                self.add_error(
                    field_name,
                    'Giá trị phải lớn hơn 0.'
                )


        return cleaned_data