typedef unsigned short int u16;
typedef unsigned long u32;
        typedef int BOOL;
extern const u16 (*ctrdgi_fl_maxtime);
typedef struct NNSGfdFrmTexVramState {
    u32 address[10];
} NNSGfdFrmTexVramState;
void native_main_0203bfcc(NNSGfdFrmTexVramState * pState);
typedef struct NNSGfdFrmTexRegionState {
    u32 head;
    u32 tail;
    BOOL bActive;
    const BOOL bHalfSize;
    const u16 index;
    const u16 pad16_;
    const u32 baseAddress;
} NNSGfdFrmTexRegionState;
extern NNSGfdFrmTexRegionState native_data_main_020dd840[5 ];
void native_main_0203bfcc (NNSGfdFrmTexVramState * pState)
{
    int i;
    ((void) 0) ;
    ((void) 0) ;
    for (i = 0; i < 5 ; i++)
    {
        pState->address[i * 2 + 0] = native_data_main_020dd840[i].head;
        pState->address[i * 2 + 1] = native_data_main_020dd840[i].tail;
    }
}
