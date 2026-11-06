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
extern u32 native_data_020edf74;
extern List native_data_020edf78;
extern u32 native_fn_0202b9cc(u32);
extern void native_fn_02008c14(u32, void *, u32);
extern void native_fn_0202b9dc(List *, u16);
extern List *native_fn_0202b8ec(Heap *);
extern void native_fn_0202ba20(List *, Heap *);
void native_main_0202b914(Heap *heap, u32 signature, void *start, void *end, u16 flags) {
    u32 span;
    heap->signature = signature;
    heap->start = start;
    heap->end = end;
    heap->attribute = 0;
    {
        u32 maskBits = 255;
        u32 newValue = flags & maskBits;
        heap->attribute &= ~maskBits;
        heap->attribute |= newValue;
    }
    span = (u32)end - (u32)start;
    if (((u16)(heap->attribute & 255)) & 2) {
        native_fn_02008c14(native_fn_0202b9cc(0), start, span);
    }
    native_fn_0202b9dc(&heap->children, 4);
    if (!native_data_020edf74) {
        native_fn_0202b9dc(&native_data_020edf78, 4);
        native_data_020edf74 = 1;
    }
    native_fn_0202ba20(native_fn_0202b8ec(heap), heap);
}
