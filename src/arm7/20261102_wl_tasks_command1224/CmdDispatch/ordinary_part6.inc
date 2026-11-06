            pCmdTbl = (LPWLLIB_CMD_TBL)native_host_arm7_table_wlibcmdtbl_paramset2_027f7624;
            vCode -= (0x40) ;
            vCodeMax = (sizeof(native_host_arm7_table_wlibcmdtbl_paramset2_027f7624) / sizeof(WLLIB_CMD_TBL)) ;
        } else if (vCode < ((0x0200 | 0xC0) & 0x00FF )) {
            ;
            if (((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work.STA < 0x10 ) {
                err = 0x01 ;
            }
            currBusy = 0x10 ;
            pCmdTbl = (LPWLLIB_CMD_TBL)native_host_arm7_table_wlibcmdtbl_paramget_027f7704;
            vCode -= (0x80) ;
            vCodeMax = (sizeof(native_host_arm7_table_wlibcmdtbl_paramget_027f7704) / sizeof(WLLIB_CMD_TBL)) ;
        } else {
            ;
            if (((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work.STA < 0x10 ) {
                err = 0x01 ;
            }
            currBusy = 0x20 ;
            pCmdTbl = (LPWLLIB_CMD_TBL)native_host_arm7_table_wlibcmdtbl_paramget2_027f75f4;
            vCode -= (0xC0) ;
            vCodeMax = (sizeof(native_host_arm7_table_wlibcmdtbl_paramget2_027f75f4) / sizeof(WLLIB_CMD_TBL)) ;
        }
        break;
    case 0x0300 :
        ;
        currBusy = 0x40 ;
        pCmdTbl = (LPWLLIB_CMD_TBL)native_host_arm7_table_wlibcmdtbl_dev_027f76ac;
        vCode = pReq->header.code & 0x00FF ;
        vCodeMax = (sizeof(native_host_arm7_table_wlibcmdtbl_dev_027f76ac) / sizeof(WLLIB_CMD_TBL)) ;
        break;
    default:
        ;
        vCode = 1;
        vCodeMax = 0;
    }
    if (vCode > vCodeMax) {
        ;
        err = 0x03 ;
    }
    else if ((pReq->header.length < pCmdTbl[vCode].RequestMinLength) || (pCfm->header.length < pCmdTbl[vCode].ConfirmMinLength)) {
        ;
        err = 0x04 ;
    }
    if (err) {
        ;
        pCfm->header.length = 1;
        pCfm->resultCode = err;
        goto end_of_command;
    }
    pCmdIf->Busy |= currBusy;
    pCfm->resultCode = (*pCmdTbl[vCode].pCmdFunc)(pReq, pCfm);
    switch (pCfm->resultCode) {
    case 0x80 :
        return;
    case 0x81 :
        pCmdIf->Busy &= ~currBusy;
        goto setup_next_command;
    }
end_of_command:
    pCmdIf->Busy &= ~currBusy;
    SendMessageToWmDirect(&((LPWL_MAN)native_host_arm7_data_0380fff4) ->HeapMan.RequestCmd, pCmdIf->pCmd);
setup_next_command:
    if (((*(LPHEAPBUF_MAN)&((LPWL_MAN)native_host_arm7_data_0380fff4)->HeapMan.RequestCmd).Count) != 0) {
        AddTask(2 , 11 );
    }
}


void SendMessageToWmDirect(LPHEAPBUF_MAN pBufMan, void *pMsg)
{
    ;
    if (((*(LPHEAPBUF_MAN)&((LPWL_MAN)native_host_arm7_data_0380fff4)->HeapMan.ToWM).Count) != 0) {
        MoveHeapBuf(pBufMan, &((LPWL_MAN)native_host_arm7_data_0380fff4) ->HeapMan.ToWM, pMsg);
        AddTask(2 , 19 );
    } else {
        if (OS_SendMessage(((LPWL_MAN)native_host_arm7_data_0380fff4) ->pSendMsgQueue, pMsg, 0 )) {
            DeleteHeapBuf(pBufMan, pMsg);
        } else {
            ;
            MoveHeapBuf(pBufMan, &((LPWL_MAN)native_host_arm7_data_0380fff4) ->HeapMan.ToWM, pMsg);
        }
    }
}


void SendMessageToWmTask(void)
{
    u16 *pMsg = (u16 *)((u32)(*(LPHEAPBUF_MAN)&((LPWL_MAN)native_host_arm7_data_0380fff4)->HeapMan.ToWM).Head) ;
    while ((u32)pMsg != (u32)(-1) ) {
        if (OS_SendMessage(((LPWL_MAN)native_host_arm7_data_0380fff4) ->pSendMsgQueue, pMsg, 0 )) {
            DeleteHeapBuf(&((LPWL_MAN)native_host_arm7_data_0380fff4) ->HeapMan.ToWM, (LPHEAPBUF_HEADER)pMsg);
            pMsg = (u16 *)((u32)(*(LPHEAPBUF_MAN)&((LPWL_MAN)native_host_arm7_data_0380fff4)->HeapMan.ToWM).Head) ;
        } else {
            break;
        }
    }
}
