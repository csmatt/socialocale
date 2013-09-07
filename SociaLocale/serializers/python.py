from wadofstuff.django.serializers.python import Serializer as PythonSerializer
from django.utils.encoding import smart_unicode, is_protected_type


class Serializer(PythonSerializer):
    def serialize(self, queryset, **options):
        '''external_related format: {rootModelName:{'external_model':ExternalModel, 'fields':[]}}'''
        self.external_related = options.pop('external_related', [])
        self.return_with_meta = options.pop('return_with_meta', False)
        super(PythonSerializer, self).serialize(queryset, **options)

    def end_object(self, obj):
        """
        Called when serializing of an object ends.
        """
        objModelName = smart_unicode(obj._meta)
        objModelPk = smart_unicode(obj._get_pk_val(), strings_only=True)
        if self.external_related:
            external_model = self.external_related.get(objModelName, None)
            if external_model:
                self._fields.update(external_model.get(objModelName=objModelPk).only(*external_model.fields))
        if self.return_with_meta:
            self.objects.append({
                "model"  : smart_unicode(obj._meta),
                "pk"     : smart_unicode(obj._get_pk_val(), strings_only=True),
                "fields" : self._fields
            })
        else:
            self.objects.append(self._fields)

        if self._extras:
            self.objects[-1]["extras"] = self._extras
        self._fields = None
        self._extras = None