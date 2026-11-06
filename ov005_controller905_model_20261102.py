import struct
import ov005_controller905_machine_20261102 as M


def profiles():
    rows = []
    for key in [0, 1, 0x80400120, 0x80000042, 0xFFFFFFFF]:
        for layout in range(3):
            keys = [0] * 16
            keys[15] = 0x13570001
            if layout == 1:
                keys[2] = key
            if layout == 2:
                keys[0] = 0x80000000
                keys[4] = 0x80000088
            for result in [0, 1, 0x80000000]:
                for override in [None, 0, 0xFFFFFFFF]:
                    for offset in [0, 0x100]:
                        rows.append(dict(ordinal=len(rows), key=key, rowKeys=keys, selectReturn=result, override=override, requestOffset=offset))
    return rows


def selection(p):
    key = p['key']
    if key == 0:
        return None, key
    for index, value in enumerate(p['rowKeys']):
        if value == key:
            return index, key
        if key & 0x80000000 and value & 0x80000000:
            if key == 0x80400120:
                if value != 0x80000000:
                    return index, value
            elif value == 0x80000000:
                return index, key
    return None, key


def logical_calls(result):
    return [{k: v for k, v in row.items() if k != 'rawPayloadAddress'} for row in result['calls']]


def model(vm, result):
    p = vm.p
    selected, key = selection(p)
    descriptorResult = p['selectReturn'] if selected is not None else 0
    value = descriptorResult if p['override'] is None else p['override']
    expected = bytearray(vm.beforeObject)
    writes = []
    selectedIndex = 15
    if selected is not None and descriptorResult != 0:
        selectedIndex = selected
        struct.pack_into('<I', expected, 0x5760 + 0x20, vm.entries[selected])
        struct.pack_into('<I', expected, 0x5760 + 0x324, key)
        writes += [[M.CONTROLLER + 0x20, 4, vm.entries[selected]], [M.CONTROLLER + 0x324, 4, key]]
    if value != 0:
        oldKey = p['rowKeys'][selectedIndex]
        struct.pack_into('<I', expected, 0xE8, oldKey)
        writes.append([M.OBJECT + 0xE8, 4, oldKey])
    calls = []
    if selected is not None:
        calls.append(dict(target=hex(M.SELECT), consumedWords=[M.CONTROLLER, vm.request], returnWord=p['selectReturn']))
    calls.append(dict(target=hex(M.CALLBACK), eventWord=6, payloadBefore=[descriptorResult, vm.request], payloadAfter=[value, vm.request], returnWord=0x12345678))
    failures = []
    for name, actual, expectedValue in [('raw R0 result', result['registers'][0], value), ('independent object effects', result['objectHex'], expected.hex()), ('ordered observable writes', result['writes'], writes), ('consumed call contracts', logical_calls(result), calls)]:
        if actual != expectedValue:
            failures.append(name)
    if len(result['nativeHelperEntries']) != 1 or result['nativeHelperEntries'][0]['callerWords'] != [M.CONTROLLER, vm.request]:
        failures.append('actual two-word descriptor entry')
    if len(result['nativeHelperPhysicalReturns']) != 1 or result['nativeHelperPhysicalReturns'][0]['actualReturnWord'] != descriptorResult:
        failures.append('actual descriptor return')
    return failures
