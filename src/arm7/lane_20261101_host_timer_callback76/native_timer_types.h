typedef unsigned int u32;
typedef void (*TimerCallback)(void *);
typedef struct { TimerCallback function; u32 enabled; void *argument; } CallbackRecord;
typedef char CallbackRecord_Size12[(sizeof(CallbackRecord)==12)?1:-1];
extern CallbackRecord native_host_arm7_timer_callbacks_038076b0[];
extern u32 native_host_arm7_arm_037fb8f0(u32);
