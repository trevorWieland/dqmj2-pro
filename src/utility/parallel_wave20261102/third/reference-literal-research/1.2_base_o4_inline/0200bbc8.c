extern const char child_reference_string_020225dc[3];
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
void MI_CpuCopy8(const void * src, void * dest, u32 size);
    static inline void MI_WriteByte (void * address, u8 value)
    {
        *(u8 *)address = value;
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
static inline BOOL FS_IsDir (volatile const FSFile * p_file)
{
	return (p_file->stat & 0x00000020 ) ? 1 : 0 ;
}
void FS_InitFile(FSFile * p_file);
extern const u16 (*ctrdgi_fl_maxtime);
FSResult FSi_TranslateCommand(FSFile * p_file, FSCommandType command);
static FSResult FSi_GetPathCommand(FSFile *p_file);
void FSi_SeekDirDirect (FSFile *p_dir, u32 id);
static FSResult FSi_GetPathCommand (FSFile *p_file)
{
	FSArchive *const p_arc = p_file->arc;
	FSGetPathInfo *p_info = &p_file->arg.getpath;
	FSDirEntry entry;
	FSFile tmp;
	u32 dir_id;
	u32 file_id;
	u32 id;
	u32 len;
	enum {
        INVALID_ID = 0x10000
    };
	FS_InitFile(&tmp);
	tmp.arc = p_file->arc;
	if (FS_IsDir(p_file)) {
		dir_id = p_file->prop.dir.pos.own_id;
		file_id = INVALID_ID;
	} else {
		file_id = p_file->prop.file.own_id;
		if (p_info->total_len != 0) {
			dir_id = p_info->dir_id;
		} else {
			u32 pos = 0;
			u32 num_dir = 0;
			dir_id = INVALID_ID;
			do {
				FSi_SeekDirDirect(&tmp, pos);
				if (!pos)
					num_dir = tmp.prop.dir.parent;
				tmp.arg.readdir.p_entry = &entry;
				tmp.arg.readdir.skip_string = 1 ;
				while (FSi_TranslateCommand(&tmp, FS_COMMAND_READDIR) == FS_RESULT_SUCCESS) {
					if (!entry.is_directory && (entry.file_id.file_id == file_id)) {
						dir_id = tmp.prop.dir.pos.own_id;
						break;
					}
				}
			} while ((dir_id == INVALID_ID) && (++pos < num_dir));
		}
	}
	if (dir_id == INVALID_ID) {
		p_info->total_len = 0;
		return FS_RESULT_FAILURE;
	}
	if (p_info->total_len == 0) {
		len = 0;
		if (p_arc->name.pack <= 0x000000FF)
			len += 1;
		else if (p_arc->name.pack <= 0x0000FF00)
			len += 2;
		else
			len += 3;
		len += 1 + 1;
		if (file_id != INVALID_ID)
			len += entry.name_len;
		id = dir_id;
		if (id != 0) {
			FSi_SeekDirDirect(&tmp, id);
			do {
				FSi_SeekDirDirect(&tmp, tmp.prop.dir.parent);
				tmp.arg.readdir.p_entry = &entry;
				tmp.arg.readdir.skip_string = 1 ;
				while (FSi_TranslateCommand(&tmp, FS_COMMAND_READDIR) == FS_RESULT_SUCCESS) {
					if (entry.is_directory && (entry.dir_id.own_id == id)) {
						len += entry.name_len + 1;
						break;
					}
				}
				id = tmp.prop.dir.pos.own_id;
			} while (id != 0);
		}
		p_info->total_len = (u16)(len + 1);
		p_info->dir_id = (u16)dir_id;
	}
	if (!p_info->buf)
		return FS_RESULT_SUCCESS;
	if (p_info->buf_len < p_info->total_len)
		return FS_RESULT_FAILURE;
	else {
		u8 *dst = p_info->buf;
		u32 total = p_info->total_len;
		u32 pos = 0;
		if (p_arc->name.pack <= 0x000000FF)
			len = 1;
		else if (p_arc->name.pack <= 0x0000FF00)
			len = 2;
		else
			len = 3;
		MI_CpuCopy8(p_arc->name.ptr, dst + pos, len);
		pos += len;
		MI_CpuCopy8(child_reference_string_020225dc, dst + pos, 2);
		pos += 2;
		id = dir_id;
		FSi_SeekDirDirect(&tmp, id);
		if (file_id != INVALID_ID) {
			tmp.arg.readdir.p_entry = &entry;
			tmp.arg.readdir.skip_string = 0 ;
			while (FSi_TranslateCommand(&tmp, FS_COMMAND_READDIR) == FS_RESULT_SUCCESS) {
				if (!entry.is_directory && (entry.file_id.file_id == file_id))
					break;
			}
			len = entry.name_len + 1;
			MI_CpuCopy8(entry.name, dst + total - len, len);
			total -= len;
		} else {
			MI_WriteByte(dst + total - 1, '\0');
			total -= 1;
		}
		if (id != 0) {
			do {
				FSi_SeekDirDirect(&tmp, tmp.prop.dir.parent);
				tmp.arg.readdir.p_entry = &entry;
				tmp.arg.readdir.skip_string = 0 ;
				MI_WriteByte(dst + total - 1, '/');
				total -= 1;
				while (FSi_TranslateCommand(&tmp, FS_COMMAND_READDIR) == FS_RESULT_SUCCESS) {
					if (entry.is_directory && (entry.dir_id.own_id == id)) {
						len = entry.name_len;
						MI_CpuCopy8(entry.name, dst + total - len, len);
						total -= len;
						break;
					}
				}
				id = tmp.prop.dir.pos.own_id;
			} while (id != 0);
		}
		((void) 0) ;
	}
	return FS_RESULT_SUCCESS;
}
