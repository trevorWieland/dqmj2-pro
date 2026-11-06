typedef unsigned short int u16;
typedef unsigned long u32;
typedef unsigned long long int u64;
typedef volatile u16 vu16;
typedef volatile u32 vu32;
typedef volatile u64 vu64;
typedef u16 REGType16;
typedef vu32 REGType32v;
typedef int BOOL;
typedef u32 OSIntrMode;
extern OSIntrMode native_fn_02007ff4(void);
extern OSIntrMode native_fn_02008008(OSIntrMode state);
typedef enum {
	OS_TIMER_0 = 0,
	OS_TIMER_1 = 1,
	OS_TIMER_2 = 2,
	OS_TIMER_3 = 3
} OSTimer;
typedef u64 OSTick;
OSTick native_main_02007a9c(void);
typedef struct {
u16 field_0000;
unsigned char padding_0002[2];
BOOL field_0004;
vu64 field_0008;
} NativeStorage_020e36f4;
extern NativeStorage_020e36f4 native_data_main_020e36f4;
