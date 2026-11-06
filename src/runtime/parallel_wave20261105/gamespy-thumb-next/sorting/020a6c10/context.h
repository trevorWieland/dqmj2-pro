typedef unsigned char u8;typedef unsigned short u16;typedef unsigned int u32;
typedef u32 goa_uint32;typedef u32 gsi_time;typedef int SBBool;typedef int SBError;typedef int SBState;typedef int SBCompareMode;
typedef struct Server{u32 publicip;u16 publicport;u32 privateip;u16 privateport;u32 icmpip;u8 state,flags;void*keyvals;u32 updatetime,querychallenge;struct Server*next;u8 splitResponseBitmap;} *SBServer;
typedef void *DArray;
typedef struct _SBServerList SBServerList;typedef SBServerList *SBServerListPtr;
typedef struct _SBQueryEngine SBQueryEngine;typedef SBQueryEngine*SBQueryEnginePtr;
typedef struct _ServerBrowser *ServerBrowser;
typedef int SBListCallbackReason;typedef int SBQueryEngineCallbackReason;
typedef void(*SBListCallBackFn)(SBServerList*,int,SBServer,void*);
typedef void(*SBEngineCallbackFn)(SBQueryEngine*,int,SBServer,void*);
typedef void(*ServerBrowserCallback)(ServerBrowser,int,SBServer,void*);
typedef struct{char sortkey[255];SBCompareMode comparemode;}SortInfo;
typedef struct{u8 cards[256];u8 rotor,ratchet,avalanche,lastplain,lastcipher;}GOACryptState;
struct _SBServerList{int state;DArray servers,keylist;char queryforgamename[36],queryfromgamename[36],queryfromkey[32],mychallenge[8];char*inbuffer;int inbufferlen;const char*popularvalues[255];int numpopularvalues,expectedelements;SBListCallBackFn ListCallback;void*MaploopCallback,*PlayerSearchCallback,*instance;SortInfo currsortinfo,prevsortinfo;SBBool sortascending;u32 mypublicip,srcip;u16 defaultport;char*lasterror;int slsocket;gsi_time lanstarttime;int fromgamever;GOACryptState cryptkey;int queryoptions,pstate;u16 backendgameflags;const char*mLanAdapterOverride;SBServer deadlist;};
typedef struct{SBServer first,last;int count;}SBServerFIFO;
struct _SBQueryEngine{int queryversion,maxupdates;SBServerFIFO querylist,pendinglist;int querysock,icmpsock;u32 mypublicip;u8 serverkeys[20];int numserverkeys;SBEngineCallbackFn ListCallback;void*instance;};
struct _ServerBrowser{SBQueryEngine engine;SBServerList list;SBBool disconnectFlag,dontUpdate;u32 triggerIP;u16 triggerPort;ServerBrowserCallback BrowserCallback;void*instance;};
enum{slc_serveradded,slc_serverupdated,slc_serverdeleted,slc_initiallistcomplete,slc_disconnected,slc_queryerror,slc_publicipdetermined,slc_serverchallengereceived};
enum{qe_updatesuccess,qe_updatefailed,qe_engineidle,qe_challengereceived};
enum{sbc_serveradded,sbc_serverupdated,sbc_serverupdatefailed,sbc_serverdeleted,sbc_updatecomplete,sbc_queryerror,sbc_serverchallengereceived};
enum{sl_lanbrowse,sl_disconnected,sl_connected,sl_mainlist};
enum{sb_disconnected,sb_listxfer,sb_querying,sb_connected};
#define NULL ((void*)0)
#define SBFalse 0
#define SBTrue 1
#define GSIACAvailable 1
#define GS_ASSERT(x)
#define GSI_UNUSED(x) ((void)(x))
#define STATE_BASICKEYS 1
#define STATE_FULLKEYS 2
#define STATE_PENDINGBASICQUERY 4
#define STATE_PENDINGFULLQUERY 8
#define STATE_PENDINGICMPQUERY 32
#define STATE_VALIDPING 64
#define UNSOLICITED_UDP_FLAG 1
#define QR2_USE_QUERY_CHALLENGE 128
#define QTYPE_BASIC 0
#define QTYPE_FULL 1
#define QTYPE_ICMP 2
#define MAX_FIELD_LIST_LEN 256
#define SORTKEY_LENGTH 255
#define _tcscpy native_fn_0201d6b8
extern int native_data_021d23ec;
void *native_fn_020a927c(u32);
int native_fn_020a8640(DArray);
void native_fn_020a5afc(SBQueryEngine*,SBServer,int,int,int);
void native_fn_020a5edc(SBQueryEngine*,SBServer);
void native_fn_020a762c(SBServerList*);
void native_fn_020a5ac0(SBQueryEngine*,u32);
void native_fn_020a6fc4(SBServerList*,const char*,const char*,const char*,int,int,SBListCallBackFn,void*);
void native_fn_020a5a74(SBQueryEngine*,int,int,int,SBEngineCallbackFn,void*);
void native_fn_020a6564(SBServerList*,int,SBServer,void*);
void native_fn_020a66c0(SBQueryEngine*,int,SBServer,void*);
int native_fn_020a6db0(SBServerList*,SBServer);
void native_fn_020a6e5c(SBServerList*,int);
char *native_fn_0201d6b8(char*,const char*);
void native_fn_020a6cc0(SBServerList*,SBBool,SortInfo);
typedef int(*ArrayCompareFn)(const void*,const void*);
#define GS_STATIC_CALLBACK
#define sbcm_int 0
#define sbcm_float 1
#define sbcm_strcase 2
#define sbcm_stricase 3
#define _tcslen native_fn_0201d69c
typedef struct{u32 uninterpreted;SBServerList*active;}SortGlobal;
extern SortGlobal native_data_021d236c;
#define currentSortList (native_data_021d236c.active)
extern const char native_data_020e0350[1];
int native_fn_020a601c(SBServer,const char*,int);
double native_fn_020a6090(SBServer,const char*,double);
const char*native_fn_020a5fe4(SBServer,const char*,const char*);
int native_fn_0201d800(const char*,const char*);
int native_fn_02023f6c(const char*,const char*);
u32 native_fn_0201d69c(const char*);
int native_fn_020a69f8(SBServer,SBServer);
int native_fn_020a6b10(const void*,const void*);
int native_fn_020a6b5c(const void*,const void*);
int native_fn_020a6c10(const void*,const void*);
int native_fn_020a6c68(const void*,const void*);
void native_fn_020a8750(DArray,ArrayCompareFn);
