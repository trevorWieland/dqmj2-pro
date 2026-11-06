typedef unsigned long u32;
    typedef unsigned long long int u64;

    typedef u32 OSIntrMode;
    extern OSIntrMode native_fn_02007ff4(void);
    extern OSIntrMode native_fn_02008008(OSIntrMode state);
    extern void native_fn_02008430(void);
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
void native_main_02007da4(OSAlarm * alarm, OSTick tick, OSAlarmHandler handler, void * arg);
extern void native_fn_02007c78(OSAlarm * alarm, OSTick fire);
void native_fn_02007c78 (OSAlarm * alarm, OSTick fire);
void native_main_02007da4 (OSAlarm * alarm, OSTick tick, OSAlarmHandler handler, void * arg)
{
    OSIntrMode enabled;
    ((void) 0) ;
    ((void) 0) ;
    if (!alarm || alarm->handler) {
        native_fn_02008430() ;
    }
    enabled = native_fn_02007ff4();
    alarm->period = 0;
    alarm->handler = handler;
    alarm->arg = arg;
    native_fn_02007c78(alarm, native_fn_02007a9c() + tick);
    (void)native_fn_02008008(enabled);
}
