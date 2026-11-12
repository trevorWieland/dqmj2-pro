/* Scale a parameter into the context slot and advance the record cursor.
   Unknowns: the parameter meaning, the bank/record roles and the caller contract. */
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
extern void native_fn_0205bd6c(int,int,int,int,int,int,int,int,int,int,int,int,int,int,int,int,int,int);
extern void native_fn_ov000_021e7940(int);
extern void native_fn_020404f0(int);
extern int native_fn_ov000_02210b98(int,int);
extern u32 native_fn_02040424(void);
extern void native_fn_0205e73c(int);
extern int native_fn_ov000_021e7b9c(int);
extern void native_fn_ov000_021e0bc4(int);
extern int native_fn_0205c1e8(void);
extern void native_fn_ov000_021e7bb0(int,int);
extern int native_fn_0205f35c(int,int);
extern void native_fn_0205f4bc(int,int,int);
extern void native_fn_0205f404(int,int);
extern void native_fn_0205f6a0(int,int,int);

void native_main_0204dd18(Context *context, const Instruction *instruction)
{
    context->parameters[0] = (float)native_fn_0221a0d8();
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}