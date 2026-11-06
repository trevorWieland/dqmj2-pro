#include "../second/context.h"
typedef struct MeasureRecord {
    u8 reserved00[0x18];
    short field18;
    u8 field1a;
    u8 reserved1b[5];
    u8 data20[0x5a];
    u8 data7a[];
} MeasureRecord;
extern int native_fn_02062aa0(void);
extern int native_fn_02062ad0(void);
extern MeasureRecord *native_fn_02062a50(int);
extern MeasureRecord *native_fn_02062a88(int);
extern void native_fn_0207b460(int,u8,const void *,void *);
extern int native_fn_0207c2b8(const void *,const void *);
extern int native_fn_0207c18c(const void *,const void *);
extern int native_fn_0207c3d8(const void *,const void *);
extern int native_fn_0207c1b8(const void *,const void *);
