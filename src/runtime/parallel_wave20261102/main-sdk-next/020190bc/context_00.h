typedef unsigned char u8;
typedef unsigned short int u16;
typedef unsigned long u32;
typedef int BOOL;
void native_fn_02008e0c(const void * src, void * dest, u32 size);
extern const u16 (*ctrdgi_fl_maxtime);
typedef struct {
	u8 type;
	u8 pad1[1];
	union {
		struct {
			u16 req;
			u8 reserved[((16) -2) ];
		} data;
		struct {
			u8 piece;
			u8 data[((16) -2) ];
			u8 pad2[1];
		} req_data;
	};
} MBCommChildBlockHeader;
typedef struct {
	u32 data_buf[15 ][((29) + 1) / sizeof(u32) + 1];
	u32 data_bmp[15 ];
} MbRequestPieceBuf;
u8 * native_main_020190bc(const MBCommChildBlockHeader * hdr, u16 child);
BOOL native_fn_02019148(u16 child);
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
BOOL native_fn_02019148 (u16 child);
