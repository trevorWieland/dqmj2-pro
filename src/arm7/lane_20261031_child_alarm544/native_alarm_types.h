typedef unsigned int u32;
typedef unsigned long long u64;
#define NULL ((void *)0)
typedef struct OSAlarm OSAlarm;
typedef void (*OSAlarmHandler)(void *);
struct OSAlarm {
    OSAlarmHandler handler;
    void *argument;
    u32 tag;
    u64 fire;
    OSAlarm *previous;
    OSAlarm *next;
    u64 period;
    u64 start;
};
typedef char OSAlarm_Size44[(sizeof(OSAlarm) == 44) ? 1 : -1];
typedef struct { OSAlarm *head; OSAlarm *tail; } AlarmQueue;
extern AlarmQueue native_utility_child_arm7_alarm_queue_03805b6c;
extern void native_utility_child_arm7_arm_037fe5e0(void);
extern u32 native_utility_child_arm7_arm_037fe41c(void);
extern u32 native_utility_child_arm7_arm_037fe430(u32);
extern u64 native_utility_child_arm7_arm_037fd724(void);
extern void native_utility_child_arm7_arm_037fdd30(OSAlarm *);
extern void native_utility_child_arm7_arm_037fdb90(OSAlarm *, u64);
