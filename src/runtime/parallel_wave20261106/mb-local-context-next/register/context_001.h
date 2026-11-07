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
extern MB_CommCommonWork * mbc;
extern void MBi_MakeDownloadFileInfo(MbDownloadFileInfoHeader * mbdlFileInfop, const void * buf);
BOOL MB_RegisterFile (const MBGameRegistry * game_reg, const void * buf)
{
	MbDownloadFileInfoHeader * mdfi;
	static u8 update = 0;
	u8 * appname = (u8 *)game_reg->gameNamep;
	u8 fileID = 0xff, i;
	OSIntrMode enabled = OS_DisableInterrupts();
	if (!MBi_IsStarted()) {
		((void)0) ;
		(void)OS_RestoreInterrupts(enabled);
		return 0 ;
	}
	if (((MB_CommPWork *)mbc) ->file_num + 1 > (16) ) {
		((void)0) ;
		(void)OS_RestoreInterrupts(enabled);
		return 0 ;
	}
	for (i = 0; i < (16) ; i++) {
		if (((MB_CommPWork *)mbc) ->fileinfo[i].game_reg == (MBGameRegistry *)game_reg) {
			((void)0) ;
			(void)OS_RestoreInterrupts(enabled);
			return 0 ;
		}
		if (((MB_CommPWork *)mbc) ->fileinfo[i].active == 0) {
			fileID = i;
			break;
		}
	}
	if (i == (16) ) {
		((void)0) ;
		(void)OS_RestoreInterrupts(enabled);
		return 0 ;
	}
	((MB_CommPWork *)mbc) ->fileinfo[fileID].game_reg = (MBGameRegistry *)game_reg;
	mdfi = &((MB_CommPWork *)mbc) ->fileinfo[fileID].dl_fileinfo.header;
	MBi_MakeDownloadFileInfo(mdfi, buf);
	MI_CpuCopy8(game_reg->userParam,
	            ((MBDownloadFileInfo *) mdfi)->reserved, 0x20 );
	if (0 == MBi_MakeBlockInfoTable(&((MB_CommPWork *)mbc) ->fileinfo[fileID].blockinfo_table, mdfi)) {
		((void)0) ;
		(void)OS_RestoreInterrupts(enabled);
		return 0 ;
	}
	MBi_MakeGameInfo(&((MB_CommPWork *)mbc) ->fileinfo[fileID].game_info, game_reg, &((MB_CommPWork *)mbc) ->common.user);
	((MB_CommPWork *)mbc) ->fileinfo[fileID].game_info.fileNo = fileID;
	MB_AddGameInfo(&((MB_CommPWork *)mbc) ->fileinfo[fileID].game_info);
	((MB_CommPWork *)mbc) ->fileinfo[fileID].game_info.seqNoFixed = update++;
	((MB_CommPWork *)mbc) ->fileinfo[fileID].gameinfo_child_bmp = (0x0001) ;
	((MB_CommPWork *)mbc) ->fileinfo[fileID].src_adr = (u32 *)buf;
	((MB_CommPWork *)mbc) ->fileinfo[fileID].cache_list = (MBiCacheList *)((u32)buf + (0x160) + (136) );
	((MB_CommPWork *)mbc) ->fileinfo[fileID].card_mapping = (u32 *) ((u32)buf + (0x160) + (136) + sizeof(MBiCacheList));
	if (((MB_CommPWork *)mbc) ->fileinfo[fileID].cache_list->list[3].state != 0 ) {
		if (!MBi_IsTaskAvailable()) {
			MBi_InitTaskInfo(&((MB_CommPWork *)mbc) ->cur_task);
			MBi_InitTaskThread(((MB_CommPWork *)mbc) ->task_work, sizeof(((MB_CommPWork *)mbc) ->task_work));
		}
	}
	((MB_CommPWork *)mbc) ->fileinfo[fileID].active = 1;
	((MB_CommPWork *)mbc) ->file_num++;
	((void)0) ;
	(void)OS_RestoreInterrupts(enabled);
	return 1 ;
}
