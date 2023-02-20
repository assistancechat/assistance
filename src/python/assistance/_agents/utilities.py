import textwrap


def items_to_list_string(items):
    return textwrap.indent("\n".join(items), "- ")
