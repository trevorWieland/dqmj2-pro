typedef unsigned short int u16;
typedef unsigned long u32;
typedef unsigned long long int u64;
typedef signed long long int s64;
typedef struct OSiAlarm OSAlarm;
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
void native_main_02007c78(OSAlarm * alarm, OSTick fire);
void native_fn_02007b4c (OSAlarm * alarm);
