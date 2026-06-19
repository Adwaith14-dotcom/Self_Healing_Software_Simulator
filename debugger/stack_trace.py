import traceback

def capture_stack_trace(error: Exception) -> str:
    """Return formatted stack trace for an error"""
    return "".join(traceback.format_exception(type(error), error, error.__traceback__))