typedef unsigned int u32;typedef void*GPConnection;typedef int GPResult,GPEnum;
#define GP_CHILDCOUNT 1821
#define GP_CONNECTIONID 1811
#define GP_CONNECTIONSPEED 1812
#define GP_CPUBRANDID 1804
#define GP_CPUSPEED 1805
#define GP_FEMALE 1281
#define GP_HASNETWORK 1813
#define GP_ICQUIN 1798
#define GP_INCOMEID 1819
#define GP_INDUSTRYID 1818
#define GP_INTERESTS1 1822
#define GP_MALE 1280
#define GP_MARRIEDID 1820
#define GP_MEMORY 1806
#define GP_NO_ERROR 0
#define GP_OCCUPATIONID 1817
#define GP_PARAMETER_ERROR 2
#define GP_PAT 1282
#define GP_PIC 1816
#define GP_SEX 1803
#define GP_VIDEOCARD1RAM 1808
#define GP_VIDEOCARD2RAM 1810
#define GP_ZIPCODE 1800
GPResult native_fn_020ae8e8(GPConnection*,const char*,const char*),native_fn_020ae918(GPConnection*,const char*,const char*);int native_fn_0200616c(char*,const char*,...);void native_fn_020b2c88(GPConnection*,const char*);
#define gpiSendLocalInfo native_fn_020ae8e8
#define gpiSendUserInfo native_fn_020ae918
#define sprintf native_fn_0200616c
#define CHECK_RESULT(f) {GPResult checked=(f);if(checked!=GP_NO_ERROR)return checked;}
#define Error(c,r,s) {native_fn_020b2c88(c,s);return r;}
extern const char native_data_020e0cf8[];
extern const char native_data_020e0d10[];
extern const char native_data_020e0d50[];
extern const char native_data_020e0d68[];
extern const char native_data_020e0d70[];
extern const char native_data_020e0d78[];
extern const char native_data_020e0d80[];
extern const char native_data_020e0d88[];
extern const char native_data_020e0d90[];
extern const char native_data_020e0d98[];
extern const char native_data_020e0e08[];
extern const char native_data_020e0e1c[];
extern const char native_data_020e0e20[];
extern const char native_data_020e0e24[];
extern const char native_data_020e0e28[];
extern const char native_data_020e0e2c[];
extern const char native_data_020e0e3c[];
extern const char native_data_020e0e4c[];
extern const char native_data_020e0e58[];
extern const char native_data_020e0e64[];
extern const char native_data_020e0e74[];
extern const char native_data_020e0e84[];
extern const char native_data_020e0e94[];
extern const char native_data_020e0ea8[];
extern const char native_data_020e0eb8[];
