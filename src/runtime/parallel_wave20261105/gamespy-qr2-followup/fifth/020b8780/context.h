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
typedef struct Result {u32 words[10];}Result;
typedef struct Event {u32 words[5];unsigned char payload[];}Event;
typedef int(*Callback)(Event*);
typedef struct Control {u32 prefix[9];Result*active;Callback callback;u32 completion;void(*boundary)(int,Event*);u32 thread[48];u32 stack[512];}Control;
extern Control*native_data_021d3020;
extern int native_fn_02006e24(void*,void*,int);
extern int api_02006ff8(void*,void*,int);
extern int api_02006eb8(void*,void*,int);
extern int api_020b8d44(Callback);
extern void api_020b8da0(void);
extern int api_020b9030(void);
typedef void(*BoundaryCallback)(int,Event*);
extern void api_020b9068(BoundaryCallback);
extern void api_020b8d14(int,Event*);
extern void api_02006b7c(unsigned int);
extern void api_020b8878(void);
extern void api_020b88a8(void);
extern void api_020b88d0(void);
extern void api_020b8958(void);
extern void api_020b89b4(void);
extern void api_020b8b0c(void);
extern void api_020b8ab0(void);
extern void api_020b8b5c(void);
extern void api_020b8bc4(void);
extern void api_020b8c2c(void);
extern void api_020b8c7c(void);
extern void api_020b8d80(void);
extern int api_020b8fd8(void);
extern int api_020b88fc(Event*);
extern int api_020b8dd8(Event*);
extern int api_020b8dfc(Event*);
extern int api_020b8dc4(void*);
extern void api_02008e0c(const void*,void*,u32);
typedef struct ThreadInfo{u32 unknown;void*current;}ThreadInfo;
extern ThreadInfo threadInfo;
extern void api_02008d78(void*,unsigned char,u32);
extern void api_02006dfc(void*,void*,int);
extern u32 api_02006b74(void*);
extern void api_020065f0(void*,void(*)(void*),void*,void*,u32,u32);
extern void api_02006ab0(void*,u32);
extern void api_020b87e4(void*);
extern void api_02006c70(void);extern int api_020068c0(void*);extern void api_0200698c(void*);extern void api_02006ca4(void);extern int api_0209afe8(void);extern void api_020b9998(void);extern void api_0209b6e4(void);extern int api_0209a930(int*);
