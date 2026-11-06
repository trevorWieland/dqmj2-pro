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
typedef struct{u8 cards[256];u8 rotor,ratchet,avalanche,last_plain,last_cipher;}GOACryptState;
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
#define assert(x) ((void)0)
#define __GSIACResult native_data_021d23ec
#define INVALID_SOCKET -1
#define SERVER_GROWBY 100
typedef struct{const char*str;int refcount;}SBRefString;
void native_fn_020a865c(DArray,const void*);
void *native_fn_020a8644(DArray,int);
u32 native_fn_020a60b0(SBServer);
u16 native_fn_020a60cc(SBServer);
void native_fn_020a6100(SBServer,SBServer);
SBServer native_fn_020a6104(SBServer);
void native_fn_020a5f80(void*);
void native_fn_020a8720(DArray,int);
void native_fn_020a6e34(SBServerList*,SBServer);
void*native_fn_020a5f1c(SBServerList*);
void*native_fn_020a8a3c(void*,const void*);
char*native_fn_020a8ea0(const char*);
void native_fn_020a89a4(void*,const void*);
int native_fn_020a89f0(void*,const void*);
void native_fn_020a6f18(SBServerList*);
void native_fn_020a7b28(SBServerList*,char*);
u32 native_fn_020a8ef8(void);
void native_fn_0201d608(u32);
void native_fn_020a8ef0(void);
extern const char native_data_020e0350[1];
typedef struct{const char*keyName;int keyType;}KeyInfo;
#define KEYTYPE_STRING 0
#define KEYTYPE_BYTE 1
#define KEYTYPE_SHORT 2
#define PRIVATE_IP_FLAG 2
#define ICMP_IP_FLAG 8
#define NONSTANDARD_PORT_FLAG 16
#define NONSTANDARD_PRIVATE_PORT_FLAG 32
#define HAS_KEYS_FLAG 64
#define HAS_FULL_RULES_FLAG 128
#define LIST_CHALLENGE_LEN 8
#define sbe_noerror 0
static inline void*copybytes(void*dst,const void*src,u32 n){u8*d=dst;const u8*s=src;if(n==4){d[0]=s[0];d[1]=s[1];d[2]=s[2];d[3]=s[3];}else if(n==2){d[0]=s[0];d[1]=s[1];}else if(n)do{*d++=*s++;}while(--n);return dst;}
#define memcpy copybytes
static inline u16 swap16(u16 x){return(u16)((u8)(x>>8)|((x<<8)&0xff00));}
#define ntohs(x) swap16(x)
u32 native_fn_0201d69c(const char*);
void native_fn_020a5710(GOACryptState*,u8*,u8);
int native_fn_020a6fa8(char*,int);
void native_fn_020a6538(SBServer,u8);
void native_fn_020a653c(SBServer,u32,u16);
void native_fn_020a6544(SBServer,u32);
void native_fn_020a6548(SBServer,u8);
u8 native_fn_020a654c(SBServer);
void native_fn_020a5fc0(SBServer,const char*,int);
void native_fn_020a5f98(SBServer,const char*,const char*);
void native_fn_020a6ea8(SBServerList*);
int native_fn_020a82a0(SBServerList*);
int native_fn_020a8480(SBServerList*);
typedef u32 size_t;
enum{pi_cryptheader,pi_fixedheader,pi_keylist,pi_uniquevaluelist,pi_servers,pi_finished};
#define FIXED_HEADER_LEN 6
#define NO_SERVER_LIST 2
#define sbe_allocerror 5
#define SBNullServer native_data_021d2368
extern SBServer native_data_021d2368;
void native_fn_020a76a0(SBServerList*,char*,int);
void native_fn_020a5820(GOACryptState*,u8*,int);
void*native_fn_020a85dc(int,int,void(*)(void*));
const char*native_fn_020a6f34(SBServerList*,const char*);
int native_fn_020a7a5c(SBServerList*,char*,int);
void*native_fn_0201b1bc(void*,const void*,u32);
typedef struct sockaddr{u8 len,family,data[6];}SOCKADDR;
struct in_addr{u32 s_addr;};
struct sockaddr_in{u8 len,sin_family;u16 sin_port;struct in_addr sin_addr;};
struct hostent{char*h_name;char**h_aliases;short h_addrtype,h_length;char**h_addr_list;};
typedef struct{char*master;SBServerList*active;}SortGlobals;
extern SortGlobals native_data_021d236c;
#define SBOverrideMasterServer native_data_021d236c.master
#define AF_INET 2
#define SOCK_STREAM 1
#define IPPROTO_TCP 0
#define INADDR_NONE 0xffffffff
#define NUM_MASTER_SERVERS 20
#define MSPORT2 28910
#define MAX_FILTER_LEN 256
#define MAX_FIELD_LIST_LEN 256
#define MAX_OUTGOING_REQUEST_SIZE 767
#define SERVER_LIST_REQUEST 0
#define LIST_PROTOCOL_VERSION 1
#define LIST_ENCODING_VERSION 3
#define ALTERNATE_SOURCE_IP 8
#define LIMIT_RESULT_COUNT 128
#define INCOMING_BUFFER_SIZE 4096
#define sbe_paramerror 6
#define sbe_dnserror 2
#define sbe_socketerror 1
#define sbe_connecterror 3
#define MULTIPLIER -1664117991
extern const u8 native_data_020d8d04[128];
extern char native_data_020e033c[14];
extern const char native_data_020e0354[];
static inline int lower(int c){return c<0||c>=128?c:native_data_020d8d04[c];}
#define tolower lower
#define htons(x) swap16(x)
#define htonl(x) (((x)>>24&0xff)|((x)>>8&0xff00)|((x)<<8&0xff0000)|((x)<<24&0xff000000))
int native_fn_0201d914(const char*,const char*,u32);
void native_fn_020a762c(SBServerList*);
int native_fn_020a710c(const char*,int);
int native_fn_0200616c(char*,const char*,...);
u32 native_fn_020a8c84(const char*);
struct hostent*native_fn_0209046c(const char*);
int native_fn_020a8b5c(int,int,int);
int native_fn_020a8bc4(int,const void*,int);
int native_fn_020a8b6c(int);
void native_fn_020a7260(char**,int,int*);
int native_fn_0201d5d4(void);
int native_fn_020a714c(SBServerList*);
void native_fn_020a72f4(SBServerList*);
void native_fn_020a724c(char**,u8,int*);
void native_fn_020a728c(char**,int,int*);
void native_fn_020a7218(char**,const char*,int*);
void native_fn_020a72d8(char**,char*,int,int*);
int native_fn_020a8c24(int,const char*,int,int);
void native_fn_020a6f78(SBServerList*,const char*);
void native_fn_020a929c(void*);
void native_fn_020a75ec(SBServerList*);
void native_fn_020a75b4(SBServerList*);
