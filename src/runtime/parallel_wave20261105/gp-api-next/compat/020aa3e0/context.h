typedef struct{void*profileTable;int num,numBuddies,numBlocked;}GPIProfileList;
typedef unsigned char u8;typedef unsigned short u16;typedef unsigned int u32;typedef void*GPConnection;typedef int GPResult,GPProfile,GPEnum,GPIBool;
typedef struct{char*buffer;int size,len,pos;}GPIBuffer;
typedef struct{void(*callback)(GPConnection*,void*,void*);void*param;}GPICallback;
typedef struct{char errorString[256];GPIBool infoCaching,infoCachingBuddyAndBlockOnly,simulation,firewall;char nick[31],uniquenick[21],email[51],password[31];int sessKey,userid,profileid,partnerID;GPICallback callbacks[9];int cmSocket,connectState;GPIBuffer socketBuffer;char*inputBuffer;int inputBufferSize;GPIBuffer outputBuffer;char mHeader[16];u16 peerPort;int nextOperationID,numSearches;GPEnum lastStatusState;u32 hostIp,hostPrivateIp;u16 queryPort,hostPort;u32 sessionFlags;char richStatus[256],gameType[33],gameVariant[33],gameMapName[33];void*extendedInfoKeys;char lastStatusString[256],lastLocationString[256];int errorCode;GPIBool fatalError;void*diskCache,*operationList;GPIProfileList profileList;}GPIConnection;
#define NULL ((void*)0)
#define GP_PARAMETER_ERROR 2
#define GP_NO_ERROR 0
#define GPI_DISCONNECTED 4
#define GP_REASON_LEN 1025
#define Error(c,r,s) do{native_fn_020b2c88(c,s);return r;}while(0)
void native_fn_020b2c88(GPConnection*,const char*);
void native_fn_020b2a38(char*,const char*,u32);
GPResult native_fn_020ac6f4(GPConnection*,GPIBuffer*,const char*);
GPResult native_fn_020ac710(GPConnection*,GPIBuffer*,int);
#define strzcpy native_fn_020b2a38
#define gpiAppendStringToBuffer native_fn_020ac6f4
#define gpiAppendIntToBuffer native_fn_020ac710
extern const char native_data_020e0480[];
extern const char native_data_020e04b4[];
extern const char native_data_020e0470[];
extern const char native_data_020e04a8[];
extern const char native_data_020e0498[];
extern const char native_data_020e048c[];
extern const char native_data_020e0440[];
#define GP_STATUS_STRING_LEN 256
#define GP_LOCATION_STRING_LEN 256
int native_fn_0201d800(const char*,const char*);
#define strcmp native_fn_0201d800
extern const char native_data_020e04f4[];
extern const char native_data_020e050c[];
extern const char native_data_020e04dc[];
extern const char native_data_020e0518[];
extern const char native_data_020e0528[];

#define GPITrue 1
extern int native_data_021d23ec;
#define __GSIACResult native_data_021d23ec
#define GSIACAvailable 1
GPResult native_fn_020aa894(GPConnection*,int,int,int);
#define gpiInitialize native_fn_020aa894
GPResult native_fn_020aec50(GPConnection*,GPEnum,int);
#define gpiSetInfoi native_fn_020aec50
GPResult native_fn_020ac404(GPConnection*,GPProfile);
#define gpiAuthBuddyRequest native_fn_020ac404
typedef struct{int buddyIndex;GPEnum status;char*statusString,*locationString;u32 ip;u16 port;GPEnum quietModeFlags;}GPIBuddyStatus;
typedef struct{int buddyIndex;GPEnum statusState;char*richStatus,*gameType,*gameVariant,*gameMapName;u32 sessionFlags,buddyIp;u16 buddyPort;u32 hostIp,hostPrivateIp;u16 queryPort,hostPort;GPEnum quietModeFlags;int productId;void*extendedInfoKeys;}GPIBuddyStatusInfo;
typedef struct GPIProfile{int profileId,userId;GPIBuddyStatus*buddyStatus;GPIBuddyStatusInfo*buddyStatusInfo;void*cache;char*authSig;int requestCount;char*peerSig;int blocked,blockIndex,buddyOrBlockCache;}GPIProfile;
int native_fn_020b0a50(GPConnection*,int,GPIProfile**);int native_fn_020b0ca8(GPIProfile*);void native_fn_020b0b48(GPConnection*,GPIProfile*);void native_fn_020a929c(void*);
#define gpiGetProfile native_fn_020b0a50
#define gpiCanFreeProfile native_fn_020b0ca8
#define gpiRemoveProfile native_fn_020b0b48
#define gsifree native_fn_020a929c

typedef struct{GPProfile profile;GPEnum status;char statusString[256],locationString[256];u32 ip;int port;GPEnum quietModeFlags;}GPBuddyStatus;
GPIProfile*native_fn_020b0c2c(GPConnection*,int);void*native_fn_0201b208(void*,int,u32);void native_fn_020ade3c(GPConnection*,GPIBool);GPResult native_fn_020aa9b4(GPConnection*);
#define gpiFindBuddy native_fn_020b0c2c
#define memset native_fn_0201b208
#define gpiDisconnect native_fn_020ade3c
#define gpiReset native_fn_020aa9b4
#define GPIFalse 0
#define assert(x) ((void)0)
extern const char native_data_020e04bc[],native_data_020e04cc[];

#define GPI_BM_MESSAGE 1
GPResult native_fn_020abfe4(GPConnection*,int,int,const char*,int,void*);
#define gpiSendBuddyMessage native_fn_020abfe4
extern const char native_data_020e0534[];

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

#define GP_DONE 0x600
GPResult native_fn_020ad144(GPConnection*,const char*,const char*,const char*,const char*,const char*,const char*,const char*,GPEnum,GPIBool,GPEnum,GPCallback,void*);
GPResult native_fn_020b0ecc(GPConnection*,const char*,const char*,const char*,const char*,const char*,int,int,GPEnum,GPCallback,void*);
GPResult native_fn_020af244(GPConnection*,GPProfile,GPEnum,GPEnum,GPCallback,void*);
#define gpiConnect native_fn_020ad144
#define gpiProfileSearch native_fn_020b0ecc
#define gpiGetInfo native_fn_020af244
extern const char native_data_020e042c[],native_data_020e043c[];
