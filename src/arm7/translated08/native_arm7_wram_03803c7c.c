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
extern u32 native_arm7_fn_037fc760(u32, u32, u32);
extern u32 native_arm7_fn_03804048(u32);
extern u32 native_arm7_fn_03805784(u32);
extern u32 native_arm7_fn_03804a20(u32);
extern u32 native_arm7_fn_027f5188(u32);
extern u32 native_arm7_data_03809be0;
void native_arm7_wram_03803c7c(void) {
    u32 *sp0;
    u32 temp_r1;

loop_1:
    native_arm7_fn_037fc760((u32) &native_arm7_data_03809be0, (u32) &sp0, 1U);
    temp_r1 = *sp0;
    switch (temp_r1) {
    case 1:
        break;
    default:
        goto loop_1;
    case 0:
        native_arm7_fn_03804048((u32) sp0);
        goto loop_1;
    case 2:
        native_arm7_fn_03805784((u32) sp0);
        goto loop_1;
    case 3:
        native_arm7_fn_03804a20((u32) sp0);
        goto loop_1;
    }
    native_arm7_fn_027f5188((u32) sp0);
    goto loop_1;
}
