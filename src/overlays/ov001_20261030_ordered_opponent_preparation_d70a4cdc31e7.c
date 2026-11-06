typedef unsigned char u8;
typedef signed char s8;
typedef signed short s16;
typedef signed int s32;
typedef unsigned int u32;
__declspec(align(4)) typedef struct { s8 side; s8 slot; s16 key; } Position;
extern Position native_data_ov001_02238d40[6];
extern u8 *native_fn_ov001_021db438(s32, s32);
extern u32 native_fn_ov001_021db530(s32);
extern u32 native_fn_ov001_021db8d0(void *);
extern void native_fn_ov001_021dccd0(s32);
extern void native_fn_ov001_021e7538(s32, u8 *, u8 *, u32);
extern s32 native_fn_ov001_021e7740(u8 *, u32, u8 *, u32);
extern void native_fn_ov001_021e7d88(void);
extern u32 native_fn_0203d294(s32);
u32 native_ov001_021e7fa8(void) {
    s32 index;
    s32 selected;
    s32 count;
    s8 slot;
    u8 *own;
    u8 *opposing;
    u32 own_count;
    u32 opposing_count;
    native_fn_ov001_021e7d88();
    native_fn_ov001_021dccd0(0);
    own = native_fn_ov001_021db438(0, 0);
    opposing = native_fn_ov001_021db438(1, 0);
    own_count = native_fn_ov001_021db530(0);
    opposing_count = native_fn_ov001_021db530(1);
    count = native_fn_ov001_021e7740(own, own_count, opposing, opposing_count);
    index = 0;
    selected = 0;
    if (count > 0) {
        do {
            slot = native_data_ov001_02238d40[index].slot;
            if (native_data_ov001_02238d40[index].side == 1 &&
                native_fn_ov001_021db8d0(opposing + slot * 1088) != 0) {
                if (selected == 0) {
                    native_fn_ov001_021e7538(slot, opposing, own, 0);
                    selected++;
                } else if (native_fn_0203d294(3) != 0) {
                    native_fn_ov001_021e7538(slot, opposing, own, 0);
                    selected++;
                } else {
                    break;
                }
            }
            index++;
        } while (index < count);
    }
    return own_count + opposing_count;
}
