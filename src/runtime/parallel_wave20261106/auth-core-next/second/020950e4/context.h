#define DWCi_AC_GetMemPtr native_fn_020946ec
#define DWCi_AC_Alloc native_fn_020945d8
#define DWCi_AC_Free native_fn_02094600
#define DWCi_AC_FreeAll native_fn_0209463c
typedef unsigned char u8;typedef unsigned short u16;typedef unsigned long u32;typedef signed long s32;typedef unsigned long long u64;typedef int BOOL;typedef void*(*ACAlloc)(u32,s32);typedef void(*ACFree)(u32,void*,s32);
typedef struct{u8 connectType,skipNetCheck;}DWCACOption;typedef struct{ACAlloc alloc;ACFree free;u8 dmaNo,powerMode;DWCACOption option;}DWCACConfig;
typedef struct{ACAlloc alloc;ACFree free;u8 allocState,phase,phaseError,findAP;int error,errorTest;u8 endState,endType,endSequence,type;char apSpotInfo[10];u8 overrideType;}tagACHOLD;
typedef struct{u8 ispId[32],ispPass[32],ssid[2][32],wep[4][16],ip[4],gateway[4],dns[2][4],netmask,wep2[4][5],authType;u8 wepMode:2,wepNotation:6;u8 setType,rsv[7],state;}DWCBmApInfo;typedef struct{DWCBmApInfo ap;u8 wifi[14];u16 crc;}DWCMemPage;
typedef struct{u8 find:4,duplicate:4;u8 type,channel,length,ssid[32];}tagACSL;typedef struct{u8 state,type,rssi;u8 channel:7,find:1;}tagACFL;typedef struct{u16 length,rssi;u8 bssid[6];u16 ssidLength;u8 ssid[32];u16 capaInfo;u8 unconsumed46to53[8];u16 channel;u8 unconsumed56to191[136];}WMBssDesc;typedef struct{u8 mode,keyId,key[80];}WCMWepDesc;
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
typedef tagACWORK ACWORK;typedef DWCMemPage tagDWCMemPage;typedef u64 OSTick;
typedef struct{u32 addr;}SOCInAddr;
typedef struct{int dmano;void*pbdbuffer;u32 nbdbuffer,nbdmode;}IWConfig;
u64 native_fn_02007a9c(void);u8 native_fn_02095bd0(ACWORK*,u8),native_fn_020953e0(int),native_fn_02095cec(ACWORK*),native_fn_020959d0(ACWORK*);
void native_fn_02095d34(void*,void*,int,int),native_fn_02095864(u8),native_fn_02094790(int),native_fn_02094d18(void*);
int native_fn_0208a268(void),native_fn_02089ba0(const IWConfig*,void(*)(void*));
u8 native_fn_0209477c(void);u32 native_fn_02095e5c(ACWORK*),native_fn_02095fa0(void),native_fn_02095e9c(ACWORK*),native_fn_02095f14(void),native_fn_02095f34(ACWORK*),native_fn_02095f8c(ACWORK*),native_fn_02090554(void);
void native_fn_020990f0(void),native_fn_02099058(void),native_fn_020960d0(ACWORK*);
s32 native_fn_02099138(void),native_fn_02099164(void);uint native_fn_02096050(u8*);
int native_fn_02090580(const SOCInAddr*,const SOCInAddr*);
extern const u8 native_data_020dc3c8[6],native_data_020dc3d0[32];
#define OS_GetTick native_fn_02007a9c
#define OS_TicksToMilliSeconds(tick) (((u64)(tick)*64)/33514)
#define NextSearchCheck native_fn_02095bd0
#define DWCi_AC_GetStealthChannel native_fn_02095818
#define ScanStart native_fn_02095d34
#define DWCi_AC_MakeSearchList native_fn_020953e0
#define CheckStartStealthSearch native_fn_02095cec
#define SearchAround2ndLap native_fn_020959d0
#define DWCi_AC_SearchReStart native_fn_02095864
#define WCM_GetPhase native_fn_0208a268
#define WCM_StartupAsync native_fn_02089ba0
#define DWCi_AC_SetError native_fn_02094790
#define DWCi_AC_CallBackWCM native_fn_02094d18
#define DWCi_AC_GetPhase native_fn_0209477c
#define ConnectTestStart native_fn_02095e5c
#define ConnectTestRetry native_fn_02095fa0
#define GetIPAddress native_fn_02095e9c
#define ConnectTestCreate native_fn_02095f14
#define ConnectTestProcess native_fn_02095f34
#define ConnectTestEnd native_fn_02095f8c
#define DWC_Netcheck_Abort native_fn_020990f0
#define DWC_Netcheck_Destroy native_fn_02099058
#define SOC_GetHostID native_fn_02090554
#define CheckSetDNS native_fn_020960d0
#define DWC_Netcheck_GetError native_fn_02099138
#define DWC_Netcheck_GetReturnCode native_fn_02099164
#define DWCi_ConvConnectAPType native_fn_02094818
#define ConvAddress native_fn_02096050
#define SOC_SetResolver native_fn_02090580
#define SOC_HtoNl(v) ((u32)((((u32)(v)>>24)&0x000000ff)|(((u32)(v)>>8)&0x0000ff00)|(((u32)(v)<<8)&0x00ff0000)|(((u32)(v)<<24)&0xff000000)))
#define SEARCH_CHANNEL_TIME_OUT 150
#define SEARCH_STEALTH_TIME_OUT 150
#define AC_PHASE_SEARCH_AROUND 3
#define AC_PHASE_SEARCH_DIFFER_CHANNEL 4
#define AC_PHASE_SEARCH_STEALTH 5
#define AC_PHASE_SEARCH_END 6
#define AC_PHASE_ERROR_OCCURED 17
#define AC_PHASE_START 1
#define AC_PHASE_SEARCH_START 2
#define AC_ERROR_WCM_START_UP 1
#define SEARCH_LIST_AROUND 0
#define SEARCH_LIST_DIFFER_CHANNEL 1
#define SEARCH_LIST_STEALTH 2
#define AROUND_SEARCH_NUM_MAX 1
#define ALLOC_NAME_WORK 16
#define WCM_PHASE_WAIT 1
#define WCM_RESULT_FAILURE 1
#define WCM_RESULT_REJECT 4
#define WCM_BSSID_ANY ((void*)native_data_020dc3c8)
#define WCM_ESSID_ANY ((void*)native_data_020dc3d0)
#define WCM_OPTION_SCANTYPE_ACTIVE 0x00300000

static inline void iScanStartDifferChannel(ACWORK*wk){wk->timeOut=OS_GetTick();ScanStart(wk->bssDesc[wk->searchListNo].bssid,wk->bssDesc[wk->searchListNo].ssid,wk->bssDesc[wk->searchListNo].channel-1,WCM_OPTION_SCANTYPE_ACTIVE);}

static inline void iScanStartStealth( ACWORK *wk )
{
	
	wk->timeOut = OS_GetTick();
	ScanStart( WCM_BSSID_ANY,
			   wk->searchList[ wk->searchListNo ].ssid,
			   wk->searchChannel,
			   WCM_OPTION_SCANTYPE_ACTIVE
			 );
}

typedef signed char s8;
s8 native_fn_02095818(u16);
u8 native_fn_02095910(ACWORK*),native_fn_02095c54(ACWORK*,u8),native_fn_02095954(ACWORK*),native_fn_02095a10(ACWORK*),native_fn_02095aec(ACWORK*);
#define SearchStart native_fn_02095910
#define SearchEndCheck native_fn_02095c54
#define SearchAround native_fn_02095954
#define SearchDifferChannel native_fn_02095a10
#define SearchStealth native_fn_02095aec
#define AC_PHASE_CONNECT_START 7
#define WCM_PHASE_IDLE 3
#define WCM_PHASE_SEARCH 6
#define DWC_AC_SEARCH_START_CHANNEL1 0
#define DWC_AC_SEARCH_START_CHANNEL2 1
#define SEARCH_AROUND_TIME_OUT 300
#define WCM_OPTION_SCANTYPE_PASSIVE 0x00200000
static inline void iScanStartAround(ACWORK*wk){wk->timeOut=OS_GetTick();ScanStart(WCM_BSSID_ANY,WCM_ESSID_ANY,wk->searchChannel,WCM_OPTION_SCANTYPE_PASSIVE);}

u8 native_main_02095910( ACWORK *wk );
u32 native_fn_02094f58(ACWORK*),native_fn_020950ac(ACWORK*),native_fn_020950c8(ACWORK*);
BOOL native_fn_020950e4(ACWORK*,int,WCMWepDesc*);
int native_fn_02089ef8(const WMBssDesc*,const WCMWepDesc*,u32);
u32 native_fn_020949e4(const WMBssDesc*);u8 native_fn_0209545c(const WMBssDesc*);
int native_fn_0201d914(const char*,const char*,u32);
void native_fn_020961bc(const char*,u8*),native_fn_0209615c(const char*,u8*);
#define GetConnectType native_fn_02094f58
#define GetWepKey native_fn_020950e4
#define GetPowerMode native_fn_020950ac
#define GetAuthMode native_fn_020950c8
#define WCM_ConnectAsync native_fn_02089ef8
#define DWCi_AC_CheckNintendoSSID native_fn_020949e4
#define DWCi_AC_CheckFreespot native_fn_0209545c
#define strncmp native_fn_0201d914
#define MI_CpuClear8(p,n) native_fn_02008d78(p,0,n)
#define MI_CpuCopy8 native_fn_02008e0c
#define DWCi_AC_GetNintendoUSBWepKey native_fn_020961bc
#define DWCi_AC_GetNintendoShopWepKey native_fn_0209615c

BOOL native_main_020950e4(ACWORK*wk,int type,WCMWepDesc*wep);
