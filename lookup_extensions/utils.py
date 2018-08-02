def merge_dicts(*dicts):
    merged = {}
    for d in dicts:
        merged.update(d)
    return merged
