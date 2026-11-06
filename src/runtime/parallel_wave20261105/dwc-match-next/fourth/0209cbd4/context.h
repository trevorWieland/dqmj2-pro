#include "string.h"
#include "stdlib.h"
typedef unsigned char u8;typedef unsigned short u16;typedef unsigned long u32;typedef unsigned long long u64;typedef u64 OSTick;typedef int BOOL;typedef int GPResult;typedef void*GPConnection;typedef int DWCError;typedef int DWCFriendState;
typedef struct{u32 id_data,userid_lo32,playerid;}DWCAccLoginId;typedef union{u32 words[3];DWCAccLoginId login_id;}DWCFriendData;typedef struct{int size;DWCAccLoginId pseudo,authentic;int gs_profile_id,flag;u32 gamecode;int reserved[5];u32 crc32;}DWCAccUserData;typedef DWCAccUserData DWCUserData;
typedef void(*DWCUpdateServersCallback)(DWCError,BOOL,void*);typedef void(*DWCFriendStatusCallback)(int,u8,const char*,void*);typedef void(*DWCDeleteFriendListCallback)(int,int,void*);typedef void(*DWCBuddyFriendCallback)(int,void*);typedef void(*DWCStorageLoginCallback)(DWCError,void*);typedef void(*DWCSaveToServerCallback)(BOOL,BOOL,void*);typedef void(*DWCLoadFromServerCallback)(BOOL,int,char*,int,void*);
typedef struct{DWCFriendState state;GPConnection*pGpObj;u32 gpProcessCount;OSTick lastGpProcess;int friendListLen;DWCFriendData*friendList;u8 buddyUpdateIdx,friendListChanged,buddyUpdateState;volatile u8 svUpdateComplete;u32 persCallbackLevel;int profileID;const u16*playerName;DWCUpdateServersCallback updateCallback;void*updateParam;DWCFriendStatusCallback statusCallback;void*statusParam;DWCDeleteFriendListCallback deleteCallback;void*deleteParam;DWCBuddyFriendCallback buddyCallback;void*buddyParam;DWCStorageLoginCallback persLoginCallback;void*persLoginParam;DWCSaveToServerCallback saveCallback;DWCLoadFromServerCallback loadCallback;}DWCFriendPrefix;
typedef struct{u32 opaque[3];DWCFriendPrefix*control;}DWCFriendGlobals;extern DWCFriendGlobals native_data_021d1b74;
#define stpFriendCnt native_data_021d1b74.control
typedef struct{int profile,status;char statusString[256],locationString[256];unsigned int ip;int port,quietModeFlags;}GPBuddyStatus;
#define NULL ((void*)0)
#define TRUE 1
#define FALSE 0
#define DWC_Printf(...) ((void)0)
#define SDK_ASSERT(x) ((void)0)
#define DWC_STATUS_OFFLINE 0
#define DWC_STATUS_MATCH_SC_SV 6
#define DWC_GS_STATUS_STRING_LEN 256
#define DWC_GP_STATUS_NO_CHANGE (-1)
#define DWC_FRIEND_STATE_INIT 0
#define DWC_BUDDY_UPDATE_STATE_WAIT 0
extern const char native_data_020e0180[],native_data_020e0184[];
#define DWC_GP_SSTR_KEY_MATCH_SC_MAX native_data_020e0180
#define DWC_GP_SSTR_KEY_MATCH_SC_NUM native_data_020e0184
BOOL native_fn_0209d690(const DWCFriendData*,GPBuddyStatus*);int native_fn_0209b2bc(const char*,char*,const char*,char);u8 native_fn_0209cbd4(const DWCFriendData*,u8*,u8*,char*);int native_fn_0209a83c(const char*,u32,char*,u32),native_fn_0209a738(const char*,u32,char*,u32);BOOL native_fn_0209cba8(void);GPResult native_fn_0209d1c8(int,const char*,const char*);DWCAccUserData*native_fn_0209c5fc(void);int native_fn_020972f4(const DWCUserData*,const DWCFriendData*);BOOL native_fn_020aa55c(GPConnection*,int);GPResult native_fn_020aa5b4(GPConnection*,int);void native_fn_02008d78(void*,int,u32);
#define DWCi_GetFriendBuddyStatus native_fn_0209d690
#define DWC_GetCommonValueString native_fn_0209b2bc
#define DWC_GetFriendStatusSC native_fn_0209cbd4
#define DWC_Auth_Base64Decode native_fn_0209a83c
#define DWC_Auth_Base64Encode native_fn_0209a738
#define DWCi_CheckLogin native_fn_0209cba8
#define DWCi_SetGPStatus native_fn_0209d1c8
#define DWCi_GetUserData native_fn_0209c5fc
#define DWC_GetGsProfileId native_fn_020972f4
#define gpIsBuddy native_fn_020aa55c
#define gpDeleteBuddy native_fn_020aa5b4
#define MI_CpuClear8(d,n) native_fn_02008d78(d,0,n)
u8 native_main_0209cbd4(const DWCFriendData*,u8*,u8*,char*);u8 native_main_0209cc98(const DWCFriendData*,u8*,u8*,char*,int*);BOOL native_main_0209ccf4(const char*,u32);void native_main_0209cd4c(DWCFriendData*);
