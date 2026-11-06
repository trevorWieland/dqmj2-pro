def number(value):
    return int(value, 0) if isinstance(value, str) else int(value)


class LinkedSourceRanges:
    def __init__(self, units):
        self.by_identity = {}
        for unit in units:
            key = unit['module'], unit['sha256']
            self.by_identity.setdefault(key, []).append((number(unit['start']), number(unit['end'])))

    def contains(self, module, address, size, object_sha256):
        return any(start <= address and address + size <= end
            for start, end in self.by_identity.get((module, object_sha256), []))


def original_contains(units, module, address, size, object_sha256):
    return any(unit['module'] == module and number(unit['start']) <= address
        and address + size <= number(unit['end']) and unit['sha256'] == object_sha256
        for unit in units)
