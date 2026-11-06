typedef unsigned char u8;
typedef unsigned int u32;
typedef unsigned long long u64;
typedef int BOOL;
#define TRUE 1
#define FALSE 0
#define NULL ((void *)0)
typedef struct OSAlarm { u8 opaque[44]; } OSAlarm;
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
