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
Block *native_main_0202adfc(Region *region, u16 signature) {
    Block *block = region->start;
    block->signature = signature;
    block->attribute = 0;
    block->size = (u32)region->end - ((u32)block + sizeof(Block));
    block->previous = 0;
    block->next = 0;
    return block;
}
