typedef unsigned char u8;
typedef signed short s16;
typedef signed int s32;
extern s32 native_fn_02066358(u8 *, const u8 *, s32, s32, const u8 *, s32, u8 *, s32);
s32 native_ov000_022140c0(u8 *record, const u8 *features, s32 item) {
    s32 species;
    u8 *block;
    u8 *bonus;
    s32 variant;
    if (record != 0) {
        block = record + 0x20;
        bonus = record + 0x40;
        species = *(s16 *)(record + 0x18);
        variant = record[0x1A];
    } else {
        block = 0;
        bonus = 0;
        species = 0;
        variant = 0;
    }
    return native_fn_02066358(block, bonus, species, variant, features, item, 0, 1);
}
