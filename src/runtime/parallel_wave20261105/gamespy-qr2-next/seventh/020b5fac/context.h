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
extern unsigned int strlen(const char*);
extern char* native_fn_0201d948(const char*,int);
extern int sprintf(char*,const char*,...);
extern int native_fn_0201f274(const char*);
extern int abs(int);
extern int rand(void);
extern void srand(unsigned int);
extern unsigned int current_time(void);
extern unsigned short htons(unsigned short);
extern unsigned short ntohs(unsigned short);
extern unsigned int htonl(unsigned int);
extern unsigned int ntohl(unsigned int);
extern unsigned int native_fn_020a8c84(const char*);
extern char* inet_ntoa(IN_ADDR);
extern HOSTENT* native_fn_0209046c(const char*);
extern HOSTENT* gethostbyaddr(const char*,int,int);
#define GTI2_STACK_HOSTLEN_MAX 256
extern const unsigned short native_data_020d8e04[128];
static inline int isdigit(int c){return (c<0||c>=128)?0:(native_data_020d8e04[c]&8); }
