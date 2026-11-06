typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef struct Block Block;
struct Block {
    u16 marker;
    volatile u16 attributes;
    u32 bytes;
    Block *previous;
    Block *next;
};
typedef struct {
    u32 begin;
    u32 end;
} Region;
typedef struct {
    Block *head;
    Block *tail;
    Block *usedHead;
    Block *usedTail;
    u16 group;
} HeapList;
extern void native_fn_0202ad78(Region *, Block *);
extern Block *native_fn_0202ada4(HeapList *, Block *);
extern Block *native_fn_0202adcc(HeapList *, Block *, Block *);
extern Block *native_fn_0202adfc(Region *, u32);
extern void native_fn_02008c14(u32, u32, u32);
extern u32 native_fn_0202b9cc(u32);

u32 native_main_0202ae9c(HeapList *list, Block *block, u32 start, u32 bytes, u16 direction) {
    Region before;
    Region after;
    Region used;
    Block *previous;
    Block *allocated;
    u32 header = start - 16;
    u32 flags;
    native_fn_0202ad78(&before, block);
    after.end = before.end;
    before.end = header;
    after.begin = start + bytes;
    previous = native_fn_0202ada4(list, block);
    if (before.end - before.begin < 20) {
        before.end = before.begin;
    } else {
        block = native_fn_0202adfc(&before, 0x4652);
        previous = native_fn_0202adcc(list, block, previous);
    }
    if (after.end - after.begin < 20) {
        after.begin = after.end;
    } else {
        block = native_fn_0202adfc(&after, 0x4652);
        native_fn_0202adcc(list, block, previous);
    }
    flags = ((u32 *)list)[-1] & 255;
    if (flags & 1) {
        native_fn_02008c14(0, before.end, after.begin - before.end);
    } else if (flags & 2) {
        native_fn_02008c14(native_fn_0202b9cc(1), before.end, after.begin - before.end);
    }
    used.begin = header;
    used.end = after.begin;
    allocated = native_fn_0202adfc(&used, 0x5544);
    allocated->attributes &= ~0x8000;
    allocated->attributes |= (direction & 1) << 15;
    allocated->attributes &= ~0x7F00;
    allocated->attributes |= ((u16)((u32)allocated - before.end) & 127) << 8;
    allocated->attributes &= ~255;
    allocated->attributes |= list->group & 255;
    native_fn_0202adcc((HeapList *)&list->usedHead, allocated, list->usedTail);
    return start;
}
