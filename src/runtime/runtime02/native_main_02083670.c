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
extern u32 native_fn_020824b4();
extern u32 native_fn_020824c4();
extern u32 native_fn_020835d4();
extern u8 native_data_021c72a0[];
u32 native_main_02083670(void *arg0) {
    u16 temp_ip;
    u16 temp_r1;
    u16 temp_r3;
    u32 temp_r0;

    temp_r1 = M2C_FIELD(arg0, u16 *, 2);
    if (temp_r1 != 0) {
        native_fn_020824c4(temp_r1);
        return native_fn_020824b4(9);
    }
    temp_r3 = M2C_FIELD(arg0, u16 *, 0xA);
    temp_ip = M2C_FIELD(arg0, u16 *, 8);
    if ((u32) M2C_FIELD(native_data_021c72a0, u16 *, 0x14) > (u32) temp_r3) {
        M2C_FIELD(native_data_021c72a0, u16 *, 0x14) = temp_r3;
        M2C_FIELD(native_data_021c72a0, u16 *, 8) = (u16) (1 << (temp_ip - 1));
    } else if (M2C_FIELD(native_data_021c72a0, u16 *, 0x14) == temp_r3) {
        M2C_FIELD(native_data_021c72a0, u16 *, 8) = (u16) (M2C_FIELD(native_data_021c72a0, u16 *, 8) | (1 << (temp_ip - 1)));
    }
    temp_r0 = native_fn_020835d4((u16) (temp_ip + 1));
    if (temp_r0 == 0x18) {
        return native_fn_020824b4(7);
    }
    if (temp_r0 == 2) {
        return temp_r0;
    }
    return native_fn_020824b4(9);
}
