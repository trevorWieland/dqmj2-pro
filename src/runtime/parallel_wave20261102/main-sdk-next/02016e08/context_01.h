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
typedef enum {
	MB_COMM_PSTATE_NONE,
	MB_COMM_PSTATE_INIT_COMPLETE,
	MB_COMM_PSTATE_CONNECTED,
	MB_COMM_PSTATE_DISCONNECTED,
	MB_COMM_PSTATE_KICKED,
	MB_COMM_PSTATE_REQ_ACCEPTED,
	MB_COMM_PSTATE_SEND_PROCEED,
	MB_COMM_PSTATE_SEND_COMPLETE,
	MB_COMM_PSTATE_BOOT_REQUEST,
	MB_COMM_PSTATE_BOOT_STARTABLE,
	MB_COMM_PSTATE_REQUESTED,
	MB_COMM_PSTATE_MEMBER_FULL,
	MB_COMM_PSTATE_END,
	MB_COMM_PSTATE_ERROR,
	MB_COMM_PSTATE_WAIT_TO_SEND,
	MB_COMM_PSTATE_WM_EVENT = 0x80000000
} MBCommPState;
typedef void (*MBCommPStateCallback) (u16 child_aid, u32 status, void * arg);
typedef struct {
	const char * romFilePathp;
	u16 * gameNamep;
	u16 * gameIntroductionp;
	const char * iconCharPathp;
	const char * iconPalettePathp;
	u32 ggid;
	u8 maxPlayerNum;
	u8 pad[3];
	u8 userParam[0x20 ];
} MBGameRegistry;
typedef struct {
	u16 palette[16 ];
	u16 data[512 / 2];
} MBIconInfo;
typedef struct {
	u8 favoriteColor : 4;
	u8 playerNo : 4;
	u8 nameLength;
	u16 name[10 ];
} MBUserInfo;
typedef struct MBGameInfoFixed {
	MBIconInfo icon;
	MBUserInfo parent;
	u8 maxPlayerNum;
	u8 pad[1];
	u16 gameName[48 ];
	u16 gameIntroduction[96 ];
} MBGameInfoFixed, MbGameInfoFixed;
typedef struct MBGameInfoVolatile {
	u8 nowPlayerNum;
	u8 pad[1];
	u16 nowPlayerFlag;
	u16 changePlayerFlag;
	MBUserInfo member[15 ];
	u8 userVolatData[8 ];
} MBGameInfoVolatile, MbGameInfoVolatile;
typedef struct MBGameInfo {
	MBGameInfoFixed fixed;
	MBGameInfoVolatile volat;
	u16 broadcastedPlayerFlag;
	u8 dataAttr;
	u8 seqNoFixed;
	u8 seqNoVolat;
	u8 fileNo;
	u8 pad[2];
	u32 ggid;
	struct MBGameInfo * nextp;
} MBGameInfo, MbGameInfo;
extern const u16 (*ctrdgi_fl_maxtime);
typedef struct ParentInfo {
	union {
		WMBssDesc parentInfo[1];
__attribute__ ((aligned(32))) u8 parentInfo_area[192 ];
	};
	WMStartScanCallback scan_data;
	u8 reserved1[8];
} ParentInfo;
typedef void (*MBCallbackFunc) (u16 type, void * arg);
typedef struct {
	union {
		WMParentParam parentParam;
__attribute__ ((aligned(32))) u8 parentParam_area[64 ];
	};
__attribute__ ((aligned(32))) u16 sendBuf[(0x400) / sizeof(u16)];
	union {
		WMBssDesc parentInfoBuf;
__attribute__ ((aligned(32))) u8 parentInfoBuf_area[192 ];
	};
	u16 p_sendlen;
	u16 p_recvlen;
	WMMpRecvBuf * recvBuf;
	void (*callback_ptr) (void * arg);
	u8 mpBusy;
	u8 mbIsStarted;
	u8 reserved0[10];
	u16 sendBufSize;
	u16 recvBufSize;
	MBCallbackFunc callback;
	const WMBssDesc * pInfo;
	u16 mode;
	u16 endReq;
	u16 mpStarted;
	u16 child_bitmap;
	u16 contSend;
	u8 reserved1[2];
__attribute__ ((aligned(4))) u8 uname[8 ];
__attribute__ ((aligned(4))) u8 gname[16 ];
	u16 currentTgid;
	u8 reserved2[22];
__attribute__ ((aligned(32))) u16 userGameInfo[((112 + 32) & ~(32 - 1)) / sizeof(u16)];
	struct {
		u16 found_parent_count;
		u16 my_aid;
		BOOL scanning_flag;
		BOOL scan_channel_flag;
		int last_found_parent_no;
		u8 reserved8[16];
		ParentInfo parent_info[16 ];
	};
} MBiParam;
typedef struct {
	u32 data_buf[15 ][((29) + 1) / sizeof(u32) + 1];
	u32 data_bmp[15 ];
} MbRequestPieceBuf;
typedef struct MbDownloadFileInfoHeader {
	u32 arm9EntryAddr;
	u32 arm7EntryAddr;
	u32 padding;
} MbDownloadFileInfoHeader;
typedef struct MbSegmentInfo {
	u32 recv_addr;
	u32 load_addr;
	u32 size;
	u32 target :1;
	u32 rsv :31;
} MbSegmentInfo;
typedef struct {
	MbDownloadFileInfoHeader header;
	MbSegmentInfo seg[(3) ];
	u32 auth_code[(136) / sizeof(u32)];
	u32 reserved[32 / sizeof(u32)];
} MBDownloadFileInfo;
typedef struct {
	u32 seg_src_offset[(3) ];
	u16 seg_head_blockno[(3) ];
	u16 block_num;
} MB_BlockInfoTable;
typedef struct {
	u32 src;
	u32 len;
	u8 * ptr;
	u32 state;
} MBiCacheInfo;
typedef struct {
	u32 lifetime;
	u32 recent;
	MBiCacheInfo * p_list;
	u32 size;
	char arc_name[FS_ARCHIVE_NAME_LEN_MAX + 1];
	u32 arc_name_len;
	FSArchive * arc_pointer;
	u8 reserved[32 - FS_ARCHIVE_NAME_LEN_MAX - 1 - sizeof(u32) - sizeof(FSArchive *)];
	MBiCacheInfo list[4 ];
} MBiCacheList;
struct MBiTaskInfo_tag;
typedef void (*MB_TASK_FUNC) (struct MBiTaskInfo_tag *);
typedef struct MBiTaskInfo_tag {
	struct MBiTaskInfo_tag * next;
	u32 busy : 1;
	u32 priority : 31;
	MB_TASK_FUNC task;
	MB_TASK_FUNC callback;
	u32 param[4];
} MBiTaskInfo;
typedef struct MB_CommCommonWork {
__attribute__ ((aligned(32))) u32 sendbuf[(0x400) / sizeof(u32)];
__attribute__ ((aligned(32))) u32 recvbuf[(0x80) * 15 * 2 / sizeof(u32)];
	MBUserInfo user;
	u16 isMbInitialized;
	int block_size_max;
	BOOL start_mp_busy;
	BOOL is_started_ex;
	u8 padding[28];
} MB_CommCommonWork;
typedef struct MB_CommPWork {
	MB_CommCommonWork common;
__attribute__ ((aligned(4))) MBUserInfo childUser[15 ];
	u16 childversion[15 ];
	u32 childggid[15 ];
	MBCommPStateCallback parent_callback;
	int p_comm_state[15 ];
	u8 file_num;
	u8 cur_fileid;
	s8 fileid_of_child[15 ];
	u8 child_num;
	u16 child_entry_bmp;
	MbRequestPieceBuf req_data_buf;
	u16 req2child[15 ];
	MBUserInfo childUserBuf;
	struct {
		MBDownloadFileInfo dl_fileinfo;
		MBGameInfo game_info;
		MB_BlockInfoTable blockinfo_table;
		MBGameRegistry * game_reg;
		void * src_adr;
		u16 currentb;
		u16 nextb;
		u16 pollbmp;
		u16 gameinfo_child_bmp;
		u16 gameinfo_changed_bmp;
		u8 active;
		u8 update;
		MBiCacheList * cache_list;
		u32 * card_mapping;
	} fileinfo[(16) ];
	BOOL useWvrFlag;
	u8 padding2[20];
	u8 task_work[2 * 1024];
	MBiTaskInfo cur_task;
} MB_CommPWork;
typedef struct {
u16 field_0000;
u16 field_0002;
u16 field_0004;
u16 field_0006;
unsigned char field_0008[4];
BOOL field_000c;
unsigned char field_0010[20];
} NativeStorage_020dce94;
extern NativeStorage_020dce94 native_data_main_020dce94;
void native_fn_020189b0(u16 apiid, int errcode);
void native_main_02016e08(void * arg);
typedef struct {
u16 field_0000;
unsigned char padding_0002[2];
u8 * field_0004;
MBiParam * field_0008;
MB_CommCommonWork * field_000c;
unsigned char padding_0010[16];
__attribute__ ((aligned(32))) WMscanParam field_0020;
} NativeStorage_020ec360;
extern NativeStorage_020ec360 native_data_main_020ec360;
BOOL native_fn_02016d14 (void);
void native_fn_02016d74 (void);
static inline void MbWaitForWvr (u32 cycles)
{
    u32 child_cnt = 0;
    u32 i;
    for (i = 0; i < 15 ; i++) {
        if (((MB_CommPWork *)native_data_main_020ec360.field_000c) ->p_comm_state[i] != MB_COMM_PSTATE_NONE) {
            if (++child_cnt >= 2)
                break;
        }
    }
    if (child_cnt == 1) {
        native_fn_02008064(cycles);
    }
}
void native_fn_02016dc4 (void * arg);
void native_fn_020189b0 (u16 apiid, int errcode);
