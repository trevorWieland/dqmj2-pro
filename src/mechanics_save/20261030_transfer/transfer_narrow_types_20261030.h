#ifndef PRIVATE_TRANSFER_TYPES_20261030
#define PRIVATE_TRANSFER_TYPES_20261030
#include "../20261030_state_writer/state_writer_types_20261030.h"
typedef struct TransferRuntime {
    u8 prefix[16];
    s8 kind;
} TransferRuntime;
extern s8 native_data_021d4c0c[];
extern u8 native_data_020e2cf0[];
extern u32 native_fn_0206c0b0(void);
extern s32 native_fn_020c0f54(u32, u32);
extern u32 native_fn_020c1794(void);
extern u32 native_fn_020bf7e0(s32);
extern s32 native_fn_020bf928(u32);
extern u32 native_fn_0206da54(s8);
extern u32 native_fn_0205e7a8(s32, u32);
extern u32 native_fn_0206dac8(s8);
extern TransferRuntime *native_fn_020c8fa8(void);
extern u32 native_fn_ov000_02227ccc(void);
extern u32 native_fn_0206da90(s8);
extern u32 native_fn_0206db00(s8);
extern void native_fn_020bfa38(u32);
extern BulkRecord *native_fn_02062a10(u32);
extern u32 native_fn_0206c1a8(s32);
extern u32 native_fn_0206c18c(u32);
extern void native_fn_02069330(BulkRecord *, u32, u32, u32, u32, u32, u32, u32);
extern void native_fn_020bf990(u32, s32);
extern void native_fn_020bfa78(u32, u32);
extern void native_fn_020c1484(WriterState *, BulkSelection *, BulkRow *, s8 *);
#endif
