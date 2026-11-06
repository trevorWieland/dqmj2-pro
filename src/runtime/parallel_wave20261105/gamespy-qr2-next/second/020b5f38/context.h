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
extern void* native_fn_0201b19c(void*,const void*,unsigned int);
extern void* memmove(void*,const void*,unsigned int);
extern unsigned int native_fn_0201d69c(const char*);
extern char* strchr(const char*,int);
extern int native_fn_0200616c(char*,const char*,...);
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
extern char* native_fn_0209073c(IN_ADDR);
extern HOSTENT* gethostbyname(const char*);
extern HOSTENT* gethostbyaddr(const char*,int,int);
extern int native_data_021d2948;
extern char native_data_021d294c[2][22];
extern const char native_data_020e1718[6];
extern const char native_data_020e1720[3];
extern const char native_data_020e1724[4];
