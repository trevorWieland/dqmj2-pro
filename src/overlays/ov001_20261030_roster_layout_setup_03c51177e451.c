typedef unsigned char u8;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
extern u32 native_fn_020443ec(void);
extern u32 native_fn_02044424(u32);
extern void native_fn_02044ff4(u8 *, s32, u32);
extern u8 *native_fn_ov001_021db438(u32, u32);
extern u32 native_fn_ov001_021db8d0(u8 *);
extern u32 native_fn_ov001_021e2c10(void);
extern void native_fn_ov001_021f1508(void);
extern void native_fn_ov001_021f153c(u8 *, s32, s32);
extern void native_fn_ov001_021f15d8(void);
extern void native_fn_ov001_021f1604(void);
extern void native_fn_ov001_021f1634(void);
extern void native_fn_ov001_021f1684(void);
extern void native_fn_ov001_021f1804(void);
extern void native_fn_ov001_022033f8(u32);
extern u8 native_data_ov001_0222e0f4[];
u32 native_ov001_02210e18(void) {
    u32 delay;
    u8 *scan_actor;
    u8 *record;
    u8 enabled;
    s32 scan_index;
    u32 created;
    s32 layout_count;
    u8 *positions;
    u8 *actor;
    s32 slot;

    layout_count = 0;
    native_fn_ov001_021f1508();
    scan_actor = native_fn_ov001_021db438(1U, 0U);
    scan_index = 0;
    do {
        enabled = scan_actor[0x31C];
        scan_index += 1;
        scan_actor += 0x440;
        if (enabled != 0) {
            layout_count += 1;
        }
    } while (scan_index < 3);
    created = 0;
    actor = native_fn_ov001_021db438(1U, 0U);
    positions = native_data_ov001_0222e0f4 + (layout_count * 3);
    layout_count &= 1;
    slot = 0;
    do {
        if (native_fn_ov001_021db8d0(actor) != 0) {
            if ((native_fn_020443ec() == 0) || (native_fn_020443ec() == 6)) {
                record = *(u8 **)(actor + 0x1E8);
                native_fn_02044ff4(record + 0xB2, *(s16 *)(record + 0x2A), record[0x2C]);
            }
            if (layout_count != 0) {
                native_fn_ov001_021f153c(*(u8 **)(actor + 0x1E8) + 0xB2, positions[-3], (s16) (((u32)slot % 2U) * 2U + 0x14));
            } else {
                native_fn_ov001_021f153c(*(u8 **)(actor + 0x1E8) + 0xB2, positions[-3], 0x14);
            }
            created += 1;
        }
        slot += 1;
        positions += 1;
        actor += 0x440;
    } while (slot < 3);
    native_fn_ov001_021f15d8();
    if (native_fn_ov001_021e2c10() != 0) {
        if (native_fn_02044424(0x08000000) != 0) {
            delay = 0xF;
        } else {
            delay = 0x1E;
        }
        native_fn_ov001_022033f8(delay);
        native_fn_ov001_021f1604();
    }
    if (native_fn_020443ec() == 6) {
        native_fn_ov001_021f1634();
        native_fn_ov001_021f1804();
    }
    native_fn_ov001_021f1684();
    return created;
}
