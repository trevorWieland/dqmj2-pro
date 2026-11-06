typedef unsigned char u8;
typedef unsigned short int u16;
typedef unsigned long u32;
extern const u16 (*ctrdgi_fl_maxtime);
typedef struct {
	u32 data_buf[15 ][((29) + 1) / sizeof(u32) + 1];
	u32 data_bmp[15 ];
} MbRequestPieceBuf;
void native_main_02018e88(u16 childMaxSize);
typedef struct {
u8 field_0000;
unsigned char padding_0001[3];
MbRequestPieceBuf * field_0004;
struct {
	int size;
	int num;
	int bufSize;
} field_0008;
} NativeStorage_020ec3a4;
extern NativeStorage_020ec3a4 native_data_main_020ec3a4;
