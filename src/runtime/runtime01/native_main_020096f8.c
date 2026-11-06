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
extern u32 native_fn_020095e8();
extern u32 native_fn_020097b8();
extern u32 native_fn_02009ad4();
extern u32 native_fn_02009b74();
extern u32 native_fn_02009b9c();
extern u32 native_fn_02009be4();
u32 native_main_020096f8(s32 arg0) {
    u32 temp_r0;
    u32 temp_r0_2;
    u32 temp_r0_3;

    if (native_fn_02009be4() == 0) {
        return 0U;
    }
    temp_r0_3 = native_fn_02009b9c();
    if (temp_r0_3 != 0) {
        return temp_r0_3;
    }
    if (!(arg0 & 1)) {
        return 0U;
    }
    if ((s32) native_fn_02009ad4() > 0) {
        do {

        } while (native_fn_020095e8(0) != 0);
        temp_r0_2 = native_fn_02009b9c();
        if (temp_r0_2 != 0) {
            return temp_r0_2;
        }
        goto block_12;
    }
    native_fn_020097b8(1);
block_12:
    native_fn_02009b74();
    do {
        native_fn_020095e8(1);
        temp_r0 = native_fn_02009b9c();
    } while (temp_r0 == 0);
    return temp_r0;
}
