#define DWCi_AC_Alloc native_fn_020945d8
#define DWCi_AC_Free native_fn_02094600
#define DWCi_AC_FreeAll native_fn_0209463c
typedef unsigned char u8;typedef unsigned short u16;typedef unsigned long u32;typedef signed long s32;typedef unsigned long long u64;typedef int BOOL;typedef void*(*ACAlloc)(u32,s32);typedef void(*ACFree)(u32,void*,s32);
typedef struct{u8 connectType,skipNetCheck;}DWCACOption;typedef struct{ACAlloc alloc;ACFree free;u8 dmaNo,powerMode;DWCACOption option;}DWCACConfig;
typedef struct{ACAlloc alloc;ACFree free;u8 allocState,phase,phaseError,findAP;int error,errorTest;u8 endState,endType,endSequence,type;char apSpotInfo[10];u8 overrideType;}tagACHOLD;
typedef struct{u8 bytes[240];}DWCBmApInfo;typedef struct{DWCBmApInfo ap;u8 wifi[14];u16 crc;}DWCMemPage;
typedef struct{u8 find:4,duplicate:4;u8 type,channel,length,ssid[32];}tagACSL;typedef struct{u8 state,type,rssi;u8 channel:7,find:1;}tagACFL;typedef struct{u8 bytes[192];}WMBssDesc;typedef struct{u8 bytes[82];}WCMWepDesc;
typedef struct{DWCMemPage userInfo[3];tagACSL searchList[9];tagACFL findList[11];WMBssDesc bssDesc[11];u64 timeOut;WCMWepDesc wepKey;u8 dmaNo;u8 powerMode:2,authMode:2,aroundCount:4;u8 connectType:4,skipNetCheck:2,duplicateFlag:2;u8 connectApType,phaseBak,searchListNo,searchListNum;char searchChannel;u8 findListNum,connectNo,connectResult,count;u16 stealthChannel;}tagACWORK;
typedef struct{u8 bytes[88];}SOCConfig;typedef struct{ACAlloc alloc;ACFree free;void*bmworkarea;}DWCNetcheckParam;
typedef struct{void*wcmBuffer;SOCConfig*socConfig;DWCNetcheckParam*netCheck;tagACHOLD*acHold;tagACWORK*acWork;}DWCACGlobals;extern DWCACGlobals native_data_021d18cc;
#define acHold native_data_021d18cc.acHold
#define acWork native_data_021d18cc.acWork
#define wcmBuffer native_data_021d18cc.wcmBuffer
#define socConfig native_data_021d18cc.socConfig
#define netCheck native_data_021d18cc.netCheck
#define NULL ((void*)0)
#define TRUE 1
#define FALSE 0
#define DWC_Printf(...) ((void)0)
#define MI_CpuClear32(d,n) native_fn_02008c14(0,d,n)
void native_fn_02008c14(u32,void*,u32),native_fn_02008c28(const void*,void*,u32),native_fn_02008e0c(const void*,void*,u32),native_fn_02008d78(void*,int,u32);
void*DWCi_AC_Alloc(u32,s32);void DWCi_AC_Free(u32,void*,s32),DWCi_AC_FreeAll(void);int native_fn_020a4640(DWCMemPage*),native_fn_02089aa4(void*,u32);
BOOL native_main_02094284(DWCACConfig*);void*native_main_020945d8(u32,s32);void native_main_02094600(u32,void*,s32),native_main_0209463c(void);
