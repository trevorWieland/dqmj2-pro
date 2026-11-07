#include "context.h"
void native_main_0209e0fc (u8 numEntry,
                                 const char * addFilter,
                                 DWCMatchedSCCallback matchedCallback,
                                 void * matchedParam,
                                 DWCEvalPlayerCallback evalCallback,
                                 void * evalParam)
{
    char filter[MAX_FILTER_LEN];
    u32 addFilterLenMax;
    SBError sbError;

    if (stpAddFilter) {
        DWC_Free(DWC_ALLOCTYPE_BASE, stpAddFilter, 0);
        stpAddFilter = NULL;
    }

    if (addFilter) {
        addFilterLenMax = MAX_FILTER_LEN - DWCi_GetDefaultMatchFilter(filter, 0xffffffff, DWC_MAX_CONNECTIONS, DWC_MATCH_TYPE_SC_CL) - strlen(native_data_020e0198);

        SDK_ASSERT(strlen(addFilter) < addFilterLenMax);

        stpAddFilter = DWC_Alloc(DWC_ALLOCTYPE_BASE, addFilterLenMax);
        if (!stpAddFilter) {
            DWCi_StopMatching(DWC_ERROR_FATAL, DWC_ECODE_SEQ_MATCH + DWC_ECODE_TYPE_ALLOC);
            return;
        }

        MI_CpuCopy8(addFilter, stpAddFilter, addFilterLenMax);
        stpAddFilter[addFilterLenMax - 1] = '\0';
    }

    DWCi_SetMatchCommonParam(DWC_MATCH_TYPE_ANYBODY,
                             numEntry, matchedCallback, matchedParam);

    DWCi_GetMatchCnt()->evalCallback = evalCallback;
    DWCi_GetMatchCnt()->evalParam = evalParam;

    DWCi_SetMatchStatus(DWC_MATCH_STATE_CL_SEARCH_OWN);

    if (!DWCi_GetMatchCnt()->sbObj)
        DWCi_GetMatchCnt()->sbObj = ServerBrowserNew(DWCi_GetMatchCnt()->gameName,
                                                     DWCi_GetMatchCnt()->gameName,
                                                     DWCi_GetMatchCnt()->secretKey, 0, 20,
                                                     QVERSION_QR2, SBFalse,
                                                     DWCi_SBCallback, NULL);
    if (!DWCi_GetMatchCnt()->sbObj) {
        if (DWCi_HandleSBError(sbe_allocerror)) return;
    }

    (void)DWCi_SetGPStatus(DWC_STATUS_MATCH_ANYBODY, native_data_020e01a0, NULL);

    sbError = DWCi_SBUpdateAsync(DWCi_GetMatchCnt()->profileID);
    if (DWCi_HandleSBError(sbError)) return;

#ifdef DWC_QR2_ALIVE_DURING_MATCHING
    if (DWCi_GetMatchCnt()->qr2Obj == NULL) {

        DWCi_QR2Startup(DWCi_GetMatchCnt()->profileID);
    }
#else
    qr2_send_statechanged(DWCi_GetMatchCnt()->qr2Obj);
#endif

    DWCi_InitOptMinCompParam(FALSE);
}
