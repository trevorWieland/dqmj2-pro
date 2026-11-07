typedef unsigned char u8;typedef unsigned short u16;typedef unsigned long u32;typedef signed long s32;typedef unsigned long long u64;typedef u64 OSTick;typedef int BOOL,DWCError,GT2Bool;typedef u8 GT2Byte;typedef struct GTI2Connection*GT2Connection;typedef void*DArray;
#define SDK_FINALROM 1
#define DWC_MAX_CONNECTIONS 32
#define NULL ((void*)0)
#define TRUE 1
#define FALSE 0
#define SDK_ASSERT(...) ((void)0)
#define SDK_ASSERTMSG(...) ((void)0)
#define DWC_Printf(...) ((void)0)
#define DWC_ERROR_NETWORK 6
#define OS_SYSTEM_CLOCK 33514000
#define OS_TicksToMilliSeconds(tick) (((u64)(tick)*64)/(OS_SYSTEM_CLOCK/1000))
#include "transport.h"
#include "errors.h"
#include "string.h"
extern DWCTransportInfo*native_data_021d2308;
#define sTransInfo native_data_021d2308
extern OSTick OS_GetTick(void);
extern int DWC_GetAIDList(u8**);
extern BOOL DWC_IsValidAID(u8);
extern u8 DWC_GetMyAID(void);
extern u8 DWCi_GetConnectionAID(GT2Connection);
extern void DWCi_SetError(DWCError,int);
extern void MI_CpuCopy8(const void*,void*,u32);
extern void MI_CpuClear8(void*,u32);
extern void DWCi_ProcessMatchSynPacket(u8,u16,u8*);
DWCTransportConnection * DWCs_GetTransConnection (u8 aid);
int DWCs_GetSendState(u8 aid);
int DWCs_GetRecvState(u8 aid);
void DWCs_Send(u8 aid, const u8 * buffer, int size, BOOL reliable);
void DWCs_HandleUnreliableMessage(GT2Connection connection, void * message, int size);
void DWCs_HandleReliableMessage(GT2Connection connection, u8 * message, int size);
void DWCs_RecvDataHeader(u8 aid, DWCTransportHeader * message, int size);
void DWCs_RecvDataBody(u8 aid, void * message, int size);
void DWCs_RecvSystemDataBody(u8 aid, void * message, int size);
void DWCs_DelayCheck(DArray delayedMessages, OSTick now, BOOL send);
void DWCs_AddDelayMessage(DArray array, u16 delayValue, GT2Connection connection, int filterID, const u8 * message, int size, BOOL reliable);
void DWCs_DelayedMessageFree(void * elem);
int DWCs_GetOutgoingBufferFreeSize(u8 aid);
void DWCs_SendFilterCallbackDrop(GT2Connection connection, int filterID, const u8 * message, int size, BOOL reliable);
void DWCs_SendFilterCallbackDelay(GT2Connection connection, int filterID, const u8 * message, int size, BOOL reliable);
void DWCs_RecvFilterCallbackDrop(GT2Connection connection, int filterID, u8 * message, int size, BOOL reliable);
void DWCs_RecvFilterCallbackDelay(GT2Connection connection, int filterID, u8 * message, int size, BOOL reliable);
void DWCs_EncodeHeader(DWCTransportHeader * header, u16 type, int size);
u16 DWCs_DecodeHeader(const DWCTransportHeader * header);
s32 DWCs_GetRequiredHeaderSize(u16 type);


s32 native_main_020a4144 (u16 type);

#define DWC_MATCH_SYN_DATA_BODY_SIZE 4
