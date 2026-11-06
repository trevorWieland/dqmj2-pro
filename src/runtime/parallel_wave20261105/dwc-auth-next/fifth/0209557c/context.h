#define DWCi_AC_GetMemPtr native_fn_020946ec
#define DWCi_AC_Alloc native_fn_020945d8
#define DWCi_AC_Free native_fn_02094600
#define DWCi_AC_FreeAll native_fn_0209463c
typedef unsigned char u8;typedef unsigned short u16;typedef unsigned long u32;typedef signed long s32;typedef unsigned long long u64;typedef int BOOL;typedef void*(*ACAlloc)(u32,s32);typedef void(*ACFree)(u32,void*,s32);
typedef struct{u8 connectType,skipNetCheck;}DWCACOption;typedef struct{ACAlloc alloc;ACFree free;u8 dmaNo,powerMode;DWCACOption option;}DWCACConfig;
typedef struct{ACAlloc alloc;ACFree free;u8 allocState,phase,phaseError,findAP;int error,errorTest;u8 endState,endType,endSequence,type;char apSpotInfo[10];u8 overrideType;}tagACHOLD;
typedef struct{u8 ispId[32],ispPass[32],ssid[2][32],wep[4][16],ip[4],gateway[4],dns[2][4],netmask,wep2[4][5],authType;u8 wepMode:2,wepNotation:6;u8 setType,rsv[7],state;}DWCBmApInfo;typedef struct{DWCBmApInfo ap;u8 wifi[14];u16 crc;}DWCMemPage;
typedef struct{u8 find:4,duplicate:4;u8 type,channel,length,ssid[32];}tagACSL;typedef struct{u8 state,type,rssi;u8 channel:7,find:1;}tagACFL;typedef struct{u16 length,rssi;u8 bssid[6];u16 ssidLength;u8 ssid[32],opaque[148];}WMBssDesc;typedef struct{u8 bytes[82];}WCMWepDesc;
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

typedef unsigned char byte;void*DWCi_AC_GetMemPtr(u32);

typedef unsigned int uint;typedef unsigned long undefined4;typedef unsigned char uchar,undefined;u8 native_fn_02094818(u8);const u8*native_fn_0208b524(u16*);void native_fn_020072d0(const void*,u32);void native_fn_02096174(const char*,u8*);void native_main_02094530(const void*,const void*,int),native_main_020945bc(int,DWCBmApInfo*),native_main_020947b4(u8);u32 native_main_02094848(void);

typedef tagACSL ACSL;
#define SSID_NO_USER_NORMAL 0
#define SSID_NO_USER_AOSS 1
#define WM_SIZE_SSID 32
#define DWC_AC_AP_TYPE_USER1 0
#define DWC_AC_AP_TYPE_USB 3
#define DWC_AC_AP_TYPE_FREESPOT 5
#define DWC_AC_AP_TYPE_WAYPORT 6
#define DWC_AC_AP_TYPE_NINTENDOWFC 7
#define AP_TYPE_USER1 0
#define AP_TYPE_AOSS_USER1 3
#define AP_TYPE_USB 6
#define AP_TYPE_FREESPOT 8
#define AP_TYPE_WAYPORT 9
#define AP_TYPE_NINTENDOWFC 10
#define FREESPOT_SSID_LENGTH 8
#define WAYPORT_SSID_LENGTH 8
#define NINTENDOWFC_SSID_LENGTH 11
#define NINTENDO_USB_SSID_LENGTH 8
extern const u8 native_data_020dc400[8],native_data_020dea58[8],native_data_020dc3f8[8],native_data_020dc408[11];
#define FREESPOT_SSID native_data_020dc400
#define NINTENDO_USB_SSID native_data_020dea58
#define WAYPORT_SSID native_data_020dc3f8
#define NINTENDOWFC_SSID native_data_020dc408
#define MI_CpuCopy8 native_fn_02008e0c
u8 native_fn_0209557c(tagACWORK*);u8 native_main_0209557c(tagACWORK*),native_main_020954dc(tagACWORK*);u32 native_main_02095494(tagACWORK*);BOOL native_main_02095630(int,DWCMemPage*,ACSL*,int);
