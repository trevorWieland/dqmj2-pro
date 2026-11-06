#include "dependency000.h"
#include "dependency001.h"
#include "dependency002.h"
#include "dependency003.h"

void native_utility_child_arm7_wram_037f8aac(void)
{
    LPCMDIF_MAN pCmdIf = &((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->CmdIf;
    LPWORK_PARAM pWork = &((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Work;
    WlCmdReq *pReq;
    WlCmdCfm *pCfm;
    LPWLLIB_CMD_TBL pCmdTbl;
    u16 vCode, vCodeMax, err = 0;
    u16 currBusy = 0;
    if (pCmdIf->Busy) {
        ;
        return;
    }
    pCmdIf->pCmd = (u8 *)((u32)(*(LPHEAPBUF_MAN)&((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34)))->HeapMan.RequestCmd).Head) ;
    if ((u32)pCmdIf->pCmd == (u32)(-1) ) {
        return;
    }
    pReq = (WlCmdReq *)pCmdIf->pCmd;
    pCfm = (WlCmdCfm *)((u32)pReq + ((WlCmdReq*)pReq)->header.length*2 + 12+4) ;
    ;
    if (((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Config.DiagResult) {
        currBusy = 0;
        pCfm->header.length = 1;
        pCfm->resultCode = 0x06 ;
        goto end_of_command;
    }
    if (pReq->header.code != pCfm->header.code) {
        pCfm->resultCode = 0x0D ;
        goto end_of_command;
    }
    switch (pReq->header.code & 0xFF00 ) {
    case 0x0000 :
        ;
        currBusy = 0x01 ;
        pCmdTbl = (LPWLLIB_CMD_TBL)native_utility_child_arm7_data_027f82c0;
        vCode = pReq->header.code & 0x00FF ;
        vCodeMax = (sizeof(native_utility_child_arm7_data_027f82c0) / sizeof(WLLIB_CMD_TBL)) ;
        if (pCmdIf->Busy & 0x01 ) {
            err = 0x02 ;
        }
        else if (((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Work.STA < 0x20 ) {
            err = 0x01 ;
        }
        break;
    case 0x0100 :
        ;
        currBusy = 0x02 ;
        pCmdTbl = (LPWLLIB_CMD_TBL)native_utility_child_arm7_data_027f8238;
        vCode = pReq->header.code & 0x00FF ;
        vCodeMax = (sizeof(native_utility_child_arm7_data_027f8238) / sizeof(WLLIB_CMD_TBL)) ;
        if (((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Work.STA != 0x40 ) {
            err = 0x01 ;
        }
        break;
    case 0x0200 :
        vCode = pReq->header.code & 0x00FF ;
        if (vCode < ((0x0200 | 0x40) & 0x00FF )) {
            ;
            if (((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Work.STA < 0x10 ) {
                err = 0x01 ;
            }
            currBusy = 0x04 ;
            pCmdTbl = (LPWLLIB_CMD_TBL)native_utility_child_arm7_data_027f8428;
            vCodeMax = (sizeof(native_utility_child_arm7_data_027f8428) / sizeof(WLLIB_CMD_TBL)) ;
        } else if (vCode < ((0x0200 | 0x80) & 0x00FF )) {
            ;
            if (((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Work.STA != 0x40 ) {
                err = 0x01 ;
            }
            currBusy = 0x08 ;
            pCmdTbl = (LPWLLIB_CMD_TBL)native_utility_child_arm7_data_027f8290;
            vCode -= (0x40) ;
            vCodeMax = (sizeof(native_utility_child_arm7_data_027f8290) / sizeof(WLLIB_CMD_TBL)) ;
        } else if (vCode < ((0x0200 | 0xC0) & 0x00FF )) {
            ;
            if (((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Work.STA < 0x10 ) {
                err = 0x01 ;
            }
            currBusy = 0x10 ;
            pCmdTbl = (LPWLLIB_CMD_TBL)native_utility_child_arm7_data_027f8370;
            vCode -= (0x80) ;
            vCodeMax = (sizeof(native_utility_child_arm7_data_027f8370) / sizeof(WLLIB_CMD_TBL)) ;
        } else {
            ;
            if (((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Work.STA < 0x10 ) {
                err = 0x01 ;
            }
            currBusy = 0x20 ;
            pCmdTbl = (LPWLLIB_CMD_TBL)native_utility_child_arm7_data_027f8260;
            vCode -= (0xC0) ;
            vCodeMax = (sizeof(native_utility_child_arm7_data_027f8260) / sizeof(WLLIB_CMD_TBL)) ;
        }
        break;
    case 0x0300 :
        ;
        currBusy = 0x40 ;
        pCmdTbl = (LPWLLIB_CMD_TBL)native_utility_child_arm7_data_027f8318;
        vCode = pReq->header.code & 0x00FF ;
        vCodeMax = (sizeof(native_utility_child_arm7_data_027f8318) / sizeof(WLLIB_CMD_TBL)) ;
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
    native_utility_child_arm7_arm_037f8dc4(&((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->HeapMan.RequestCmd, pCmdIf->pCmd);
setup_next_command:
    if (((*(LPHEAPBUF_MAN)&((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34)))->HeapMan.RequestCmd).Count) != 0) {
        native_utility_child_arm7_arm_037f8558(2 , 11 );
    }
}
#include "dependency004.h"
