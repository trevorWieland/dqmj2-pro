typedef unsigned char u8;
typedef unsigned long u32;
typedef int BOOL;
void native_fn_02008d78(void * dest, u8 data, u32 size);
void native_fn_02008e0c(const void * src, void * dest, u32 size);
void native_fn_0200d3e4(void * digest, void * bin_ptr, int bin_len, void * key_ptr, int key_len);
typedef struct {
const void *field_0000;
int field_0004;
} NativeStorage_020dcb64;
extern NativeStorage_020dcb64 native_data_main_020dcb64;
static inline void MI_CpuClear8 (void * dest, u32 size)
{
	native_fn_02008d78(dest, 0, size);
}
