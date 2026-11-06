typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef struct Range {
    u16 first;
    u16 last;
    struct Range *next;
    u8 bytes[];
} Range;
typedef struct {
    u32 opaque;
    u8 fallback[8];
    Range *head;
} Map;

u32 native_main_02036994(void **holder, u32 key) {
    u16 first;
    Range *range;
    Map *base = (Map *)*holder;
    range = base->head;
    while (range) {
        first = range->first;
        if ((u32)first <= key && key <= (u32)range->last) {
            return (u32)(range->bytes + (key - first) * 3);
        }
        range = range->next;
    }
    return (u32)base->fallback;
}
