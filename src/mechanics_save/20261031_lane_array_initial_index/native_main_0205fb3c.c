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
extern u32 native_fn_02048a9c(void *,u32);
extern u32 native_fn_0205f98c(s32,s32);
void native_main_0205fb3c(void *arg0, u32 arg1) {
    u32 temp_r0_3;
    u8 temp_r0;
    u8 temp_r0_2;
    u8 var_r4;

    temp_r0_3 = M2C_FIELD(arg0, u32 *, 0x1C);
    if (temp_r0_3 == 0) {
        return;
    }
    temp_r0_2 = M2C_FIELD(arg0, u8 *, 0x22);
    var_r4 = 0;
    if ((u32)temp_r0_2 <= (u32)var_r4) {
        return;
    }
    do {
        native_fn_02048a9c((void *)native_fn_0205f98c(M2C_FIELD(arg0, u32 *, 0x1C), var_r4), arg1);
        temp_r0 = M2C_FIELD(arg0, u8 *, 0x22);
        var_r4 += 1;
    } while ((u32) var_r4 < (u32) temp_r0);
    return;
}
