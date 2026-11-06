typedef unsigned short u16;
typedef unsigned int u32;
typedef unsigned long long u64;
typedef void (*TimerCallback)(void *);
extern volatile u64 native_utility_child_arm7_tick_counter_03805b60;
extern u32 native_utility_child_arm7_tick_reset_03805b5c;
#define native_utility_child_arm7_timer_counter_04000100 (*(volatile u16 *)0x04000100)
#define native_utility_child_arm7_timer_control_04000102 (*(volatile u16 *)0x04000102)
extern void native_utility_child_arm7_arm_037fbcf8(u32, TimerCallback, void *);
extern void native_utility_child_arm7_arm_037fd7d4(void *);
