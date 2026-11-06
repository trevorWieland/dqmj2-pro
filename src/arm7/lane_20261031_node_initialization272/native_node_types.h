typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
typedef struct NativeNode {
    u32 previous;
    u32 next;
    u16 count;
    u16 id;
} NativeNode;
extern void native_host_arm7_arm_027e8c5c(u32, u32);
extern void native_utility_child_arm7_arm_027e8fc8(u32, u32);
