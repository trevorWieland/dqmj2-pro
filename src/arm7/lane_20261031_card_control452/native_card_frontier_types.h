#include "native_card_types.h"
typedef CardArgumentStorage CardExtendedArgument;
typedef CardCommonStorage CardTaskState;
extern u32 native_host_arm7_fn_037fdd00(void);
extern u32 native_host_arm7_fn_037fdd14(u32);
extern void native_host_arm7_fn_037fc2e4(void *);
extern void native_host_arm7_fn_038028e4(CardTransfer *);
typedef CardArgumentStorage CardDispatchArgument;
extern void native_host_arm7_fn_037fc290(void *);
extern s32 native_host_arm7_fn_037fe410(u32,u32,u32);
extern void native_host_arm7_fn_03802aac(void);
extern u32 native_host_arm7_fn_03803094(void);
extern void native_host_arm7_fn_03802b04(u32,u32,u32);
extern void native_host_arm7_fn_03802b70(u32,const void *,u32);
extern void native_host_arm7_fn_03802c28(u32,const void *,u32);
extern void native_host_arm7_fn_03802ce0(u32,const void *,u32);
extern void native_host_arm7_fn_03802d70(u32,u32);
extern void native_host_arm7_fn_03802e0c(u32,u32);
extern void native_host_arm7_fn_03802ea8(void);
extern void native_host_arm7_fn_03802f04(u32);
extern u32 native_host_arm7_fn_03803070(u32);
extern void native_host_arm7_fn_03802f9c(u32,u32);
static inline u32 CardReadPhase(CardCommonStorage *state) { return *(volatile u32 *)&state->prefix.command; }
static inline u32 CardReadRequest(CardCommonStorage *state) { return *(volatile u32 *)&state->prefix.unknown04; }
static inline void CardWriteRequest(CardCommonStorage *state,u32 request) { *(volatile u32 *)&state->prefix.unknown04=request; }
