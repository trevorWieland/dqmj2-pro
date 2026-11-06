typedef unsigned short int u16;
typedef unsigned long u32;
typedef unsigned long long int u64;
typedef volatile u32 vu32;
typedef u16 REGType16;
typedef u32 OSIrqMask;
extern u32 native_data_main_027e0000[];
typedef struct OSiAlarm OSAlarm;
OSIrqMask native_fn_02005d50(OSIrqMask intr);
typedef enum {
	OS_TIMER_0 = 0,
	OS_TIMER_1 = 1,
	OS_TIMER_2 = 2,
	OS_TIMER_3 = 3
} OSTimer;
typedef u64 OSTick;
OSTick native_fn_02007a9c(void);
typedef void (*OSAlarmHandler) (void *);
struct OSiAlarm {
	OSAlarmHandler handler;
	void * arg;
	u32 tag;
	OSTick fire;
	OSAlarm * prev;
	OSAlarm * next;
	OSTick period;
	OSTick start;
};
struct OSiAlarmQueue {
	OSAlarm * head;
	OSAlarm * tail;
};
typedef struct {
u16 field_0000;
unsigned char padding_0002[2];
struct OSiAlarmQueue field_0004;
} NativeStorage_020e3704;
extern NativeStorage_020e3704 native_data_main_020e3704;
void native_fn_02007b4c(OSAlarm * alarm);
void native_fn_02007c78(OSAlarm * alarm, OSTick fire);
void native_main_02007ea8(void);
void native_fn_02007b4c (OSAlarm * alarm);
void native_fn_02007c78 (OSAlarm * alarm, OSTick fire);
static inline void OS_SetIrqCheckFlag (OSIrqMask intr)
{
	*(vu32 *)((((u32)native_data_main_027e0000) + 0x00003fc0) + 0x38) |= (u32)intr;
}
static inline void OS_SetTimerControl (OSTimer id, u16 control)
{
	((void) 0) ;
	*((REGType16 *)((u32)(0x04000000 + 0x102) + id * 4)) = control;
}
