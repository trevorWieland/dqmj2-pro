typedef unsigned short u16;
typedef struct { void *previous; void *next; } ChildLink;
typedef struct { void *first; void *last; u16 count; u16 linkOffset; } ChildList;
#define CHILD_LINK(list, object) ((ChildLink *)((char *)(object) + (list)->linkOffset))
extern void native_utility_child_arm9_arm_02003780(ChildList *, void *);
extern void native_utility_child_arm9_arm_02003720(ChildList *, void *);
extern void native_utility_child_arm9_arm_020036c4(ChildList *, void *);
void native_utility_child_arm9_main_020035e8(ChildList *list, void *object) {
    ChildLink *link = CHILD_LINK(list, object);
    if (link->previous == 0) list->first = link->next;
    else CHILD_LINK(list, link->previous)->next = link->next;
    if (link->next == 0) list->last = link->previous;
    else CHILD_LINK(list, link->next)->previous = link->previous;
    link->previous = 0;
    link->next = 0;
    list->count--;
}
