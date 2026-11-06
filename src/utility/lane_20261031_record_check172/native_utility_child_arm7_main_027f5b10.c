typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
extern u32 native_utility_child_arm7_pointer_word_0380fff4;
extern u32 native_utility_child_arm7_arm_027e94c8(u32);
extern u32 native_utility_child_arm7_arm_027e93d4(u32,u32);
u32 native_utility_child_arm7_main_027f5b10(u32 *output) {
    u8 *record = *(u8 **)((u8 *)native_utility_child_arm7_pointer_word_0380fff4 + 0x318);
    u32 value;
    u8 *cursor;
    u32 remaining = *(u16 *)(record + 2);
    u32 stored;
    if (remaining < 0xA4 || remaining > 0x1D6) return 2;
    cursor = record + 2;
    value = 0;
    while (remaining != 0) {
        u32 byte = native_utility_child_arm7_arm_027e94c8((u32)cursor);
        ++cursor;
        value = native_utility_child_arm7_arm_027e93d4((u8)byte, (u16)value);
        --remaining;
    }
    record = *(u8 **)((u8 *)native_utility_child_arm7_pointer_word_0380fff4 + 0x318);
    stored = *(u16 *)record;
    if (output != 0) *output = stored | (value << 16);
    return value != stored;
}
