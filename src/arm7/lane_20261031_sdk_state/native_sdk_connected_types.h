typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef int BOOL;
typedef u64 OSTick;
#define NULL ((void *)0)
#define SND_ALARM_COUNT 8
#define SND_CHANNEL_COUNT 16
struct OSAlarm { u8 opaque[44]; };
struct SNDAlarm { u8 enable,id; u16 padding; OSTick tick,period; struct OSAlarm alarm; };
struct SNDWork { u8 prefix[0xf80]; struct SNDAlarm alarms[8]; };
struct NativePlayer { u8 flags,opaque[3]; u32 storage[8]; };
struct SharedWork { u32 finishedCommandTag,playerStatus; u16 channelStatus,captureStatus; };
typedef char AlarmSize[(sizeof(struct SNDAlarm)==64)?1:-1];
typedef char WorkSize[(sizeof(struct SNDWork)==0x1180)?1:-1];
typedef char PlayerSize[(sizeof(struct NativePlayer)==36)?1:-1];
extern struct SNDWork native_host_arm7_data_03807ee0;
extern struct NativePlayer native_host_arm7_data_03808420[16];
extern struct SharedWork *native_host_arm7_data_03807edc;
extern void native_host_arm7_arm_038000b4(int,const void *,u32,void *);
extern void native_host_arm7_arm_037fd5c0(void *);
extern void native_host_arm7_arm_037fd3a0(void *);
extern void native_host_arm7_arm_037fd4dc(void *,u64,void (*)(void *),void *);
extern void native_host_arm7_arm_037fd54c(void *,u64,u64,void (*)(void *),void *);
extern u64 native_host_arm7_arm_037fd21c(void);
extern void native_host_arm7_arm_03801ea8(void *);
extern BOOL native_host_arm7_arm_037feb50(int);
extern BOOL native_host_arm7_arm_037ff14c(int);
#define SNDi_Work native_host_arm7_data_03807ee0
#define SNDi_SharedWork native_host_arm7_data_03807edc
#define OS_CancelAlarm native_host_arm7_arm_037fd5c0
#define OS_CreateAlarm native_host_arm7_arm_037fd3a0
#define OS_SetAlarm native_host_arm7_arm_037fd4dc
#define OS_SetPeriodicAlarm native_host_arm7_arm_037fd54c
#define OS_GetTick native_host_arm7_arm_037fd21c
#define AlarmHandler native_host_arm7_arm_03801ea8
#define SND_IsChannelActive native_host_arm7_arm_037feb50
#define SND_IsCaptureActive native_host_arm7_arm_037ff14c
