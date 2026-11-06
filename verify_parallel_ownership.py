from parallel_status import collisions, interval, finalized


def row(module='ov000', address='0x021d8000', mode='arm', program='', processor='arm9', size=32):
    return interval(dict(module=module, address=address, mode=mode, program=program, processor=processor, bytes=size))


def main():
    owned = [('one', row())]
    assert collisions(owned + [('two', row(address='0x021d8010'))], [])
    assert not collisions(owned + [('two', row(module='ov001'))], [])
    assert not collisions(owned + [('two', row(processor='arm7'))], [])
    assert not collisions(owned + [('two', row(program='separate-program'))], [])
    assert not collisions(owned + [('two', row(address='0x021d8020'))], [])
    assert collisions(owned, [('prepared', row(address='0x021d8002', mode='thumb'))])
    assert collisions(owned, [('accepted', row())])
    assert interval(dict(module='utility-child-arm7-main', address='0x027e0000', mode='arm', bytes=4))[0] == (
        'dwc/utility.bin/move/child.srl', 'arm7', 'utility-child-arm7-main')
    for address, mode, size in [('0x021d8002', 'arm', 4), ('0x021d8001', 'thumb', 2), ('0x021d8000', 'arm', 0)]:
        try:
            row(address=address, mode=mode, size=size)
        except ValueError:
            pass
        else:
            raise AssertionError('Invalid extent/alignment accepted')
    receipt = dict(linksPending=False, acceptedBuildCreatedUtc='measured-time', transactionPreparedOnly=True,
        sourceMatchedFunctions=10, expectedSourceMatchedFunctions=10, sourceLinkedBytes=100,
        expectedSourceLinkedBytes=100, moduleComparisonsExact=20)
    assert finalized(receipt, dict(passed=True))
    assert not finalized({**receipt, 'linksPending': True}, dict(passed=True))
    assert not finalized(receipt, dict(passed=False))
    assert not finalized({**receipt, 'sourceLinkedBytes': 101}, dict(passed=True))
    print(dict(passed=True, ownershipAndAcceptanceControls=15, sourceCredit=0))


if __name__ == '__main__':
    main()
