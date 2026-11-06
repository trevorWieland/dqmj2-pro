import json
from wave20261102_child_research import setup
from wave20261102_child_prepare import ROOT, WORK, LANE
from project import write_json
import utility_code as matcher

PRELUDE = '''typedef unsigned short u16;
typedef struct { void *previous; void *next; } ChildLink;
typedef struct { void *first; void *last; u16 count; u16 linkOffset; } ChildList;
#define CHILD_LINK(list, object) ((ChildLink *)((char *)(object) + (list)->linkOffset))
extern void native_utility_child_arm9_arm_02003780(ChildList *, void *);
extern void native_utility_child_arm9_arm_02003720(ChildList *, void *);
extern void native_utility_child_arm9_arm_020036c4(ChildList *, void *);
'''
BODIES = {
0x020035bc: '''void *FN(ChildList *list, void *object) {
    if (object == 0) return list->last;
    return CHILD_LINK(list, object)->previous;
}
''',
0x020035e8: '''void FN(ChildList *list, void *object) {
    ChildLink *link = CHILD_LINK(list, object);
    if (link->previous == 0) list->first = link->next;
    else CHILD_LINK(list, link->previous)->next = link->next;
    if (link->next == 0) list->last = link->previous;
    else CHILD_LINK(list, link->next)->previous = link->previous;
    link->previous = 0;
    link->next = 0;
    list->count--;
}
''',
0x02003650: '''void FN(ChildList *list, void *before, void *object) {
    ChildLink *link;
    if (before == 0) {
        native_utility_child_arm9_arm_02003720(list, object);
        return;
    }
    if (before == list->first) {
        native_utility_child_arm9_arm_020036c4(list, object);
        return;
    }
    link = CHILD_LINK(list, object);
    link->previous = CHILD_LINK(list, before)->previous;
    link->next = before;
    CHILD_LINK(list, link->previous)->next = object;
    CHILD_LINK(list, before)->previous = object;
    list->count++;
}
''',
0x020036c4: '''void FN(ChildList *list, void *object) {
    ChildLink *link;
    if (list->first == 0) {
        native_utility_child_arm9_arm_02003780(list, object);
        return;
    }
    link = CHILD_LINK(list, object);
    link->previous = 0;
    link->next = list->first;
    CHILD_LINK(list, list->first)->previous = object;
    list->first = object;
    list->count++;
}
''',
0x02003720: '''void FN(ChildList *list, void *object) {
    ChildLink *link;
    if (list->first == 0) {
        native_utility_child_arm9_arm_02003780(list, object);
        return;
    }
    link = CHILD_LINK(list, object);
    link->previous = list->last;
    link->next = 0;
    CHILD_LINK(list, list->last)->next = object;
    list->last = object;
    list->count++;
}
''',
0x02003780: '''void FN(ChildList *list, void *object) {
    ChildLink *link = CHILD_LINK(list, object);
    link->next = 0;
    link->previous = 0;
    list->first = object;
    list->last = object;
    list->count++;
}
'''
}


def main():
    specs = {s['address']: s for s in setup()}
    matcher.WORK = WORK / 'list-compiled'
    for address, body in BODIES.items():
        spec = specs[address]
        directory = WORK / 'list-sources' / ('%08x' % address)
        directory.mkdir(parents=True, exist_ok=True)
        source = directory / ('list_%08x.c' % address)
        source.write_text(PRELUDE + body.replace('FN', spec['name']))
        attempts = []
        result = dict(address=hex(address), bytes=spec['bytes'])
        for profile in ['1.2/sp4', '1.2/sp3', '1.2/base', '2.0/base', '2.0/sp1p5']:
            for level, speed in [('4,p', False), (2, True), (2, False)]:
                row, code = matcher.compile_compare(source, dict(spec,
                    compilerPath=ROOT / ('tools/mwccarm/mwccarm/' + profile + '/mwccarm.exe')), level, 'off', speed)
                attempts.append(row)
                if code is not None:
                    result.update(match=row, draftSource=source.relative_to(ROOT).as_posix())
                    break
            if 'match' in result:
                break
        result['attempts'] = attempts
        write_json(LANE / 'lists' / ('%08x.json' % address), result)
        print(dict(address=hex(address), matched='match' in result,
                   bestMatching=max((r.get('matchingBytes', 0) for r in attempts), default=0)), flush=True)


if __name__ == '__main__':
    main()
