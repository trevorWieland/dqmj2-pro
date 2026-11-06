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
extern u32 native_fn_02049ffc(u32);
extern u32 native_fn_02061dcc(u32);
extern u32 native_fn_02087a48(u32, u32, u32, u32, u32, u32);
void native_itcm_01ffb648(u32 arg0, u32 arg1) {
    u32 temp_r4;

    temp_r4 = M2C_FIELD(*(void **) native_fn_02061dcc((u32) (s8) arg0), u32 *, 4);
    native_fn_02049ffc(temp_r4);
    native_fn_02087a48(temp_r4, 0U, 0U, 0U, 1U, arg1);
}
