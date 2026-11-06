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
extern u32 native_fn_01ffa978();
extern u32 native_fn_01ffae9c();
extern u32 native_fn_01ffb0bc();
extern u32 native_fn_01ffb324();
extern u32 native_fn_01ffb340();
extern u32 native_fn_01ffb35c();
extern u32 native_fn_01ffb368();
extern u32 native_fn_020896b8();
extern u32 native_data_01fff950;
u32 native_itcm_01ffb158(s32 arg0, s32 arg1) {
    native_fn_020896b8();
    if (M2C_FIELD((void *) native_fn_01ffb340(), u8 *, 0x11) != 0) {
        return 0U;
    }
    if (!(M2C_FIELD((void *) native_fn_01ffb35c(), u16 *, 2) & 0x800)) {
        return 0U;
    }
    native_fn_01ffae9c(native_fn_01ffa978(), arg0, arg1, 0x57);
    native_fn_01ffb0bc((s8) (native_fn_01ffb368() + 5));
    native_fn_01ffb324(0);
    native_data_01fff950 = 1;
    return 1U;
}
