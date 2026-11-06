typedef unsigned int u32;
typedef struct Node { struct Node *next; } Node;
extern Node *native_utility_child_arm9_data_02029650;
extern u32 native_utility_child_arm9_arm_0200a64c(void);
extern u32 native_utility_child_arm9_arm_0200a660(u32);
u32 native_utility_child_arm9_main_0200b204(void) {
u32 state = native_utility_child_arm9_arm_0200a64c();
u32 count = 0;
Node *node = native_utility_child_arm9_data_02029650;
while (node) { ++count; node = node->next; }
(void)native_utility_child_arm9_arm_0200a660(state);
return count;
}
