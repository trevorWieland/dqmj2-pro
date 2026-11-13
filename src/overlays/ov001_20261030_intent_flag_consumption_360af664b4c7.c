typedef unsigned char u8;
typedef unsigned int u32;
typedef signed int s32;
extern u32 native_fn_01ffa824(void);
extern u32 native_fn_01ffa84c(void);
extern u32 native_fn_020444ec(void);
extern u8 *ov001_side_slot_record_021db438(s32, s32);
extern u32 ov001_record_is_active_021db8d0(u8 *);
extern u8 *native_fn_ov001_021e81d0(s32, s32);
extern void native_fn_ov001_021e8398(s32, s32);
void native_ov001_021dcbe4(void) {
    s32 sides[2];
    s32 side_index;
    s32 actor_index;
    s32 side;
    u8 *actor;
    u32 selector;
    u32 result;
    if (native_fn_020444ec() != 0) {
        selector = native_fn_01ffa824();
        if ((u8)selector >= native_fn_01ffa84c()) {
            goto opposing_first;
        }
    }
    sides[0] = 0;
    sides[1] = 1;
    goto ready;
opposing_first:
    sides[0] = 1;
    sides[1] = 0;
ready:
    side_index = 0;
    do {
        side = sides[side_index];
        actor = ov001_side_slot_record_021db438(side, 0);
        actor_index = 0;
        do {
            result = ov001_record_is_active_021db8d0(actor);
            if (result != 0) {
                result = ((u32)actor[0x35D] << 29) >> 31;
                if (result != 0) {
                    if (native_fn_ov001_021e81d0(side, actor_index)[4] == 0) {
                        native_fn_ov001_021e8398(side, actor_index);
                    }
                    result = actor[0x35D] & ~4;
                    actor[0x35D] = result;
                }
            }
            actor_index++;
            actor += 1088;
        } while (actor_index < 3);
        side_index++;
    } while (side_index < 2);
}
