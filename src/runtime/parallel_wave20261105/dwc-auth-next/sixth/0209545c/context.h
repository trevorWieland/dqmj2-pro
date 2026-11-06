typedef unsigned char u8;typedef unsigned short u16;typedef unsigned long u32;typedef signed long s32;typedef unsigned long long u64;typedef unsigned int uint;
typedef struct{u8 bytes[240];}DWCBmApInfo;typedef struct{DWCBmApInfo ap;u8 wifi[14];u16 crc;}DWCMemPage;
typedef struct{u8 find:4,duplicate:4;u8 type,channel,length,ssid[32];}tagACSL;typedef struct{u8 state,type,rssi;u8 channel:7,find:1;}tagACFL;
typedef struct{u16 length,rssi;u8 bssid[6];u16 ssidLength;u8 ssid[32];u16 capaInfo;struct{u16 basic,support;}rateSet;u16 beaconPeriod,dtimPeriod,channel;u8 opaque[136];}WMBssDesc;
typedef struct{u8 bytes[82];}WCMWepDesc;
typedef struct{DWCMemPage userInfo[3];tagACSL searchList[9];tagACFL findList[11];WMBssDesc bssDesc[11];u64 timeOut;WCMWepDesc wepKey;u8 dmaNo;u8 powerMode:2,authMode:2,aroundCount:4;u8 connectType:4,skipNetCheck:2,duplicateFlag:2;u8 connectApType,phaseBak,searchListNo,searchListNum;char searchChannel;u8 findListNum,connectNo,connectResult,count;u16 stealthChannel;}tagACWORK;
void*native_fn_020946ec(u32);int native_fn_020949e4(WMBssDesc*);extern const u8 native_data_020dc400[8];
#define DWCi_AC_GetMemPtr native_fn_020946ec
#define FREESPOT_SSID native_data_020dc400
u8 native_main_0209545c(WMBssDesc*);
