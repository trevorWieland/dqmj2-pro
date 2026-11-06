typedef unsigned short u16;
typedef unsigned int u32;
typedef struct Block Block;
struct Block {
    u16 marker;
    u16 attributes;
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
} List;
extern Block *native_fn_0202ada4(List *, Block *);
extern Block *native_fn_0202adcc(List *, Block *, Block *);
extern Block *native_fn_0202adfc(Region *, u32);
extern void native_fn_02008c14(u32, u32, u32);
extern u32 native_fn_0202b9cc(u32);

u32 native_main_0202b1a8(List *list, Region *region) {
    Region combined = *region;
    Block *current = list->head;
    Block *previous = 0;
    Block *created;
    u32 flags;
    u32 begin;
    u32 bytes;
    while (current != 0) {
        if ((u32)current < region->begin) {
            previous = current;
            current = current->next;
            continue;
        }
        if ((u32)current == region->end) {
            combined.end = (u32)(current + 1) + current->bytes;
            native_fn_0202ada4(list, current);
            if (((u32 *)list)[-1] & 2) {
                native_fn_02008c14(native_fn_0202b9cc(0), (u32)current, 16);
            }
        }
        break;
    }
    if (previous != 0 && (u32)(previous + 1) + previous->bytes == region->begin) {
        combined.begin = (u32)previous;
        previous = native_fn_0202ada4(list, previous);
    }
    if (combined.end - combined.begin < 16) return 0;
    flags = ((u32 *)list)[-1];
    begin = region->begin;
    bytes = region->end - begin;
    flags &= 255;
    if (flags & 2) {
        native_fn_02008c14(native_fn_0202b9cc(2), begin, bytes);
    }
    created = native_fn_0202adfc(&combined, 0x4652);
    native_fn_0202adcc(list, created, previous);
    return 1;
}
