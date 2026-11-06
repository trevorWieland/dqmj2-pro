#include "context_00.h"
#include "context_01.h"
void native_main_02018640 (u16 aid)
{
    ((void) 0) ;
    ((void) 0) ;
    if (native_fn_02012d84(native_fn_02016e08, aid) != WM_ERRCODE_OPERATING) {
        ((void)0) ;
    }
    if (aid == 0 || aid >= 16) {
        ((void)0) ;
        return;
    }
    ((MB_CommPWork *)native_data_main_020ec360.field_000c) ->childversion[aid - 1] = 0;
    MI_CpuClear8(&((MB_CommPWork *)native_data_main_020ec360.field_000c) ->childggid[aid - 1], sizeof(u32));
    MI_CpuClear8(&((MB_CommPWork *)native_data_main_020ec360.field_000c) ->childUser[aid - 1], sizeof(MBUserInfo));
    native_fn_02018ed8(aid);
    ((MB_CommPWork *)native_data_main_020ec360.field_000c) ->req2child[aid - 1] = MB_COMM_USER_REQ_NONE;
    if (((MB_CommPWork *)native_data_main_020ec360.field_000c) ->fileid_of_child[aid - 1] != -1) {
        u8 fileID = (u8)((MB_CommPWork *)native_data_main_020ec360.field_000c) ->fileid_of_child[aid - 1];
        u16 nowChildFlag = ((MB_CommPWork *)native_data_main_020ec360.field_000c) ->fileinfo[fileID].gameinfo_child_bmp;
        u16 child = aid;
        ((MB_CommPWork *)native_data_main_020ec360.field_000c) ->fileinfo[fileID].gameinfo_child_bmp &= ~((1 << (child)) );
        ((MB_CommPWork *)native_data_main_020ec360.field_000c) ->fileinfo[fileID].gameinfo_changed_bmp |= (1 << (child)) ;
        ((MB_CommPWork *)native_data_main_020ec360.field_000c) ->fileid_of_child[child - 1] = -1;
        ((MB_CommPWork *)native_data_main_020ec360.field_000c) ->fileinfo[fileID].pollbmp &= ~(0x0001 << child);
        ((void)0) ;
    }
    if (((MB_CommPWork *)native_data_main_020ec360.field_000c) ->child_entry_bmp & (0x0001 << aid)) {
        ((MB_CommPWork *)native_data_main_020ec360.field_000c) ->child_num--;
        ((MB_CommPWork *)native_data_main_020ec360.field_000c) ->child_entry_bmp &= ~(0x0001 << aid);
    }
    ((MB_CommPWork *)native_data_main_020ec360.field_000c) ->p_comm_state[aid - 1] = MB_COMM_PSTATE_NONE;
}
