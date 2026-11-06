import itertools
import struct
import ov006_row841_machine_20261102 as M


def profiles():
    output = []

    def add(**changes):
        ordinal = len(output)
        p = dict(ordinal=ordinal, index=ordinal % 8, word2C=[0, 1, 65535, 0x80008000, 0xFFFFFFFF][ordinal % 5], word30=[0, 1, 0xFFFFFFFF][ordinal % 3], word34=[0, 1, 2, 0x80000000, 0xFFFFFFFF][ordinal % 5], half3E=[0, 1, 32767, 32768, 65535][ordinal % 5], quantityWord=ordinal * 997, lookupWord=0xAB120000 + ordinal, valueWord=[0, 1, 0x80000000, 0xFFFFFFFF][ordinal % 4], returnWord=[0, 0x7FFFFFFF, 0x80000000, 0xFFFFFFFF][ordinal % 4], priorReturnWord=0x98230000 + ordinal)
        p.update(changes)
        output.append(p)

    for flag, word30, word2C in itertools.product([0, 1, 2, 0x80000000, 0xFFFFFFFF], [0, 1, 0xFFFFFFFF], [0, 1, 65535, 0x80008000, 0xFFFFFFFF]):
        add(word34=flag, word30=word30, word2C=word2C)
    values = [0, 0x7FFFFFFF, 0x80000000, 0xFFFFFFFF]
    values += [value + delta for value in [2500, 5000, 7500, 12500, 25000, 45000, 55000] for delta in [-1, 0, 1]]
    for quantity, flag in itertools.product(values, [0, 1, 2, 0x80000000, 0xFFFFFFFF]):
        add(quantityWord=quantity, word34=flag)
    for index, flag in itertools.product(range(8), [0, 1, 2]):
        add(index=index, word34=flag)
    for half, flag in itertools.product([0, 1, 32767, 32768, 65535], [0, 1, 2, 0x80000000, 0xFFFFFFFF]):
        add(half3E=half, word34=flag)
    return output


def expected(vm, result):
    p = vm.p
    calls = []
    buffers = [row for row in result['calls'] if row['target'] == '0x2046af4']
    if len(buffers) != 1:
        return None
    buffer = buffers[0]['callerWords'][4]

    def emit(pc, *args, **extra):
        args = [value & 0xFFFFFFFF for value in args]
        calls.append(dict(target=hex(pc), callerWords=args, suppliedReturn=vm.provider(pc, args) & 0xFFFFFFFF, **extra))

    emit(0x021D7E34)
    emit(0x02067BD4, p['index'])
    emit(0x02048094, p['index'] + 1, 0)
    emit(0x021D79E4, 0, 15, 2, 0x8D)
    emit(0x02046AF4, 0x021C9698, vm.row + 0x10, 31, 0, buffer, 255, suppliedOutputHex=vm.buffer.hex())
    emit(0x021D7AD0, 2, buffer, observed64ByteBufferHex=vm.buffer.hex())
    if p['word30'] == 0:
        emit(0x021D79E4, 6, 15, 2, 0x7A)
    else:
        emit(0x02048094, p['word30'], 0)
        emit(0x021D79E4, 6, 15, 2, 0x8B)
    emit(0x020643FC, p['word2C'] & 65535)
    emit(0x021D7EBC, p['lookupWord'], 14, 7)
    emit(0x021D79E4, 4, 15, 15, p['word2C'] & 65535)
    emit(0x021DE1A8, p['index'])
    category = sum(M.signed(p['quantityWord']) >= threshold for threshold in [2500, 5000, 7500, 12500, 25000, 45000, 55000])
    emit(0x021D79E4, 8, 15, 2, category + 0xA4)
    emit(0x021D79E4, 10, 15, 2, 0x9F if p['word34'] == 0 else 0x9E)
    if p['word34'] != 0:
        emit(0x021DE228, p['index'])
    value = 0
    if p['word34'] == 1:
        emit(0x02067B48, 1, p['index'])
        value = p['valueWord']
    emit(0x021DC08C, 12, value, 4)
    emit(0x021DC08C, 14, p['half3E'] if p['word34'] == 1 else 0, 4)
    return calls


def model(vm, result):
    calls = expected(vm, result)
    failures = []
    if result['registers'][0] != pword(vm.p['returnWord']):
        failures.append('full physical renderer-return forwarding')
    if result['calls'] != calls:
        failures.append('ordered raw-word/buffer contracts')
    if result['rows'] != vm.before:
        failures.append('synthetic row window unchanged under supplied no-effect services')
    if struct.unpack_from('<I', result['state'], 0x14)[0] != vm.p['index']:
        failures.append('selected index unchanged')
    classifier = [row for row in result['nativeEntries'] if row['address'] == '0x2067d54']
    if len(classifier) != 1 or classifier[0]['rawWords'][0] != vm.p['quantityWord']:
        failures.append('actual transitive classifier inputR0')
    return failures


def pword(value):
    return value & 0xFFFFFFFF
