typedef unsigned short int u16;

typedef unsigned long u32;

typedef volatile u16 vu16;

typedef vu16 REGType16v;

typedef enum {
    MIC_STATUS_READY = 0,
    MIC_STATUS_AUTO_START,
    MIC_STATUS_AUTO_SAMPLING,
    MIC_STATUS_AUTO_END,
    MIC_STATUS_END_WAIT,
} MICStatus;

typedef struct MICWork {
    u16 command[16 ];
    MICStatus status;
    u16 type;
    u16 admode;
    void *buf;
    u32 index;
    u32 size;
    u16 timerValue;
    u16 timerPrescaler;
    u16 temp16;
    u16 temporary;
} MICWork;

void native_host_arm7_wram_038053d0(void);

extern const u16 (*ctrdgi_fl_maxtime);

extern MICWork native_host_arm7_data_0380b258;

extern u16 native_host_arm7_mic_words_0380b258[16];
