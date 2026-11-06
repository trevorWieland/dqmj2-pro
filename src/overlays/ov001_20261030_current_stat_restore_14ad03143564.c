typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
typedef float f32;
typedef double f64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
#define MULT_HI(a, b) ((s32)(((s64)(s32)(a) * (s32)(b)) >> 32))
#define MULTU_HI(a, b) ((u32)(((u64)(u32)(a) * (u32)(b)) >> 32))
#define ROTATE_RIGHT(value, amount) (((u32)(value) >> ((u32)(amount) & 31)) | ((u32)(value) << ((0U - (u32)(amount)) & 31)))
#define NULL ((void *)0)
extern u32 native_fn_02026144();
extern u32 native_fn_0207c2b8();
extern u32 native_fn_0207c3d8();
void native_ov001_021d9d0c(void *actor) {
    u32 temp_r0;
    u32 temp_r0_2;
    u32 var_r0;
    u32 var_r0_2;
    u32 var_r0_3;
    u8 *data;
    void *stats;
    void *modifiers;
    s16 currentHp;
    s16 currentMp;
    s32 modifiedMpMaximum;
    s32 modifiedHpMaximum;

    modifiers = actor + 0x21C;
    data = M2C_FIELD(actor, u8 **, 0x1E8);
    stats = actor + 0x1EC;
    modifiedHpMaximum = M2C_FIELD(modifiers, s16 *, 0) + native_fn_0207c2b8(stats, data + 0x46);
    if (modifiedHpMaximum <= 0) {
        var_r0_2 = 0;
    } else {
        var_r0_2 = native_fn_02026144(((M2C_FIELD(stats, s16 *, 4) * native_fn_0207c2b8(stats, data + 0x46)) + modifiedHpMaximum) - 1, modifiedHpMaximum);
    }
    M2C_FIELD(stats, s16 *, 4) = (s16) var_r0_2;
    modifiedMpMaximum = M2C_FIELD(modifiers, s16 *, 2) + native_fn_0207c3d8(stats, data + 0x46);
    if (modifiedMpMaximum <= 0) {
        var_r0_3 = 0;
    } else {
        var_r0_3 = native_fn_02026144(((M2C_FIELD(stats, s16 *, 6) * native_fn_0207c3d8(stats, data + 0x46)) + modifiedMpMaximum) - 1, modifiedMpMaximum);
    }
    M2C_FIELD(stats, s16 *, 6) = (s16) var_r0_3;
    currentHp = M2C_FIELD(stats, s16 *, 4);
    if ((s32) currentHp > 0) {
        if ((s32) currentHp >= (s32) (s16) native_fn_0207c2b8(stats, data + 0x46)) {
            currentHp = (s16) native_fn_0207c2b8(stats, data + 0x46);
        }
        M2C_FIELD(stats, s16 *, 4) = currentHp;
    }
    currentMp = M2C_FIELD(stats, s16 *, 6);
    temp_r0 = native_fn_0207c3d8(stats, data + 0x46);
    var_r0 = temp_r0 << 0x10;
    if ((s32) currentMp >= (s32) (s16) temp_r0) {
        temp_r0_2 = native_fn_0207c3d8(stats, data + 0x46);
        var_r0 = temp_r0_2 << 0x10;
        currentMp = (s16) temp_r0_2;
    }
    M2C_FIELD(stats, s16 *, 6) = currentMp;
    return;
}
