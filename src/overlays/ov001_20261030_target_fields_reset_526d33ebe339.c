typedef unsigned char u8;
typedef signed char s8;
typedef unsigned int u32;
typedef signed int s32;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 ov001_side_slot_record_021db438(s32, u32);
extern u32 ov001_record_is_active_021db8d0(void *);
extern u32 native_fn_ov001_021ee9fc(void *);
u32 native_ov001_021ec620(void *actor) {
    u32 other_team;
    u32 result;
    s32 index;
    u32 target;

    if (M2C_FIELD(actor, u8 *, 0x31E) == 0) {
        other_team = 1;
    } else {
        other_team = 0;
    }
    target = ov001_side_slot_record_021db438(other_team, 0);
    index = 0;
    do {
        result = ov001_record_is_active_021db8d0((void *)target);
        if (result != 0) {
            result = native_fn_ov001_021ee9fc((void *)target);
        }
        index += 1;
        target += 0x440;
    } while (index < 3);
    return result;
}
