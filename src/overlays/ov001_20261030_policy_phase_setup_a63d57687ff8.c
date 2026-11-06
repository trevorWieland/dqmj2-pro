typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_fn_020649c0();
extern u32 native_fn_ov001_021e6d58();
extern u8 native_data_ov001_022355e8[];
extern u8 native_data_ov001_022362ac[];
u32 native_ov001_021da124(s32 initialize) {
    s32 slot;
    u32 count;
    u32 prepared;
    u8 *actor;
    u8 *savedPhase;

    count = 0;
    prepared = native_fn_020649c0(0);
    actor = native_data_ov001_022362ac;
    savedPhase = native_data_ov001_022355e8;
    slot = 0;
    do {
        if (((s32) M2C_FIELD(prepared, s16 *, 0x2E) >= 0) && (M2C_FIELD(actor, u8 *, 0x322) == 1)) {
            if (initialize == 0) {
                M2C_FIELD(actor, u8 *, 0x35B) = (u8) *savedPhase;
            } else {
                native_fn_ov001_021e6d58(slot);
            }
            count += 1;
        }
        slot += 1;
        prepared += 0x210;
        actor += 0x440;
        savedPhase += 1;
    } while (slot < 3);
    return count;
}
