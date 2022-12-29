from  print_pp.logging import Print


def validate_mutation_input(serializer, input) -> tuple[bool, dict]:
    serializer = serializer(data=input)

    if not serializer.is_valid(): return False, serializer.errors
    try: serializer.save()
    except Exception as e: return False, e

    return True, serializer.instance
