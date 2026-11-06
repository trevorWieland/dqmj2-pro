typedef unsigned int gsi_time;
typedef char gsi_char;
typedef struct hostent{char*h_name;char**h_aliases;short h_addrtype;short h_length;char**h_addr_list;}HOSTENT;
#define AF_INET 2
#define INADDR_NONE 0xffffffff
#define GSI_DOMAIN_NAME "gamespy.com"
typedef unsigned char u8;
typedef unsigned int u32;
typedef unsigned int size_t;
typedef int SOCKET;
typedef int gsi_bool;
typedef struct in_addr { unsigned int s_addr; } IN_ADDR;
struct sockaddr {u8 sa_len;u8 sa_family;char sa_data[6];};
struct sockaddr_in {u8 sin_len;u8 sin_family;unsigned short sin_port;IN_ADDR sin_addr;};
#define NULL ((void*)0)
#define gsDebugFormat(...)
#define gsiSocketIsError(x) ((x)==-1)
#ifndef _DARRAY_H
#define _DARRAY_H
#ifdef __cplusplus
extern "C" {
#endif
typedef struct DArrayImplementation *DArray;
typedef int (*ArrayCompareFn)(const void *elem1, const void *elem2);
typedef void (*ArrayMapFn)(void *elem, void *clientData);
typedef int (*ArrayMapFn2)(void *elem, void *clientData);
typedef void (*ArrayElementFreeFn)(void *elem);
DArray native_fn_020a85dc(int elemSize, int numElemsToAllocate,
                ArrayElementFreeFn elemFreeFn);
void ArrayFree(DArray array);
int native_fn_020a8640(const DArray array);
void *native_fn_020a8644(DArray array, int n);
void native_fn_020a865c(DArray array, const void *newElem);
void ArrayInsertAt(DArray array, const void *newElem, int n);
void ArrayInsertSorted(DArray array, const void *newElem, ArrayCompareFn comparator);
void ArrayDeleteAt(DArray array, int n);
void ArrayRemoveAt(DArray array, int n);
void ArrayReplaceAt(DArray array, const void *newElem, int n);
void ArraySort(DArray array, ArrayCompareFn comparator);
#define NOT_FOUND -1
int ArraySearch(DArray array, const void *key, ArrayCompareFn comparator,
                  int fromIndex, int isSorted);
void ArrayMap(DArray array, ArrayMapFn fn, void *clientData);
void ArrayMapBackwards(DArray array, ArrayMapFn fn, void *clientData);
void * ArrayMap2(DArray array, ArrayMapFn2 fn, void *clientData);
void * ArrayMapBackwards2(DArray array, ArrayMapFn2 fn, void *clientData);
void ArrayClear(DArray array);
#ifdef __cplusplus
}
#endif
#endif
#if !defined(AFX_NATIFY_H__B8FF4369_8789_4674_8569_3D52CE8CA890__INCLUDED_)
#define AFX_NATIFY_H__B8FF4369_8789_4674_8569_3D52CE8CA890__INCLUDED_
#if _MSC_VER > 1000
#pragma once
#endif
#define NATIFY_COOKIE		777
#define NATIFY_TIMEOUT		10000
#define NATIFY_STATUS_STEPS (NATIFY_TIMEOUT / 1000) + 7
typedef enum { packet_map1a, packet_map2, packet_map3, packet_map1b, NUM_PACKETS } NatifyPacket;
typedef enum { no_nat, firewall_only, full_cone, restricted_cone, port_restricted_cone, symmetric, unknown, NUM_NAT_TYPES } NatType;
typedef enum { promiscuous, not_promiscuous, port_promiscuous, ip_promiscuous, promiscuity_not_applicable, NUM_PROMISCUITY_TYPES } NatPromiscuity;
typedef enum { unrecognized, private_as_public, consistent_port, incremental, mixed, NUM_MAPPING_SCHEMES } NatMappingScheme;
typedef struct _AddressMapping {
	unsigned int privateIp;
	unsigned short privatePort;
	unsigned int publicIp;
	unsigned short publicPort;
} AddressMapping;
typedef struct _NAT {
	char brand[32];
	char model[32];
	char firmware[64];
	gsi_bool ipRestricted;
	gsi_bool portRestricted;
	NatPromiscuity promiscuity;
	NatType natType;
	NatMappingScheme mappingScheme;
	AddressMapping mappings[4];
	gsi_bool qr2Compatible;
} NAT;
int DiscoverReachability(SOCKET sock, unsigned int ip, unsigned short port, int portType);
int DiscoverMapping(SOCKET sock, unsigned int ip, unsigned short port, int portType, int id);
int NatifyThink(SOCKET sock, NAT * nat);
gsi_bool DetermineNatType(NAT * nat);
void OutputMapping(const AddressMapping * theMap);
#endif
#ifndef _NATNEG_H_
#define _NATNEG_H_
#ifdef __cplusplus
extern "C" {
#endif
#define NATNEG_MAGIC_LEN 6
#define NN_MAGIC_0 0xFD
#define NN_MAGIC_1 0xFC
#define NN_MAGIC_2 0x1E
#define NN_MAGIC_3 0x66
#define NN_MAGIC_4 0x6A
#define NN_MAGIC_5 0xB2
extern unsigned char NNMagicData[];
typedef enum {ns_initsent, ns_initack, ns_connectping, ns_finished, ns_canceled, ns_reportsent, ns_reportack } NegotiateState;
typedef enum {nr_success, nr_deadbeatpartner, nr_inittimeout, nr_pingtimeout, nr_unknownerror, nr_noresult } NegotiateResult;
typedef enum {ne_noerror, ne_allocerror, ne_socketerror, ne_dnserror} NegotiateError;
typedef void (*NegotiateProgressFunc)(NegotiateState state, void *userdata);
typedef void (*NegotiateCompletedFunc)(NegotiateResult result, SOCKET gamesocket, struct sockaddr_in *remoteaddr, void *userdata);
typedef void (*NatDetectionResultsFunc)(gsi_bool success, NAT nat);
NegotiateError NNBeginNegotiation(int cookie, int clientindex, NegotiateProgressFunc progresscallback, NegotiateCompletedFunc completedcallback, void *userdata);
NegotiateError NNBeginNegotiationWithSocket(SOCKET gamesocket, int cookie, int clientindex, NegotiateProgressFunc progresscallback, NegotiateCompletedFunc completedcallback, void *userdata);
void NNThink();
void NNProcessData(char *data, int len, struct sockaddr_in *fromaddr);
void native_fn_020b6c90(int cookie);
void NNFreeNegotiateList();
NegotiateError NNStartNatDetection(NatDetectionResultsFunc resultscallback);
extern char *Matchup2Hostname;
extern char *Matchup1Hostname;
#ifdef __cplusplus
}
#endif
#endif
struct _NATNegotiator
{
	SOCKET negotiateSock;
	SOCKET gameSock;
	int cookie;
	int clientindex;
	NegotiateState state;
	int initAckRecv[4];
	int retryCount;
	int maxRetryCount;
	unsigned long retryTime;
	unsigned int guessedIP;
	unsigned short guessedPort;
	unsigned char gotRemoteData;
	unsigned char sendGotRemoteData;
	NegotiateProgressFunc progressCallback;
	NegotiateCompletedFunc completedCallback;
	void *userdata;
	NegotiateResult result;
	SOCKET connectedSocket;
	struct sockaddr_in remoteaddr;
};
typedef struct _NATNegotiator* NATNegotiator;
extern DArray native_data_021d2bc4;
extern int native_fn_020a8c68(SOCKET,struct sockaddr*,int*);
#ifndef _AVAILABLE_H_
#define _AVAILABLE_H_
#ifdef __cplusplus
extern "C" {
#endif
#ifndef GSI_UNICODE
#define GSIStartAvailableCheck   GSIStartAvailableCheckA
#else
#define GSIStartAvailableCheck   GSIStartAvailableCheckW
#endif
extern char GSIACHostname[64];
typedef enum
{
	GSIACWaiting,
	GSIACAvailable,
	GSIACUnavailable,
	GSIACTemporarilyUnavailable
} GSIACResult;
void GSIStartAvailableCheck(const gsi_char * gamename);
GSIACResult GSIAvailableCheckThink(void);
void GSICancelAvailableCheck(void);
extern GSIACResult __GSIACResult;
extern char __GSIACGamename[64];
#ifdef __cplusplus
}
#endif
#endif
#ifndef _NNINTERNAL_H_
#define _NNINTERNAL_H_
#define MATCHUP1_HOSTNAME "natneg1." GSI_DOMAIN_NAME
#define MATCHUP2_HOSTNAME "natneg2." GSI_DOMAIN_NAME
#define MATCHUP3_HOSTNAME "natneg3." GSI_DOMAIN_NAME
#define MATCHUP_PORT1 27901
#define MATCHUP_PORT2 27901
#define MATCHUP_PORT3 27901
#define FINISHED_NOERROR 0
#define FINISHED_ERROR_DEADBEAT_PARTNER 1
#define FINISHED_ERROR_INIT_PACKETS_TIMEDOUT 2
#define INIT_RETRY_TIME 500
#define INIT_RETRY_COUNT 10
#define NNINBUF_LEN 512
#define PING_RETRY_TIME 700
#define PING_RETRY_COUNT 7
#define FINISHED_IDLE_TIME 5000
#define PARTNER_WAIT_TIME 60000
#define REPORT_RETRY_TIME 1000
#define REPORT_RETRY_COUNT 5
#define NN_PROTVER 3
#define NN_PT_GP  0
#define NN_PT_NN1 1
#define NN_PT_NN2 2
#define NN_PT_NN3 3
#define NN_INIT	0
#define NN_INITACK 1
#define NN_ERTTEST 2
#define NN_ERTACK 3
#define NN_STATEUPDATE 4
#define NN_CONNECT 5
#define NN_CONNECT_ACK 6
#define NN_CONNECT_PING 7
#define NN_BACKUP_TEST 8
#define NN_BACKUP_ACK 9
#define NN_ADDRESS_CHECK 10
#define NN_ADDRESS_REPLY 11
#define NN_NATIFY_REQUEST 12
#define NN_REPORT 13
#define NN_REPORT_ACK 14
#if !defined(_PS2) && !defined(_NITRO)
#pragma pack(1)
#endif
#define INITPACKET_SIZE BASEPACKET_SIZE + 9
#define INITPACKET_ADDRESS_OFFSET BASEPACKET_SIZE + 3
typedef struct _InitPacket
{
	unsigned char porttype;
	unsigned char clientindex;
	unsigned char usegameport;
	unsigned int localip;
	unsigned short localport;
} InitPacket;
#define REPORTPACKET_SIZE BASEPACKET_SIZE + 61
typedef struct _ReportPacket
{
	unsigned char porttype;
	unsigned char clientindex;
	unsigned char negResult;
	NatType natType;
	NatMappingScheme natMappingScheme;
	char gamename[50];
} ReportPacket;
#define CONNECTPACKET_SIZE BASEPACKET_SIZE + 8
typedef struct _ConnectPacket
{
	unsigned int remoteIP;
	unsigned short remotePort;
	unsigned char gotyourdata;
	unsigned char finished;
} ConnectPacket;
#define BASEPACKET_SIZE 12
#define BASEPACKET_TYPE_OFFSET 7
typedef struct _NatNegPacket {
	unsigned char magic[NATNEG_MAGIC_LEN];
	unsigned char version;
	unsigned char packettype;
	int cookie;
	union
	{
		InitPacket Init;
		ConnectPacket Connect;
		ReportPacket Report;
	} Packet;
} NatNegPacket;
#if !defined(_PS2) && !defined(_NITRO)
#pragma pack()
#endif
#endif
#define gsi_true 1
#define gsi_false 0
#define gsDebugBinary(...)
#define GSI_UNUSED(x) ((void)(x))
#define assert(x)
#define GS_ASSERT(x)
#define INVALID_SOCKET (-1)
#define SOCKET_ERROR (-1)
extern void*memset(void*,int,unsigned int);
extern void*memcpy(void*,const void*,unsigned int);
extern int memcmp(const void*,const void*,unsigned int);
extern void gsifree(void*);
extern unsigned int native_fn_020a8ef8(void);
#define htons(n) ((unsigned char)((n)>>8)|(((n)<<8)&0xff00))
#define ntohs(n) htons(n)
#define htonl(n) ((unsigned char)((unsigned int)(n)>>24)|(((unsigned int)(n)>>8)&0xff00)|(((unsigned int)(n)<<8)&0xff0000)|(((unsigned int)(n)<<24)&0xff000000))
#define ntohl(n) htonl(n)
#define SOCK_DGRAM 2
#define offsetof(T,m) ((unsigned int)&(((T*)0)->m))
#define IPPROTO_UDP 17
typedef unsigned char u8;
static inline void*copybytes(void*dst,const void*src,u32 n){u8*d=dst;const u8*s=src;if(n==4){d[0]=s[0];d[1]=s[1];d[2]=s[2];d[3]=s[3];}else if(n==2){d[0]=s[0];d[1]=s[1];}else if(n)do{*d++=*s++;}while(--n);return dst;}
#define memcpy copybytes
static inline void*copy8(void*dst,const void*src,u32 ignored){u8*d=dst;const u8*s=src;u32 left=8;do{*d++=*s++;}while(--left);return dst;}
void native_fn_020b6708(NATNegotiator neg);
