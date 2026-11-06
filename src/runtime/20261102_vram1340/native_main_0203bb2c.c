typedef unsigned long u32;
        typedef int BOOL;
typedef u32 NNSGfdPlttKey;
typedef NNSGfdPlttKey (*NNSGfdFuncAllocPlttVram)(u32 szByte, BOOL is4pltt, u32 opt);
typedef int (*NNSGfdFuncFreePlttVram)(NNSGfdPlttKey plttKey);
extern NNSGfdFuncAllocPlttVram native_data_main_020dd8b8;
extern NNSGfdFuncFreePlttVram native_data_main_020dd8bc;
void native_main_0203bb2c(u32 szByte, BOOL useAsDefault);
NNSGfdPlttKey native_data_main_0203bb78(u32 szByte, BOOL b4Pltt, u32 bAllocFromLo);
int native_data_main_0203bcb4(NNSGfdPlttKey plttKey);
void native_fn_0203bcf4(void);
typedef struct NNSGfdFramPlttVramManager {
    u32 loAddr;
    u32 hiAddr;
    u32 szTotal;
} NNSGfdFrmPlttVramManager;
extern NNSGfdFrmPlttVramManager native_data_main_020f5bcc;
void native_main_0203bb2c (u32 szByte, BOOL useAsDefault)
{
    ((void) 0) ;
    native_data_main_020f5bcc.szTotal = szByte;
    native_fn_0203bcf4();
    ((void) 0) ;
    if (useAsDefault) {
        native_data_main_020dd8b8 = native_data_main_0203bb78;
        native_data_main_020dd8bc = native_data_main_0203bcb4;
    }
}
NNSGfdPlttKey native_data_main_0203bb78 (u32 szByte, BOOL bPltt4, u32 allocFrom);
int native_data_main_0203bcb4 (NNSGfdPlttKey plttKey);
void native_fn_0203bcf4 (void);
