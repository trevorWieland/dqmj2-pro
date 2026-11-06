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
extern Control*control;
extern int api_02006e24(void*,void*,int);
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
typedef void*(*Alloc)(u32,int);typedef void(*Free)(u32,void*,int);typedef u32(*Mask)(u32);
typedef struct Pair{u32 lo,hi;}Pair;
typedef struct State{volatile u32 f0,f4;u32 mutex8[6];u32 f20,f24;Alloc alloc;Free free;u32 f30,f34;char text38[8];u32 f40;u32 gap44[93];volatile int error1b8;u32 mutex1bc[6];u32 gap1d4[512];u32 f9d4;u32 gap9d8[3];Mask mask9e4;const void*config9e8;u32 flag9ec;u32 gap9f0[5];Pair paira04;u32 gapa0c;u32 threada10[48];u32 stackad0[512];}State;
extern State*native_data_021d3028;extern const char empty_text[];extern const u32 config_words[];extern u32 config_value;
extern void api_02007074(void*);extern char*api_02019d20(char*,const char*,u32);extern u32 api_020b9908(u32);extern void api_020b92b4(void*);
extern void native_fn_0200708c(void*);extern void native_fn_02007110(void*);
extern void api_020b90ec(u32);
extern void api_020b9328(void);
extern void api_020b9364(void);
extern void api_020b9404(void);
extern void api_020b94b0(void);
extern void api_020b95d8(void);
extern void api_020b9650(void);
extern void api_020b97bc(void);
extern void native_fn_020b90bc(u32);extern int native_fn_0209045c(int,int);extern void native_fn_020b9d08(u32,int);extern u32 api_020b8e6c(void);extern u32 api_020b86c4(void);extern void native_fn_0209a9d0(void);
typedef struct Status{u32 prefix[5];Result request;void(*callback)(u32);u32 extra40,extra44;}Status;extern Status*native_data_021d3030;
typedef struct ErrorPair{u32 code;int detail;}ErrorPair;extern ErrorPair native_data_021d3038;
extern int native_fn_020b8748(void);extern int native_fn_020b8f8c(void);extern u32 native_fn_020b9c2c(void);extern void native_fn_0209aa64(u32,void*,u32);extern int api_020b9c74(u32,u32);extern int api_020b8780(Result*);
