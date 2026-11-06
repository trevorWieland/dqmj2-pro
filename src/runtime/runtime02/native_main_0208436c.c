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
extern u32 native_fn_02083504();
extern u8 native_data_021c9600[];
u32 native_main_0208436c(void) {
    s32 var_r3;
    u32 var_r4;
    void *var_ip;

    var_r4 = 0;
    if (native_fn_02083504() == 2) {
        var_r3 = 0;
        var_ip = M2C_FIELD(native_data_021c9600, void **, 0x18);
        if ((s32) M2C_FIELD(native_data_021c9600, u8 *, 0) > 0) {
            do {
                if (M2C_FIELD(var_ip, u8 *, 0xC0) != 0) {
                    var_r4 += 1;
                    M2C_FIELD(var_ip, u16 *, 0xC2) = (u16) (M2C_FIELD(var_ip, u16 *, 0xC2) - 1);
                    if (M2C_FIELD(var_ip, u16 *, 0xC2) == 0) {
                        M2C_FIELD(var_ip, u8 *, 0xC0) = 0U;
                    }
                }
                var_r3 += 1;
                var_ip += 0xC4;
            } while (var_r3 < (s32) M2C_FIELD(native_data_021c9600, u8 *, 0));
        }
    }
    return var_r4;
}
