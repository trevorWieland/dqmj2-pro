typedef unsigned char u8;
typedef unsigned short int u16;
    void native_main_02009ca4(int alarmNo);
    typedef struct AlarmCallbackInfo {
        void (*func)(void *);
        void * arg;
        u8 id;
        u8 pad;
        u16 pad2;
    } AlarmCallbackInfo;
    extern AlarmCallbackInfo native_data_main_020e5260[8 ];
    void native_main_02009ca4 (int msg)
    {
        AlarmCallbackInfo * info;
        int alarmNo = msg & 0xff;
        int id = (msg >> 8) & 0xff;
        ((void) 0) ;
        info = &native_data_main_020e5260[alarmNo];
        if (id == info->id) {
            if (info->func != ((void *)0) ) {
                info->func(info->arg);
            }
        }
    }
