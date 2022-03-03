def action_attrs(**kwargs):
    """
    This decorator is mainly used to imitate @action and make view attribute more flexible,
    it can be used to override/define view attribute like serializer_class, queryset...
    """

    def decorator(action):
        def wrapper(self, *function_args, **function_kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)
            return action(self, *function_args, **function_kwargs)

        return wrapper

    return decorator
