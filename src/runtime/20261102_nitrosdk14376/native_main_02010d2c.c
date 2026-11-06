typedef unsigned char u8;
typedef unsigned short int u16;
typedef unsigned long u32;
    typedef unsigned long long int u64;
typedef signed long s32;
typedef volatile u32 vu32;
        typedef int BOOL;
    typedef u32 OSIntrMode;
    extern OSIntrMode native_fn_02007ff4(void);
    extern OSIntrMode native_fn_02008008(OSIntrMode state);
        typedef u32 OSIrqMask;
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
typedef void (*OSIrqFunction) (void);
OSIrqMask native_fn_02005d20(OSIrqMask intr);
OSIrqMask native_fn_02005d80(OSIrqMask intr);
void native_fn_02005b50(OSIrqMask intrBit, OSIrqFunction function);
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
static inline u32 OS_GetITCMAddress (void)
{
	return (u32)0x01ff8000 ;
}
u32 native_fn_02007714(void);
void native_fn_0200729c(void);
void native_fn_020072d0(void * startAddr, u32 nBytes);
void native_fn_020072ec(const void * startAddr, u32 nBytes);
void native_fn_0200732c(void);
void native_fn_02007338(void);
void native_fn_02007344(void * startAddr, u32 nBytes);
typedef void (*MIDmaCallback) (void *);
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
extern const u16 (*ctrdgi_fl_maxtime);
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
	u8 backup_cache_page_buf[256] __attribute__ ((aligned(32))) ;
} CARDiCommon;
extern CARDiCommon native_data_main_020e5500;
typedef struct CARDRomStat {
	void (*read_func) (struct CARDRomStat *);
	u32 ctrl;
	u8 * cache_page;
	u32 dummy[5];
	u8 cache_buf[512 ];
} CARDRomStat;
extern CARDRomStat rom_stat;
extern u32 native_data_main_020dce80;
static inline BOOL CARDi_IsInTcm (u32 buf, u32 len)
{
	const u32 i = OS_GetITCMAddress();
	const u32 d = native_fn_02007714();
	return
	    ((i < buf + len) && (i + 0x8000 > buf)) ||
	    ((d < buf + len) && (d + 0x4000 > buf));
}
static inline u32 CARDi_GetRomFlag (u32 flag)
{
	const u32 rom_ctrl = *(vu32 *)(native_data_main_020dce80 + 0x60);
	return (u32)((rom_ctrl & ~0x07000000 ) | flag |
	             0x00000000 | 0x80000000 | 0x20000000 );
}
BOOL native_main_02010d2c(CARDRomStat * p);
CARDRomStat rom_stat __attribute__ ((aligned(32))) ;
    void native_fn_02010c08 (void);
    void native_data_main_02010c5c (void);
    BOOL native_main_02010d2c (CARDRomStat *p)
    {
        CARDiCommon *const c = &native_data_main_020e5500;
        const u32 dst = c->dst;
        u32 len = c->len;
        const BOOL is_async = !(dst & 31) &&
                            (c->dma <= 3 ) &&
                            !CARDi_IsInTcm(dst, len) &&
                            !(((u32)(c->src | len)) & ((512) - 1)) &&
                            (len > 0);
        p->ctrl = CARDi_GetRomFlag(0x01000000 );
        if (is_async) {
            OSIntrMode bak_psr = native_fn_02007ff4();
            if (len < c->flush_threshold_ic) {
                native_fn_02007344((void *)dst, len);
            } else {
                native_fn_02007338();
            }
            if (len < c->flush_threshold_dc) {
                u32 pos = dst;
                u32 mod = (dst & (32 - 1));
                if (mod) {
                    pos -= mod;
                    native_fn_020072ec((void *)(pos), 32 );
                    native_fn_020072ec((void *)(pos + len), 32 );
                    len += 32 ;
                }
                native_fn_020072d0((void *)pos, len);
                native_fn_0200732c();
            } else {
                native_fn_0200729c();
            }
            (void)native_fn_02005b50((1UL << 19) , native_data_main_02010c5c);
            (void)native_fn_02005d80((1UL << 19) );
            (void)native_fn_02005d20((1UL << 19) );
            (void)native_fn_02008008(bak_psr);
            native_fn_02010c08();
        }
        return is_async;
    }
