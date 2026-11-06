#include "context_00.h"
void native_main_020176d0 (void * arg)
{
    WMCallback * buf = (WMCallback *)arg;
    MBiParam * const p_param = native_data_main_020ec360.field_0008;
    int errcode;
    switch (buf->apiid) {
    case WM_APIID_INITIALIZE:
    {
        if (buf->errcode != WM_ERRCODE_SUCCESS) {
            p_param->callback(256 , arg);
            return;
        }
        p_param->callback(21 , arg);
        errcode = native_fn_02014200(native_main_020176d0, native_data_main_020dce94.field_0006, native_data_main_020dce94.field_0002, native_data_main_020dce94.field_0000, native_data_main_020dce94.field_0004);
        native_fn_020189b0(WM_APIID_SET_LIFETIME, errcode);
    }
    break;
    case WM_APIID_SET_LIFETIME:
    {
        if (buf->errcode != WM_ERRCODE_SUCCESS) {
            p_param->callback(256 , arg);
            return;
        }
        native_data_main_020ec360.field_0020.scanBuf = &p_param->parentInfoBuf;
        if (native_data_main_020ec360.field_0020.channel == 0)
            native_data_main_020ec360.field_0020.channel = 1;
        if (native_data_main_020ec360.field_0020.maxChannelTime == 0) {
            native_data_main_020ec360.field_0020.maxChannelTime = 200;
        }
        native_data_main_020ec360.field_0020.bssid[0] = 0xff;
        native_data_main_020ec360.field_0020.bssid[1] = 0xff;
        native_data_main_020ec360.field_0020.bssid[2] = 0xff;
        native_data_main_020ec360.field_0020.bssid[3] = 0xff;
        native_data_main_020ec360.field_0020.bssid[4] = 0xff;
        native_data_main_020ec360.field_0020.bssid[5] = 0xff;
        p_param->scanning_flag = 1 ;
        p_param->scan_channel_flag = 1 ;
        errcode = native_fn_02012a3c(native_main_020176d0, &native_data_main_020ec360.field_0020);
        native_fn_020189b0(WM_APIID_START_SCAN, errcode);
    }
    break;
    case WM_APIID_START_SCAN:
    {
        WMstartScanCallback * callback = (WMstartScanCallback *)arg;
        if (callback->errcode != WM_ERRCODE_SUCCESS) {
            p_param->callback(256 , arg);
            return;
        }
        switch (callback->state) {
        case WM_STATECODE_SCAN_START:
            break;
        case WM_STATECODE_PARENT_FOUND:
        {
            WMstartScanCallback * buf = (WMstartScanCallback *)arg;
            ParentInfo * p = &p_param->parent_info[0];
            int i;
            for (i = 0; i < p_param->found_parent_count; ++i) {
                if (WM_IsBssidEqual(buf->macAddress, p[i].scan_data.macAddress)) {
                    p[i].scan_data.gameInfoLength = buf->gameInfoLength;
                    p[i].scan_data.gameInfo = buf->gameInfo;
                    native_fn_020072d0(p_param->parent_info[i].parentInfo, 192 );
                    native_fn_0200854c(native_data_main_020ec360.field_0000, &p_param->parentInfoBuf, p_param->parent_info[i].parentInfo, 192 );
                    p_param->last_found_parent_no = i;
                    goto scan_end;
                }
            }
            if (i < 16 ) {
                p_param->found_parent_count = (u16)(i + 1);
                MI_CpuCopy16(buf, &p[i].scan_data, sizeof(p[i].scan_data));
                native_fn_020072d0(p_param->parent_info[i].parentInfo, 192 );
                native_fn_0200854c(native_data_main_020ec360.field_0000, &p_param->parentInfoBuf, p_param->parent_info[i].parentInfo, 192 );
                p_param->last_found_parent_no = i;
            }
        }
scan_end:
            p_param->callback(4 , arg);
            if (!p_param->scanning_flag) {
                return;
            }
            if (p_param->scan_channel_flag) {
                if (0 == native_fn_02016ca4(&native_data_main_020ec360.field_0020)) {
                    (void)native_fn_02018570();
                }
            }
            errcode = native_fn_02012a3c(native_main_020176d0, &native_data_main_020ec360.field_0020);
            native_fn_020189b0(WM_APIID_START_SCAN, errcode);
            break;
        case WM_STATECODE_PARENT_NOT_FOUND:
            p_param->callback(5 , arg);
            if (!p_param->scanning_flag) {
                return;
            }
            if (p_param->scan_channel_flag) {
                if (0 == native_fn_02016ca4(&native_data_main_020ec360.field_0020)) {
                    (void)native_fn_02018570();
                }
            }
            errcode = native_fn_02012a3c(native_main_020176d0, &native_data_main_020ec360.field_0020);
            native_fn_020189b0(WM_APIID_START_SCAN, errcode);
            break;
        default:
            p_param->callback(256 , arg);
            break;
        }
    }
    break;
    case WM_APIID_END_SCAN:
    {
        if (buf->errcode != WM_ERRCODE_SUCCESS) {
            p_param->callback(256 , arg);
            return;
        }
        errcode = WM_StartConnect(native_main_020176d0, p_param->pInfo, ((void *)0) );
        native_fn_020189b0(WM_APIID_START_CONNECT, errcode);
    }
    break;
    case WM_APIID_START_CONNECT:
    {
        WMstartConnectCallback * callback = (WMstartConnectCallback *)arg;
        if (callback->errcode != WM_ERRCODE_SUCCESS) {
            p_param->found_parent_count = 0;
            p_param->callback(11 , arg);
            return;
        }
        switch (callback->state) {
        case WM_STATECODE_CONNECT_START:
            p_param->child_bitmap = 0;
            p_param->mpStarted = 1;
            break;
        case WM_STATECODE_CONNECTED:
            p_param->my_aid = (u16)callback->aid;
            p_param->callback(6 , arg);
            p_param->child_bitmap = 1;
            errcode = native_fn_02011f58(WM_PORT_BT, native_fn_02017660, ((void *)0) );
            if (errcode != WM_ERRCODE_SUCCESS) {
                break;
            }
            errcode = native_fn_02012fdc(native_main_020176d0, (u16 *)p_param->recvBuf, p_param->recvBufSize, (u16 *)p_param->sendBuf, p_param->sendBufSize, (u16)(p_param->contSend ? 0 : 1), 0,
                                   0 , 0 , 1,
                                   1
                                   );
            native_fn_020189b0(WM_APIID_START_MP, errcode);
            break;
        case WM_STATECODE_DISCONNECTED:
            p_param->callback(10 , arg);
            p_param->child_bitmap = 0;
            p_param->mpStarted = 0;
            break;
        case WM_STATECODE_DISCONNECTED_FROM_MYSELF:
            break;
        default:
            p_param->callback(256 , arg);
            break;
        }
    }
    break;
    case WM_APIID_START_MP:
    {
        WMstartMPCallback * callback = (WMstartMPCallback *)arg;
        switch (callback->state) {
        case WM_STATECODE_MP_START:
            p_param->mpStarted = 1;
            {
                if (native_fn_02016d14()) {
                    p_param->callback(25 , ((void *)0) );
                }
            }
            break;
        case WM_STATECODE_MP_IND:
            if (callback->errcode == WM_ERRCODE_INVALID_POLLBITMAP) {
            } else {
            }
            break;
        case WM_STATECODE_MPACK_IND:
        {
        }
        break;
        default:
            p_param->callback(256 , arg);
            break;
        }
    }
    break;
    case WM_APIID_SET_MP_DATA:
    {
        p_param->mpBusy = 0;
        if (buf->errcode == WM_ERRCODE_SUCCESS) {
            p_param->callback(8 , arg);
        } else if (buf->errcode == WM_ERRCODE_TIMEOUT)   {
            p_param->callback(41 , arg);
        } else {
            p_param->callback(18 , arg);
        }
        if (native_data_main_020ec360.field_0008->endReq == 0) {
            p_param->callback(25 , ((void *)0) );
        }
    }
    break;
    case WM_APIID_RESET:
    {
        if (buf->errcode != WM_ERRCODE_SUCCESS) {
            p_param->endReq = 0;
            p_param->callback(256 , arg);
            return;
        }
        native_data_main_020ec360.field_0008->child_bitmap = 0;
        native_data_main_020ec360.field_0008->mpStarted = 0;
        errcode = native_fn_02012824(native_main_020176d0);
        native_fn_020189b0(WM_APIID_END, errcode);
    }
    break;
    case WM_APIID_END:
    {
        if (buf->errcode != WM_ERRCODE_SUCCESS) {
            p_param->endReq = 0;
            p_param->callback(256 , arg);
            return;
        }
        native_fn_02016dc4(arg);
    }
    break;
    case WM_APIID_START_KS:
    {
        if (native_fn_02016d14()) {
            p_param->callback(25 , ((void *)0) );
        }
    }
    break;
    case WM_APIID_INDICATION:
    {
        WMindCallback * cb = (WMindCallback *)arg;
        switch (cb->state) {
        case WM_STATECODE_FIFO_ERROR:
            native_fn_02008430() ;
            break;
        case WM_STATECODE_INFORMATION:
            break;
        }
    }
    break;
    default:
        p_param->callback(256 , arg);
        break;
    }
}
