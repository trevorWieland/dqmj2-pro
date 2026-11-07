#include "gp_types.h"
#include "error_types.h"
typedef unsigned char u8;typedef unsigned short u16;typedef unsigned long u32;typedef unsigned long long u64;typedef u64 OSTick;typedef int BOOL;typedef void*GPConnection;typedef enum {
    DWC_FRIEND_STATE_INIT = 0,
    DWC_FRIEND_STATE_PERS_LOGIN,
    DWC_FRIEND_STATE_LOGON,
    DWC_FRIEND_STATE_NUM
} DWCFriendState;
typedef struct{u32 id_data,userid_lo32,playerid;}DWCAccLoginId;typedef union{u32 words[3];DWCAccLoginId login_id;}DWCFriendData;typedef struct{int size;DWCAccLoginId pseudo,authentic;int gs_profile_id,flag;u32 gamecode;int reserved[5];u32 crc32;}DWCAccUserData;typedef DWCAccUserData DWCUserData;
typedef void(*DWCUpdateServersCallback)(DWCError,BOOL,void*);typedef void(*DWCFriendStatusCallback)(int,u8,const char*,void*);typedef void(*DWCDeleteFriendListCallback)(int,int,void*);typedef void(*DWCBuddyFriendCallback)(int,void*);typedef void(*DWCStorageLoginCallback)(DWCError,void*);typedef void(*DWCSaveToServerCallback)(BOOL,BOOL,void*);typedef void(*DWCLoadFromServerCallback)(BOOL,int,char*,int,void*);
typedef struct{DWCFriendState state;GPConnection*pGpObj;u32 gpProcessCount;OSTick lastGpProcess;int friendListLen;DWCFriendData*friendList;u8 buddyUpdateIdx,friendListChanged,buddyUpdateState;volatile u8 svUpdateComplete;u32 persCallbackLevel;int profileID;const u16*playerName;DWCUpdateServersCallback updateCallback;void*updateParam;DWCFriendStatusCallback statusCallback;void*statusParam;DWCDeleteFriendListCallback deleteCallback;void*deleteParam;DWCBuddyFriendCallback buddyCallback;void*buddyParam;DWCStorageLoginCallback persLoginCallback;void*persLoginParam;DWCSaveToServerCallback saveCallback;DWCLoadFromServerCallback loadCallback;}DWCFriendPrefix;
typedef struct{u32 opaque[3];DWCFriendPrefix*control;}DWCFriendGlobals;extern DWCFriendGlobals native_data_021d1b74;
#define stpFriendCnt native_data_021d1b74.control
typedef struct{int profile,status;char statusString[256],locationString[256];unsigned int ip;int port,quietModeFlags;}GPBuddyStatus;
#define NULL ((void*)0)
#define TRUE 1
#define FALSE 0
#define SDK_ASSERT(...)
#define DWC_Printf(...)
#define DWC_FRIENDDATA_NODATA 0
#define DWC_BUDDY_UPDATE_STATE_CHECK 1
extern int native_fn_02096d9c(const DWCFriendData*);
#define DWC_GetFriendDataType native_fn_02096d9c
extern int native_fn_0209d134(int);
#define DWCi_GetProfileIDFromList native_fn_0209d134
extern int native_fn_0209d168(int);
#define DWCi_GetFriendListIndex native_fn_0209d168
extern GPResult native_fn_020aa3e0(GPConnection*,int,GPBuddyStatus*);
#define gpGetBuddyStatus native_fn_020aa3e0
extern OSTick native_fn_02007a9c(void);
#define OS_GetTick native_fn_02007a9c
extern u8 native_fn_0209cbc4(const DWCFriendData*,char*);
#define DWC_GetFriendStatus native_fn_0209cbc4
extern void native_fn_0209d03c(DWCError,int);
#define DWCi_StopFriendProcess native_fn_0209d03c
extern BOOL native_fn_0209d514(DWCFriendData[],int,int);
#define DWCi_RefreshFriendListForth native_fn_0209d514
extern GPResult native_fn_020aa4f0(GPConnection*,int,int*);
#define gpGetBuddyIndex native_fn_020aa4f0
extern GPResult native_fn_0209d704(GPResult);
#define DWCi_HandleGPError native_fn_0209d704
extern GPResult native_fn_0209d66c(int);
#define DWCi_GPSendBuddyRequest native_fn_0209d66c
extern void native_fn_020973a8(DWCFriendData*,int);
#define DWC_SetGsProfileId native_fn_020973a8
extern void native_fn_02096dd0(DWCFriendData*);
#define DWCi_SetBuddyFriendData native_fn_02096dd0
extern void native_fn_0209d238(int);
#define DWCi_CallBuddyFriendCallback native_fn_0209d238
extern u32 native_fn_02096e50(DWCFriendData*,int);
extern u32 native_fn_02096e08(DWCFriendData*,int);
extern u32 native_fn_02096d04(const DWCFriendData*);
extern u32 native_fn_02096e2c(DWCFriendData*,int);

void native_main_0209d238 (int index);
