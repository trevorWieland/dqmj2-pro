typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef struct {
    void *previous;
    void *next;
} Link;
typedef struct {
    void *head;
    void *tail;
    u16 count;
    u16 offset;
} List;
typedef struct {
    u32 signature;
    Link link;
    List children;
    void *start;
    void *end;
    u32 attribute;
} Heap;
typedef struct Block Block;
struct Block {
    u16 signature;
    u16 attribute;
    u32 size;
    Block *previous;
    Block *next;
};
typedef struct {
    Block *freeHead;
    Block *freeTail;
    Block *usedHead;
    Block *usedTail;
    u16 group;
    u16 feature;
} ExpHeap;
typedef struct {
    void *start;
    void *end;
} Region;
extern void native_fn_0202b9f4(List *, void *);
void native_main_0202ba20(List *list, void *object) {
    if (!list->head) {
        native_fn_0202b9f4(list, object);
    } else {
        Link *link = (Link *)((u8 *)object + list->offset);
        link->previous = list->tail;
        link->next = 0;
        ((Link *)((u8 *)list->tail + list->offset))->next = object;
        list->tail = object;
        ++list->count;
    }
}
