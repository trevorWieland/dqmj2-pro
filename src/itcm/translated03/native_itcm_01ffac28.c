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
extern u32 native_fn_01ffb34c();
extern u32 native_fn_0204983c();
extern u32 native_fn_02049d50();
extern u32 native_fn_0204b77c();
extern u32 native_fn_0205fd80();
extern u32 native_fn_ov000_02215a14();
extern u32 native_fn_ov000_022162b4();
extern u8 native_data_01fff960[];
extern u8 native_data_01fff9a8[];
u8 native_data_01fff960[0x48];
u8 native_data_01fff9a8[0xC];

u32 native_itcm_01ffac28(void) {
    native_fn_ov000_02215a14();
    native_fn_ov000_022162b4(M2C_FIELD(native_data_01fff9a8, s8 *, 0x1C), 3);
    native_fn_ov000_022162b4(M2C_FIELD(native_data_01fff9a8, s8 *, 0x1C), 0x7F);
    native_fn_0204983c(0x7F, 0);
    native_fn_0204983c(0x7F, 1);
    native_fn_0204983c(0x7F, 0xC);
    native_fn_0204b77c(native_data_01fff960);
    native_fn_01ffb34c();
    native_fn_0204b77c();
    native_fn_02049d50();
    return native_fn_0205fd80(1);
}
