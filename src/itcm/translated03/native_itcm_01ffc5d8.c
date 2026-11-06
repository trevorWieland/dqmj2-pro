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
extern u32 native_fn_01ffa5ac();
extern u32 native_fn_01ffa5fc();
extern u32 native_fn_01ffb500();
extern u32 native_fn_020894bc();
extern u32 native_fn_020894d4();
extern u8 native_data_021d4100[];
extern u8 native_data_021d4120[];
u32 native_itcm_01ffc5d8(void) {
    if (native_fn_01ffa5fc(0, M2C_FIELD(native_data_021d4100, u16 *, 4)) == 0) {
        return 0U;
    }
    M2C_FIELD(native_data_021d4100, s32 *, 0x20) = (s32) *(s32 *) native_fn_020894bc();
    M2C_FIELD(native_data_021d4100, u16 *, 0x24) = (u16) *(u16 *) native_fn_01ffb500();
    M2C_FIELD(native_data_021d4100, s8 *, 0x29) = (s8) *(s32 *) native_fn_020894d4();
    M2C_FIELD(native_data_021d4100, u16 *, 4) = (u16) (M2C_FIELD(native_data_021d4100, u16 *, 4) + 1);
    native_fn_01ffa5ac(native_data_021d4120, 0xC, M2C_FIELD(native_data_021d4100, u16 *, 4));
    return 1U;
}
