#include "../../main-runtime-tail/context.h"
typedef unsigned short u16;
typedef struct NativeVec3 { int x; int y; int z; } NativeVec3;
typedef struct CommandContext {
    u8 reserved[3];
    u8 bank;
    u32 reservedWords[3];
    float parameters[16];
    u8 padding[0x420];
    CommandRecord records[];
} CommandContext;
typedef struct TargetRecord {
    u8 reserved00[9];
    u8 state09;
    u8 reserved0a[0x66];
    u32 slot70[3];
    u8 reserved7c[0x0c];
    u32 slot88[3];
    u8 reserved94[0x24];
} TargetRecord;
extern int native_fn_0205f2d8(int);
extern int native_fn_0205f45c(int);
extern void native_fn_0205e814(int,int,int);
extern void native_fn_0205f7e0(int,int,int);
extern void native_fn_0205f6a0(int,int,int);
extern void native_fn_ov000_021e582c(u16,const NativeVec3 *,const NativeVec3 *,const NativeVec3 *,const NativeVec3 *,u8);
extern void native_fn_ov000_021e58a0(u16);
extern int native_fn_ov000_0221221c(int,int,int);
extern void native_fn_ov000_022124e8(int,int,int);
extern int native_fn_ov000_0221225c(int,int,int);
extern void native_fn_ov000_02212518(int,int,int);
extern void native_fn_ov000_0221229c(int,int,int);
extern void native_fn_ov000_02211188(int,const NativeVec3 *,const NativeVec3 *,int);
extern void native_fn_ov000_02212480(int,int,int);
extern void native_fn_ov000_022124b4(int,int,int);
extern void native_fn_ov000_022122dc(int,int,const NativeVec3 *,int);
extern void native_fn_ov000_021e77f8(int,NativeVec3 *);
extern int native_fn_ov000_021e784c(int);
extern TargetRecord *native_fn_ov000_0221220c(short,short);
