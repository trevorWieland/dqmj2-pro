typedef unsigned char GT2Byte;
typedef int GT2Bool;
typedef unsigned int u32;
typedef unsigned int size_t;
typedef struct GTI2Buffer { GT2Byte* buffer; int size; int len; } GTI2Buffer;
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
typedef unsigned char gsi_u8;
typedef unsigned short gsi_u16;
typedef unsigned int gsi_u32;
typedef signed int gsi_i32;
typedef unsigned int gsi_time;
typedef char gsi_char;
typedef int gsi_bool;
typedef int SOCKET;
#define _NITRO
#define GS_STATIC_CALLBACK
#define gsi_false 0
#define gsi_true 1
#define INVALID_SOCKET -1
#define SOCKET_ERROR -1
#define GSI_DOMAIN_NAME "gs.nintendowifi.net"
#define gsDebugFormat(...)
#define gsDebugBinary(...)
#define gsDebugHexDump(...)
#define INADDR_ANY 0
#define SOCK_DGRAM 2
#define IPPROTO_UDP 17
typedef struct sockaddr { unsigned char sa_len; unsigned char sa_family; char sa_data[6]; } SOCKADDR;
typedef struct sockaddr_in { unsigned char sin_len; unsigned char sin_family; unsigned short sin_port; IN_ADDR sin_addr; } SOCKADDR_IN;
extern void gsifree(void*);
extern char* strdup(const char*);
extern int strcmp(const char*,const char*);
extern int strncmp(const char*,const char*,unsigned int);
extern char* strcpy(char*,const char*);
extern char* strncpy(char*,const char*,unsigned int);
extern void* memset(void*,int,unsigned int);
extern int memcmp(const void*,const void*,unsigned int);
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
#ifndef _QR2_H_
#define _QR2_H_
#ifndef GSI_UNICODE
#define qr2_init			qr2_initA
#define qr2_init_socket		qr2_init_socketA
#define qr2_parse_query		qr2_parse_queryA
#define qr2_buffer_add		qr2_buffer_addA
#else
#define qr2_init			qr2_initW
#define qr2_init_socket		qr2_init_socketW
#define qr2_parse_query		qr2_parse_queryW
#define qr2_buffer_add		qr2_buffer_addW
#endif
#ifdef __cplusplus
extern "C" {
#endif
typedef enum
{e_qrnoerror,
e_qrwsockerror,
e_qrbinderror,
e_qrdnserror,
e_qrconnerror,
e_qrnochallengeerror,
qr2_error_t_count
} qr2_error_t;
typedef enum {key_server, key_player, key_team, key_type_count} qr2_key_type;
#define NUM_PORTS_TO_TRY 100
#define QR_MAGIC_1 0xFE
#define QR_MAGIC_2 0xFD
extern char qr2_hostname[64];
typedef struct qr2_implementation_s *qr2_t;
typedef struct qr2_keybuffer_s *qr2_keybuffer_t;
typedef struct qr2_buffer_s *qr2_buffer_t;
typedef struct qr2_ipverify_node_s *qr2_ipverify_node_t;
typedef void (*qr2_serverkeycallback_t)(int keyid, qr2_buffer_t outbuf, void *userdata);
typedef void (*qr2_playerteamkeycallback_t)(int keyid, int index, qr2_buffer_t outbuf, void *userdata);
typedef void (*qr2_keylistcallback_t)(qr2_key_type keytype, qr2_keybuffer_t keybuffer, void *userdata);
typedef int  (*qr2_countcallback_t)(qr2_key_type keytype, void *userdata);
typedef void (*qr2_adderrorcallback_t)(qr2_error_t error, gsi_char *errmsg, void *userdata);
typedef void (*qr2_natnegcallback_t)(int cookie, void *userdata);
typedef void (*qr2_clientmessagecallback_t)(gsi_char *data, int len, void *userdata);
typedef void (*qr2_publicaddresscallback_t)(unsigned int ip, unsigned short port, void *userdata);
typedef void (*qr2_clientconnectedcallback_t)(SOCKET gamesocket, struct sockaddr_in *remoteaddr, void *userdata);
typedef void (*qr2_denyqr2responsetoipcallback_t)(void *userdata, unsigned int sender_ip, int * result);
void qr2_register_natneg_callback(qr2_t qrec, qr2_natnegcallback_t nncallback);
void qr2_register_clientmessage_callback(qr2_t qrec, qr2_clientmessagecallback_t cmcallback);
void qr2_register_publicaddress_callback(qr2_t qrec, qr2_publicaddresscallback_t pacallback);
void qr2_register_clientconnected_callback(qr2_t qrec, qr2_clientconnectedcallback_t cccallback);
void qr2_register_denyresponsetoip_callback(qr2_t qrec, qr2_denyqr2responsetoipcallback_t dertoipcallback);
void qr2_register_key(int keyid, const gsi_char *key);
qr2_error_t qr2_init(qr2_t *qrec, const gsi_char *ip, int baseport, const gsi_char *gamename, const gsi_char *secret_key,
			int ispublic, int natnegotiate,
			qr2_serverkeycallback_t server_key_callback,
			qr2_playerteamkeycallback_t player_key_callback,
			qr2_playerteamkeycallback_t team_key_callback,
			qr2_keylistcallback_t key_list_callback,
			qr2_countcallback_t playerteam_count_callback,
			qr2_adderrorcallback_t adderror_callback,
			void *userdata);
qr2_error_t qr2_init_socket(qr2_t *qrec, SOCKET s, int boundport, const gsi_char *gamename, const gsi_char *secret_key,
					 int ispublic, int natnegotiate,
					 qr2_serverkeycallback_t server_key_callback,
					 qr2_playerteamkeycallback_t player_key_callback,
					 qr2_playerteamkeycallback_t team_key_callback,
					 qr2_keylistcallback_t key_list_callback,
					 qr2_countcallback_t playerteam_count_callback,
					 qr2_adderrorcallback_t adderror_callback,
					 void *userdata);
void qr2_think(qr2_t qrec);
void qr2_parse_query(qr2_t qrec, gsi_char *query, int len, struct sockaddr *sender);
void qr2_send_statechanged(qr2_t qrec);
void qr2_shutdown(qr2_t qrec);
gsi_bool qr2_keybuffer_add(qr2_keybuffer_t keybuffer, int keyid);
gsi_bool qr2_buffer_add(qr2_buffer_t outbuf, const gsi_char *value);
gsi_bool qr2_buffer_add_int(qr2_buffer_t outbuf, int value);
#define REQUEST_KEY_LEN 4
#define RECENT_CLIENT_MESSAGES_TO_TRACK 10
typedef void (*cdkey_process_t)(char *buf, int len, struct sockaddr *fromaddr);
#define QR2_IPVERIFY_TIMEOUT        4000
#define QR2_IPVERIFY_ARRAY_SIZE     200
#define QR2_IPVERIFY_MAXDUPLICATES  5
struct qr2_ipverify_info_s
{
	struct sockaddr_in addr;
	gsi_u32            challenge;
	gsi_time           createtime;
};
struct qr2_implementation_s
{
	SOCKET hbsock;
	char gamename[64];
	char secret_key[64];
	char instance_key[REQUEST_KEY_LEN];
	qr2_serverkeycallback_t server_key_callback;
	qr2_playerteamkeycallback_t player_key_callback;
	qr2_playerteamkeycallback_t team_key_callback;
	qr2_keylistcallback_t key_list_callback;
	qr2_countcallback_t playerteam_count_callback;
	qr2_adderrorcallback_t adderror_callback;
	qr2_natnegcallback_t nn_callback;
	qr2_clientmessagecallback_t cm_callback;
	qr2_publicaddresscallback_t pa_callback;
	gsi_time lastheartbeat;
	gsi_time lastka;
	int userstatechangerequested;
	int listed_state;
	int ispublic;
	int qport;
	int read_socket;
	int nat_negotiate;
	struct sockaddr_in hbaddr;
	cdkey_process_t cdkeyprocess;
	int client_message_keys[RECENT_CLIENT_MESSAGES_TO_TRACK];
	int cur_message_key;
	unsigned int publicip;
	unsigned short publicport;
	void *udata;
	gsi_u8 backendoptions;
struct qr2_ipverify_info_s ipverify[QR2_IPVERIFY_ARRAY_SIZE];
};
void qr2_parse_queryA(qr2_t qrec, char *query, int len, struct sockaddr *sender);
gsi_bool qr2_buffer_addA(qr2_buffer_t outbuf, const char *value);
qr2_error_t qr2_initA(qr2_t *qrec, const char *ip, int baseport, const char *gamename, const char *secret_key,
			int ispublic, int natnegotiate,
			qr2_serverkeycallback_t server_key_callback,
			qr2_playerteamkeycallback_t player_key_callback,
			qr2_playerteamkeycallback_t team_key_callback,
			qr2_keylistcallback_t key_list_callback,
			qr2_countcallback_t playerteam_count_callback,
			qr2_adderrorcallback_t adderror_callback,
			void *userdata);
qr2_error_t qr2_init_socketA(qr2_t *qrec, SOCKET s, int boundport, const char *gamename, const char *secret_key,
					 int ispublic, int natnegotiate,
					 qr2_serverkeycallback_t server_key_callback,
					 qr2_playerteamkeycallback_t player_key_callback,
					 qr2_playerteamkeycallback_t team_key_callback,
					 qr2_keylistcallback_t key_list_callback,
					 qr2_countcallback_t playerteam_count_callback,
					 qr2_adderrorcallback_t adderror_callback,
					 void *userdata);
#ifdef __cplusplus
}
#endif
#endif
#ifndef _QR2REGKEYS_H_
#define _QR2REGKEYS_H_
#ifdef __cplusplus
extern "C" {
#endif
#define MAX_REGISTERED_KEYS 254
#define NUM_RESERVED_KEYS 50
#define HOSTNAME_KEY		1
#define GAMENAME_KEY		2
#define GAMEVER_KEY			3
#define HOSTPORT_KEY		4
#define MAPNAME_KEY			5
#define GAMETYPE_KEY		6
#define GAMEVARIANT_KEY		7
#define NUMPLAYERS_KEY		8
#define NUMTEAMS_KEY		9
#define MAXPLAYERS_KEY		10
#define GAMEMODE_KEY		11
#define TEAMPLAY_KEY		12
#define FRAGLIMIT_KEY		13
#define TEAMFRAGLIMIT_KEY	14
#define TIMEELAPSED_KEY		15
#define TIMELIMIT_KEY		16
#define ROUNDTIME_KEY		17
#define ROUNDELAPSED_KEY	18
#define PASSWORD_KEY		19
#define GROUPID_KEY			20
#define PLAYER__KEY			21
#define SCORE__KEY			22
#define SKILL__KEY			23
#define PING__KEY			24
#define TEAM__KEY			25
#define DEATHS__KEY			26
#define PID__KEY			27
#define TEAM_T_KEY			28
#define SCORE_T_KEY			29
#define NN_GROUP_ID_KEY		30
#define COUNTRY_KEY			31
#define REGION_KEY			32
#ifndef GSI_UNICODE
	#define qr2_register_key	qr2_register_keyA
#else
	#define qr2_register_key	qr2_register_keyW
#endif
extern const char *qr2_registered_key_list[];
void qr2_register_key(int keyid, const gsi_char *key);
void qr2_internal_key_list_append(char* theKey);
void qr2_internal_key_list_free();
gsi_bool qr2_internal_is_master_only_key(const char * keyname);
void qr2_register_keyA(int keyid, const char *key);
void qr2_register_keyW(int keyid, const unsigned short *key);
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
#define gsi_is_false(x) ((x)==gsi_false)
#define gsi_is_true(x) ((x)!=gsi_false)
void qr2_think(qr2_t qrec);
void qr2_check_queries(qr2_t qrec);
void qr2_check_send_heartbeat(qr2_t qrec);
void qr2_send_statechanged(qr2_t qrec);
void qr2_shutdown(qr2_t qrec);
void send_keepalive(qr2_t qrec);
void handle_public_address(qr2_t qrec, char * buffer);
qr2_error_t qr2_init_socketA(qr2_t *qrec, SOCKET s, int boundport, const char *gamename, const char *secret_key,
					 int ispublic, int natnegotiate,
					 qr2_serverkeycallback_t server_key_callback,
					 qr2_playerteamkeycallback_t player_key_callback,
					 qr2_playerteamkeycallback_t team_key_callback,
					 qr2_keylistcallback_t key_list_callback,
					 qr2_countcallback_t playerteam_count_callback,
					 qr2_adderrorcallback_t adderror_callback,
					 void *userdata);
void enum_local_ips();
int get_sockaddrin(const char *host, int port, struct sockaddr_in *saddr, struct hostent **savehent);
extern qr2_t current_rec;
extern struct qr2_implementation_s static_qr2_rec;
extern int native_data_021d2ec8;
extern struct in_addr native_data_021d2ecc[5];
extern int sendto(SOCKET,const char*,int,int,const struct sockaddr*,int);
#define MASTER_PORT 27900
#define MASTER_ADDR "master." GSI_DOMAIN_NAME
#define FIRST_HB_TIME 10000
#define HB_TIME 60000
#define KA_TIME 20000
#define MIN_STATECHANGED_HB_TIME 10000
#define MAX_FIRST_COUNT 4
#define MAX_DATA_SIZE 1400
#define INBUF_LEN 256
#define PUBLIC_ADDR_LEN 12
#define QR2_OPTION_USE_QUERY_CHALLENGE 128
#define PACKET_QUERY              0x00
#define PACKET_CHALLENGE          0x01
#define PACKET_ECHO               0x02
#define PACKET_ECHO_RESPONSE      0x05
#define PACKET_HEARTBEAT          0x03
#define PACKET_ADDERROR           0x04
#define PACKET_CLIENT_MESSAGE     0x06
#define PACKET_CLIENT_MESSAGE_ACK 0x07
#define PACKET_KEEPALIVE          0x08
#define PACKET_PREQUERY_IP_VERIFY 0x09
#define MAX_LOCAL_IP 5
#define NATNEG_MAGIC_LEN 6
#define NN_MAGIC_0 0xFD
#define NN_MAGIC_1 0xFC
#define NN_MAGIC_2 0x1E
#define NN_MAGIC_3 0x66
#define NN_MAGIC_4 0x6A
#define NN_MAGIC_5 0xB2
#define QR2_EXFLAG_SPLIT		(1<<0)
#define QR2_SPLITNUM_MAX		7
#define QR2_SPLITNUM_FINALFLAG	(1<<7)
#define AVAILABLE_BUFFER_LEN(a) (MAX_DATA_SIZE - (a)->len)
typedef unsigned char uchar;
struct qr2_keybuffer_s
{
	uchar keys[MAX_REGISTERED_KEYS];
	int numkeys;
};
struct qr2_buffer_s
{
	char buffer[MAX_DATA_SIZE];
	int len;
};
void qr_add_packet_header(qr2_buffer_t,int,const char*);
void send_heartbeat(qr2_t,int);
void qr2_expire_ip_verify(qr2_t);
#define gsiSocketIsNotError(s) ((s)!=-1)
#define htons(n) ((unsigned char)((n)>>8)|(((n)<<8)&0xff00))
#define ntohs(n) htons(n)
#define htonl(n) ((unsigned char)((unsigned int)(n)>>24)|(((unsigned int)(n)>>8)&0xff00)|(((unsigned int)(n)<<8)&0xff0000)|(((unsigned int)(n)<<24)&0xff000000))
static inline void*copy4(void*dst,const void*src){unsigned char*d=dst;const unsigned char*s=src;d[0]=s[0];d[1]=s[1];d[2]=s[2];d[3]=s[3];return dst;}
extern char native_data_021d2f20[256];
extern HOSTENT* native_fn_020a8dc0(void);
void SocketShutDown(void);
int CanReceiveOnSocket(SOCKET);
