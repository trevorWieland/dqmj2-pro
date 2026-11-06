typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_arm_0380576c(void);
extern u32 native_utility_child_arm7_arm_038057c8(u32);
extern u8 native_utility_child_arm7_data_027f94f0[];
void native_utility_child_arm7_main_027e1ddc(void) {
    void *temp_r0;

    if (M2C_FIELD(M2C_FIELD(native_utility_child_arm7_data_027f94f0, void **, 0x550), u16 *, 0xC2) != 0) {
        temp_r0 = (void *) native_utility_child_arm7_arm_0380576c();
        M2C_FIELD(temp_r0, s16 *, 0) = 8;
        M2C_FIELD(temp_r0, s16 *, 2) = 0;
        M2C_FIELD(temp_r0, s16 *, 8) = 2;
        native_utility_child_arm7_arm_038057c8((u32) temp_r0);
    }
}
