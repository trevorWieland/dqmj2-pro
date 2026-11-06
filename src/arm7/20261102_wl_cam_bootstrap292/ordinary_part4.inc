                            if ((u32)pTxDeAuthFrm != (0) ) {
                                pTxDeAuthFrm->FirmHeader.FrameId = 0x0001 ;
                                TxManCtrlFrame((LPTXFRM)pTxDeAuthFrm);
                                i++;
                                continue;
                            } else {
                                WSetStaState(0x20 );
                                WClearAids();
                                MLME_IssueDeAuthIndication(pCAM->macAdrs, 1 );
                            }
                        }
                    }
                }
                pCAM->state = 0x00 ;
                pWlMan->CamMan.Count--;
            }
            i++;
        }
        if (i >= cnt) {
            break;
        }
    }
}
void CAM_Delete(u16 camAdrs)
{
    DeleteTxFrames(camAdrs);
    ((LPWL_MAN)native_host_arm7_data_0380fff4) ->Config.pCAM[camAdrs].state = 0x00 ;
    ((LPWL_MAN)native_host_arm7_data_0380fff4) ->CamMan.Count--;
}
void InitializeCAM(void)
{
    LPCAM_ELEMENT pCAM = ((LPWL_MAN)native_host_arm7_data_0380fff4) ->Config.pCAM;
    u32 i, max;
    max = ((LPWL_MAN)native_host_arm7_data_0380fff4) ->Config.MaxStaNum;
    MI_CpuClear16((void *)(u32)pCAM, sizeof(CAM_ELEMENT) * max) ;
    MI_CpuClear16((void *)(u32)&((LPWL_MAN)native_host_arm7_data_0380fff4)->CamMan, sizeof(CAM_MAN)) ;
    pCAM[0].maxLifeTime = 0xFFFF;
    for (i = 1; i < max; i++) {
        pCAM[i].maxLifeTime = 0xFFFF ;
    }
    CAM_InitElement(0, (u16 *)BC_ADRS);
    CAM_SetStaState(0, 0x40 );
}
void InitCAM(void)
{
    LPCAM_ELEMENT pCAM = ((LPWL_MAN)native_host_arm7_data_0380fff4) ->Config.pCAM;
    LPCAM_MAN pCamMan = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->CamMan;
    u32 i, max;
    max = ((LPWL_MAN)native_host_arm7_data_0380fff4) ->Config.MaxStaNum;
    for (i = 1; i < max; i++) {
        MI_CpuClear16((void *)(u32)&pCAM[i], sizeof(CAM_ELEMENT) - 2) ;
    }
    pCamMan->Count = 1;
    pCamMan->PowerMgtMode = 0;
    pCamMan->PowerState = 1;
    pCamMan->NotClass3 = 0xFFFE;
    pCamMan->ConnectSta = 0;
    pCamMan->NotSetTIM = 0;
    pCamMan->UseAidMap = 1;
}
void CAM_InitElement(u32 camAdrs, u16 *pMacAdrs)
{
    LPCAM_ELEMENT pCAM = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->Config.pCAM[camAdrs];
    ;
    if (pCAM->state == 0x00 ) {
        ((LPWL_MAN)native_host_arm7_data_0380fff4) ->CamMan.Count++;
    }
    MI_CpuClear16((void *)(u32)pCAM, sizeof(CAM_ELEMENT) - 2) ;
    ((LPWL_MAN)native_host_arm7_data_0380fff4) ->CamMan.NotSetTIM &= ~(1 << camAdrs);
    CAM_SetPowerMgtMode(camAdrs, 0);
    CAM_SetAwake(camAdrs);
    WSetMacAdrs1(pCAM->macAdrs, pMacAdrs);
    pCAM->lastSeqCtrl = 0xFFFF;
    pCAM->supRateSet = ((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work.RateSet.Support;
    pCAM->lifeTime = pCAM->maxLifeTime;
    CAM_SetStaState(camAdrs, 0x20 );
}
