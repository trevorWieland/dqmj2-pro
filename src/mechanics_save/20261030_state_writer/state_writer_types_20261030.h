#ifndef PRIVATE_STATE_WRITER_TYPES_20261030
#define PRIVATE_STATE_WRITER_TYPES_20261030
#include "bulk_types_20261030.h"
typedef struct WriterState {
    u8 x;
    u8 y;
    s8 index;
} WriterState;
typedef struct WriterCache {
    u8 prefix[16];
    u32 currentUid;
} WriterCache;
extern WriterCache native_data_021d4bec;
extern void native_fn_020c0210(void);
extern s32 native_fn_020bf8c8(u32);
extern u32 native_fn_02069000(void);
extern void native_fn_020c06e8(s32, BulkRow *, s8 *, u32);
extern void native_fn_020c01f0(void);
#endif
