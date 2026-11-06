typedef unsigned char u8;
typedef unsigned short int u16;
typedef void (*SNDAlarmHandler) (void *);
    u8 native_main_02009c74(int alarmNo, SNDAlarmHandler handler, void * arg);
    typedef struct AlarmCallbackInfo {
        void (*func)(void *);
        void * arg;
        u8 id;
        u8 pad;
        u16 pad2;
    } AlarmCallbackInfo;
    extern AlarmCallbackInfo native_data_main_020e5260[8 ];
    u8 native_main_02009c74 (int alarmNo, SNDAlarmHandler handler, void * arg)
    {
        AlarmCallbackInfo * info;
        ((void) 0) ;
        info = &native_data_main_020e5260[alarmNo];
        info->func = handler;
        info->arg = arg;
        info->id++;
        return info->id;
    }
