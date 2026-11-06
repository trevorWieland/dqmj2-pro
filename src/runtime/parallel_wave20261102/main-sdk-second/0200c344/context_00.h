typedef unsigned char u8;
typedef unsigned short int u16;
typedef unsigned long u32;
typedef unsigned long long int u64;
typedef signed long s32;
typedef int BOOL;
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
s32 native_fn_020060e4(void);
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
void native_fn_02011194(void);
typedef struct {
	u32 offset;
	u32 length;
} CARDRomRegion;
enum {
	FS_ARCHIVE_NAME_LEN_MAX = 3
};
typedef enum {
	FS_COMMAND_ASYNC_BEGIN = 0,
	FS_COMMAND_READFILE = FS_COMMAND_ASYNC_BEGIN,
	FS_COMMAND_WRITEFILE,
	FS_COMMAND_ASYNC_END,
	FS_COMMAND_SYNC_BEGIN = FS_COMMAND_ASYNC_END,
	FS_COMMAND_SEEKDIR = FS_COMMAND_SYNC_BEGIN,
	FS_COMMAND_READDIR,
	FS_COMMAND_FINDPATH,
	FS_COMMAND_GETPATH,
	FS_COMMAND_OPENFILEFAST,
	FS_COMMAND_OPENFILEDIRECT,
	FS_COMMAND_CLOSEFILE,
	FS_COMMAND_SYNC_END,
	FS_COMMAND_STATUS_BEGIN = FS_COMMAND_SYNC_END,
	FS_COMMAND_ACTIVATE = FS_COMMAND_STATUS_BEGIN,
	FS_COMMAND_IDLE,
	FS_COMMAND_SUSPEND,
	FS_COMMAND_RESUME,
	FS_COMMAND_STATUS_END,
	FS_COMMAND_INVALID
} FSCommandType;
typedef enum {
	FS_RESULT_SUCCESS = 0,
	FS_RESULT_FAILURE,
	FS_RESULT_BUSY,
	FS_RESULT_CANCELED,
	FS_RESULT_CANCELLED = FS_RESULT_CANCELED,
	FS_RESULT_UNSUPPORTED,
	FS_RESULT_ERROR,
	FS_RESULT_PROC_ASYNC,
	FS_RESULT_PROC_DEFAULT,
	FS_RESULT_PROC_UNKNOWN
} FSResult;
struct FSFile;
struct FSFileLink;
struct FSArchive;
typedef FSResult (*FS_ARCHIVE_PROC_FUNC) (struct FSFile *, FSCommandType);
typedef FSResult (*FS_ARCHIVE_READ_FUNC) (struct FSArchive * p, void * dst, u32 pos, u32 size);
typedef FSResult (*FS_ARCHIVE_WRITE_FUNC) (struct FSArchive * p, const void * src, u32 pos, u32 size);
typedef struct FSFileLink {
	struct FSFile * prev;
	struct FSFile * next;
} FSFileLink;
typedef struct FSArchive {
	union {
		char ptr[FS_ARCHIVE_NAME_LEN_MAX + 1];
		u32 pack;
	} name;
	struct FSArchive * next;
	struct FSArchive * prev;
	OSThreadQueue sync_q;
	OSThreadQueue stat_q;
	u32 flag;
	FSFileLink list;
	u32 base;
	u32 fat;
	u32 fat_size;
	u32 fnt;
	u32 fnt_size;
	u32 fat_bak;
	u32 fnt_bak;
	void * load_mem;
	FS_ARCHIVE_READ_FUNC read_func;
	FS_ARCHIVE_WRITE_FUNC write_func;
	FS_ARCHIVE_READ_FUNC table_func;
	FS_ARCHIVE_PROC_FUNC proc;
	u32 proc_flag;
} FSArchive;
void native_fn_0200b6a8(FSArchive * p_arc);
BOOL native_fn_0200b714(FSArchive * p_arc, const char * name, u32 name_len);
BOOL native_fn_0200b84c(FSArchive * p_arc, u32 base,
                    u32 fat, u32 fat_size, u32 fnt, u32 fnt_size,
                    FS_ARCHIVE_READ_FUNC read_func, FS_ARCHIVE_WRITE_FUNC write_func);
void native_fn_0200bc38(struct FSArchive * p_arc, FS_ARCHIVE_PROC_FUNC proc, u32 flags);
struct FSFile;
typedef struct {
	struct FSArchive * arc;
	u16 own_id;
	u16 index;
	u32 pos;
} FSDirPos;
typedef struct {
	struct FSArchive * arc;
	u32 file_id;
} FSFileID;
typedef struct {
	union {
		FSFileID file_id;
		FSDirPos dir_id;
	};
	u32 is_directory;
	u32 name_len;
	char name[127 + 1];
} FSDirEntry;
typedef struct {
	FSDirPos pos;
} FSSeekDirInfo;
typedef struct {
	FSDirEntry * p_entry;
	BOOL skip_string;
} FSReadDirInfo;
typedef struct {
	FSDirPos pos;
	const char * path;
	BOOL find_directory;
	union {
		FSFileID * file;
		FSDirPos * dir;
	}
	result;
} FSFindPathInfo;
typedef struct {
	u8 * buf;
	u32 buf_len;
	u16 total_len;
	u16 dir_id;
} FSGetPathInfo;
typedef struct {
	FSFileID id;
} FSOpenFileFastInfo;
typedef struct {
	u32 top;
	u32 bottom;
	u32 index;
} FSOpenFileDirectInfo;
typedef struct {
	u32 reserved;
} FSCloseFileInfo;
typedef struct {
	void * dst;
	u32 len_org;
	u32 len;
} FSReadFileInfo;
typedef struct {
	const void * src;
	u32 len_org;
	u32 len;
} FSWriteFileInfo;
typedef struct FSFile {
	FSFileLink link;
	struct FSArchive * arc;
	u32 stat;
	FSCommandType command;
	FSResult error;
	OSThreadQueue queue[1];
	union {
		struct {
			u32 own_id;
			u32 top;
			u32 bottom;
			u32 pos;
		} file;
		struct {
			FSDirPos pos;
			u32 parent;
		} dir;
	}
	prop;
	union {
		FSReadFileInfo readfile;
		FSWriteFileInfo writefile;
		FSSeekDirInfo seekdir;
		FSReadDirInfo readdir;
		FSFindPathInfo findpath;
		FSGetPathInfo getpath;
		FSOpenFileFastInfo openfilefast;
		FSOpenFileDirectInfo openfiledirect;
		FSCloseFileInfo closefile;
	} arg;
} FSFile;
extern const u16 (*ctrdgi_fl_maxtime);
typedef struct {
	u16 length;
	u16 rssi;
	u16 bssid[3];
	u16 ssidLength;
	u8 ssid[32];
	u16 capaInfo;
	struct {
		u16 basic;
		u16 support;
	} rateSet;
	u16 beaconPeriod;
	u16 dtimPeriod;
	u16 channel;
	u16 cfpPeriod;
	u16 cfpMaxDuration;
} MBParentBssDesc;
typedef struct {
	u16 boot_type;
	MBParentBssDesc parent_bss_desc;
} MBParam;
void native_main_0200c344(u32 default_dma_no);
typedef struct {
s32 field_0000;
u32 field_0004;
CARDRomRegion field_0008;
CARDRomRegion field_0010;
FSArchive field_0018;
} NativeStorage_020e535c;
extern NativeStorage_020e535c native_data_main_020e535c;
FSResult native_fn_0200c278 (FSArchive *p_arc, void *dst, u32 src, u32 len);
FSResult native_fn_0200c2c0 (FSArchive *p_arc, const void *src, u32 dst, u32 len);
FSResult native_fn_0200c2c8 (FSFile *p_file, FSCommandType cmd);
FSResult native_fn_0200c334 (FSArchive *p_arc, void *dst, u32 src, u32 len);
FSResult native_fn_0200c33c (FSFile *p_file, FSCommandType cmd);
extern const char native_data_main_020dcb60[4];
static inline const CARDRomRegion * CARD_GetRomRegionFNT (void)
{
	return (const CARDRomRegion *)((const u8 *)(0x02000000 + 0x007ffe00) + 0x40);
}
static inline const CARDRomRegion * CARD_GetRomRegionFAT (void)
{
	return (const CARDRomRegion *)((const u8 *)(0x02000000 + 0x007ffe00) + 0x48);
}
static inline const MBParam * MB_GetMultiBootParam (void)
{
	return (const MBParam *)(0x02000000 + 0x007ffc40) ;
}
static inline BOOL MB_IsMultiBootChild (void)
{
	return MB_GetMultiBootParam()->boot_type == 2 ;
}
