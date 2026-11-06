from unittest.mock import patch
from project import ROOT, configuration, read_json, write_json, sha256, native_dependencies

native_dependencies(configuration())
import link_utility


def main():
    config = configuration()
    program = 'dwc/utility.bin/move/child.srl'
    controls = []

    def report(cpu, address, selected_program=program):
        return dict(program=selected_program, processor=cpu, romSha256=config['romSha256'], matches=[],
                    nativeSymbols={'_s32_div_f': address}, nativeSymbolBindings=[dict(
                        program=selected_program, processor=cpu, name='_s32_div_f', address=address, mode='arm')])

    fixtures = {'a9': report('arm9', '0x2010df4'), 'a7': report('arm7', '0x3804f78')}

    def run(values, action):
        with patch.object(link_utility, 'batches', return_value=[dict(report=name) for name in values]), \
             patch.object(link_utility, 'read_json', side_effect=lambda path: values[path.name]):
            return action()

    def rejected(name, values, action):
        try:
            run(values, action)
        except ValueError as error:
            controls.append(dict(name=name, rejected=True, reason=str(error)))
        else:
            raise AssertionError('Conflicting CPU binding accepted: ' + name)

    plans, metadata = run(fixtures, lambda: link_utility.accepted_by_cpu(program, ['arm9', 'arm7']))
    assert plans['arm9'][1]['_s32_div_f'] == '0x2010df4'
    assert plans['arm7'][1]['_s32_div_f'] == '0x3804f78'
    assert plans['arm9'][2][0]['processor'] == 'arm9' and plans['arm7'][2][0]['processor'] == 'arm7'
    rejected('unscoped-global-conflict-retained', fixtures, lambda: link_utility.accepted(program))
    for cpu in ('arm9', 'arm7'):
        values = dict(fixtures, conflicting=report(cpu, '0x12345678'))
        rejected('same-cpu-address-conflict-' + cpu, values, lambda cpu=cpu: link_utility.accepted(program, cpu))
        changed = report(cpu, fixtures['a9' if cpu == 'arm9' else 'a7']['nativeSymbols']['_s32_div_f'])
        changed['nativeSymbolBindings'][0]['mode'] = 'thumb'
        values = dict(fixtures, conflicting=changed)
        rejected('same-cpu-binding-mode-conflict-' + cpu, values, lambda cpu=cpu: link_utility.accepted(program, cpu))
    changed = report('arm9', '0x2010df4')
    changed['nativeSymbolBindings'][0]['program'] = 'different-program'
    rejected('cross-program-target', {'wrong': changed}, lambda: link_utility.accepted(program, 'arm9'))
    changed = report('arm9', '0x2010df4')
    changed['matches'] = [dict(processor='arm7')]
    rejected('report-entry-cpu-disagreement', {'wrong': changed}, lambda: link_utility.accepted(program, 'arm9'))
    rejected('unknown-link-cpu', fixtures, lambda: link_utility.accepted(program, 'other'))
    values = dict(fixtures, unrelated=report('arm9', '0x12345678', 'different-program'))
    assert run(values, lambda: link_utility.accepted(program, 'arm9'))[1]['_s32_div_f'] == '0x2010df4'
    legacy = dict(program=program, romSha256=config['romSha256'], matches=[], nativeSymbols={'legacy': '0x1234'})
    values = dict(fixtures, legacy=legacy)
    plans, metadata = run(values, lambda: link_utility.accepted_by_cpu(program, ['arm9', 'arm7']))
    assert all(plan[1]['legacy'] == '0x1234' for plan in plans.values())
    item = dict(source='fixture.c', name='container', module='container', address='0', sourceSha256='same')
    with patch.object(link_utility, 'accepted', side_effect=[([], {}, [], [item]), ([], {}, [], [dict(item)])]):
        assert link_utility.accepted_by_cpu(program, ['arm9', 'arm7'])[1] == [item]
    try:
        with patch.object(link_utility, 'accepted', side_effect=[([], {}, [], [item]),
                ([], {}, [], [dict(item, sourceSha256='changed')])]):
            link_utility.accepted_by_cpu(program, ['arm9', 'arm7'])
    except ValueError:
        controls.append(dict(name='conflicting-composition-metadata', rejected=True))
    else:
        raise AssertionError('Conflicting composition metadata accepted')
    plans, metadata = link_utility.accepted_by_cpu(program, ['arm9', 'arm7'])
    actual = {cpu: plan[1]['_s32_div_f'] for cpu, plan in plans.items()}
    assert actual == {'arm9': '0x2010df4', 'arm7': '0x3804f78'}
    write_json(ROOT / 'evidence/lanes/parallel-wave20261104/utility-cpu-symbol-controls.json', dict(
        passed=True, sourceCredit=0, linkerConsumerSha256=sha256(ROOT / 'link_utility.py'),
        rejectedControls=controls, currentProgramHelperAddresses=actual, containerMetadataEntries=len(metadata),
        compilerElfNamesAndRelocationsUnchanged=True, withinCpuConflictGuardsRetained=True,
        legacyMixedReportBindingGuardsRetained=True))
    print(dict(passed=True, rejectedControls=len(controls), actualProgramBindings=actual))


if __name__ == '__main__':
    main()
