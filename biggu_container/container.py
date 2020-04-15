import inspect

class Container:

    def __init__(self):
        self.bindings = {}
        self.instances = {}

    @staticmethod
    def ensure_key_string(key):
        allowed = (int, str, bool, float)
        if not isinstance(key, allowed):
            key = key.__module__ + '.' + key.__name__
        return str(key)

    # Bind a resolver in container
    def bind(self, name, resolver, shared = False):
        self.bindings[name] = {
            'resolver': resolver,
            'shared': shared,
        }

    # Register an instance of class in container
    def instance(self, name, instance):
        self.instances[self.ensure_key_string(name)] = instance

    # Register an singleton instance in container
    def singleton(self, name, resolver):
        self.bind(self.ensure_key_string(name), resolver, True)

    @staticmethod
    def import_class(namespace):
        class_data = namespace.split(".")
        submodules_list = class_data[0:-1]
        submodule = '.'.join(submodules_list)
        class_name = class_data[-1]
        module = __import__(submodule, fromlist=[class_name])
        return getattr(module, class_name)

    # Build instances with dependencies
    def build(self, _class, arguments = None):
        class_info = inspect.getfullargspec(_class.__init__)
        if not len(class_info.args[1:]):
            return _class()

        if arguments is None:
            arguments = {}

        dependencies = self.resolve_dependencies(class_info, arguments)

        return _class(**dependencies)

    def resolve_dependencies(self, class_info, arguments):
        dependencies = {}
        class_arguments = class_info.args[1:]
        for key in class_info.args[1:]:
            if key in arguments:
                dependencies[key] = arguments[key]
                continue

            if key in class_info.annotations and inspect.isclass(class_info.annotations[key]):
                dependencies[key] = self.build(class_info.annotations[key])
            else:
                if class_info.defaults is None:
                    raise Exception('Provide the value of the parameter [%s]' % key)

                last_required_index = len(class_arguments) - len(class_info.defaults)
                defaults = class_arguments[last_required_index:]
                for index in range(len(defaults)):
                    name = defaults[index]
                    dependencies[name] = class_info.defaults[index]
        return dependencies

    # Make a instance using a key name in container
    def make(self, name, arguments = None):
        name = self.ensure_key_string(name)
        if name in self.instances:
            return self.instances[name]

        if name in self.bindings:
            resolver = self.bindings[name]['resolver']
            shared = self.bindings[name]['shared']
        else:
            resolver = name
            shared = False

        if callable(resolver):
            instance = resolver(self)
        else:
            if type(resolver) != str:
                instance = resolver
            else:
                _class = self.import_class(resolver)
                instance = self.build(_class, arguments)

        # If was bound as singleton then register instance
        if shared :
            self.instance(name, instance)

        return instance

    def bound(self, name):
        return name in self.bindings or name in self.instances

    def flush(self):
        self.bindings = {}
        self.instances = {}