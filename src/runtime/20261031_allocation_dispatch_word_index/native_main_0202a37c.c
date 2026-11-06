typedef unsigned char u8;
typedef signed char s8;
typedef unsigned int u32;
typedef signed int s32;
typedef struct {
    u32 enabled;
    u32 unknown4;
    u32 unknown8;
    u32 allocations;
    u32 heap;
} HeapSlot;
extern s8 native_data_020dd580[];
extern HeapSlot native_data_020edd64[];
extern u8 native_data_020edd54[];
extern u32 native_fn_0202b334(u32 heap, u32 bytes, s32 alignment);

u32 native_main_0202a37c(u32 index, u32 bytes, s32 alignment) {
    u32 result = 0;
    if (index == 0xFFFFFFFF) index = (u32)(s32)native_data_020dd580[0];
    if ((u8)index < 16) {
        HeapSlot *slot = &native_data_020edd64[index];
        if (slot->enabled != 0) {
            result = native_fn_0202b334(slot->heap, bytes, alignment);
            if (result != 0) {
                slot->allocations++;
                native_data_020edd54[2] = 0;
            } else {
                native_data_020edd54[2] = 5;
            }
        } else {
            native_data_020edd54[2] = 1;
        }
    } else {
        native_data_020edd54[2] = 1;
    }
    return result;
}
