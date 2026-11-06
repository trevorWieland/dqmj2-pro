typedef unsigned short int u16;
typedef unsigned long u32;
typedef unsigned long long int u64;
typedef volatile u64 vu64;
typedef u16 REGType16;
typedef int BOOL;
extern void native_data_main_02005cac(u32 timerNo, void (*callback)(void *), void * arg);
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
typedef struct {
u16 field_0000;
unsigned char padding_0002[2];
BOOL field_0004;
vu64 field_0008;
} NativeStorage_020e36f4;
extern NativeStorage_020e36f4 native_data_main_020e36f4;
void native_main_02007a34(void);
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
