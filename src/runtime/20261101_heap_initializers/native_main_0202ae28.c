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
extern void native_fn_0202b914(Heap *, u32, void *, void *, u16);
extern Block *native_fn_0202adfc(Region *, u16);
Heap *native_main_0202ae28(void *start, void *end, u16 flags) {
    Heap *heap = start;
    ExpHeap *exp = (ExpHeap *)((u8 *)heap + sizeof(Heap));
    native_fn_0202b914(heap, 0x45585048, (u8 *)exp + sizeof(ExpHeap), end, flags);
    exp->group = 0;
    exp->feature = 0;
    {
        u32 maskBits = 1;
        u32 newValue = 0;
        exp->feature &= ~maskBits;
        exp->feature |= newValue;
    }
    {
        Block *block;
        Region region;
        region.start = heap->start;
        region.end = heap->end;
        block = native_fn_0202adfc(&region, 0x4652);
        exp->freeHead = block;
        exp->freeTail = block;
        exp->usedHead = 0;
        exp->usedTail = 0;
        return heap;
    }
}
