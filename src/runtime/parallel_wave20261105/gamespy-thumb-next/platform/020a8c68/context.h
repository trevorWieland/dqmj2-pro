typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef long long s64;
typedef int SOCKET;
typedef struct{u8 len,family,data[6];} SOCKADDR;
typedef struct{u8 len,family;u16 port;u32 addr;} SOCKADDR_IN;
typedef struct{int fd;short events,revents;} SOPollFD;
#define NULL ((void*)0)
#define NITRO_SOCKET_ERROR -1
#define SOC_POLLRDNORM 1
#define SOC_POLLWRNORM 8
#define SOC_POLLHUP 64
#define SOC_POLLERR 32
void *memcpy(void*,const void*,u32);
int native_fn_020a8b4c(int,int);
int native_fn_020902f0(SOCKET,const SOCKADDR*);
int native_fn_02090310(SOCKET,const SOCKADDR*);
int native_fn_02090378(SOCKET,char*,int,int,SOCKADDR*);
int native_fn_020903f8(SOCKET,const char*,int,int,const SOCKADDR*);
int native_fn_020904ec(SOCKET,SOCKADDR*);
int native_fn_020907f4(SOPollFD*,u32,s64);
