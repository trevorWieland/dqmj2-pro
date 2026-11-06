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
extern MB_CommCommonWork * native_data_main_020ec36c;
void native_fn_02014504(u16 child, int state, void * arg);
void native_fn_02014efc(void * arg);
int native_fn_020154c0(void);
void native_fn_020156e8(u16 aid, u16 errcode);
void native_fn_02014504 (u16 child, int state, void * arg);
void native_fn_02014efc (void * arg);
int native_fn_020154c0 (void);
void native_fn_020156e8 (u16 aid, u16 errcode);
static inline void MI_CpuFillFast (void * dest, u32 data, u32 size)
{
	((void) 0) ;
	((void) 0) ;
	native_fn_02008c58(data, dest, size);
}
static inline void MI_CpuClearFast (void * dest, u32 size)
{
	MI_CpuFillFast(dest, 0, size);
}
static inline void MI_CpuClear8 (void * dest, u32 size)
{
	native_fn_02008d78(dest, 0, size);
}
