typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_thumb_03804d08(void);
extern u32 native_utility_child_arm7_thumb_03804d14(void);
extern u32 native_utility_child_arm7_thumb_037fecc8(u32);
extern u32 native_utility_child_arm7_thumb_03804848(void);
extern u32 native_utility_child_arm7_thumb_03804870(void);
extern u32 native_utility_child_arm7_thumb_037fe94c(void);
extern u32 native_utility_child_arm7_thumb_037feae0(u32, u32);
extern u32 native_utility_child_arm7_thumb_03804bec(void);
extern u32 native_utility_child_arm7_thumb_03804bc5(u32, u32);
extern u32 native_utility_child_arm7_thumb_03804ba9(u32, u32);
extern u32 native_utility_child_arm7_thumb_0380487d(u32, u32);
extern u8 native_utility_child_arm7_data_0380919c[];
extern u32 native_utility_child_arm7_data_03809180[];
extern u16 native_utility_child_arm7_data_0380916c[];
extern u8 native_utility_child_arm7_data_03804b9d[];
u32 native_utility_child_arm7_wram_03804c8c(void) {
    u32 *var_r0;

    native_utility_child_arm7_thumb_03804d08();
    native_utility_child_arm7_thumb_03804d14();
    native_utility_child_arm7_thumb_037fecc8((u32) native_utility_child_arm7_data_0380919c);
    var_r0 = native_utility_child_arm7_data_03809180;
    if (*native_utility_child_arm7_data_03809180 == 0) {
        *native_utility_child_arm7_data_03809180 = 1;
        native_utility_child_arm7_thumb_03804848();
        var_r0 = (u32 *) native_utility_child_arm7_thumb_03804870();
        if (var_r0 != (u32 *)-3) {
            *native_utility_child_arm7_data_0380916c = (u16) var_r0;
            native_utility_child_arm7_thumb_037fe94c();
            native_utility_child_arm7_thumb_037feae0(0xDU, (u32) native_utility_child_arm7_thumb_03804bc5);
            native_utility_child_arm7_thumb_03804bec();
            native_utility_child_arm7_thumb_037feae0(0xDU, (u32) native_utility_child_arm7_thumb_03804ba9);
            native_utility_child_arm7_thumb_037feae0(0x10U, (u32) native_utility_child_arm7_data_03804b9d);
            var_r0 = (u32 *) native_utility_child_arm7_thumb_037feae0(0x11U, (u32) native_utility_child_arm7_thumb_0380487d);
        }
    }
    return (u32) var_r0;
}
