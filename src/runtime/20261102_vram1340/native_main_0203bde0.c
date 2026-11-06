typedef unsigned short int u16;
typedef unsigned long u32;
        typedef int BOOL;
extern const u16 (*ctrdgi_fl_maxtime);
void native_main_0203bde0(void);
typedef struct NNSGfdFrmTexRegionState {
    u32 head;
    u32 tail;
    BOOL bActive;
    const BOOL bHalfSize;
    const u16 index;
    const u16 pad16_;
    const u32 baseAddress;
} NNSGfdFrmTexRegionState;
typedef struct NNSGfdFrmTexVramMnager {
    u16 numSlot;
} NNSGfdFrmTexVramMnager;
extern NNSGfdFrmTexVramMnager native_data_main_020f5bd8;
extern NNSGfdFrmTexRegionState native_data_main_020dd840[5 ];
static inline void ResetRegionNormal_ (NNSGfdFrmTexRegionState * pRegion)
{
    ((void) 0) ;
    pRegion->head = 0x0;
    pRegion->tail = 0x20000 ;
}
static inline void ResetRegionHalf_ (NNSGfdFrmTexRegionState * pRegion)
{
    ((void) 0) ;
    pRegion->head = 0x0;
    pRegion->tail = 0x20000 / 2;
}
void native_main_0203bde0 (void)
{
    int i;
    u16 numSlot = native_data_main_020f5bd8.numSlot;
    const numRegion = (numSlot > 1) ? numSlot + 1 : numSlot + 0;
    ((void) 0) ;
    for (i = 0; i < 5 ; i++) {
        if ( i < numRegion ) {
            native_data_main_020dd840[i].bActive = 1 ;
        } else {
            native_data_main_020dd840[i].bActive = 0 ;
        }
        if ( native_data_main_020dd840[i].bHalfSize ) {
            ResetRegionHalf_(&native_data_main_020dd840[i]);
        } else {
            ResetRegionNormal_(&native_data_main_020dd840[i]);
        }
    }
}
