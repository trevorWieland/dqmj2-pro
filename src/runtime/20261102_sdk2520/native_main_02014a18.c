#include "native_main_02014a18_types.h"

void native_main_02014a18 (void * arg, u16 child)
{
	MBCommChildBlockHeader hd;
	int state;
	u8 * p_data;
	if (child == 0 || child > 15 ) {
		return;
	}
	p_data = native_fn_02018fa0((u8 *)&((WMMpRecvData *)arg)->cdata[0], &hd, child);
	state = ((MB_CommPWork *)native_data_main_020ec36c) ->p_comm_state[child - 1];
	((void)0) ;
	((void)0) ;
	switch (hd.type) {
	case MB_COMM_TYPE_CHILD_FILEREQ:
	{
		if (state == MB_COMM_PSTATE_CONNECTED) {
			MBCommRequestData req_data;
			if (p_data == ((void *)0) ) {
				break;
			}
			native_fn_02008e0c(p_data, &req_data, (29) );
			((MB_CommPWork *)native_data_main_020ec36c) ->childggid[child - 1] = req_data.ggid;
			((MB_CommPWork *)native_data_main_020ec36c) ->childversion[child - 1] = req_data.version;
			((void)0) ;
			native_fn_02008e0c(&req_data.userinfo, &((MB_CommPWork *)native_data_main_020ec36c) ->childUser[child - 1], sizeof(MBUserInfo));
			((MB_CommPWork *)native_data_main_020ec36c) ->childUser[child - 1].playerNo = child;
			native_fn_02014504(child, MB_COMM_PSTATE_REQUESTED, &req_data.userinfo);
		}
		if (state == MB_COMM_PSTATE_REQUESTED) {
			u8 i, entry_num = 0;
			u8 fileid = ((MBCommRequestData *)p_data)->fileid;
			if (fileid >= (16)
			    || ((MB_CommPWork *)native_data_main_020ec36c) ->fileinfo[fileid].active == 0
			    || ((MB_CommPWork *)native_data_main_020ec36c) ->childggid[child - 1] != ((MB_CommPWork *)native_data_main_020ec36c) ->fileinfo[fileid].game_reg->ggid) {
				((MB_CommPWork *)native_data_main_020ec36c) ->req2child[child - 1] = MB_COMM_USER_REQ_KICK;
			} else {
				for (i = 0; i < 15 + 1; i++) {
					if (((MB_CommPWork *)native_data_main_020ec36c) ->fileinfo[fileid].gameinfo_child_bmp & (0x0001 << i)) {
						entry_num++;
					}
				}
				if (entry_num >= ((MB_CommPWork *)native_data_main_020ec36c) ->fileinfo[fileid].game_reg->maxPlayerNum) {
					((void)0) ;
					((MB_CommPWork *)native_data_main_020ec36c) ->req2child[child - 1] = MB_COMM_USER_REQ_NONE;
					native_fn_02014504(child, MB_COMM_PSTATE_MEMBER_FULL, ((void *)0) );
					break;
				}
			}
			switch (((MB_CommPWork *)native_data_main_020ec36c) ->req2child[child - 1]) {
			case MB_COMM_USER_REQ_ACCEPT:
			{
				if (0 == (((MB_CommPWork *)native_data_main_020ec36c) ->child_entry_bmp & (0x0001 << (child)))) {
					((MB_CommPWork *)native_data_main_020ec36c) ->child_num++;
					((MB_CommPWork *)native_data_main_020ec36c) ->child_entry_bmp |= (0x0001 << (child));
					((MB_CommPWork *)native_data_main_020ec36c) ->fileid_of_child[child - 1] = (s8)fileid;
					((MB_CommPWork *)native_data_main_020ec36c) ->fileinfo[fileid].gameinfo_child_bmp |= (1 << (child)) ;
					((MB_CommPWork *)native_data_main_020ec36c) ->fileinfo[fileid].gameinfo_changed_bmp |= (1 << (child)) ;
					((void)0) ;
					((MB_CommPWork *)native_data_main_020ec36c) ->req2child[child - 1] = MB_COMM_USER_REQ_NONE;
					native_fn_02014504(child, MB_COMM_PSTATE_REQ_ACCEPTED, ((void *)0) );
				}
			}
			break;
			case MB_COMM_USER_REQ_KICK:
				((void)0) ;
				((MB_CommPWork *)native_data_main_020ec36c) ->req2child[child - 1] = MB_COMM_USER_REQ_NONE;
				native_fn_02014504(child, MB_COMM_PSTATE_KICKED, ((void *)0) );
				break;
			}
		}
	}
	break;
	case MB_COMM_TYPE_CHILD_ACCEPT_FILEINFO:
		if (state == MB_COMM_PSTATE_REQ_ACCEPTED) {
			native_fn_02014504(child, MB_COMM_PSTATE_WAIT_TO_SEND, ((void *)0) );
		} else if (state == MB_COMM_PSTATE_WAIT_TO_SEND)   {
			if (((MB_CommPWork *)native_data_main_020ec36c) ->req2child[child - 1] == MB_COMM_USER_REQ_SEND_START) {
				u8 fid = (u8)((MB_CommPWork *)native_data_main_020ec36c) ->fileid_of_child[child - 1];
				((MB_CommPWork *)native_data_main_020ec36c) ->fileinfo[fid].pollbmp |= (0x0001 << (child));
				((MB_CommPWork *)native_data_main_020ec36c) ->fileinfo[fid].currentb = 0;
				((MB_CommPWork *)native_data_main_020ec36c) ->req2child[child - 1] = MB_COMM_USER_REQ_NONE;
				native_fn_02014504(child, MB_COMM_PSTATE_SEND_PROCEED, ((void *)0) );
			}
		}
		break;
	case MB_COMM_TYPE_CHILD_CONTINUE:
		if (state == MB_COMM_PSTATE_SEND_PROCEED) {
			u8 fileid = (u8)((MB_CommPWork *)native_data_main_020ec36c) ->fileid_of_child[child - 1];
			if (fileid == (u8) - 1)
				break;
			((void) 0) ;
			((void) 0) ;
			((MB_CommPWork *)native_data_main_020ec36c) ->fileinfo[fileid].nextb = native_fn_020156bc(((MB_CommPWork *)native_data_main_020ec36c) ->fileinfo[fileid].nextb, hd.data.req);
			native_data_main_020e68a0 |= (1 << fileid);
		}
		break;
	case MB_COMM_TYPE_CHILD_STOPREQ:
		if (state == MB_COMM_PSTATE_SEND_PROCEED) {
			u8 fileid = (u8)((MB_CommPWork *)native_data_main_020ec36c) ->fileid_of_child[child - 1];
			if (fileid == (u8) - 1)
				break;
			((void) 0) ;
			((MB_CommPWork *)native_data_main_020ec36c) ->fileinfo[fileid].pollbmp &= ~(0x0001 << (child));
			native_fn_02014504(child, MB_COMM_PSTATE_SEND_COMPLETE, ((void *)0) );
		} else if (state == MB_COMM_PSTATE_SEND_COMPLETE)   {
			if (((MB_CommPWork *)native_data_main_020ec36c) ->req2child[child - 1] == MB_COMM_USER_REQ_BOOT) {
				((MB_CommPWork *)native_data_main_020ec36c) ->req2child[child - 1] = MB_COMM_USER_REQ_NONE;
				native_fn_02014504(child, MB_COMM_PSTATE_BOOT_REQUEST, ((void *)0) );
				break;
			}
		}
		break;
	case MB_COMM_TYPE_CHILD_BOOTREQ_ACCEPTED:
		if (state == MB_COMM_PSTATE_BOOT_REQUEST) {
			break;
		}
		break;
	default:
		break;
	}
}
u16 native_fn_020156bc (u16 next_block, u16 next_block_req);
