#define GP_ZIPCODE_LEN 11
#define GP_COUNTRYCODE_LEN 3
#define GP_PLACE_LEN 128
typedef int GPEnum;
typedef struct
{
  char * nick;
  char * uniquenick;
  char * email;
  char * firstname;
  char * lastname;
  char * homepage;
  int icquin;
  char zipcode[GP_ZIPCODE_LEN];
  char countrycode[GP_COUNTRYCODE_LEN];
  float longitude; 
  float latitude;  
  char place[GP_PLACE_LEN];  
  int birthday;
  int birthmonth;
  int birthyear;
  GPEnum sex;
  int publicmask;
  char * aimname;
  int pic;
  int occupationid;
  int industryid;
  int incomeid;
  int marriedid;
  int childcount;
  int interests1;
  int ownership1;
  int conntypeid;
} GPIInfoCache;
typedef struct{void*profileTable;int num,numBuddies,numBlocked;}GPIProfileList;
typedef unsigned char u8;typedef unsigned short u16;typedef unsigned int u32;typedef void*GPConnection;typedef int GPResult,GPProfile,GPEnum,GPIBool;
typedef struct{char*buffer;int size,len,pos;}GPIBuffer;
typedef struct{void(*callback)(GPConnection*,void*,void*);void*param;}GPICallback;
typedef struct{char errorString[256];GPIBool infoCaching,infoCachingBuddyAndBlockOnly,simulation,firewall;char nick[31],uniquenick[21],email[51],password[31];int sessKey,userid,profileid,partnerID;GPICallback callbacks[9];int cmSocket,connectState;GPIBuffer socketBuffer;char*inputBuffer;int inputBufferSize;GPIBuffer outputBuffer;char mHeader[16];u16 peerPort;int nextOperationID,numSearches;GPEnum lastStatusState;u32 hostIp,hostPrivateIp;u16 queryPort,hostPort;u32 sessionFlags;char richStatus[256],gameType[33],gameVariant[33],gameMapName[33];void*extendedInfoKeys;char lastStatusString[256],lastLocationString[256];int errorCode;GPIBool fatalError;void*diskCache,*operationList;GPIProfileList profileList;}GPIConnection;

#define NULL ((void*)0)
#define GP_NICK_LEN 31
#define GP_EMAIL_LEN 51
#define GP_NO_ERROR 0
#define GPIFalse 0
#define GPITrue 1
#define GSI_UNUSED(x) ((void)(x))
typedef struct{int buddyIndex;GPEnum status;char*statusString,*locationString;u32 ip;u16 port;GPEnum quietModeFlags;}GPIBuddyStatus;
typedef struct{int buddyIndex;GPEnum statusState;char*richStatus,*gameType,*gameVariant,*gameMapName;u32 sessionFlags,buddyIp;u16 buddyPort;u32 hostIp,hostPrivateIp;u16 queryPort,hostPort;GPEnum quietModeFlags;int productId;void*extendedInfoKeys;}GPIBuddyStatusInfo;
typedef struct GPIProfile{int profileId,userId;GPIBuddyStatus*buddyStatus;GPIBuddyStatusInfo*buddyStatusInfo;GPIInfoCache*cache;char*authSig;int requestCount;char*peerSig;}GPIProfile;
typedef GPIBool(*gpiProfileMapFunc)(GPConnection*,GPIProfile*,void*);
typedef struct{char*nick,*email;GPIProfile**profile;GPIBool found;}GPIFindProfileByUserData;
typedef struct{GPConnection*connection;gpiProfileMapFunc func;void*data;}GPIProfileMapData;
typedef struct{int index;GPIProfile*profile;}GPIFindProfileData;
int native_fn_020a89f0(void*,const void*);void*native_fn_020a8ab0(void*,int(*)(void*,void*),void*);
GPIBool native_fn_020b0bd0(GPConnection*,gpiProfileMapFunc,void*);int native_fn_020b0bbc(void*,void*);
GPIBool native_fn_020b0b5c(GPConnection*,GPIProfile*,void*);GPIBool native_fn_020b0c00(GPConnection*,GPIProfile*,void*);
#define TableRemove native_fn_020a89f0
#define TableMapSafe2 native_fn_020a8ab0
#define gpiProfileMap native_fn_020b0bd0
#define gpiProfileMapCallback native_fn_020b0bbc
#define gpiCheckProfileForUser native_fn_020b0b5c
#define gpiCheckForBuddy native_fn_020b0c00

typedef struct GPIOperation_s{int type;void*data;GPIBool blocking;GPICallback callback;int state,id;GPResult result;struct GPIOperation_s*pnext;}GPIOperation;
#define GPI_PROFILE_SEARCH 3

#define assert(x)
void*native_fn_020a8a3c(void*,const void*);void native_fn_020a89a4(void*,const void*);GPIBool native_fn_020b0a50(GPConnection*,GPProfile,GPIProfile**);void*memset(void*,int,u32);
#define TableLookup native_fn_020a8a3c
#define TableEnter native_fn_020a89a4
#define gpiGetProfile native_fn_020b0a50

typedef GPIProfile*pGPIProfile;void native_fn_020af3c8(pGPIProfile);void*native_fn_020a927c(u32);char*native_fn_020a8ea0(const char*);
#define gpiFreeInfoCache native_fn_020af3c8
#define gsimalloc native_fn_020a927c
#define goastrdup native_fn_020a8ea0

typedef char gsi_char;typedef void(*GPCallback)(GPConnection*,void*,void*);typedef struct GPProfileSearchMatch GPProfileSearchMatch;
#define GP_NICK_LEN                 31
#define GP_UNIQUENICK_LEN           21
#define GP_FIRSTNAME_LEN            31
#define GP_LASTNAME_LEN             31
#define GP_EMAIL_LEN                51
#define GP_PASSWORD_LEN             31
#define GP_PASSWORDENC_LEN          ((((GP_PASSWORD_LEN+2)*4)/3)+1)
#define GP_HOMEPAGE_LEN             76
#define GP_ZIPCODE_LEN              11
#define GP_COUNTRYCODE_LEN          3
#define GP_PLACE_LEN                128
#define GP_AIMNAME_LEN              51
#define GP_ERROR_STRING_LEN         256
#define GP_AUTHTOKEN_LEN            256
#define GP_PARTNERCHALLENGE_LEN     256
#define GP_CDKEY_LEN                65
#define GP_CDKEYENC_LEN             ((((GP_CDKEY_LEN+2)*4)/3)+1)
#define GP_LOGIN_TICKET_LEN         25
#define GP_RICH_STATUS_LEN          256
#define GP_STATUS_BASIC_STR_LEN     33
typedef struct
{
  GPResult result;
  GPProfile profile;
  gsi_char uniquenick[GP_UNIQUENICK_LEN];
} GPConnectResponseArg;
typedef struct
{
  GPResult result;
  int numMatches;
  GPEnum more;
  GPProfileSearchMatch * matches;
} GPProfileSearchResponseArg;
typedef struct
{
  GPResult result;
  GPProfile profile;
  gsi_char nick[GP_NICK_LEN];
  gsi_char uniquenick[GP_UNIQUENICK_LEN];
  gsi_char email[GP_EMAIL_LEN];
  gsi_char firstname[GP_FIRSTNAME_LEN];
  gsi_char lastname[GP_LASTNAME_LEN];
  gsi_char homepage[GP_HOMEPAGE_LEN];
  int icquin;
  gsi_char zipcode[GP_ZIPCODE_LEN];
  gsi_char countrycode[GP_COUNTRYCODE_LEN];
  float longitude; 
  float latitude;  
  gsi_char place[GP_PLACE_LEN];  
  int birthday;
  int birthmonth;
  int birthyear;
  GPEnum sex;
  GPEnum publicmask;
  gsi_char aimname[GP_AIMNAME_LEN];
  int pic;
  int occupationid;
  int industryid;
  int incomeid;
  int marriedid;
  int childcount;
  int interests1;
  int ownership1;
  int conntypeid;
} GPGetInfoResponseArg;



#define GP_CHECK_CACHE 1
#define GP_BLOCKING 1
#define GPI_GET_INFO 2
#define GP_MEMORY_ERROR 1
#define CHECK_RESULT(f) {GPResult checked=(f);if(checked!=GP_NO_ERROR)return checked;}
#define Error(c,r,s) {native_fn_020b2c88(c,s);return r;}
void native_fn_020ae0e4(const GPIInfoCache*,GPGetInfoResponseArg*);GPResult native_fn_020afa1c(GPConnection*,int,void*,GPIOperation**,GPEnum,GPCallback,void*);GPResult native_fn_020acc28(GPConnection*,GPICallback,void*,const GPIOperation*,int);void native_fn_020afad8(GPConnection*,GPIOperation*);GPResult native_fn_020af1c4(GPConnection*,int,int);GPResult native_fn_020aae0c(GPConnection*,int);void native_fn_020b2c88(GPConnection*,const char*);extern const char native_data_020e0db8[];
#define gpiInfoCacheToArg native_fn_020ae0e4
#define gpiAddOperation native_fn_020afa1c
#define gpiAddCallback native_fn_020acc28
#define gpiRemoveOperation native_fn_020afad8
#define gpiSendGetInfo native_fn_020af1c4
#define gpiProcess native_fn_020aae0c
