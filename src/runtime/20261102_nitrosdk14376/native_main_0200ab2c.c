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
    static inline u8 MI_ReadByte (const void * address)
    {
        return *(u8 *)address;
    }
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
extern const u16 (*ctrdgi_fl_maxtime);
static inline BOOL FSi_IsSlash (u32 c)
{
	return (c == '/') || (c == '\\');
}
int native_fn_0200a7cc(const char * str1, const char * str2, u32 len);
FSResult native_fn_0200a63c(FSFile * p_file, FSCommandType command);
FSResult native_main_0200ab2c(FSFile *p_dir);
int native_fn_0200a7cc (const char *str1, const char *str2, u32 len);
void native_fn_0200a8dc (FSFile *p_dir, u32 id);
FSResult native_main_0200ab2c (FSFile *p_dir)
{
	const char *path = p_dir->arg.findpath.path;
	const BOOL is_dir = p_dir->arg.findpath.find_directory;
	p_dir->arg.seekdir.pos = p_dir->arg.findpath.pos;
	(void)native_fn_0200a63c(p_dir, FS_COMMAND_SEEKDIR);
	for (; MI_ReadByte(path); path += (MI_ReadByte(path) ? 1 : 0)) {
		u32 is_directory;
		int name_len = 0;
		while ((is_directory = MI_ReadByte(path + name_len)),
		       (is_directory && !FSi_IsSlash(is_directory)))
			++name_len;
		if (is_directory || is_dir)
			is_directory = 1;
		if (name_len == 0) {
			return FS_RESULT_FAILURE;
		} else if (MI_ReadByte(path) == '.')   {
			if (name_len == 1) {
				path += 1;
				continue;
			} else if ((name_len == 2) & (MI_ReadByte(path + 1) == '.'))   {
				if (p_dir->prop.dir.pos.own_id != 0)
					native_fn_0200a8dc(p_dir, p_dir->prop.dir.parent);
				path += 2;
				continue;
			}
		}
		if (name_len > 127 ) {
			return FS_RESULT_FAILURE;
		} else {
			FSDirEntry etr;
			p_dir->arg.readdir.p_entry = &etr;
			p_dir->arg.readdir.skip_string = 0 ;
			for (;;) {
				if (native_fn_0200a63c(p_dir, FS_COMMAND_READDIR) != FS_RESULT_SUCCESS)
					return FS_RESULT_FAILURE;
				if ((is_directory != etr.is_directory) ||
				    (name_len != etr.name_len) || native_fn_0200a7cc(path, etr.name, (u32)name_len))
					continue;
				if (is_directory) {
					path += name_len;
					p_dir->arg.seekdir.pos = etr.dir_id;
					(void)native_fn_0200a63c(p_dir, FS_COMMAND_SEEKDIR);
					break;
				} else if (is_dir)   {
					return FS_RESULT_FAILURE;
				} else {
					*p_dir->arg.findpath.result.file = etr.file_id;
					return FS_RESULT_SUCCESS;
				}
			}
		}
	}
	if (!is_dir)
		return FS_RESULT_FAILURE;
	*p_dir->arg.findpath.result.dir = p_dir->prop.dir.pos;
	return FS_RESULT_SUCCESS;
}
