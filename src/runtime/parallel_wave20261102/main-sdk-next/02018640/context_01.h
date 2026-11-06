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
typedef enum MBCommUserReq {
	MB_COMM_USER_REQ_NONE = 0,
	MB_COMM_USER_REQ_DL_START,
	MB_COMM_USER_REQ_SEND_START,
	MB_COMM_USER_REQ_ACCEPT,
	MB_COMM_USER_REQ_KICK,
	MB_COMM_USER_REQ_BOOT
} MBCommUserReq;
typedef struct {
	u32 data_buf[15 ][((29) + 1) / sizeof(u32) + 1];
	u32 data_bmp[15 ];
} MbRequestPieceBuf;
void native_fn_02018ed8(u16 child_aid);
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
void native_fn_02016e08(void * arg);
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
void native_fn_02016e08 (void * arg);
