typedef unsigned short int u16;
typedef unsigned long u32;
typedef unsigned long long int u64;
typedef signed long long int s64;
typedef u16 REGType16;
typedef u32 OSIrqMask;
typedef struct OSiAlarm OSAlarm;
void native_fn_02005cac(u32 timerNo, void (*callback)(void *), void * arg);
OSIrqMask native_fn_02005d20(OSIrqMask intr);
typedef enum {
	OS_TIMER_PRESCALER_1       = (0UL << 0 ),
	OS_TIMER_PRESCALER_64      = (1UL << 0 ),
	OS_TIMER_PRESCALER_256     = (2UL << 0 ),
	OS_TIMER_PRESCALER_1024    = (3UL << 0 )
} OSTimerPrescaler;
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
void native_main_02007b4c(OSAlarm * alarm);
void native_fn_02007e98(void * arg);
void native_fn_02007e98 (void * arg);
static inline void OS_SetTimerCount (OSTimer id, u16 count)
{
	((void) 0) ;
	*((REGType16 *)((u32)(0x04000000 + 0x100) + id * 4)) = count;
}
static inline void OS_SetTimerControl (OSTimer id, u16 control)
{
	((void) 0) ;
	*((REGType16 *)((u32)(0x04000000 + 0x102) + id * 4)) = control;
}
