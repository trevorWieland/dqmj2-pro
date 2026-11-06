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
static inline unsigned short htons(unsigned short n){return (unsigned char)(n>>8)|((n<<8)&0xff00);}
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

