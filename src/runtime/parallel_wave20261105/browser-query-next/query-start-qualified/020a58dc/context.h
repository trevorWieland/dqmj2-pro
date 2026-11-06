typedef int SOCKET;
#define QVERSION_GOA 0
#define QVERSION_QR2 1
#define ICMP_IP_FLAG 8
#define assert(x)
extern const char*native_data_020e277c[256];
#define qr2_registered_key_list native_data_020e277c
int native_fn_020a6fa8(const char*,int);
int native_fn_020b85a8(const char*);
int native_fn_0201d914(const char*,const char*,unsigned int);
#define NTSLengthSB native_fn_020a6fa8
#define qr2_internal_is_master_only_key native_fn_020b85a8
#define strncmp native_fn_0201d914
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
typedef int gsi_bool;typedef u32 gsi_u32;
#define gsi_false 0
#define gsi_true 1
#define gsi_is_true(x) ((x)==1)
#define gsDebugFormat(...)
#define FIFODebugCheckAdd(a,b)
#define FIFODebugCheck(a)
#define MAX_RECVFROM_SIZE 2048
#define MAX_QUERY_MSEC 2500
#define MAX_QUERY_KEYS 20
#define QTYPE_BASIC 0
#define QTYPE_FULL 1
#define QTYPE_ICMP 2
#define STATE_PENDINGBASICQUERY 4
#define STATE_PENDINGFULLQUERY 8
#define STATE_QUERYFAILED 16
#define STATE_PENDINGICMPQUERY 32
#define STATE_VALIDPING 64
#define STATE_PENDINGQUERYCHALLENGE 128
#define PRIVATE_IP_FLAG 2
#define QR2_MAGIC_1 254
#define QR2_MAGIC_2 253
#define BASIC_GOA_QUERY native_data_020e02d4
#define BASIC_GOA_QUERY_LEN 13
#define FULL_GOA_QUERY native_data_020e02e4
#define FULL_GOA_QUERY_LEN 8
#define AF_INET 2
#define SOCK_DGRAM 2
#define IPPROTO_UDP 17
#define GSIACAvailable 1
#define __GSIACResult native_data_021d23ec
extern int native_data_021d23ec;
extern const char native_data_020e02d4[],native_data_020e02e4[],native_data_020e02f0[],native_data_020e02fc[];
struct in_addr{u32 s_addr;};
struct sockaddr{u8 len,family,data[6];};
struct sockaddr_in{u8 len,sin_family;u16 sin_port;struct in_addr sin_addr;};
typedef struct{const char*key,*value;}SBKeyValuePair;
static inline void*copybytes(void*dst,const void*src,u32 n){u8*d=dst;const u8*s=src;u32 i;if(n==4){d[0]=s[0];d[1]=s[1];d[2]=s[2];d[3]=s[3];return dst;}if(n==2){d[0]=s[0];d[1]=s[1];return dst;}if(n)do{*d++=*s++;}while(--n);return dst;}
#define memcpy copybytes
#define htonl(x) ((((u32)(x))>>24&0xff)|(((u32)(x))>>8&0xff00)|(((u32)(x))<<8&0xff0000)|(((u32)(x))<<24&0xff000000))
SBBool native_fn_020a5894(SBServerFIFO*,SBServer);
#define FIFORemove native_fn_020a5894
void native_fn_020a58dc(SBQueryEngine*,SBServer);
#define QEStartQuery native_fn_020a58dc
#define SBQueryEngineInit native_fn_020a5a74
#define SBQueryEngineUpdateServer native_fn_020a5afc
void native_fn_020a5b74(SBQueryEngine*,SBServer,char*,int);
#define ParseSingleQR2Reply native_fn_020a5b74
void native_fn_020a5cb0(SBQueryEngine*,SBServer,char*,int);
#define ParseSingleGOAReply native_fn_020a5cb0
void native_fn_020a5d1c(SBQueryEngine*,SBBool);
#define ProcessIncomingReplies native_fn_020a5d1c
void native_fn_020a5e14(SBQueryEngine*);
#define TimeoutOldQueries native_fn_020a5e14
void native_fn_020a5e68(SBQueryEngine*);
#define QueueNextQueries native_fn_020a5e68
void native_fn_020a5e90(SBQueryEngine*);
#define SBQueryEngineThink native_fn_020a5e90
void native_fn_020a5ec8(SBQueryEngine*,u8);
#define SBQueryEngineAddQueryKey native_fn_020a5ec8
void native_fn_020a5f98(SBServer,const char*,const char*);
#define SBServerAddKeyValue native_fn_020a5f98
const char* native_fn_020a5fe4(SBServer,const char*,const char*);
#define SBServerGetStringValue native_fn_020a5fe4
void native_fn_020a5840(SBServerFIFO*,SBServer);
#define FIFOAddRear native_fn_020a5840
void native_fn_020a5860(SBServerFIFO*,SBServer);
#define FIFOAddFront native_fn_020a5860
SBServer native_fn_020a5878(SBServerFIFO*);
#define FIFOGetFirst native_fn_020a5878
void native_fn_020a58d0(SBServerFIFO*);
#define FIFOClear native_fn_020a58d0
u32 native_fn_020a8ef8(void);
#define current_time native_fn_020a8ef8
int native_fn_020a8c34(int,const char*,int,int,struct sockaddr*,int);
#define sendto native_fn_020a8c34
void native_fn_020a8ef0(void);
#define SocketStartUp native_fn_020a8ef0
int native_fn_020a8b5c(int,int,int);
#define socket native_fn_020a8b5c
int native_fn_0201f274(const char*);
#define atoi native_fn_0201f274
char* native_fn_0201d984(const char*,const char*);
#define strstr native_fn_0201d984
int native_fn_020a8d88(int);
#define CanReceiveOnSocket native_fn_020a8d88
int native_fn_020a8c00(int,char*,int,int,struct sockaddr*,int*);
#define recvfrom native_fn_020a8c00
void native_fn_020a6300(SBServer,char*,int);
#define SBServerParseQR2FullKeysSplit native_fn_020a6300
void native_fn_020a61d0(SBServer,char*,int);
#define SBServerParseQR2FullKeysSingle native_fn_020a61d0
void native_fn_020a6180(SBServer,char*);
#define SBServerParseKeyVals native_fn_020a6180
const char* native_fn_020a6f34(SBServer,const char*);
#define SBRefStr native_fn_020a6f34
void native_fn_020a89a4(void*,const void*);
#define TableEnter native_fn_020a89a4
void* native_fn_020a8a3c(void*,const void*);
#define TableLookup native_fn_020a8a3c
u32 native_fn_0201d69c(const char*);
#define strlen native_fn_0201d69c
