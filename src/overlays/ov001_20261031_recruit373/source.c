#include "context.h"
void native_ov001_02209b4c(void) {
    void *first_actor;
    void *second_actor;
    void *current_actor;
    u32 first_index;
    u32 second_index;

    first_index = 0;
    do {
        first_actor = ov001_side_slot_record_021db438(0, first_index);
        if ((M2C_FIELD(first_actor, u8 *, 0x31C) != 0) && (native_fn_ov001_02209ac0(first_actor) != 0)) {
            M2C_FIELD(first_actor, s8 *, 0x1FD) = 0;
            M2C_FIELD(first_actor, s8 *, 0x1FF) = 0;
            native_fn_ov001_021db788(first_actor, native_fn_ov001_021dbcbc(first_actor));
            native_fn_ov001_021db7cc(first_actor, native_fn_ov001_021dbcf0(first_actor));
        }
        first_index += 1;
    } while ((s32) first_index < 3);
    second_index = 0;
    do {
        second_actor = ov001_side_slot_record_021db438(2, second_index);
        current_actor = second_actor;
        if (M2C_FIELD(current_actor, u8 *, 0x31C) != 0) {
            if (native_fn_ov001_02209ac0(second_actor) != 0) {
                M2C_FIELD(current_actor, s8 *, 0x1FD) = 0;
                M2C_FIELD(current_actor, s8 *, 0x1FF) = 0;
                native_fn_ov001_021db788(current_actor, native_fn_ov001_021dbcbc(current_actor));
                native_fn_ov001_021db7cc(current_actor, native_fn_ov001_021dbcf0(current_actor));
            }
        }
        second_index += 1;
    } while ((s32) second_index < 3);

}
