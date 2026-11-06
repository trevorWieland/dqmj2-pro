typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_thumb_0200cce0(void);
extern u32 native_utility_child_arm9_thumb_0200f8d4(void);
extern u32 native_utility_child_arm9_thumb_0200fa48(u32, u32);
extern u32 native_utility_child_arm9_thumb_0200fa74(u32, u32);
extern u32 native_utility_child_arm9_thumb_0200cd98(void);
extern u32 native_utility_child_arm9_thumb_0200d034(u32);
extern u32 native_utility_child_arm9_thumb_0200cab0(u32);
extern u32 native_utility_child_arm9_thumb_0200cd71(u32, u32);
extern u32 native_utility_child_arm9_thumb_0200cd29(u32, u32, u32, u32);
extern u32 native_utility_child_arm9_data_0202b21c[];
extern u32 native_utility_child_arm9_data_0202b220[];
extern u32 native_utility_child_arm9_data_0202b224[];
extern u8 native_utility_child_arm9_data_0202b300[];
extern u8 native_utility_child_arm9_data_0200cd09[];
u32 native_utility_child_arm9_main_0200cf04(void) {
    u32 *var_r0;

    var_r0 = native_utility_child_arm9_data_0202b21c;
    if (*native_utility_child_arm9_data_0202b21c == 0) {
        *native_utility_child_arm9_data_0202b21c = 1;
        native_utility_child_arm9_thumb_0200cce0();
        *native_utility_child_arm9_data_0202b220 = 0;
        native_utility_child_arm9_thumb_0200f8d4();
        do {

        } while (native_utility_child_arm9_thumb_0200fa48(0xDU, 1U) == 0);
        native_utility_child_arm9_thumb_0200fa74(0xDU, (u32) native_utility_child_arm9_thumb_0200cd71);
        native_utility_child_arm9_thumb_0200cd98();
        native_utility_child_arm9_thumb_0200fa74(0xDU, 0U);
        native_utility_child_arm9_thumb_0200fa74(0xDU, (u32) native_utility_child_arm9_thumb_0200cd29);
        *native_utility_child_arm9_data_0202b224 = 0;
        native_utility_child_arm9_thumb_0200d034((u32) native_utility_child_arm9_data_0202b300);
        native_utility_child_arm9_thumb_0200fa74(0x11U, (u32) native_utility_child_arm9_data_0200cd09);
        var_r0 = (u32 *) native_utility_child_arm9_thumb_0200cab0(0U);
    }
    return (u32) var_r0;
}
