typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef signed int s32;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_fn_ov001_021db438();
extern u32 native_fn_ov001_021e2b88();
extern u32 native_fn_ov001_021e81d0();
extern u32 native_fn_ov001_022180e0();
u32 native_ov001_021e6db4(u32 side, s32 action, s32 slot) {
    s32 member;
    u32 actor;
    u32 otherAction;

    actor = native_fn_ov001_021db438(side, slot);
    if (M2C_FIELD((void *) native_fn_ov001_022180e0(action), u8 *, 4) & 0x20) {
        if (((s32) native_fn_ov001_021e2b88() >= 2) && (M2C_FIELD(actor, u16 *, 0x344) == action)) {
            return 1U;
        }
        member = 0;
        do {
            if (member != slot) {
                otherAction = *(u16 *) native_fn_ov001_021e81d0(side, member);
                if (otherAction == action) return 1U;
            }
            member += 1;
        } while (member < 3);
    }
    return 0U;
}
