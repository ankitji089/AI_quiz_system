def update_level(current_level, correct):

    if correct:
        return min(current_level + 1, 10)

    else:
        return max(current_level - 1, 1)