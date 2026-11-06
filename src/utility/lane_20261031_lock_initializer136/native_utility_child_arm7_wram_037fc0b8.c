#include "native_lock_types.h"
extern volatile u32 native_utility_child_arm7_bitmap_word_027fffb8;
extern volatile u32 native_utility_child_arm7_bitmap_word_027fffbc;
extern u32 native_utility_child_arm7_data_038059b8;
extern volatile RawLockWord native_utility_child_arm7_data_027ffff0;
extern void native_utility_child_arm7_arm_037fc0ac(u32);
void native_utility_child_arm7_wram_037fc0b8(void)
{
    volatile RawLockWord *lock;
    if (native_utility_child_arm7_data_038059b8) return;
    native_utility_child_arm7_data_038059b8 = 1;
    native_utility_child_arm7_data_027ffff0.extension = 0;
    lock = &native_utility_child_arm7_data_027ffff0;
    while (lock->owner != 0x7f) native_utility_child_arm7_arm_037fc0ac(0x400U);
    native_utility_child_arm7_bitmap_word_027fffb8 = 0xffffffffU;
    native_utility_child_arm7_bitmap_word_027fffbc = 0xffff0000U;
    lock->extension = 0xbf;
}
