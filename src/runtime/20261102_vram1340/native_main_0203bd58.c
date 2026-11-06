typedef unsigned short int u16;
typedef unsigned long u32;
        typedef int BOOL;
extern const u16 (*ctrdgi_fl_maxtime);
typedef u32 NNSGfdTexKey;
typedef NNSGfdTexKey (*NNSGfdFuncAllocTexVram)(u32 szByte, BOOL is4x4comp, u32 opt);
typedef int (*NNSGfdFuncFreeTexVram)(NNSGfdTexKey key);
extern NNSGfdFuncAllocTexVram native_data_main_020dd8c0;
extern NNSGfdFuncFreeTexVram native_data_main_020dd8c4;
void native_fn_0203bd10(int idx1st, int idx2nd, int idx3rd, int idx4th, int idx5th);
void native_main_0203bd58(u16 numSlot, BOOL useAsDefault);
NNSGfdTexKey native_fn_0203be54(u32 szByte, BOOL is4x4comp, u32 opt);
int native_fn_0203bfc4(NNSGfdTexKey memKey);
void native_fn_0203bde0(void);
typedef struct NNSGfdFrmTexVramMnager {
    u16 numSlot;
} NNSGfdFrmTexVramMnager;
extern NNSGfdFrmTexVramMnager native_data_main_020f5bd8;
void native_fn_0203bd10 (int idx1st, int idx2nd, int idx3rd, int idx4th, int idx5th);
void native_main_0203bd58 (u16 numSlot, BOOL useAsDefault)
{
    ((void) 0) ;
    if ( numSlot <= 2 ) {
        native_fn_0203bd10(4, 3, 2, 0, 1);
    } else {
        native_fn_0203bd10(4, 3, 0, 2, 1);
    }
    native_data_main_020f5bd8.numSlot = numSlot;
    native_fn_0203bde0();
    if (useAsDefault) {
        native_data_main_020dd8c0 = native_fn_0203be54;
        native_data_main_020dd8c4 = native_fn_0203bfc4;
    }
}
void native_fn_0203bde0 (void);
NNSGfdTexKey native_fn_0203be54 (u32 szByte, BOOL is4x4comp, u32 opt);
int native_fn_0203bfc4 (NNSGfdTexKey texKey);
