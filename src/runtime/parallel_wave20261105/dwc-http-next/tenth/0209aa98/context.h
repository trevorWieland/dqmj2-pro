typedef unsigned char u8;typedef unsigned short u16;typedef unsigned int u32;typedef unsigned long long u64;typedef unsigned long size_t;typedef int BOOL;
#define SDK_ASSERT(...)
#define SDK_ASSERTMSG(...)
#define NULL ((void*)0)
#define SDK_FINALROM 1
#define DWC_COMMONSTR_MAX_KEY_VALUE_LEN 4096
#define TRUE 1
#define FALSE 0
typedef enum {
    DWC_ERROR_NONE = 0,
    DWC_ERROR_DS_MEMORY_ANY,
    DWC_ERROR_AUTH_ANY,
    DWC_ERROR_AUTH_OUT_OF_SERVICE,
    DWC_ERROR_AUTH_STOP_SERVICE,
    DWC_ERROR_AC_ANY,
    DWC_ERROR_NETWORK,
    DWC_ERROR_GHTTP_ANY,
    DWC_ERROR_DISCONNECTED,
    DWC_ERROR_FATAL,
    DWC_ERROR_FRIENDS_SHORTAGE,
    DWC_ERROR_NOT_FRIEND_SERVER,
    DWC_ERROR_MO_SC_CONNECT_BLOCK,
    DWC_ERROR_SERVER_FULL,
    DWC_ERROR_ND_ANY,
    DWC_ERROR_ND_HTTP,
    DWC_ERROR_SVL_ANY,
    DWC_ERROR_SVL_HTTP,
    DWC_ERROR_PROF_ANY,
    DWC_ERROR_PROF_HTTP,
    DWC_ERROR_NUM
} DWCError;
typedef enum {
    DWC_ETYPE_NO_ERROR = 0,
    DWC_ETYPE_LIGHT,
    DWC_ETYPE_SHOW_ERROR,
    DWC_ETYPE_SHUTDOWN_FM,
    DWC_ETYPE_SHUTDOWN_GHTTP,
    DWC_ETYPE_SHUTDOWN_ND,
    DWC_ETYPE_DISCONNECT,
    DWC_ETYPE_FATAL,
    DWC_ETYPE_NUM
} DWCErrorType;
typedef int DWCAllocType;typedef void*(*DWCAllocEx)(DWCAllocType,u32,int);typedef void(*DWCFreeEx)(DWCAllocType,void*,u32);typedef struct{u32 signature;u32 size;u32 dummy[6];}DWCiAllocHeader;typedef struct{DWCFreeEx free;DWCAllocEx alloc;}DWCAllocatorState;extern DWCAllocatorState native_data_021d19b4;typedef struct{DWCError last;int code;}DWCErrorState;extern DWCErrorState native_data_021d19ac;
#define s_alloc native_data_021d19b4.alloc
#define s_free native_data_021d19b4.free
#define stDwcLastError native_data_021d19ac.last
#define stDwcErrorCode native_data_021d19ac.code
extern void*native_fn_0209aa0c(void*);extern void*native_fn_0209aa10(void*,u32);extern u32 native_fn_0209aa20(void*);extern void*native_fn_0209aa44(DWCAllocType,u32,int);extern void*native_fn_0209aa98(DWCAllocType,void*,u32,u32,int);extern void native_fn_0209aa64(DWCAllocType,void*,u32);extern void native_fn_02008e0c(const void*,void*,u32);extern int native_fn_020061ac(char*,u32,const char*,...);
#include "string.h"
extern const char native_data_020e0160[];
void * native_main_0209aa98 (DWCAllocType name, void * ptr, u32 oldsize, u32 newsize, int align)
;
