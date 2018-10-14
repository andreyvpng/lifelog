import factory
from core.models import Action, Record
from django.conf import settings


class CreateFactoryMixin(factory.DjangoModelFactory):

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)
        return manager.create(*args, **kwargs)


class UserFactory(factory.DjangoModelFactory):
    username = factory.Sequence(lambda n: 'user %d' % n)
    password = 'unittest'

    class Meta:
        model = settings.AUTH_USER_MODEL

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)
        return manager.create_user(*args, **kwargs)


class ActionFactory(CreateFactoryMixin, factory.DjangoModelFactory):
    text = factory.Sequence(lambda n: 'Action #%d' % n)
    unit = 'unit'
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Action


class RecordFactory(CreateFactoryMixin, factory.DjangoModelFactory):
    value = 1000
    action = factory.SubFactory(ActionFactory)

    class Meta:
        model = Record
