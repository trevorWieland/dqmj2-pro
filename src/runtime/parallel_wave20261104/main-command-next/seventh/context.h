#include "../third/context.h"
typedef struct Matrix33 { int value[9]; } Matrix33;
typedef struct MatrixRecord { u8 reserved00[9]; u8 state09; u8 reserved0a[0x7e]; u32 slot88[3]; Matrix33 matrix94; } MatrixRecord;
extern int native_fn_02028158(int);
extern void native_fn_02000ce8(Matrix33 *);
extern void native_fn_020280a0(Matrix33 *,int);
extern void native_fn_02028044(Matrix33 *,int);
extern void native_fn_02027fe8(Matrix33 *,int);
extern void native_fn_02000e1c(const Matrix33 *,const Matrix33 *,Matrix33 *);
