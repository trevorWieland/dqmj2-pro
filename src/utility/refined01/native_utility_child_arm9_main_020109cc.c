typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_thumb_0200f8d4(void);
extern u32 native_utility_child_arm9_thumb_0200fa48(u32, u32);
extern u32 native_utility_child_arm9_thumb_0200fa74(u32, u32);
extern u32 native_utility_child_arm9_thumb_02009e30(u32);
extern u32 native_utility_child_arm9_thumb_02010935(u32, u32, u32);
extern u16 native_utility_child_arm9_data_0202cc88[];
extern u8 native_utility_child_arm9_data_0202cca0[];
extern u16 native_utility_child_arm9_data_0202ccc8[];
extern u8 native_utility_child_arm9_data_0202ccb0[];
extern u32 native_utility_child_arm9_data_027ffc3c[];
extern u32 native_utility_child_arm9_data_0202cc98[];
void native_utility_child_arm9_main_020109cc(void) {
    s32 var_r2;
    u16 *var_r1;

    if (*native_utility_child_arm9_data_0202cc88 == 0) {
        *native_utility_child_arm9_data_0202cc88 = 1;
        M2C_FIELD(native_utility_child_arm9_data_0202cca0, s32 *, 0) = 0;
        M2C_FIELD(native_utility_child_arm9_data_0202cca0, s32 *, 4) = 0;
        native_utility_child_arm9_thumb_0200f8d4();
        do {

        } while (native_utility_child_arm9_thumb_0200fa48(8U, 1U) == 0);
        native_utility_child_arm9_thumb_0200fa74(8U, (u32) native_utility_child_arm9_thumb_02010935);
        var_r2 = 0;
        var_r1 = native_utility_child_arm9_data_0202ccc8;
        do {
            *var_r1 = 0;
            var_r1 += 4;
            var_r2 += 1;
        } while (var_r2 < 5);
        native_utility_child_arm9_thumb_02009e30((u32) native_utility_child_arm9_data_0202ccb0);
        *native_utility_child_arm9_data_0202cc98 = *native_utility_child_arm9_data_027ffc3c;
    }
}
