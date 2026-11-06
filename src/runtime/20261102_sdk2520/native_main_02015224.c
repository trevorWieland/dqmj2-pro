#include "native_main_02015224_types.h"

int native_main_02015224 (void)
{
	MBCommParentBlockHeader hd;
	u8 * databuf;
	u8 i;
	MB_BlockInfo bi;
	if (((MB_CommPWork *)native_data_main_020ec36c) ->file_num == 0)
		return (WM_ERRCODE_MAX + 1) ;
	for (i = 0; i < (16) ; i++) {
		((MB_CommPWork *)native_data_main_020ec36c) ->cur_fileid = (u8)((((MB_CommPWork *)native_data_main_020ec36c) ->cur_fileid + 1) % (16) );
		if (((MB_CommPWork *)native_data_main_020ec36c) ->fileinfo[((MB_CommPWork *)native_data_main_020ec36c) ->cur_fileid].active
		    && ((MB_CommPWork *)native_data_main_020ec36c) ->fileinfo[((MB_CommPWork *)native_data_main_020ec36c) ->cur_fileid].pollbmp) {
			((void)0) ;
			break;
		}
	}
	if (i == (16) ) {
		return (WM_ERRCODE_MAX + 1) ;
	}
	native_fn_02015640(((MB_CommPWork *)native_data_main_020ec36c) ->cur_fileid);
	if (!native_fn_020161b8(&bi,
	                       &((MB_CommPWork *)native_data_main_020ec36c) ->fileinfo[((MB_CommPWork *)native_data_main_020ec36c) ->cur_fileid].blockinfo_table,
	                       ((MB_CommPWork *)native_data_main_020ec36c) ->fileinfo[((MB_CommPWork *)native_data_main_020ec36c) ->cur_fileid].currentb,
	                       &((MB_CommPWork *)native_data_main_020ec36c) ->fileinfo[((MB_CommPWork *)native_data_main_020ec36c) ->cur_fileid].dl_fileinfo.header)) {
		return (WM_ERRCODE_MAX + 1) ;
	}
	hd.type = MB_COMM_TYPE_PARENT_DATA;
	hd.fid = ((MB_CommPWork *)native_data_main_020ec36c) ->cur_fileid;
	hd.seqno = ((MB_CommPWork *)native_data_main_020ec36c) ->fileinfo[((MB_CommPWork *)native_data_main_020ec36c) ->cur_fileid].currentb;
	databuf = native_fn_02018f1c(&hd, (u8 *)((MB_CommPWork *)native_data_main_020ec36c) ->common.sendbuf);
	{
		u32 card_addr = (u32)(bi.offset -
		                      ((MB_CommPWork *)native_data_main_020ec36c) ->fileinfo[((MB_CommPWork *)native_data_main_020ec36c) ->cur_fileid].blockinfo_table.
		                      seg_src_offset[bi.segment_no] +
		                      ((MB_CommPWork *)native_data_main_020ec36c) ->fileinfo[((MB_CommPWork *)native_data_main_020ec36c) ->cur_fileid].card_mapping[bi.segment_no]);
		MBiCacheList * const pl = ((MB_CommPWork *)native_data_main_020ec36c) ->fileinfo[((MB_CommPWork *)native_data_main_020ec36c) ->cur_fileid].cache_list;
		if (!native_fn_02018a64(pl, card_addr, databuf, bi.size)) {
			MBiTaskInfo * const p_task = &((MB_CommPWork *)native_data_main_020ec36c) ->cur_task;
			if (!native_fn_02018cc4(p_task)) {
				if (pl->lifetime) {
					--pl->lifetime;
				} else {
					MBiCacheInfo * pi = pl->list;
					MBiCacheInfo * trg = ((void *)0) ;
					int i;
					for (i = 0; i < 4 ; ++i) {
						if (pi[i].state == 2 ) {
							if (!trg || (trg->src > pi[i].src))
								trg = &pi[i];
						}
					}
					if (!trg) {
						native_fn_02008430() ;
					}
					pl->lifetime = 2;
					trg->state = 1 ;
					trg->src = (card_addr & ~31);
					p_task->param[0] = (u32)trg;
					p_task->param[1] = (u32)pl;
					native_fn_02018cdc(p_task, native_data_main_02015180, ((void *)0) , 4);
				}
			}
			return (WM_ERRCODE_MAX + 1) ;
		}
	}
	return native_fn_020163e4((int)(bi.size + (6) ),
	                          ((MB_CommPWork *)native_data_main_020ec36c) ->fileinfo[((MB_CommPWork *)native_data_main_020ec36c) ->cur_fileid].pollbmp, ((MB_CommPWork *)native_data_main_020ec36c) ->common.sendbuf);
}
void native_fn_02015640 (u8 file_id);
