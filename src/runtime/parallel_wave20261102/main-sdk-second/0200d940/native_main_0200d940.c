#include "context_00.h"
void native_main_0200d940 (PXIFifoTag tag, u32 data, BOOL err)
{
    u16 result;
    u16 command;
    result = (u16)(data & 0x0000ffff );
    command = (u16)((result & 0x7f00) >> 8);
    if (err) {
        TPi_ErrorAtPxi((TPRequestCommand)command);
        return;
    }
    if (command == 0x0010 ) {
        native_data_main_020e53d0.field_0004.index++;
        if (native_data_main_020e53d0.field_0004.index >= native_data_main_020e53d0.field_0004.bufSize) {
            native_data_main_020e53d0.field_0004.index = 0;
        }
        TPi_CopyTpFromSystemWork(&native_data_main_020e53d0.field_0004.samplingBufs[native_data_main_020e53d0.field_0004.index]);
        if (native_data_main_020e53d0.field_0004.callback) {
            (native_data_main_020e53d0.field_0004.callback)((TPRequestCommand)command, TP_RESULT_SUCCESS, (u8)native_data_main_020e53d0.field_0004.index);
        }
        return;
    }
    if (!(data & 0x01000000 )) {
        return;
    }
    ((void) 0) ;
    switch ((u8)(result & 0x00ff)) {
    case 0x0000 :
        switch (command) {
        case 0x0000 :
            TPi_CopyTpFromSystemWork(&native_data_main_020e53d0.field_0004.buf);
            native_data_main_020e53d0.field_0004.state = TP_STATE_READY;
            break;
        case 0x0001 :
            native_data_main_020e53d0.field_0004.state = TP_STATE_AUTO_SAMPLING;
            break;
        case 0x0002 :
            native_data_main_020e53d0.field_0004.state = TP_STATE_READY;
            break;
        }
        native_data_main_020e53d0.field_0004.command_flg &= ~(1 << command);
        if (native_data_main_020e53d0.field_0004.callback) {
            (native_data_main_020e53d0.field_0004.callback)((TPRequestCommand)command, TP_RESULT_SUCCESS, 0);
        }
        break;
    case 0x0004 :
        result = TP_RESULT_EXCLUSIVE;
        goto common;
    case 0x0002 :
        result = TP_RESULT_INVALID_PARAMETER;
        goto common;
    case 0x0003 :
        result = TP_RESULT_ILLEGAL_STATUS;
common:
        native_data_main_020e53d0.field_0004.err_flg |= (1 << command);
        native_data_main_020e53d0.field_0004.command_flg &= ~(1 << command);
        if (native_data_main_020e53d0.field_0004.callback) {
            (native_data_main_020e53d0.field_0004.callback)((TPRequestCommand)command, (TPRequestResult)(result & 0xff), 0);
        }
        break;
    case 0x0001 :
    default:
        native_fn_02008430() ;
        return;
    }
}
