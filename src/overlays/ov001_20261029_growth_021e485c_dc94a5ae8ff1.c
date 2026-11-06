typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_fn_02008d78();
extern u32 native_fn_02063c00();
extern u32 native_fn_02065380();
extern u32 native_fn_ov001_021d8d1c();
extern u32 native_fn_ov001_021e4120();
extern u32 native_fn_ov001_021e4500();
u32 native_ov001_021e485c(void *arg0, s32 arg1, s32 arg2, s32 arg3) {
    s16 skill_delta;
    s32 level;
    u8 skill_count;
    void *growth;

    growth = arg0 + 0x20C;
    native_fn_02008d78(growth, 0, 0x20);
    level = arg1 + 1;
    skill_count = M2C_FIELD(M2C_FIELD(arg0, void **, 0x1E8), u8 *, 0xA8);
    if (level <= arg2) {
        do {
            native_fn_ov001_021e4120(growth, M2C_FIELD(M2C_FIELD(arg0, void **, 0x1E8), s32 *, 0), level);
            M2C_FIELD(growth, u8 *, 0xC) = (u8) (M2C_FIELD(growth, u8 *, 0xC) + 1);
            M2C_FIELD(growth, s16 *, 0xE) = (s16) (M2C_FIELD(growth, s16 *, 0xE) + (((s32)(skill_count * native_fn_ov001_021d8d1c(level)) + 4) / 5));
            level += 1;
        } while (level <= arg2);
    }
    M2C_FIELD(arg0, s16 *, 0x1EC) = (s16) (M2C_FIELD(arg0, s16 *, 0x1EC) + M2C_FIELD(growth, s16 *, 0));
    M2C_FIELD(arg0, s16 *, 0x1EE) = (s16) (M2C_FIELD(arg0, s16 *, 0x1EE) + M2C_FIELD(growth, s16 *, 2));
    M2C_FIELD(arg0, s16 *, 0x1F4) = (s16) (M2C_FIELD(arg0, s16 *, 0x1F4) + M2C_FIELD(growth, s16 *, 4));
    M2C_FIELD(arg0, s16 *, 0x1F6) = (s16) (M2C_FIELD(arg0, s16 *, 0x1F6) + M2C_FIELD(growth, s16 *, 6));
    M2C_FIELD(arg0, s16 *, 0x1F8) = (s16) (M2C_FIELD(arg0, s16 *, 0x1F8) + M2C_FIELD(growth, s16 *, 8));
    M2C_FIELD(arg0, s16 *, 0x1FA) = (s16) (M2C_FIELD(arg0, s16 *, 0x1FA) + M2C_FIELD(growth, s16 *, 0xA));
    M2C_FIELD(arg0, u8 *, 0x1FC) = (u8) (M2C_FIELD(arg0, u8 *, 0x1FC) + M2C_FIELD(growth, u8 *, 0xC));
    M2C_FIELD(arg0, s16 *, 0x208) = (s16) (M2C_FIELD(arg0, s16 *, 0x208) + M2C_FIELD(growth, s16 *, 0xE));
    if ((s32) M2C_FIELD(arg0, s16 *, 0x208) > 0x3E7) {
        M2C_FIELD(arg0, s16 *, 0x208) = 0x3E7;
    }
    if ((s32) M2C_FIELD(growth, s16 *, 0xE) > 0) {
        native_fn_02063c00(0x13, 1);
    }
    native_fn_ov001_021e4500(arg0, growth);
    skill_delta = M2C_FIELD(growth, s16 *, 0xE);
    if ((skill_delta != 0) && (arg3 != 0)) {
        return native_fn_02065380(M2C_FIELD(arg0, u8 *, 0x31F));
    }
    return (u32) skill_delta;
}
