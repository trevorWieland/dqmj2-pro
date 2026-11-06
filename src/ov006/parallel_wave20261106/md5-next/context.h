typedef unsigned char*POINTER;typedef unsigned int UINT4;
typedef struct{UINT4 state[4];UINT4 count[2];unsigned char buffer[64];}MD5_CTX;
extern void native_ov006_021f152c(MD5_CTX*,unsigned char*,unsigned int);
extern void native_ov006_021f15a4(unsigned char[16],MD5_CTX*);
extern void native_ov006_021f15f8(UINT4[4],unsigned char[64]);
extern void native_ov006_021f1e40(unsigned char*,UINT4*,unsigned int);
extern void native_ov006_021f1e6c(UINT4*,unsigned char*,unsigned int);
extern void native_ov006_021f1e98(POINTER,POINTER,unsigned int);
extern void native_ov006_021f1eb0(POINTER,int,unsigned int);
extern unsigned char native_data_ov006_0220d500[64];
#define PADDING native_data_ov006_0220d500
#define Encode native_ov006_021f1e40
#define Decode native_ov006_021f1e6c
#define MD5_memcpy native_ov006_021f1e98
#define MD5_memset native_ov006_021f1eb0
#define S11 7
#define S12 12
#define S13 17
#define S14 22
#define S21 5
#define S22 9
#define S23 14
#define S24 20
#define S31 4
#define S32 11
#define S33 16
#define S34 23
#define S41 6
#define S42 10
#define S43 15
#define S44 21
#define F(x, y, z) (((x) & (y)) | ((~x) & (z)))
#define G(x, y, z) (((x) & (z)) | ((y) & (~z)))
#define H(x, y, z) ((x) ^ (y) ^ (z))
#define I(x, y, z) ((y) ^ ((x) | (~z)))
#define ROTATE_LEFT(x, n) (((x) << (n)) | ((x) >> (32-(n))))
#define FF(a, b, c, d, x, s, ac) {     (a) += F ((b), (c), (d)) + (x) + (UINT4)(ac);     (a) = ROTATE_LEFT ((a), (s));     (a) += (b);   }
#define GG(a, b, c, d, x, s, ac) {     (a) += G ((b), (c), (d)) + (x) + (UINT4)(ac);     (a) = ROTATE_LEFT ((a), (s));     (a) += (b);   }
#define HH(a, b, c, d, x, s, ac) {     (a) += H ((b), (c), (d)) + (x) + (UINT4)(ac);     (a) = ROTATE_LEFT ((a), (s));     (a) += (b);   }
#define II(a, b, c, d, x, s, ac) {     (a) += I ((b), (c), (d)) + (x) + (UINT4)(ac);     (a) = ROTATE_LEFT ((a), (s));     (a) += (b);   }
