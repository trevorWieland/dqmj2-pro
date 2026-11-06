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
void NNCancel(int cookie);
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
