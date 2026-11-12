/* Convert parameters to fixed point, publish them and advance the record.
   Unknowns: the fixed-point consumer and the record bank roles. */
#include "context.h"
typedef struct CommandRecord {
    u32 position;
    u8 reserved[3];
    u8 status;
    u8 padding[0x104];
} CommandRecord;
typedef struct Context {
    u8 reserved[3];
    u8 bank;
    u32 reservedWords[3];
    float parameters[8];
    u8 padding[0x440];
    CommandRecord records[];
} Context;
typedef struct Instruction {
    u32 opcode;
    u32 advance;
    u8 payload[];
} Instruction;
extern u32 native_fn_02064000(void);
extern void native_fn_02064038(u32);
extern void native_fn_02040820(void);
extern int native_fn_ov000_021e9aa0(void);
extern void native_fn_0204071c(int);
extern void native_fn_ov000_02208dcc(void);
extern void native_fn_ov000_02209670(void);
extern void native_fn_ov000_022096bc(void);
extern void native_fn_ov000_02209554(void);
extern void native_fn_0205e61c(void);
extern void native_fn_0205e520(void);
extern void native_fn_ov000_021f4110(int, u8);
extern void native_fn_ov000_021f4174(int, int);
extern int native_fn_0205c668(int, int);
extern int native_fn_ov000_021e96cc(int, int, signed char, int);
extern int native_fn_ov000_021e31f0(int, int);
extern int native_fn_ov000_021e9738(int, int, int);
extern int native_fn_0205d718(int);
extern int native_fn_ov000_02221444(const void *);
extern void native_fn_0205e3f0(u8);
extern void native_fn_ov000_021e9df4(u8);
extern void native_fn_ov000_021e9e4c(u8, u8);
extern int native_fn_ov000_021e9794(int);
extern void native_fn_ov000_021f3e5c(int, int *);
extern int native_fn_ov000_021f3f68(int);
extern void native_fn_ov000_021f3dac(int, int);
extern int native_fn_ov000_021f3ec4(int, int);
extern void native_fn_ov000_021f3fec(int, int, int, int);
extern void native_fn_ov000_021e71a4(int, int);
#define TO_FIXED(value) ((int)((value) > 0.0f ? 0.5f + 4096.0f * (value) : 4096.0f * (value) - 0.5f))
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
typedef struct CountRecord { u8 reserved[0x18]; short slot18; } CountRecord;
extern void native_fn_ov000_0220a040(int,u8);
extern void native_fn_ov000_021e5c88(u8,int,const void *,u8);
extern int native_fn_02028158(int);
extern void native_fn_ov000_021e5ec0(u8,int);
extern void native_fn_ov000_021e5ffc(int,int,int,u8);
extern int native_fn_0203d294(int);
extern int native_fn_0206344c(void);
extern int native_fn_0206349c(void);
extern int native_fn_020629e0(void);
extern int native_fn_02062aa0(void);
extern int native_fn_02062ad0(void);
extern CountRecord *native_fn_02062a50(int);
extern CountRecord *native_fn_02062a88(int);
extern int native_fn_02044cdc(int);

void native_main_02052720(Context *context, const Instruction *instruction)
{
    int third;
    int first = TO_FIXED(context->parameters[0]);
    int second = TO_FIXED(context->parameters[1]);
    u8 last;
    third = TO_FIXED(context->parameters[2]);
    last = (u32)context->parameters[3];
    native_fn_021e6114(first,second,third,last);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}