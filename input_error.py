def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please"
        except KeyError as e:
            return f"KeyError: Contact {e} not found" 
        except IndexError:
            return "Give me name"

    return inner

if __name__ == "__main__":
    input_error()