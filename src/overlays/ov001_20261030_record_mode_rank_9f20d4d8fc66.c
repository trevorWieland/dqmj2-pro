typedef unsigned char u8;
typedef signed char s8;
typedef unsigned int u32;
typedef signed int s32;
extern u32 native_fn_ov001_0220e3a8(u8 *, s32, s32, s32, s32);
u32 native_ov001_021f0ca0(u8 *actor, u8 *target, s32 primary_mode, s32 secondary_mode, s32 modifier_control) {
    u8 *record;
    u8 secondary_rank;
    s32 primary_rank;

    if (primary_mode > 0) {
        record = *(u8 **)(target + 0x1E8);
        primary_rank = (record + primary_mode)[0x86];
        if (secondary_mode != 0) {
            secondary_rank = (record + secondary_mode)[0x86];
        } else {
            secondary_rank = 0;
        }
        if (modifier_control != 0) {
            primary_rank = (s32) native_fn_ov001_0220e3a8(actor, primary_mode, secondary_mode, (s32) primary_rank, (s32) secondary_rank);
        } else if ((secondary_mode != 0) && ((s32) primary_rank >= (s32) secondary_rank)) {
            primary_rank = secondary_rank;
        }
        return (u32) primary_rank;
    }
    return 1U;
}
