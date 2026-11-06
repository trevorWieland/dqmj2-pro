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
extern u32 native_fn_ov001_02204250();
extern u8 native_data_ov001_0223e120[];
void native_ov001_022116d0(void) {
    s8 var_r5;
    u8 *var_r6;

    var_r6 = native_data_ov001_0223e120;
    var_r5 = 0;
    do {
        if ((s8) *var_r6 != 0x7F) {
            M2C_FIELD((void *) native_fn_ov001_02204250(), s16 *, 0x26) = 0xF;
        }
        var_r5 += 1;
        var_r6 += 1;
    } while ((s32) var_r5 < 3);
}
