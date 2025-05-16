def model_to_dict(obj):
    """
    Makes a dictionary out of a ORM object

    - obj: The ORM object
    """
    return {k: v for k, v in vars(obj).items() if not k.startswith('_')}
    # if it starts with _ its an internal attribute, we dont want those
