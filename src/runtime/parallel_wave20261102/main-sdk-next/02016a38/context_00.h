typedef unsigned char u8;
typedef unsigned short int u16;
typedef unsigned long u32;
typedef signed short int s16;
void native_fn_02008be0(u16 data, void * destp, u32 size);
void native_fn_02008bf8(const void * srcp, void * destp, u32 size);
static inline void MI_CpuFill16 (void * dest, u16 data, u32 size)
{
	((void) 0) ;
	((void) 0) ;
	native_fn_02008be0(data, dest, size);
}
static inline void MI_CpuCopy16 (const void * src, void * dest, u32 size)
{
	((void) 0) ;
	((void) 0) ;
	((void) 0) ;
	native_fn_02008bf8(src, dest, size);
}
static inline void MI_CpuClear16 (void * dest, u32 size)
{
	MI_CpuFill16(dest, 0, size);
}
typedef enum WMErrCode {
	WM_ERRCODE_SUCCESS               = 0,
	WM_ERRCODE_FAILED                = 1,
	WM_ERRCODE_OPERATING             = 2,
	WM_ERRCODE_ILLEGAL_STATE         = 3,
	WM_ERRCODE_WM_DISABLE            = 4,
	WM_ERRCODE_NO_KEYSET             = 5,
	WM_ERRCODE_NO_DATASET            = 5,
	WM_ERRCODE_INVALID_PARAM         = 6,
	WM_ERRCODE_NO_CHILD              = 7,
	WM_ERRCODE_FIFO_ERROR            = 8,
	WM_ERRCODE_TIMEOUT               = 9,
	WM_ERRCODE_SEND_QUEUE_FULL       = 10,
	WM_ERRCODE_NO_ENTRY              = 11,
	WM_ERRCODE_OVER_MAX_ENTRY        = 12,
	WM_ERRCODE_INVALID_POLLBITMAP    = 13,
	WM_ERRCODE_NO_DATA               = 14,
	WM_ERRCODE_SEND_FAILED           = 15,
	WM_ERRCODE_DCF_TEST,
	WM_ERRCODE_WL_INVALID_PARAM,
	WM_ERRCODE_WL_LENGTH_ERR,
	WM_ERRCODE_FLASH_ERROR,
	WM_ERRCODE_MAX
} WMErrCode;
typedef void (*WMCallbackFunc) (void * arg);
typedef struct WMGameInfo {
	u16 magicNumber;
	u8 ver;
	u8 platform;
	u32 ggid;
	u16 tgid;
	u8 userGameInfoLength;
	union {
		u8 gameNameCount_attribute;
		u8 attribute;
	};
	u16 parentMaxSize;
	u16 childMaxSize;
	union {
		u16 userGameInfo[112 / sizeof(u16)];
		struct {
			u16 userName[8 / sizeof(u16)];
			u16 gameName[16 / sizeof(u16)];
			u16 padd1[44];
		} old_type;
	};
} WMGameInfo, WMgameInfo;
typedef struct WMBssDesc {
        u16 length;
        u16 rssi;
        u8 bssid[6 ];
        u16 ssidLength;
        u8 ssid[32 ];
        u16 capaInfo;
        struct {
            u16 basic;
            u16 support;
        } rateSet;
        u16 beaconPeriod;
        u16 dtimPeriod;
        u16 channel;
        u16 cfpPeriod;
        u16 cfpMaxDuration;
        u16 gameInfoLength;
        u16 otherElementCount;
        WMGameInfo gameInfo;
    } WMBssDesc, WMbssDesc;
WMErrCode native_fn_020140f8(WMCallbackFunc callback,
                         const u16 * userGameInfo, u16 userGameInfoSize,
                         u32 ggid, u16 tgid, u8 attr);
extern const u16 (*ctrdgi_fl_maxtime);
typedef struct {
	u16 palette[16 ];
	u16 data[512 / 2];
} MBIconInfo;
typedef struct {
	u8 favoriteColor : 4;
	u8 playerNo : 4;
	u8 nameLength;
	u16 name[10 ];
} MBUserInfo;
typedef void (*MBSendVolatCallbackFunc) (u32 ggid);
typedef struct MBGameInfoFixed {
	MBIconInfo icon;
	MBUserInfo parent;
	u8 maxPlayerNum;
	u8 pad[1];
	u16 gameName[48 ];
	u16 gameIntroduction[96 ];
} MBGameInfoFixed, MbGameInfoFixed;
typedef struct MBGameInfoVolatile {
	u8 nowPlayerNum;
	u8 pad[1];
	u16 nowPlayerFlag;
	u16 changePlayerFlag;
	MBUserInfo member[15 ];
	u8 userVolatData[8 ];
} MBGameInfoVolatile, MbGameInfoVolatile;
typedef enum MbBeaconDataAttr {
	MB_BEACON_DATA_ATTR_FIXED_NORMAL = 0,
	MB_BEACON_DATA_ATTR_FIXED_NO_ICON,
	MB_BEACON_DATA_ATTR_VOLAT
} MBBeaconDataAttr, MbBeaconDataAttr;
typedef struct MBGameInfo {
	MBGameInfoFixed fixed;
	MBGameInfoVolatile volat;
	u16 broadcastedPlayerFlag;
	u8 dataAttr;
	u8 seqNoFixed;
	u8 seqNoVolat;
	u8 fileNo;
	u8 pad[2];
	u32 ggid;
	struct MBGameInfo * nextp;
} MBGameInfo, MbGameInfo;
enum {
	MB_SEND_VOLAT_CALLBACK_TIMMING_BEFORE,
	MB_SEND_VOLAT_CALLBACK_TIMMING_AFTER
};
typedef struct MBGameInfoRecvList {
	MBGameInfo gameInfo;
	WMBssDesc bssDesc;
	u32 getFlagmentFlag;
	u32 allFlagmentFlag;
	u16 getPlayerFlag;
	s16 lifetimeCount;
	u16 linkLevel;
	u8 beaconNo;
	u8 sameBeaconRecvCount;
} MBGameInfoRecvList, MbGameInfoRecvList;
typedef struct MbBeaconRecvStatus {
	u16 usingGameInfoFlag;
	u16 usefulGameInfoFlag;
	u16 validGameInfoFlag;
	u16 nowScanTargetFlag;
	s16 nowLockTimeCount;
	s16 notFoundLockTargetCount;
	u16 scanCountUnit;
	u8 pad[2];
	MBGameInfoRecvList list[16 ];
} MbBeaconRecvStatus;
typedef void (*MbScanLockFunc)         (u8 * macAddress);
typedef void (*MbScanUnlockFunc)       (void);
u16 native_fn_0201641c(const u16 * buf, int length);
typedef enum MbBeaconState {
	MB_BEACON_STATE_STOP = 0,
	MB_BEACON_STATE_READY,
	MB_BEACON_STATE_FIXED_START,
	MB_BEACON_STATE_FIXED,
	MB_BEACON_STATE_VOLAT_START,
	MB_BEACON_STATE_VOLAT,
	MB_BEACON_STATE_NEXT_GAME
} MbBeaconState;
typedef struct MbBeacon {
	u32 ggid;
	u8 dataAttr :2;
	u8 fileNo :6;
	u8 seqNoFixed;
	u8 seqNoVolat;
	u8 beaconNo;
	union {
		struct {
			u16 sum;
			u8 flagmentNo;
			u8 flagmentMaxNum;
			u8 size;
			u8 rsv;
			u8 data[((112 - 8) - 6) ];
		} fixed;
		struct {
			u16 sum;
			u8 nowPlayerNum;
			u8 pad[1];
			u16 nowPlayerFlag;
			u16 changePlayerFlag;
			MBUserInfo member[(((112 - 8) - 8) / sizeof(MBUserInfo)) ];
			u8 userVolatData[8 ];
		} volat;
	} data;
} MbBeacon;
typedef struct MbBeaconSendStatus {
	MBGameInfo * gameInfoListTop;
	MBGameInfo * nowGameInfop;
	u8 * srcp;
	u8 state;
	u8 seqNoFixed;
	u8 seqNoVolat;
	u8 flagmentNo;
	u8 flagmentMaxNum;
	u8 beaconNo;
	u8 pad[2];
} MbBeaconSendStatus;
void native_fn_02016a08(void);
void native_main_02016a38(u32 ggid, u16 tgid, u8 attribute);
typedef struct {
MbScanUnlockFunc field_0000;
MbScanLockFunc field_0004;
MbBeacon * field_0008;
MbBeaconRecvStatus * field_000c;
u32 field_0010;
MBSendVolatCallbackFunc field_0014;
MbBeaconSendStatus field_0018;
unsigned char padding_002c[20];
__attribute__ ((aligned(32))) MbBeacon field_0040;
unsigned char padding_00b0[16];
__attribute__ ((aligned(32))) WMBssDesc field_00c0;
MbBeaconRecvStatus field_0180;
} NativeStorage_020e68c0;
extern NativeStorage_020e68c0 native_data_main_020e68c0;
void native_fn_02016a08 (void);
