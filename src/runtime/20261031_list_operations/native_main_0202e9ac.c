#define NULL ((void *)0)
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
void native_main_0202e9ac(void **arg0, void *arg1) {
    void *var_r2;
    u32 key;
    u32 priority;
    u32 var_r0_2;
    void **var_r0;
    void *var_r3;
    void *var_r3_2;
    void *var_ip;

    var_r0 = arg0;
    var_ip = *var_r0;
    if (var_ip == NULL) {
        *var_r0 = arg1;
        return;
    }
    var_r2 = M2C_FIELD(var_ip, void **, 0x10);
    if (var_r2 == NULL) {
        if ((u32) M2C_FIELD(var_ip, u8 *, 0x18) > (u32) M2C_FIELD(arg1, u8 *, 0x18)) {
            var_r3 = arg1;
            if (M2C_FIELD(arg1, u32 *, 0x10) != 0) {
                do {
                    var_r3 = M2C_FIELD(var_r3, void **, 0x10);
                } while (M2C_FIELD(var_r3, s32 *, 0x10) != 0);
            }
            M2C_FIELD(var_r3, void **, 0x10) = var_ip;
            *var_r0 = arg1;
            return;
        }
        M2C_FIELD(var_ip, void **, 0x10) = arg1;
        return;
    }
    if (var_r2 != NULL) {
        key = M2C_FIELD(arg1, u8 *, 0x18);
        do {
        priority = M2C_FIELD(var_r2, u8 *, 0x18);
        if (priority >= key) {
            var_r0_2 = M2C_FIELD(arg1, u32 *, 0x10);
            var_r3_2 = arg1;
            if (var_r0_2 != 0) {
                do {
                    var_r3_2 = M2C_FIELD(var_r3_2, void **, 0x10);
                    var_r0_2 = M2C_FIELD(var_r3_2, u32 *, 0x10);
                } while (var_r0_2 != 0);
            }
            M2C_FIELD(var_ip, void **, 0x10) = arg1;
            M2C_FIELD(var_r3_2, void **, 0x10) = var_r2;
            return;
        }
        var_ip = var_r2;
        var_r2 = M2C_FIELD(var_r2, void **, 0x10);
        } while (var_r2 != NULL);
    }
    M2C_FIELD(var_ip, void **, 0x10) = arg1;
    return;
}
