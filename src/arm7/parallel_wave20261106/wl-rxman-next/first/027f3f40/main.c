#include "context000.h"

#include "context001.h"

#include "context002.h"

#include "context003.h"

void native_host_arm7_main_027f3f40(void)
{
    LPHEAP_MAN pHeapMan = &((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->HeapMan;
    WlCounter *pCounter = &((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Counter;
    u32 mode = ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Work.Mode;
    LPRXFRM pFrm;
    LPRXPACKET pPacket;
    LPMAN_HEADER pDot11Header;
    u32 cam_adrs, type, subtype;
    pPacket = (LPRXPACKET)((u32)(*(LPHEAPBUF_MAN)&pHeapMan->RxManCtrl).Head) ;
    if ((u32)pPacket == (u32)(-1) ) {
        return;
    }
    pFrm = &pPacket->frame;
    pDot11Header = (LPMAN_HEADER)&pFrm->Dot11Header;
    if (pFrm->Dot11Header.Adrs1[0] & 0x0001) {
        pCounter->rx.multicast++;
    } else {
        pCounter->rx.unicast++;
    }
    pCounter->rx.fragment += (((pFrm->MacHeader.Rx.Status & (0x000F * (0x0001 << 4))) / (0x0001 << 4)) - 1);
    type = pDot11Header->FrameCtrl.Bit.Type;
    subtype = pDot11Header->FrameCtrl.Bit.SubType;
    cam_adrs = native_host_arm7_arm_027eb9b4(pDot11Header->SA);
    pFrm->FirmHeader.CamAdrs = cam_adrs;
    switch (cam_adrs) {
    case 255 :
        cam_adrs = 0;
        pFrm->FirmHeader.CamAdrs = 0;
        switch (mode) {
        case 1 :
            if (type == 0x00 ) {
                switch (subtype) {
                case 0x0B :
                    native_host_arm7_arm_027f35cc((LPAUTH_FRAME)pFrm);
                    break;
                case 0x04 :
                    native_host_arm7_arm_027f3148((LPPRBREQ_FRAME)pFrm);
                    break;
                case 0x00 :
                    native_host_arm7_arm_027f2f78((LPASSREQ_FRAME)pFrm);
                    break;
                }
            }
        }
        break;
    default:
        native_host_arm7_arm_027ebe98(cam_adrs);
        native_host_arm7_arm_027ebd38(cam_adrs, LoadLow(&pFrm->MacHeader.Rx.rsv_RSSI));
        if (type == 0x00 ) {
            u32 seqctrl = pFrm->Dot11Header.SeqCtrl.Data;
            if (seqctrl == native_host_arm7_arm_027ec08c(cam_adrs)) {
                ;
                pCounter->rx.duplicateErr++;
                break;
            }
            native_host_arm7_arm_027ebe58(cam_adrs, seqctrl);
        }
        switch (mode) {
        case 1 :
        {
            native_host_arm7_arm_027ebd58(cam_adrs, pDot11Header->FrameCtrl.Bit.PowerMan);
        }
            if (type == 0x00 ) {
                switch (subtype) {
                case 0x08 :
                    native_host_arm7_arm_027f284c((LPBEACON_FRAME)pFrm);
                    break;
                case 0x00 :
                    native_host_arm7_arm_027f2f78((LPASSREQ_FRAME)pFrm);
                    break;
                case 0x02 :
                    RxReAssReqFrame((LPREASSREQ_FRAME)pFrm);
                    break;
                case 0x04 :
                    native_host_arm7_arm_027f3148((LPPRBREQ_FRAME)pFrm);
                    break;
                case 0x05 :
                    native_host_arm7_arm_027f31fc((LPPRBRES_FRAME)pFrm, 0 );
                    break;
                case 0x0A :
                    native_host_arm7_arm_027f2e98((LPDISASS_FRAME)pFrm);
                    break;
                case 0x0B :
                    native_host_arm7_arm_027f35cc((LPAUTH_FRAME)pFrm);
                    break;
                case 0x0C :
                    native_host_arm7_arm_027f3b6c((LPDEAUTH_FRAME)pFrm);
                    break;
                default:
                    ;
                }
            } else if (type == 0x01 ) {
                switch (subtype) {
                case 0x0A :
                    RxPsPollFrame((LPPSPOLL_FRAME)pFrm);
                    break;
                default:
                    ;
                }
            } else {
                ;
            }
            break;
        case 2 :
        case 3 :
            if (type == 0x00 ) {
                switch (subtype) {
                case 0x08 :
                    native_host_arm7_arm_027f284c((LPBEACON_FRAME)pFrm);
                    break;
                case 0x01 :
                    RxAssResFrame((LPASSRES_FRAME)pFrm);
                    break;
                case 0x03 :
                    RxReAssResFrame((LPREASSRES_FRAME)pFrm);
                    break;
                case 0x04 :
                    break;
                case 0x05 :
                    native_host_arm7_arm_027f31fc((LPPRBRES_FRAME)pFrm, 0 );
                    break;
                case 0x0A :
                    native_host_arm7_arm_027f2e98((LPDISASS_FRAME)pFrm);
                    break;
                case 0x0B :
                    native_host_arm7_arm_027f35cc((LPAUTH_FRAME)pFrm);
                    break;
                case 0x0C :
                    native_host_arm7_arm_027f3b6c((LPDEAUTH_FRAME)pFrm);
                    break;
                default:
                    ;
                }
            } else if (type == 0x01 ) {
                switch (subtype) {
                case 0x0E :
                case 0x0F :
                    RxCfEndFrame((LPCFEND_FRAME)pFrm);
                    break;
                default:
                    ;
                }
            } else {
                ;
            }
            break;
        }
    }
    native_host_arm7_arm_037f8908(&pHeapMan->RxManCtrl, pPacket);
    if (((*(LPHEAPBUF_MAN)&pHeapMan->RxManCtrl).Count) != 0) {
        native_host_arm7_arm_037f8598(1 , 7 );
    }
}
