#include "context_00.h"
#include "context_01.h"
int native_main_02014fe8 (void)
{
	MBCommParentBlockHeader hd;
	u8 * databuf = ((u8 *)((MB_CommPWork *)native_data_main_020ec36c) ->common.sendbuf) + (6) ;
	u16 child;
	u8 i, fid;
	s8 send_candidate_fid = -1;
	u8 file_req_num[(16) ];
	u16 pollbmp = 0;
	MI_CpuClear8(&file_req_num[0], sizeof(u8) * (16) );
	for (child = 1; child <= 15 ; child++) {
		if (((MB_CommPWork *)native_data_main_020ec36c) ->p_comm_state[child - 1] == MB_COMM_PSTATE_REQ_ACCEPTED) {
			++(file_req_num[((MB_CommPWork *)native_data_main_020ec36c) ->fileid_of_child[child - 1]]);
		}
	}
	fid = (u8)native_data_main_020dce88.field_0000;
	for (i = 0; i < (16) ; i++) {
		fid = (u8)((fid + 1) % (16) );
		if (((MB_CommPWork *)native_data_main_020ec36c) ->fileinfo[fid].active && file_req_num[fid] > 0) {
			send_candidate_fid = (s8)fid;
			break;
		}
	}
	if (send_candidate_fid == -1)
		return (WM_ERRCODE_MAX + 1) ;
	native_data_main_020dce88.field_0000 = send_candidate_fid;
	for (child = 1; child <= 15 ; child++) {
		if (((MB_CommPWork *)native_data_main_020ec36c) ->p_comm_state[child - 1] == MB_COMM_PSTATE_REQ_ACCEPTED
		    && ((MB_CommPWork *)native_data_main_020ec36c) ->fileid_of_child[child - 1] == send_candidate_fid) {
			pollbmp |= (1 << child);
		}
	}
	((void)0) ;
	hd.type = MB_COMM_TYPE_PARENT_DL_FILEINFO;
	hd.fid = send_candidate_fid;
	databuf = native_fn_02018f1c(&hd, (u8 *)((MB_CommPWork *)native_data_main_020ec36c) ->common.sendbuf);
	if (databuf) {
		native_fn_02008e0c(&((MB_CommPWork *)native_data_main_020ec36c) ->fileinfo[send_candidate_fid].dl_fileinfo,
		            databuf, sizeof(MBDownloadFileInfo));
	}
	return native_fn_020163e4(sizeof(MBDownloadFileInfo) + (6) , pollbmp, ((MB_CommPWork *)native_data_main_020ec36c) ->common.sendbuf);
}
