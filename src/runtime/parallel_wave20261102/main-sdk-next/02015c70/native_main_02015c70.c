#include "context_00.h"
BOOL native_main_02015c70 (const MBGameRegistry * game_reg, const void * buf)
{
	MbDownloadFileInfoHeader * mdfi;
	u8 * appname = (u8 *)game_reg->gameNamep;
	u8 fileID = 0xff, i;
	OSIntrMode enabled = native_fn_02007ff4();
	if (!native_fn_02018990()) {
		((void)0) ;
		(void)native_fn_02008008(enabled);
		return 0 ;
	}
	if (((MB_CommPWork *)native_data_main_020ec36c) ->file_num + 1 > (16) ) {
		((void)0) ;
		(void)native_fn_02008008(enabled);
		return 0 ;
	}
	for (i = 0; i < (16) ; i++) {
		if (((MB_CommPWork *)native_data_main_020ec36c) ->fileinfo[i].game_reg == (MBGameRegistry *)game_reg) {
			((void)0) ;
			(void)native_fn_02008008(enabled);
			return 0 ;
		}
		if (((MB_CommPWork *)native_data_main_020ec36c) ->fileinfo[i].active == 0) {
			fileID = i;
			break;
		}
	}
	if (i == (16) ) {
		((void)0) ;
		(void)native_fn_02008008(enabled);
		return 0 ;
	}
	((MB_CommPWork *)native_data_main_020ec36c) ->fileinfo[fileID].game_reg = (MBGameRegistry *)game_reg;
	mdfi = &((MB_CommPWork *)native_data_main_020ec36c) ->fileinfo[fileID].dl_fileinfo.header;
	native_fn_02015f00(mdfi, buf);
	native_fn_02008e0c(game_reg->userParam,
	            ((MBDownloadFileInfo *) mdfi)->reserved, 0x20 );
	if (0 == native_fn_020160ec(&((MB_CommPWork *)native_data_main_020ec36c) ->fileinfo[fileID].blockinfo_table, mdfi)) {
		((void)0) ;
		(void)native_fn_02008008(enabled);
		return 0 ;
	}
	native_fn_02016468(&((MB_CommPWork *)native_data_main_020ec36c) ->fileinfo[fileID].game_info, game_reg, &((MB_CommPWork *)native_data_main_020ec36c) ->common.user);
	((MB_CommPWork *)native_data_main_020ec36c) ->fileinfo[fileID].game_info.fileNo = fileID;
	native_fn_02016690(&((MB_CommPWork *)native_data_main_020ec36c) ->fileinfo[fileID].game_info);
	((MB_CommPWork *)native_data_main_020ec36c) ->fileinfo[fileID].game_info.seqNoFixed = native_data_main_020e68a4.field_0000++;
	((MB_CommPWork *)native_data_main_020ec36c) ->fileinfo[fileID].gameinfo_child_bmp = (0x0001) ;
	((MB_CommPWork *)native_data_main_020ec36c) ->fileinfo[fileID].src_adr = (u32 *)buf;
	((MB_CommPWork *)native_data_main_020ec36c) ->fileinfo[fileID].cache_list = (MBiCacheList *)((u32)buf + (0x160) + (136) );
	((MB_CommPWork *)native_data_main_020ec36c) ->fileinfo[fileID].card_mapping = (u32 *) ((u32)buf + (0x160) + (136) + sizeof(MBiCacheList));
	if (((MB_CommPWork *)native_data_main_020ec36c) ->fileinfo[fileID].cache_list->list[3].state != 0 ) {
		if (!native_fn_02018c94()) {
			native_fn_02018cb0(&((MB_CommPWork *)native_data_main_020ec36c) ->cur_task);
			native_fn_02018c14(((MB_CommPWork *)native_data_main_020ec36c) ->task_work, sizeof(((MB_CommPWork *)native_data_main_020ec36c) ->task_work));
		}
	}
	((MB_CommPWork *)native_data_main_020ec36c) ->fileinfo[fileID].active = 1;
	((MB_CommPWork *)native_data_main_020ec36c) ->file_num++;
	((void)0) ;
	(void)native_fn_02008008(enabled);
	return 1 ;
}
