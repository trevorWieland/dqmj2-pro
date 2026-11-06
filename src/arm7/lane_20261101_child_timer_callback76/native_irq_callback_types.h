typedef unsigned int u32;
typedef void (*TimerCallback)(void *);
typedef struct CallbackRecord {
    TimerCallback function;
    u32 enabled;
    void *argument;
} CallbackRecord;
typedef char CallbackRecord_Size12[(sizeof(CallbackRecord) == 12) ? 1 : -1];
extern CallbackRecord native_utility_child_arm7_timer_callbacks_0380597c[];
extern u32 native_utility_child_arm7_arm_037fbc8c(u32);
