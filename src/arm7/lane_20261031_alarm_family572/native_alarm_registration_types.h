typedef unsigned char u8;
typedef unsigned int u32;
typedef unsigned long long u64;
typedef int BOOL;
#define TRUE 1
#define FALSE 0
#define NULL ((void *)0)
typedef unsigned short u16;
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
typedef struct { u16 initialized; u16 pad; OSAlarm *head; OSAlarm *tail; } AlarmQueue;
extern AlarmQueue native_host_arm7_alarm_queue_038078a8;
extern void native_host_arm7_arm_037fd2c0(OSAlarm *);
extern void native_host_arm7_arm_037fd3b0(OSAlarm *, u64);
extern void native_host_arm7_arm_037fde70(void);
extern u32 native_host_arm7_arm_037fdd00(void);
extern u32 native_host_arm7_arm_037fdd14(u32);
extern u32 native_host_arm7_data_03807950;
extern OSAlarm native_host_arm7_data_03807954;
extern BOOL native_host_arm7_arm_037fd1a4(void);
extern BOOL native_host_arm7_arm_037fd390(void);
extern void native_host_arm7_arm_037fd3a0(OSAlarm *);
extern u64 native_host_arm7_arm_037fd21c(void);
extern void native_host_arm7_arm_037fd54c(OSAlarm *,u64,u64,void (*)(void *),void *);
extern void native_host_arm7_arm_037fe65c(void *);
#define enabled native_host_arm7_data_03807950
#define alarm native_host_arm7_data_03807954
#define OS_IsTickAvailable native_host_arm7_arm_037fd1a4
#define OS_IsAlarmAvailable native_host_arm7_arm_037fd390
#define OS_CreateAlarm native_host_arm7_arm_037fd3a0
#define OS_GetTick native_host_arm7_arm_037fd21c
#define OS_SetPeriodicAlarm native_host_arm7_arm_037fd54c
#define Callback native_host_arm7_arm_037fe65c
