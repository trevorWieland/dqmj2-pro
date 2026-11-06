typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define CHILD_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_thumb_02009478(void);
extern u32 native_utility_child_arm9_thumb_02009d60(u32);
extern u32 native_utility_child_arm9_thumb_020099c8(u32, u32);
extern u32 native_utility_child_arm9_thumb_02009948(u32);
extern u32 native_utility_child_arm9_thumb_020095a0(u32);
extern u32 native_utility_child_arm9_thumb_02009450(void);
extern u32 native_utility_child_arm9_thumb_0200954c(void);
extern u32 native_utility_child_arm9_thumb_0200a888(void);
#define native_utility_child_arm9_data_020292f8 ((volatile u32 *)0x20292f8)
u32 native_utility_child_arm9_main_0200962c(void) {
    u32 temp_r4;
    u32 temp_r0;

    temp_r4 = *(u32 *)(*native_utility_child_arm9_data_020292f8);
    native_utility_child_arm9_thumb_02009478();
    native_utility_child_arm9_thumb_02009d60(temp_r4);
    temp_r0 = CHILD_FIELD(temp_r4, u32 *, 0x78);
    if (temp_r0 != 0) {
        native_utility_child_arm9_thumb_020099c8(temp_r0, temp_r4);
    }
    native_utility_child_arm9_thumb_02009948(temp_r4);
    CHILD_FIELD(temp_r4, s32 *, 0x64) = 2;
    native_utility_child_arm9_thumb_020095a0(temp_r4 + 0x9C);
    native_utility_child_arm9_thumb_02009450();
    native_utility_child_arm9_thumb_0200954c();
    return native_utility_child_arm9_thumb_0200a888();
}
