typedef unsigned char uint8_t;typedef unsigned long uint32_t;
#define GETU32(pt) (((uint32_t)(pt)[0]<<24)^((uint32_t)(pt)[1]<<16)^((uint32_t)(pt)[2]<<8)^((uint32_t)(pt)[3]))
#define PUTU32(ct,st) {(ct)[0]=(uint8_t)((st)>>24);(ct)[1]=(uint8_t)((st)>>16);(ct)[2]=(uint8_t)((st)>>8);(ct)[3]=(uint8_t)(st);}
extern int native_ov006_021f0944(uint32_t*,const uint8_t*,int);
extern int native_ov006_021f0bfc(uint32_t*,const uint8_t*,int);
extern void native_ov006_021f0d8c(const uint32_t*,int,const uint8_t*,uint8_t*);
extern void native_ov006_021f1148(const uint32_t*,int,const uint8_t*,uint8_t*);
extern const uint32_t native_data_ov006_02208890[10];
#define rcon native_data_ov006_02208890
extern const uint32_t native_data_ov006_022094b8[256];
#define Te0 native_data_ov006_022094b8
extern const uint32_t native_data_ov006_022098b8[256];
#define Te1 native_data_ov006_022098b8
extern const uint32_t native_data_ov006_02209cb8[256];
#define Te2 native_data_ov006_02209cb8
extern const uint32_t native_data_ov006_0220a0b8[256];
#define Te3 native_data_ov006_0220a0b8
extern const uint32_t native_data_ov006_0220a4b8[256];
#define Te4 native_data_ov006_0220a4b8
extern const uint32_t native_data_ov006_0220a8b8[256];
#define Td0 native_data_ov006_0220a8b8
extern const uint32_t native_data_ov006_0220acb8[256];
#define Td1 native_data_ov006_0220acb8
extern const uint32_t native_data_ov006_022088b8[256];
#define Td2 native_data_ov006_022088b8
extern const uint32_t native_data_ov006_02208cb8[256];
#define Td3 native_data_ov006_02208cb8
extern const uint32_t native_data_ov006_022090b8[256];
#define Td4 native_data_ov006_022090b8
