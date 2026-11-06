#include "context_00.h"
#include "context_01.h"
int native_main_02018324 (int channel)
{
    int i, ret;
    MBCommPStateCallback cb_tmp;
    OSIntrMode enabled;
    enabled = native_fn_02007ff4();
    native_data_main_020ec360.field_0008->parentParam.channel = (u16)channel;
    native_data_main_020ec360.field_0004 = (u8 *)((((u32)native_data_main_020ec360.field_000c) + sizeof(MB_CommPWork) + 31) & ~31);
    cb_tmp = ((MB_CommPWork *)native_data_main_020ec360.field_000c) ->parent_callback;
    MI_CpuClear16((void *)((u32)((MB_CommPWork *)native_data_main_020ec360.field_000c) + sizeof(MB_CommCommonWork)), sizeof(MB_CommPWork) - sizeof(MB_CommCommonWork));
    native_fn_02014324(cb_tmp);
    native_data_main_020ec360.field_000c->block_size_max = ((native_data_main_020ec360.field_0008->p_sendlen) -(6)) ;
    native_fn_02018e88(native_data_main_020ec360.field_0008->p_recvlen);
    native_fn_02018eb8(&((MB_CommPWork *)native_data_main_020ec360.field_000c) ->req_data_buf);
    for (i = 0; i < 15 ; i++) {
        ((MB_CommPWork *)native_data_main_020ec360.field_000c) ->p_comm_state[i] = MB_COMM_PSTATE_NONE;
        ((MB_CommPWork *)native_data_main_020ec360.field_000c) ->fileid_of_child[i] = -1;
    }
    ((MB_CommPWork *)native_data_main_020ec360.field_000c) ->file_num = 0;
    MI_CpuClear16(&((MB_CommPWork *)native_data_main_020ec360.field_000c) ->fileinfo[0], sizeof(((MB_CommPWork *)native_data_main_020ec360.field_000c) ->fileinfo));
    MI_CpuClear8(&((MB_CommPWork *)native_data_main_020ec360.field_000c) ->req2child[0], sizeof(((MB_CommPWork *)native_data_main_020ec360.field_000c) ->req2child));
    native_data_main_020ec360.field_0008->mode = 1 ;
    native_data_main_020ec360.field_0008->callback = native_data_main_02014578;
    native_data_main_020ec360.field_0008->callback_ptr = native_fn_02016e08;
    native_data_main_020ec360.field_0008->parentParam.parentMaxSize = native_data_main_020ec360.field_0008->p_sendlen;
    native_data_main_020ec360.field_0008->sendBufSize = (u16)((((((MBiParam *)(native_data_main_020ec360.field_0008))->parentParam.parentMaxSize) + 4 + (( 0) ? (2 * 16 + 4) + (2 + 4) : 0) + 31) & ~0x1f)) ;
    native_data_main_020ec360.field_0008->parentParam.childMaxSize = native_data_main_020ec360.field_0008->p_recvlen;
    native_data_main_020ec360.field_0008->recvBufSize = (u16)((((sizeof(WMMpRecvHeader) - sizeof(WMMpRecvData) + ((sizeof(WMMpRecvData) + (((MBiParam *)(native_data_main_020ec360.field_0008))->parentParam.childMaxSize) + 2 - 2 + 2 + (( 0) ? 2 + (2 + 2) : 0)) * ( 15)) + 31) & ~0x1f) * 2)) ;
    ((void)0) ;
    ((void)0) ;
    ((void)0) ;
    ((void)0) ;
    native_fn_020166d4();
    ret = native_fn_02018250();
    (void)native_fn_02008008(enabled);
    ((MB_CommPWork *)native_data_main_020ec360.field_000c) ->useWvrFlag = native_fn_0200a41c(PXI_FIFO_TAG_WVR, PXI_PROC_ARM7);
    return ret;
}
