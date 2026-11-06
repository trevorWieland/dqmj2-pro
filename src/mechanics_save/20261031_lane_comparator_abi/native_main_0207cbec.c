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
typedef struct { u8 prefix[4]; u16 low:4; u16 four:4; u16 rest:8; u16 key:13; u16 other:3; u8 tail[92]; } NativeKind;
extern const NativeKind *native_fn_020449d4(s32);
extern const u8 *native_fn_02062a10(u32);
s32 native_main_0207cbec(const u32 *arg0, const u32 *arg1) {
    u8 temp_r0;
    u32 temp_r4_2;
    const NativeKind *temp_r4;
    u8 temp_r5;
    u32 temp_r6;

    temp_r4_2 = *arg1;
    temp_r6 = *arg0;
    if (temp_r4_2 == 0) {
        return -1;
    }
    if (temp_r6 == 0) {
        return 1;
    }
    temp_r5 = M2C_FIELD((void *) native_fn_02062a10(temp_r6), u8 *, 0x30);
    temp_r0 = M2C_FIELD((void *) native_fn_02062a10(temp_r4_2), u8 *, 0x30);
    if (temp_r5 != temp_r0) {
        return temp_r0 - temp_r5;
    }
    temp_r4 = native_fn_020449d4(M2C_FIELD((void *) native_fn_02062a10(temp_r4_2), s16 *, 0x18));
    return temp_r4->key-native_fn_020449d4(M2C_FIELD(native_fn_02062a10(temp_r6),s16 *,0x18))->key;
}
