typedef unsigned short int u16;
typedef unsigned long u32;
        typedef int BOOL;
extern const u16 (*ctrdgi_fl_maxtime);
typedef enum NNS_GFD_DST_TYPE {
    NNS_GFD_DST_3D_TEX_VRAM = 0,
    NNS_GFD_DST_3D_TEX_PLTT,
    NNS_GFD_DST_3D_CLRIMG_COLOR,
    NNS_GFD_DST_3D_CLRIMG_DEPTH,
    NNS_GFD_DST_2D_BG0_CHAR_MAIN,
    NNS_GFD_DST_2D_BG1_CHAR_MAIN,
    NNS_GFD_DST_2D_BG2_CHAR_MAIN,
    NNS_GFD_DST_2D_BG3_CHAR_MAIN,
    NNS_GFD_DST_2D_BG0_SCR_MAIN,
    NNS_GFD_DST_2D_BG1_SCR_MAIN,
    NNS_GFD_DST_2D_BG2_SCR_MAIN,
    NNS_GFD_DST_2D_BG3_SCR_MAIN,
    NNS_GFD_DST_2D_BG2_BMP_MAIN,
    NNS_GFD_DST_2D_BG3_BMP_MAIN,
    NNS_GFD_DST_2D_OBJ_PLTT_MAIN,
    NNS_GFD_DST_2D_BG_PLTT_MAIN,
    NNS_GFD_DST_2D_OBJ_EXTPLTT_MAIN,
    NNS_GFD_DST_2D_BG_EXTPLTT_MAIN,
    NNS_GFD_DST_2D_OBJ_OAM_MAIN,
    NNS_GFD_DST_2D_OBJ_CHAR_MAIN,
    NNS_GFD_DST_2D_BG0_CHAR_SUB,
    NNS_GFD_DST_2D_BG1_CHAR_SUB,
    NNS_GFD_DST_2D_BG2_CHAR_SUB,
    NNS_GFD_DST_2D_BG3_CHAR_SUB,
    NNS_GFD_DST_2D_BG0_SCR_SUB,
    NNS_GFD_DST_2D_BG1_SCR_SUB,
    NNS_GFD_DST_2D_BG2_SCR_SUB,
    NNS_GFD_DST_2D_BG3_SCR_SUB,
    NNS_GFD_DST_2D_BG2_BMP_SUB,
    NNS_GFD_DST_2D_BG3_BMP_SUB,
    NNS_GFD_DST_2D_OBJ_PLTT_SUB,
    NNS_GFD_DST_2D_BG_PLTT_SUB,
    NNS_GFD_DST_2D_OBJ_EXTPLTT_SUB,
    NNS_GFD_DST_2D_BG_EXTPLTT_SUB,
    NNS_GFD_DST_2D_OBJ_OAM_SUB,
    NNS_GFD_DST_2D_OBJ_CHAR_SUB,
    NNS_GFD_DST_MAX
} NNS_GFD_DST_TYPE;
typedef struct NNSGfdVramTransferTask {
    NNS_GFD_DST_TYPE type;
    void * pSrc;
    u32 dstAddr;
    u32 szByte;
} NNSGfdVramTransferTask;
typedef struct NNSGfdVramTransferTaskQueue {
    NNSGfdVramTransferTask * pTaskArray;
    u32 lengthOfArray;
    u16 idxFront;
    u16 idxRear;
    u16 numTasks;
    u16 pad16_;
    u32 totalSize;
} NNSGfdVramTransferTaskQueue;
typedef struct NNSGfdVramTransferManager {
    NNSGfdVramTransferTaskQueue taskQueue;
} NNSGfdVramTransferManager;
BOOL native_fn_0203c3a0(NNSGfdVramTransferTaskQueue * pQueue);
NNSGfdVramTransferTask * native_fn_0203c3ec(NNSGfdVramTransferTaskQueue * pQueue);
BOOL native_main_0203c4bc(NNS_GFD_DST_TYPE type, u32 dstAddr, void * pSrc, u32 szByte);
extern NNSGfdVramTransferManager native_data_main_020f5bdc;
BOOL native_fn_0203c08c (const NNSGfdVramTransferTaskQueue * pQueue);
BOOL native_fn_0203c3a0 (NNSGfdVramTransferTaskQueue * pQueue);
NNSGfdVramTransferTask * native_fn_0203c3ec (NNSGfdVramTransferTaskQueue * pQueue);
BOOL native_main_0203c4bc (NNS_GFD_DST_TYPE type, u32 dstAddr, void * pSrc, u32 szByte)
{
    NNSGfdVramTransferManager * pMan = &native_data_main_020f5bdc;
    if ( !native_fn_0203c08c(&pMan->taskQueue)) {
        NNSGfdVramTransferTask * pTask =
            native_fn_0203c3ec(&pMan->taskQueue);
        pTask->type = type;
        pTask->pSrc = pSrc;
        pTask->dstAddr = dstAddr;
        pTask->szByte = szByte;
        (void)native_fn_0203c3a0(&pMan->taskQueue);
        pMan->taskQueue.totalSize += pTask->szByte;
        return 1 ;
    }
    return 0 ;
}
