#ifndef J2P_SDK187_BEACON_TYPES_H
#define J2P_SDK187_BEACON_TYPES_H
#include "../20261101_wl_counter504/wl_complete_types.h"
typedef union {
    u16 Data;
    struct {
        u16 ESS : 1;
        u16 IBSS : 1;
        u16 CFPollable : 1;
        u16 CFPollRequest : 1;
        u16 Privacy : 1;
        u16 ShortPreamble : 1;
        u16 rsv6 : 1;
        u16 rsv7 : 1;
        u16 rsv8 : 1;
        u16 rsv9 : 1;
        u16 rsv10 : 1;
        u16 rsv11 : 1;
        u16 rsv12 : 1;
        u16 rsv13 : 1;
        u16 rsv14 : 1;
        u16 rsv15 : 1;
    } Bit;
} CAPA_INFO, *LPCAPA_INFO;
typedef struct {
    u8 ID;
    u8 Length;
    u8 SSID[32];
} SSID_ELEMENT, *LPSSID_ELEMENT;
typedef struct {
    u8 ID;
    u8 Length;
    u8 SupportedRate[2];
} SUP_RATE_ELEMENT, *LPSUP_RATE_ELEMENT;
typedef struct {
    u8 ID;
    u8 Length;
    u8 CurrChannel;
} DS_PARAM_ELEMENT, *LPDS_PARAM_ELEMENT;
typedef struct {
    u8 ID;
    u8 Length;
    u8 OUI[3];
    u8 SubType;
    u8 ActZone[2];
    u8 VTSF[2];
    u8 GameInfo[3];
} GAME_INFO_ELEMENT, *LPGAME_INFO_ELEMENT;
typedef struct {
    u32 TimeStamp[2];
    u16 BeaconInterval;
    CAPA_INFO CapaInfo;
    u8 Buf[sizeof(SSID_ELEMENT) + sizeof(SUP_RATE_ELEMENT) + sizeof(DS_PARAM_ELEMENT) + sizeof(GAME_INFO_ELEMENT) + 0];
    u8 pad[2];
} BEACON_BODY, *LPBEACON_BODY;
#endif
