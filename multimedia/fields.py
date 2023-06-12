from multiupload.fields import MultiImageField

class ValidatedMultiImageField(MultiImageField):
    def run_validators(self, value):
        value = value or []

        for item in value:
            super().run_validators(item)