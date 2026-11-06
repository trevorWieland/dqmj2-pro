typedef unsigned short u16;
typedef struct { void *previous; void *next; } ChildLink;
typedef struct { void *first; void *last; u16 count; u16 linkOffset; } ChildList;
#define CHILD_LINK(list, object) ((ChildLink *)((char *)(object) + (list)->linkOffset))
extern void native_utility_child_arm9_arm_02003780(ChildList *, void *);
extern void native_utility_child_arm9_arm_02003720(ChildList *, void *);
extern void native_utility_child_arm9_arm_020036c4(ChildList *, void *);
void native_utility_child_arm9_main_02003720(ChildList *list, void *object) {
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
