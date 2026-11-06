typedef unsigned char u8;
typedef unsigned short int u16;
typedef unsigned long u32;
typedef unsigned long long int u64;
typedef signed long s32;
typedef int BOOL;
typedef u32 OSIntrMode;
extern OSIntrMode native_fn_02007ff4(void);
extern OSIntrMode native_fn_02008008(OSIntrMode state);
typedef struct CPContext {
	u64 div_numer;
	u64 div_denom;
	u64 sqrt;
	u16 div_mode;
	u16 sqrt_mode;
} CPContext;
typedef struct OSContext {
	u32 cpsr;
	u32 r[13];
	u32 sp;
	u32 lr;
	u32 pc_plus4;
	u32 sp_svc;
	CPContext cp_context;
} OSContext;
typedef struct _OSThread OSThread;
typedef struct _OSThreadQueue OSThreadQueue;
typedef struct _OSThreadLink OSThreadLink;
typedef struct _OSMutexQueue OSMutexQueue;
typedef struct _OSMutexLink OSMutexLink;
typedef struct OSMutex OSMutex;
typedef struct OSiAlarm OSAlarm;
struct _OSThreadQueue {
        OSThread * head;
        OSThread * tail;
    };
struct _OSThreadLink {
        OSThread * prev;
        OSThread * next;
    };
struct _OSMutexQueue {
        OSMutex * head;
        OSMutex * tail;
    };
struct _OSMutexLink {
        OSMutex * next;
        OSMutex * prev;
    };
typedef enum {
    OS_THREAD_STATE_WAITING       = 0,
    OS_THREAD_STATE_READY         = 1,
    OS_THREAD_STATE_TERMINATED    = 2
} OSThreadState;
typedef void (*OSThreadDestructor) (void *);
struct _OSThread {
    OSContext context;
    OSThreadState state;
    OSThread * next;
    u32 id;
    u32 priority;
    void * profiler;
    OSThreadQueue * queue;
    OSThreadLink link;
    OSMutex * mutex;
    OSMutexQueue mutexQueue;
    u32 stackTop;
    u32 stackBottom;
    u32 stackWarningOffset;
    OSThreadQueue joinQueue;
    void * specific[3 ];
    OSAlarm * alarmForSleep;
    OSThreadDestructor destructor;
    void * userParameter;
    int systemErrno;
};
typedef struct OSThreadInfo {
    u16 isNeedRescheduling;
    u16 irqDepth;
    OSThread * current;
    OSThread * list;
    void * switchCallback;
} OSThreadInfo;
void native_fn_020068d4(OSThreadQueue * queue);
extern OSThreadInfo native_data_main_020e33e4;
struct OSMutex {
	OSThreadQueue queue;
	OSThread * thread;
	s32 count;
	OSMutexLink link;
};
typedef u64 OSTick;
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
typedef void (*MIDmaCallback) (void *);
void native_fn_0200877c(u32 dmaNo);
typedef enum {
	CARD_RESULT_SUCCESS = 0,
	CARD_RESULT_FAILURE,
	CARD_RESULT_INVALID_PARAM,
	CARD_RESULT_UNSUPPORTED,
	CARD_RESULT_TIMEOUT,
	CARD_RESULT_ERROR,
	CARD_RESULT_NO_RESPONSE,
	CARD_RESULT_CANCELED
} CARDResult;
typedef enum {
	CARD_BACKUP_TYPE_EEPROM_4KBITS = (((1) << 0) | (( 9) << 8) | (( 0) << 16)) ,
	CARD_BACKUP_TYPE_EEPROM_64KBITS = (((1) << 0) | (( 13) << 8) | (( 0) << 16)) ,
	CARD_BACKUP_TYPE_EEPROM_512KBITS = (((1) << 0) | (( 16) << 8) | (( 0) << 16)) ,
	CARD_BACKUP_TYPE_FLASH_2MBITS = (((2) << 0) | (( 18) << 8) | (( 0) << 16)) ,
	CARD_BACKUP_TYPE_FLASH_4MBITS = (((2) << 0) | (( 19) << 8) | (( 0) << 16)) ,
	CARD_BACKUP_TYPE_FLASH_8MBITS = (((2) << 0) | (( 20) << 8) | (( 0) << 16)) ,
	CARD_BACKUP_TYPE_FLASH_16MBITS = (((2) << 0) | (( 21) << 8) | (( 0) << 16)) ,
	CARD_BACKUP_TYPE_FLASH_64MBITS = (((2) << 0) | (( 23) << 8) | (( 0) << 16)) ,
	CARD_BACKUP_TYPE_FRAM_256KBITS = (((3) << 0) | (( 15) << 8) | (( 0) << 16)) ,
	CARD_BACKUP_TYPE_NOT_USE = 0
} CARDBackupType;
typedef enum {
	CARD_REQ_INIT = 0,
	CARD_REQ_ACK,
	CARD_REQ_IDENTIFY,
	CARD_REQ_READ_ID,
	CARD_REQ_READ_ROM,
	CARD_REQ_WRITE_ROM,
	CARD_REQ_READ_BACKUP,
	CARD_REQ_WRITE_BACKUP,
	CARD_REQ_PROGRAM_BACKUP,
	CARD_REQ_VERIFY_BACKUP,
	CARD_REQ_ERASE_PAGE_BACKUP,
	CARD_REQ_ERASE_SECTOR_BACKUP,
	CARD_REQ_ERASE_CHIP_BACKUP,
	CARD_REQ_READ_STATUS,
	CARD_REQ_WRITE_STATUS,
	CARD_REQ_ERASE_SUBSECTOR_BACKUP,
	CARD_REQ_MAX
} CARDRequest;
typedef enum {
	CARD_REQUEST_MODE_RECV,
	CARD_REQUEST_MODE_SEND,
	CARD_REQUEST_MODE_SEND_VERIFY,
	CARD_REQUEST_MODE_SPECIAL
} CARDRequestMode;
void native_fn_02010204(void);
void native_main_0201109c(u32 dma,
                   const void * src, void * dst, u32 len,
                   MIDmaCallback callback, void * arg, BOOL is_async);
void native_fn_020111f8(void);
extern const u16 (*ctrdgi_fl_maxtime);
enum {
	CARD_STAT_INIT        = (1 << 0),
	CARD_STAT_INIT_CMD    = (1 << 1),
	CARD_STAT_BUSY        = (1 << 2),
	CARD_STAT_TASK        = (1 << 3),
	CARD_STAT_RECV        = (1 << 4),
	CARD_STAT_REQ         = (1 << 5),
	CARD_STAT_CANCEL      = (1 << 6)
};
typedef enum {
	CARD_TARGET_NONE,
	CARD_TARGET_ROM,
	CARD_TARGET_BACKUP
} CARDTargetMode;
typedef s32 CARDiOwner;
typedef struct CARDiCommandArg {
	CARDResult result;
	CARDBackupType type;
	u32 id;
	u32 src;
	u32 dst;
	u32 len;
	struct {
		u32 total_size;
		u32 sect_size;
		u32 subsect_size;
		u32 page_size;
		u32 addr_width;
		u32 program_page;
		u32 write_page;
		u32 write_page_total;
		u32 erase_chip;
		u32 erase_chip_total;
		u32 erase_sector;
		u32 erase_sector_total;
		u32 erase_subsector;
		u32 erase_subsector_total;
		u32 erase_page;
		u8 initial_status;
		u8 padding1[3];
		u32 caps;
		u8 padding2[4];
	} spec;
} CARDiCommandArg;
typedef struct CARDiCommon {
	CARDiCommandArg * cmd;
	int command;
	volatile CARDiOwner lock_owner;
	volatile int lock_ref;
	OSThreadQueue lock_queue[1];
	CARDTargetMode lock_target;
	u32 src;
	u32 dst;
	u32 len;
	u32 dma;
	CARDRequest req_type;
	int req_retry;
	CARDRequestMode req_mode;
	MIDmaCallback callback;
	void * callback_arg;
	void (*task_func) (struct CARDiCommon *);
	OSThread thread[1];
	OSThread * cur_th;
	u32 priority;
	OSThreadQueue busy_q[1];
	volatile u32 flag;
	u32 flush_threshold_ic;
	u32 flush_threshold_dc;
__attribute__ ((aligned(32))) u8 backup_cache_page_buf[256];
} CARDiCommon;
extern CARDiCommon native_data_main_020e5500;
void native_fn_0200ff98(void (*task)(CARDiCommon *));
typedef struct CARDRomStat {
	void (*read_func) (struct CARDRomStat *);
	u32 ctrl;
	u8 * cache_page;
	u32 dummy[5];
	u8 cache_buf[512 ];
} CARDRomStat;
BOOL native_fn_02010d2c(CARDRomStat * p);
typedef struct {
u32 field_0000;
unsigned char padding_0004[28];
__attribute__ ((aligned(32))) CARDRomStat field_0020;
} NativeStorage_020e5b20;
extern NativeStorage_020e5b20 native_data_main_020e5b20;
BOOL native_fn_02010d2c (CARDRomStat *p);
void native_fn_02011004 (CARDiCommon *c);
void native_fn_020111f8 (void);
static inline OSThreadInfo * OS_GetThreadInfo (void)
{
    return &native_data_main_020e33e4;
}
static inline OSThread * OS_GetCurrentThread (void)
{
    return OS_GetThreadInfo()->current;
}
static inline void CARDi_WaitTask (CARDiCommon * p, MIDmaCallback callback, void * callback_arg)
{
	OSIntrMode bak_psr = native_fn_02007ff4();
	while ((p->flag & CARD_STAT_BUSY) != 0) {
		native_fn_020068d4(p->busy_q);
	}
	p->flag |= CARD_STAT_BUSY;
	p->callback = callback;
	p->callback_arg = callback_arg;
	(void)native_fn_02008008(bak_psr);
}
