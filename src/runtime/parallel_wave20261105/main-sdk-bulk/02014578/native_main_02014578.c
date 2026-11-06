#include "context_00.h"
#include "context_01.h"
void native_main_02014578 (u16 type, void * arg)
{
	((void)0) ;
	switch (type) {
	case 21 :
		native_fn_02014504(0, MB_COMM_PSTATE_INIT_COMPLETE, arg);
		break;
	case 17 :
		break;
	case 0 :
	{
		WMstartParentCallback * sparg = (WMstartParentCallback *)arg;
		if (sparg->aid == 0)
			break;
		if (sparg->aid >= 16) {
			((void)0) ;
			break;
		}
		((void)0) ;
		native_fn_02014504(sparg->aid, MB_COMM_PSTATE_CONNECTED, arg);
	}
	break;
	case 1 :
	{
		WMstartParentCallback * sparg = (WMstartParentCallback *)arg;
		if (sparg->aid == 0)
			break;
		if (sparg->aid >= 16) {
			((void)0) ;
			break;
		}
		((void)0) ;
		((MB_CommPWork *)native_data_main_020ec36c) ->childversion[sparg->aid - 1] = 0;
		MI_CpuClear8(&((MB_CommPWork *)native_data_main_020ec36c) ->childggid[sparg->aid - 1], sizeof(u32));
		MI_CpuClear8(&((MB_CommPWork *)native_data_main_020ec36c) ->childUser[sparg->aid - 1], sizeof(MBUserInfo));
		native_fn_02018ed8(sparg->aid);
		((MB_CommPWork *)native_data_main_020ec36c) ->req2child[sparg->aid - 1] = MB_COMM_USER_REQ_NONE;
		if (((MB_CommPWork *)native_data_main_020ec36c) ->fileid_of_child[sparg->aid - 1] != -1) {
			u8 fileID = (u8)((MB_CommPWork *)native_data_main_020ec36c) ->fileid_of_child[sparg->aid - 1];
			u16 nowChildFlag = ((MB_CommPWork *)native_data_main_020ec36c) ->fileinfo[fileID].gameinfo_child_bmp;
			u16 child = sparg->aid;
			((MB_CommPWork *)native_data_main_020ec36c) ->fileinfo[fileID].gameinfo_child_bmp &= ~((1 << (child)) );
			((MB_CommPWork *)native_data_main_020ec36c) ->fileinfo[fileID].gameinfo_changed_bmp |= (1 << (child)) ;
			((MB_CommPWork *)native_data_main_020ec36c) ->fileid_of_child[child - 1] = -1;
			((MB_CommPWork *)native_data_main_020ec36c) ->fileinfo[fileID].pollbmp &= ~(0x0001 << (child));
			((void)0) ;
		}
		if (((MB_CommPWork *)native_data_main_020ec36c) ->child_entry_bmp & (0x0001 << (sparg->aid))) {
			((MB_CommPWork *)native_data_main_020ec36c) ->child_num--;
			((MB_CommPWork *)native_data_main_020ec36c) ->child_entry_bmp &= ~(0x0001 << (sparg->aid));
		}
		if (((MB_CommPWork *)native_data_main_020ec36c) ->p_comm_state[sparg->aid - 1] == MB_COMM_PSTATE_BOOT_REQUEST) {
			native_fn_02014504(sparg->aid, MB_COMM_PSTATE_BOOT_STARTABLE, ((void *)0) );
		}
		native_fn_02014504(sparg->aid, MB_COMM_PSTATE_DISCONNECTED, arg);
		((MB_CommPWork *)native_data_main_020ec36c) ->p_comm_state[sparg->aid - 1] = MB_COMM_PSTATE_NONE;
	}
	break;
	case 3 :
		native_fn_02014efc(arg);
		break;
	case 25 :
		(void)native_fn_020154c0();
		break;
	case 28 :
	{
		u8 i;
		for (i = 0; i < (16) ; i++) {
			if (((MB_CommPWork *)native_data_main_020ec36c) ->fileinfo[i].active && ((MB_CommPWork *)native_data_main_020ec36c) ->fileinfo[i].gameinfo_changed_bmp) {
				native_fn_020165f8(&((MB_CommPWork *)native_data_main_020ec36c) ->fileinfo[i].game_info,
				                        &((MB_CommPWork *)native_data_main_020ec36c) ->childUser[0],
				                        ((MB_CommPWork *)native_data_main_020ec36c) ->fileinfo[i].gameinfo_child_bmp,
				                        ((MB_CommPWork *)native_data_main_020ec36c) ->fileinfo[i].gameinfo_changed_bmp);
				((MB_CommPWork *)native_data_main_020ec36c) ->fileinfo[i].gameinfo_changed_bmp = 0;
			}
		}
	}
		native_fn_02016724(native_fn_02018908(), native_fn_0201891c(), native_fn_02018930());
		break;
	case 255 :
	{
		u16 apiid, errcode;
		apiid = ((u16 *)arg)[0];
		errcode = ((u16 *)arg)[1];
		switch (errcode) {
		case WM_ERRCODE_INVALID_PARAM:
		case WM_ERRCODE_FAILED:
		case WM_ERRCODE_WM_DISABLE:
		case WM_ERRCODE_NO_DATASET:
		case WM_ERRCODE_FIFO_ERROR:
		case WM_ERRCODE_TIMEOUT:
			native_fn_020156e8(0, MB_ERRCODE_FATAL);
			break;
		case WM_ERRCODE_OPERATING:
		case WM_ERRCODE_ILLEGAL_STATE:
		case WM_ERRCODE_NO_CHILD:
		case WM_ERRCODE_OVER_MAX_ENTRY:
		case WM_ERRCODE_NO_ENTRY:
		case WM_ERRCODE_INVALID_POLLBITMAP:
		case WM_ERRCODE_NO_DATA:
		case WM_ERRCODE_SEND_QUEUE_FULL:
		case WM_ERRCODE_SEND_FAILED:
		default:
			native_fn_020156e8(0, MB_ERRCODE_WM_FAILURE);
			break;
		}
	}
	break;
	case 256 :
	{
		WMCallback * pWmcb = (WMCallback *)arg;
		switch (pWmcb->apiid) {
		case WM_APIID_INITIALIZE:
		case WM_APIID_SET_LIFETIME:
		case WM_APIID_SET_P_PARAM:
		case WM_APIID_SET_BEACON_IND:
		case WM_APIID_START_PARENT:
		case WM_APIID_START_MP:
		case WM_APIID_SET_MP_DATA:
		case WM_APIID_START_DCF:
		case WM_APIID_SET_DCF_DATA:
		case WM_APIID_DISCONNECT:
		case WM_APIID_START_KS:
			native_fn_020156e8(0, MB_ERRCODE_FATAL);
			break;
		case WM_APIID_RESET:
		case WM_APIID_END:
		default:
			native_fn_020156e8(0, MB_ERRCODE_WM_FAILURE);
			break;
		}
	}
	break;
	}
	if (type == 17 ) {
		MBCommPStateCallback tmpCb = ((MB_CommPWork *)native_data_main_020ec36c) ->parent_callback;
		MI_CpuClearFast(((MB_CommPWork *)native_data_main_020ec36c) , sizeof(MB_CommPWork));
		((MB_CommPWork *)native_data_main_020ec36c) = ((void *)0) ;
		if (tmpCb) {
			(*tmpCb)(0, MB_COMM_PSTATE_END, ((void *)0) );
		}
	}
}
