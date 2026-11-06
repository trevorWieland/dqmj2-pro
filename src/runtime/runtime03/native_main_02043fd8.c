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
extern u32 native_fn_020431d4();
extern u32 native_fn_02043304();
extern u32 native_fn_02043370();
extern u32 native_fn_02043d9c();
extern u32 native_fn_0204411c();
extern u32 native_fn_02064438();
extern u32 native_fn_02064454();
extern u32 native_fn_020c5914();
extern u32 native_fn_020c5938();
extern u32 native_fn_020c5948();
extern u32 native_fn_ov001_021d9120();
extern u32 native_fn_ov001_021d93d8();
extern u32 native_fn_ov001_021da448();
extern u32 native_fn_ov001_021db64c();
extern u32 native_fn_ov001_021e3288();
extern u32 native_fn_ov001_021fc19c();
extern u32 native_fn_ov001_021fc36c();
extern u32 native_fn_ov001_0221395c();
extern u32 native_fn_ov001_022139b8();
extern u32 native_fn_ov001_022139e8();
extern u8 native_data_020f69c4[];
u32 native_main_02043fd8(void) {
    u32 temp_r4;

    native_fn_ov001_021da448();
    native_fn_ov001_021e3288();
    native_fn_02043d9c();
    native_fn_ov001_021db64c();
    native_fn_ov001_021d93d8();
    native_fn_0204411c();
    native_fn_ov001_021d9120();
    native_fn_02043370();
    native_fn_020431d4();
    native_fn_02043304();
    native_fn_020c5914();
    temp_r4 = native_fn_020c5938();
    if (temp_r4 > native_fn_02064454()) {
        native_fn_02064438(temp_r4);
        native_fn_020c5948(1);
    } else {
        native_fn_020c5948(0);
    }
    native_fn_ov001_021fc36c();
    native_fn_ov001_022139b8();
    native_fn_ov001_0221395c();
    native_fn_ov001_021fc19c();
    native_fn_ov001_022139e8(0);
    M2C_FIELD(native_data_020f69c4, s8 *, 3) = 0;
    return 1U;
}
