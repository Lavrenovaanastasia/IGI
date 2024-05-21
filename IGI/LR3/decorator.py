def funcInfoDec(func):
    """Prints name and documentation of a current function."""
    def wrapper(*args, **kwargs):
        #{func.name} обращается к атрибуту name функции, который содержит ее имя, 
        # а func.doc обращается к атрибуту doc, который содержит документацию функци
        print(f'\033[33m Сalling {func.__name__}() that {func.__doc__} \033[00m')
        result = func(*args, **kwargs)
        return result
    return wrapper

