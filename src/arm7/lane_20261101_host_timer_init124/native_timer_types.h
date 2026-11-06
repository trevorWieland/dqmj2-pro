typedef unsigned short u16;
typedef unsigned int u32;
typedef unsigned long long u64;
typedef void (*TimerCallback)(void *);
typedef struct { u16 initialized; u16 pad; u32 reset; u64 counter; } TickState;
typedef char tick_state_view_must_be_16[sizeof(TickState) == 16 ? 1 : -1];
extern TickState native_host_arm7_timer_state_03807898;
extern void native_host_arm7_arm_037fb858(u32, TimerCallback, void *);
#define NATIVE_TIMER_CONTROL (*(volatile u16 *)0x04000102)
#define NATIVE_TIMER_COUNTER (*(volatile u16 *)0x04000100)
typedef signed int s32;
extern void native_host_arm7_arm_037fd10c(s32);
extern void native_host_arm7_arm_037fd1b4(void *);
extern void native_host_arm7_arm_037fb7bc(u32,TimerCallback);
extern u32 native_host_arm7_arm_037fb8f0(u32);
