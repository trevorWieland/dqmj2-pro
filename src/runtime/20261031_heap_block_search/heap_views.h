typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef signed int s32;
typedef struct Block Block;
struct Block {
    u16 marker;
    u16 attributes;
    u32 bytes;
    Block *previous;
    Block *next;
};
typedef struct {
    u8 unknown[0x24];
    Block *head;
    Block *tail;
    u32 unknown2c;
    u32 unknown30;
    u16 unknown34;
    u16 flags;
} Heap;
extern u32 native_fn_0202ae9c(void *list, Block *block, u32 start, u32 bytes, u32 direction);

static inline u16 heap_mode(Heap *heap) {
    return (u16)(heap->flags & 1);
}
