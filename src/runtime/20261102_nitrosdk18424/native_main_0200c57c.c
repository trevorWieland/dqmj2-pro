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
typedef enum {
	MI_PROCESSOR_ARM9 = 0,
	MI_PROCESSOR_ARM7 = 1
} MIProcessor;
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
void native_fn_0200bd04(FSFile * p_file);
BOOL native_fn_0200bf74(FSFile * p_file, FSFileID file_id);
BOOL native_fn_0200c02c(FSFile * p_file);
static inline u32 FS_GetLength (const FSFile * p_file)
{
	return p_file->prop.file.bottom - p_file->prop.file.top;
}
s32 native_fn_0200c180(FSFile * p_file, void * dst, s32 len);
BOOL native_fn_0200bf2c(FSFile * p_file, FSArchive * p_arc,
                       u32 image_top, u32 image_bottom, u32 file_index);
static inline u32 FS_GetFileImageTop (const FSFile * p_file)
{
	return p_file->prop.file.top;
}
typedef u32 FSOverlayID;
typedef void (*FSOverlayInitFunc) (void);
typedef struct {
	u32 id;
	u8 * ram_address;
	u32 ram_size;
	u32 bss_size;
	FSOverlayInitFunc * sinit_init;
	FSOverlayInitFunc * sinit_init_end;
	u32 file_id;
	u32 compressed : 24;
	u32 flag : 8;
} FSOverlayInfoHeader;
typedef struct {
	FSOverlayInfoHeader header;
	MIProcessor target;
	CARDRomRegion file_pos;
} FSOverlayInfo;
FSFileID native_fn_0200c554(const FSOverlayInfo * p_ovi);
BOOL native_main_0200c57c(FSOverlayInfo * p_ovi, MIProcessor target, FSOverlayID id,
                             FSArchive * p_arc,
                             u32 offset_arm9, u32 len_arm9, u32 offset_arm7, u32 len_arm7);
static const u8 fsi_def_digest_key[64] = {
	0x21, 0x06, 0xc0, 0xde,
	0xba, 0x98, 0xce, 0x3f,
	0xa6, 0x92, 0xe3, 0x9d,
	0x46, 0xf2, 0xed, 0x01,
	0x76, 0xe3, 0xcc, 0x08,
	0x56, 0x23, 0x63, 0xfa,
	0xca, 0xd4, 0xec, 0xdf,
	0x9a, 0x62, 0x78, 0x34,
	0x8f, 0x6d, 0x63, 0x3c,
	0xfe, 0x22, 0xca, 0x92,
	0x20, 0x88, 0x97, 0x23,
	0xd2, 0xcf, 0xae, 0xc2,
	0x32, 0x67, 0x8d, 0xfe,
	0xca, 0x83, 0x64, 0x98,
	0xac, 0xfd, 0x3e, 0x37,
	0x87, 0x46, 0x58, 0x24,
};
static int fsi_digest_key_len = sizeof(fsi_def_digest_key);
    FSFileID native_fn_0200c554 (const FSOverlayInfo *p_ovi);
    BOOL native_main_0200c57c (FSOverlayInfo *p_ovi, MIProcessor target, FSOverlayID id,
                                FSArchive *p_arc,
                                u32 offset_arm9, u32 len_arm9, u32 offset_arm7, u32 len_arm7)
    {
        CARDRomRegion pr[1];
        u32 pos;
        if (target == MI_PROCESSOR_ARM9) {
            pr->offset = offset_arm9;
            pr->length = len_arm9;
        } else {
            pr->offset = offset_arm7;
            pr->length = len_arm7;
        }
        pos = (u32)id * sizeof(FSOverlayInfoHeader);
        if (pos >= pr->length) {
            return 0 ;
        } else {
            FSFile file[1];
            native_fn_0200bd04(file);
            if (!native_fn_0200bf2c(file, p_arc, pr->offset + pos, pr->offset + pr->length, (u32) ~0)) {
                return 0 ;
            } else {
                if (native_fn_0200c180(file, p_ovi, sizeof(FSOverlayInfoHeader)) !=
                    sizeof(FSOverlayInfoHeader)) {
                    (void)native_fn_0200c02c(file);
                    return 0 ;
                }
                (void)native_fn_0200c02c(file);
                p_ovi->target = target;
                if (!native_fn_0200bf74(file, native_fn_0200c554(p_ovi))) {
                    return 0 ;
                } else {
                    p_ovi->file_pos.offset = FS_GetFileImageTop(file);
                    p_ovi->file_pos.length = FS_GetLength(file);
                    (void)native_fn_0200c02c(file);
                }
            }
        }
        return 1 ;
    }
