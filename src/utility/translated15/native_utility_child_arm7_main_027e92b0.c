typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_arm_027e92fc(void);
extern u32 native_utility_child_arm7_arm_027f25e0(u32, u32);
extern u32 native_utility_child_arm7_data_0380fff4[];
void native_utility_child_arm7_main_027e92b0(void *arg0) {
    if (M2C_FIELD(arg0, u16 *, 0) != 0) {
        native_utility_child_arm7_arm_027e92fc();
        native_utility_child_arm7_arm_027f25e0(M2C_FIELD(arg0, u32 *, 8), M2C_FIELD(arg0, s32 *, 0xC) - 0x10);
        M2C_FIELD(*native_utility_child_arm7_data_0380fff4, u16 *, 0x3FC) = (u16) (M2C_FIELD(*native_utility_child_arm7_data_0380fff4, u16 *, 0x3FC) + 1);
    }
}
