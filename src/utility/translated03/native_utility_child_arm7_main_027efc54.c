typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_arm_037f8dc4(u32, u32);
u32 native_utility_child_arm7_main_027efc54(u32 arg0, void *arg1) {
    void *temp_r2;
    void *temp_r3;

    temp_r2 = arg1 + (M2C_FIELD(arg1, u16 *, 0xE) * 2);
    temp_r3 = temp_r2 + 0x10;
    M2C_FIELD(arg1, u16 *, 0xC) = (u16) M2C_FIELD(temp_r2, u16 *, 0x10);
    M2C_FIELD(temp_r3, s16 *, 2) = 2;
    M2C_FIELD(temp_r3, s16 *, 4) = 0;
    M2C_FIELD(temp_r3, u16 *, 6) = (u16) M2C_FIELD(arg1, u16 *, 0x18);
    return native_utility_child_arm7_arm_037f8dc4(arg0, (u32) arg1);
}
