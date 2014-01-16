# mangal-api

This repository contains the files necessary to add tha `mangal` API to your `django` project. Up-to-date versions of `django` and `django-tastypie` are required.

```python
from tastypie.api import Api
from api.resources import *

v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(TaxaResource())
v1_api.register(PopulationResource())
v1_api.register(InteractionResource())
v1_api.register(NetworkResource())
v1_api.register(DatasetResource())
v1_api.register(RefResource())
v1_api.register(TraitResource())
v1_api.register(EnvironmentResource())
v1_api.register(ItemResource())
```

Then, in the `urlpatterns` variable, add

```python
    url(r'^api/', include(v1_api.urls)),
```

And don't forget to add `api` in the list of `INSTALLED_APPS`.
