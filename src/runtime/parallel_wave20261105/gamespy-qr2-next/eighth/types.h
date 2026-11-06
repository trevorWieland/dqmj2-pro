typedef unsigned char GT2Byte;
typedef int GT2Bool;
typedef unsigned int u32;
typedef unsigned int size_t;
typedef struct in_addr { unsigned int s_addr; } IN_ADDR;
typedef struct hostent { char* h_name; char** h_aliases; short h_addrtype; short h_length; char** h_addr_list; } HOSTENT;
#define NULL ((void*)0)
#define assert(x)
#define GS_ASSERT(x)
#define GSI_UNUSED(x) ((void)(x))
#define GT2True 1
#define GT2False 0
#define AF_INET 2
#define INADDR_NONE 0xffffffff
#define GTI2_CHALLENGE_LEN 32
#define GTI2_RESPONSE_LEN 32
extern void* gsimalloc(unsigned int);
extern void* memcpy(void*,const void*,unsigned int);
extern void* memmove(void*,const void*,unsigned int);
extern unsigned int strlen(const char*);
extern char* strchr(const char*,int);
extern int sprintf(char*,const char*,...);
extern int atoi(const char*);
extern int isdigit(int);
extern int abs(int);
extern int rand(void);
extern void srand(unsigned int);
extern unsigned int current_time(void);
extern unsigned short htons(unsigned short);
extern unsigned short ntohs(unsigned short);
extern unsigned int htonl(unsigned int);
extern unsigned int ntohl(unsigned int);
extern unsigned int inet_addr(const char*);
extern char* inet_ntoa(IN_ADDR);
extern HOSTENT* gethostbyname(const char*);
extern HOSTENT* gethostbyaddr(const char*,int,int);
typedef unsigned int gsi_time;
typedef unsigned int gsi_u32;
typedef int gsi_bool;
typedef int SOCKET;
#define _NITRO
#define INVALID_SOCKET (-1)
#define SOCKET_ERROR (-1)
#define GS_STATIC_CALLBACK
#define gsi_true 1
#define gsi_false 0
extern void gsifree(void*);
extern void* gsirealloc(void*,unsigned int);
extern int memcmp(const void*,const void*,unsigned int);
extern void* memset(void*,int,unsigned int);
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
DArray ArrayNew(int elemSize, int numElemsToAllocate,
                ArrayElementFreeFn elemFreeFn);
void ArrayFree(DArray array);
int ArrayLength(const DArray array);
void *ArrayNth(DArray array, int n);
void ArrayAppend(DArray array, const void *newElem);
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
 #ifndef _HASHTABLE_H
#define _HASHTABLE_H
typedef struct HashImplementation *HashTable;
typedef int (*TableHashFn)(const void *elem, int numBuckets);
typedef int (*TableCompareFn)(const void *elem1, const void *elem2);
typedef void (*TableMapFn)(void *elem, void *clientData);
typedef int (*TableMapFn2)(void *elem, void *clientData);
typedef void (*TableElementFreeFn)(void *elem);
#ifdef __cplusplus
extern "C" {
#endif
HashTable TableNew(int elemSize, int nBuckets,
                   TableHashFn hashFn, TableCompareFn compFn,
                      TableElementFreeFn freeFn);
HashTable TableNew2(int elemSize, int nBuckets, int nChains,
                   TableHashFn hashFn, TableCompareFn compFn,
                      TableElementFreeFn freeFn);
void TableFree(HashTable table);
int TableCount(HashTable table);
void TableEnter(HashTable table, const void *newElem);
int TableRemove(HashTable table, const void *delElem);
void *TableLookup(HashTable table, const void *elemKey);
void TableMap(HashTable table, TableMapFn fn, void *clientData);
void TableMapSafe(HashTable table, TableMapFn fn, void *clientData);
void * TableMap2(HashTable table, TableMapFn2 fn, void *clientData);
void * TableMapSafe2(HashTable table, TableMapFn2 fn, void *clientData);
void TableClear(HashTable table);
#ifdef __cplusplus
}
#endif
#endif
#ifndef _GT2_H_
#define _GT2_H_
#ifdef __cplusplus
extern "C" {
#endif
typedef int GT2Bool;
#define GT2False 0
#define GT2True 1
typedef unsigned char GT2Byte;
typedef struct GTI2Socket * GT2Socket;
typedef struct GTI2Connection * GT2Connection;
typedef unsigned short GT2MessageID;
typedef enum
{
	GT2Success,
	GT2OutOfMemory,
	GT2Rejected,
	GT2NetworkError,
	GT2AddressError,
	GT2DuplicateAddress,
	GT2TimedOut,
	GT2NegotiationError,
	GT2InvalidConnection,
	GT2InvalidMessage,
	GT2SendFailed
} GT2Result;
typedef enum
{
	GT2Connecting,
	GT2Connected,
	GT2Closing,
	GT2Closed
} GT2ConnectionState;
typedef enum
{
	GT2LocalClose,
	GT2RemoteClose,
	GT2CommunicationError,
	GT2SocketError,
	GT2NotEnoughMemory
} GT2CloseReason;
extern char GT2ChallengeKey[33];
typedef void (* gt2SocketErrorCallback)
(
	GT2Socket socket
);
GT2Result gt2CreateSocket
(
	GT2Socket * socket,
	const char * localAddress,
	int outgoingBufferSize,
	int incomingBufferSize,
	gt2SocketErrorCallback callback
);
GT2Result gt2CreateAdHocSocket
(
	GT2Socket * socket,
	const char * localAddress,
	int outgoingBufferSize,
	int incomingBufferSize,
	gt2SocketErrorCallback callback
);
#ifdef _XBOX
GT2Result gt2CreateVDPSocket
(
	GT2Socket * socket,
	const char * localAddress,
	int outgoingBufferSize,
	int incomingBufferSize,
	gt2SocketErrorCallback callback
);
#endif
void gt2CloseSocket(GT2Socket socket);
void gt2Think(GT2Socket socket);
GT2Result gt2SendRawUDP
(
	GT2Socket socket,
	const char * remoteAddress,
	const GT2Byte * message,
	int len
);
typedef void (* gt2ConnectedCallback)
(
	GT2Connection connection,
	GT2Result result,
	GT2Byte * message,
	int len
);
typedef void (* gt2ReceivedCallback)
(
	GT2Connection connection,
	GT2Byte * message,
	int len,
	GT2Bool reliable
);
typedef void (* gt2ClosedCallback)
(
	GT2Connection connection,
	GT2CloseReason reason
);
typedef void (* gt2PingCallback)
(
	GT2Connection connection,
	int latency
);
typedef struct
{
	gt2ConnectedCallback connected;
	gt2ReceivedCallback received;
	gt2ClosedCallback closed;
	gt2PingCallback ping;
} GT2ConnectionCallbacks;
GT2Result gt2Connect
(
	GT2Socket socket,
	GT2Connection * connection,
	const char * remoteAddress,
	const GT2Byte * message,
	int len,
	int timeout,
	GT2ConnectionCallbacks * callbacks,
	GT2Bool blocking
);
GT2Result gt2Send
(
	GT2Connection connection,
	const GT2Byte * message,
	int len,
	GT2Bool reliable
);
void gt2Ping(GT2Connection connection);
void gt2CloseConnection(GT2Connection connection);
void gt2CloseConnectionHard(GT2Connection connection);
void gt2CloseAllConnections(GT2Socket socket);
void gt2CloseAllConnectionsHard(GT2Socket socket);
typedef void (* gt2ConnectAttemptCallback)
(
	GT2Socket socket,
	GT2Connection connection,
	unsigned int ip,
	unsigned short port,
	int latency,
	GT2Byte * message,
	int len
);
void gt2Listen(GT2Socket socket, gt2ConnectAttemptCallback callback);
GT2Bool gt2Accept(GT2Connection connection, GT2ConnectionCallbacks * callbacks);
void gt2Reject(GT2Connection connection, const GT2Byte * message, int len);
GT2MessageID gt2GetLastSentMessageID(GT2Connection connection);
GT2Bool gt2WasMessageIDConfirmed(GT2Connection connection, GT2MessageID messageID);
typedef void (* gt2SendFilterCallback)
(
	GT2Connection connection,
	int filterID,
	const GT2Byte * message,
	int len,
	GT2Bool reliable
);
typedef void (* gt2ReceiveFilterCallback)
(
	GT2Connection connection,
	int filterID,
	GT2Byte * message,
	int len,
	GT2Bool reliable
);
GT2Bool gt2AddSendFilter
(
	GT2Connection connection,
	gt2SendFilterCallback callback
);
void gt2RemoveSendFilter
(
	GT2Connection connection,
	gt2SendFilterCallback callback
);
void gt2FilteredSend
(
	GT2Connection connection,
	int filterID,
	const GT2Byte * message,
	int len,
	GT2Bool reliable
);
GT2Bool gt2AddReceiveFilter
(
	GT2Connection connection,
	gt2ReceiveFilterCallback callback
);
void gt2RemoveReceiveFilter
(
	GT2Connection connection,
	gt2ReceiveFilterCallback callback
);
void gt2FilteredReceive
(
	GT2Connection connection,
	int filterID,
	GT2Byte * message,
	int len,
	GT2Bool reliable
);
typedef GT2Bool (* gt2UnrecognizedMessageCallback)
(
	GT2Socket socket,
	unsigned int ip,
	unsigned short port,
	GT2Byte * message,
	int len
);
SOCKET gt2GetSocketSOCKET(GT2Socket socket);
void gt2SetUnrecognizedMessageCallback(GT2Socket socket, gt2UnrecognizedMessageCallback callback);
GT2Socket gt2GetConnectionSocket(GT2Connection connection);
GT2ConnectionState gt2GetConnectionState(GT2Connection connection);
unsigned int gt2GetRemoteIP(GT2Connection connection);
unsigned short gt2GetRemotePort(GT2Connection connection);
unsigned int gt2GetLocalIP(GT2Socket socket);
unsigned short gt2GetLocalPort(GT2Socket socket);
int gt2GetIncomingBufferSize(GT2Connection connection);
int gt2GetIncomingBufferFreeSpace(GT2Connection connection);
int gt2GetOutgoingBufferSize(GT2Connection connection);
int gt2GetOutgoingBufferFreeSpace(GT2Connection connection);
void gt2SetSocketData(GT2Socket socket, void * data);
void * gt2GetSocketData(GT2Socket socket);
void gt2SetConnectionData(GT2Connection connection, void * data);
void * gt2GetConnectionData(GT2Connection connection);
unsigned int gt2NetworkToHostInt(unsigned int i);
unsigned int gt2HostToNetworkInt(unsigned int i);
unsigned short gt2HostToNetworkShort(unsigned short s);
unsigned short gt2NetworkToHostShort(unsigned short s);
const char * gt2AddressToString
(
	unsigned int ip,
	unsigned short port,
	char string[22]
);
GT2Bool gt2StringToAddress
(
	const char * string,
	unsigned int * ip,
	unsigned short * port
);
const char * gt2IPToHostInfo(unsigned int ip, char *** aliases, unsigned int *** ips);
const char * gt2StringToHostInfo(const char * string, char *** aliases, unsigned int *** ips);
const char * gt2IPToHostname(unsigned int ip);
const char * gt2StringToHostname(const char * string);
char ** gt2IPToAliases(unsigned int ip);
char ** gt2StringToAliases(const char * string);
unsigned int ** gt2IPToIPs(unsigned int ip);
unsigned int ** gt2StringToIPs(const char * string);
#ifdef _XBOX
unsigned int gt2XnAddrToIP(XNADDR theAddr, XNKID theKeyId);
GT2Bool gt2IPToXnAddr(int ip, XNADDR *theAddr, XNKID *theKeyId);
#endif
void gt2IpToMac(gsi_u32 ip,char *mac);
gsi_u32 gt2MacToIp(const char *mac);
typedef void (* gt2DumpCallback)
(
	GT2Socket socket,
	GT2Connection connection,
	unsigned int ip,
	unsigned short port,
	GT2Bool reset,
	const GT2Byte * message,
	int len
);
void gt2SetSendDump(GT2Socket socket, gt2DumpCallback callback);
void gt2SetReceiveDump(GT2Socket socket, gt2DumpCallback callback);
#ifdef __cplusplus
}
#endif
#endif
#ifndef _GT2_AUTH_H_
#define _GT2_AUTH_H_
#define GTI2_CHALLENGE_LEN           32
#define GTI2_RESPONSE_LEN            32
#ifdef __cplusplus
extern "C" {
#endif
GT2Byte * gti2GetChallenge
(
	GT2Byte * buffer
);
GT2Byte * gti2GetResponse
(
	GT2Byte * buffer,
	const GT2Byte * challenge
);
GT2Bool gti2CheckResponse
(
	const GT2Byte * response1,
	const GT2Byte * response2
);
#ifdef __cplusplus
}
#endif
#endif
