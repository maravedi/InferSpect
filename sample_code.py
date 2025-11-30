def process_user_input(user_input):
    """
    Process user input in an unsafe way to trigger security scanners.
    """
    # This is intentionally insecure to trigger bandit or other tools
    cmd = "echo " + user_input
    import os
    os.system(cmd)
    return True

def add_numbers(a, b):
    """
    Simple function to test.
    """
    return a + b
