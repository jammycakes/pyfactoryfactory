factoryfactory - a simple service locator in Python
===================================================

[![Build Status][shield-travis]][info-travis]

factoryfactory is a simple implementation of the Service Locator pattern.

It is actually a hybrid of the Dependency Injection and Service Locator
patterns. The service locator itself is injected into the services that it
creates, but the services themselves then issue requests to it for the
dependencies that they require. This allows you much more control over the
lifecycles of these dependencies.

The name is inspired by the classic article, "[Why I Hate Frameworks](http://discuss.joelonsoftware.com/default.asp?joel.3.219431.12)".

Usage
-----

To create a service locator:

```
import factoryfactory

locator = factoryfactory.ServiceLocator()
```

To instantiate a service:

```
session = locator.get(boto3.Session)

# You can pass arguments to the service's constructor:
session = locator.get(boto3.Session, region_name='eu-west-1')

# Alternative syntax:
session = locator[boto3.Session](region_name = 'eu-west-1')
```

By default, calling `locator.get` will call the class or function that you
requested.

To register a service:

```
locator.register(boto3.Session, FakeSession)
```

The service being registered can be a class:

```
class FakeSession:

    def client(self, *args, **kwargs):
        pass

locator.register(boto3.Session, FakeSession)
```

or a factory method:

```
def session_builder(*args, **kwargs):
    return boto3.session.Session(*args, **kwargs)

locator.register(boto3.Session, session_builder)
```

or an instance of a class:

```
session = boto3.Session(region_name='eu-west-1')
locator.register(boto3.Session, session)
```

If you are registering an instance of a class, it will always be registered as
a singleton. You can specify a factory method to create a singleton by passing
`singleton=True` to the `register` method:

```
locator.register(boto3.Session. boto3.Session, singleton=True)
```

You can also register services by name:

```
locator.register('welcome', lambda *args, **kwargs: 'Hello world')
```

A service doesn't need to be a class or a factory method; it can even be a string:

```
locator.register('welcome', 'Ceud Mìle Fàilte')
```

Serviceable class
-----------------

If a service inherits from `Serviceable` (remember that Python has multiple
inheritance), the service locator will inject an instance of itself into the
`services` property. This is available in the service's `__init__` method, so
you can resolve dependencies in the constructor:

```
class UserService(factoryfactory.Serviceable):

    def __init__(self):
        self.repository = self.services.get(UserRepository)
```

The `Serviceable` class comes with a default service locator in its `services`
property, so if you instantiate your service directly, it will use this:

```
factoryfactory.Serviceable.services.register(UserRepository, PostgresqlRepository)

locator = factoryfactory.ServiceLocator()
locator.register(UserRepository, DynamoDBRepository)

users1 = UserService()            # This will use Postgresql
users2 = locator.get(UserService) # This will use Amazon DynamoDB
```

Note that your class must inherit from `Serviceable` if it is to have the
`services` locator injected into it.

[info-travis]:   https://travis-ci.org/jammycakes/factoryfactory
[shield-travis]: https://img.shields.io/travis/jammycakes/factoryfactory.svg