#define DWC_GetGsProfileId native_fn_020972f4
#define DWCi_CheckLogin native_fn_0209cba8
#define DWCi_GetUserData native_fn_0209c5fc
#define OS_GetTick native_fn_02007a9c
#define gpGetBuddyIndex native_fn_020aa4f0
#define gpGetBuddyStatus native_fn_020aa3e0
#define gpProcess native_fn_020a9f60
#include "string.h"
#include "stdlib.h"
typedef unsigned char u8;typedef unsigned short u16;typedef unsigned long u32;typedef unsigned long long u64;typedef u64 OSTick;typedef int BOOL;typedef int GPResult;typedef void*GPConnection;typedef int DWCError;typedef enum {
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
#define DWC_Printf(...) ((void)0)
#define SDK_ASSERT(x) ((void)0)
#define DWC_GS_STATUS_STRING_LEN 256
#define DWC_GP_STATUS_NO_CHANGE (-1)
extern const char native_data_020e0180[],native_data_020e0184[];
#define DWC_GP_SSTR_KEY_MATCH_SC_MAX native_data_020e0180
#define DWC_GP_SSTR_KEY_MATCH_SC_NUM native_data_020e0184

typedef DWCFriendPrefix DWCFriendControl;typedef int GPEnum;typedef char gsi_char;typedef volatile u8 vu8;
enum {
    DWC_STATUS_OFFLINE = 0,
    DWC_STATUS_ONLINE,
    DWC_STATUS_PLAYING,
    DWC_STATUS_MATCH_ANYBODY,
    DWC_STATUS_MATCH_FRIEND,
    DWC_STATUS_MATCH_SC_CL,
    DWC_STATUS_MATCH_SC_SV,
    DWC_STATUS_NUM
};
enum {
    DWC_BUDDY_UPDATE_STATE_WAIT = 0,
    DWC_BUDDY_UPDATE_STATE_CHECK,
    DWC_BUDDY_UPDATE_STATE_PSEARCH,
    DWC_BUDDY_UPDATE_STATE_COMPLETE,
    DWC_BUDDY_UPDATE_STATE_NUM
};
enum {
    DWC_PERS_STATE_INIT = 0,
    DWC_PERS_STATE_LOGIN,
    DWC_PERS_STATE_CONNECTED,
    DWC_PERS_STATE_NUM
};
#define s_bInPersistThink native_data_021d1b74.opaque[1]
#define s_bNeedCloseStatsConnection native_data_021d1b74.opaque[0]
#define stPersState native_data_021d1b74.opaque[2]
#define SDK_ASSERTMSG(...) ((void)0)
#define GP_NO_ERROR 0
#define GP_NO_CHECK 0
#define GP_CHECK_CACHE 1
#define DWC_ERROR_NONE 0
#define DWC_FRIEND_UPDATE_WAIT_COUNT 7
#define DWC_GP_STATUS_NO_CHANGE (-1)
#define OS_TicksToMilliSeconds(t) (((u64)(t)*64)/33514)
BOOL DWCi_IsError(void);GPResult DWCi_GPProcess(void);u32 DWCi_GetPersCallbackLevel(void);int IsStatsConnected(void),PersistThink(void);void CloseStatsConnection(void),DWCi_UpdateFriendReq(DWCFriendData[],int),DWCi_EndUpdateServers(void),DWCi_SetError(DWCError,int),DWCi_CloseFriendProcess(void),DWCi_StopPersLogin(DWCError,int);void DWCi_StopFriendProcess(DWCError,int);OSTick OS_GetTick(void);
void native_main_0209cdac(DWCFriendControl * friendcnt,
                      GPConnection * pGpObj,
                      const u16 * playerName,
                      DWCFriendData * friendList,
                      int friendListLen);
void native_main_0209ce3c(void);
void native_main_0209cfe4(const char * authToken,
                              const char * partnerChallenge,
                              DWCUpdateServersCallback updateCallback,
                              void * updateParam,
                              DWCFriendStatusCallback statusCallback,
                              void * statusParam,
                              DWCDeleteFriendListCallback deleteCallback,
                              void * deleteParam);
void native_main_0209d03c(DWCError error, int errorCode);

#define DWC_GP_PROCESS_INTERVAL 300
GPResult gpProcess(GPConnection*),gpGetBuddyIndex(GPConnection*,int,int*),gpGetBuddyStatus(GPConnection*,int,GPBuddyStatus*);BOOL DWCi_CheckLogin(void),DWC_IsBuddyFriendData(const DWCFriendData*);DWCAccUserData*DWCi_GetUserData(void);int DWC_GetGsProfileId(const DWCUserData*,const DWCFriendData*),DWCi_GetProfileIDFromList(int);void DWCi_DeleteFriendFromList(DWCFriendData[],int,int);void native_fn_02008d78(void*,int,u32);
#define MI_CpuClear8(d,n) native_fn_02008d78(d,0,n)
GPResult native_main_0209d294(void);
void native_main_0209d4c0(void);
void native_main_0209d4e0(DWCFriendData friendData[], int deleteIndex, int otherIndex);
BOOL native_main_0209d514(DWCFriendData friendList[], int index, int profileID);
BOOL native_main_0209d690(const DWCFriendData * friendData, GPBuddyStatus * status);

#define SDK_FINALROM 1
#define GP_NON_BLOCKING 0
typedef void(*GPCallback)(GPConnection*,void*,void*);typedef struct GPProfileSearchResponseArg GPProfileSearchResponseArg;
GPResult gpGetNumBuddies(GPConnection*,int*),DWCi_HandleGPError(GPResult),gpDeleteBuddy(GPConnection*,int),DWCi_GPSendBuddyRequest(int);void DWC_SetGsProfileId(DWCFriendData*,int),DWCi_SetBuddyFriendData(DWCFriendData*),DWC_LoginIdToUserName(const DWCUserData*,const DWCFriendData*,char*);BOOL DWCi_RefreshFriendListForth(DWCFriendData[],int,int);GPResult gpProfileSearch(GPConnection*,const char*,const char*,const char*,const char*,const char*,int,GPEnum,GPCallback,void*);void DWCi_GPProfileSearchCallback(GPConnection*,GPProfileSearchResponseArg*,void*);
void native_main_0209d30c(DWCFriendData[],int);
