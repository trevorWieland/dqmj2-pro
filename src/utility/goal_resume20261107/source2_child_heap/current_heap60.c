typedef unsigned int u32;
typedef signed int s32;

typedef struct HeapSelection {
    s32 currentHeap;
} HeapSelection;

extern HeapSelection *native_utility_child_arm7_data_03805b30[];
extern u32 native_utility_child_arm7_arm_037fe41c(void);
extern u32 native_utility_child_arm7_arm_037fe430(u32 irqMask);

s32 native_utility_child_arm7_wram_037fd448(u32 arenaSlot, s32 replacementHeap)
{
    u32 irqMask;
    s32 previousHeap;

    irqMask = native_utility_child_arm7_arm_037fe41c();
    previousHeap = native_utility_child_arm7_data_03805b30[arenaSlot]->currentHeap;
    native_utility_child_arm7_data_03805b30[arenaSlot]->currentHeap = replacementHeap;
    native_utility_child_arm7_arm_037fe430(irqMask);
    return previousHeap;
}
