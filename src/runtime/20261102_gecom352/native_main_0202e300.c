typedef unsigned long u32;
typedef struct NNSG3dGeBuffer_ { u32 idx; u32 data[192]; } NNSG3dGeBuffer;
typedef struct { NNSG3dGeBuffer *buffer; volatile int asyncFlag; } OriginalGecomState;
extern OriginalGecomState native_data_main_020edf84;

typedef volatile u32 vu32;
typedef vu32 REGType32v;
void native_fn_02008c40(const void * srcp, volatile void * destp, u32 size);
static inline void MI_CpuSend32 (const void * src, volatile void * dest, u32 size)
{
	((void) 0) ;
	((void) 0) ;
	((void) 0) ;
	native_fn_02008c40(src, dest, size);
}
void native_fn_0202e35c(void);
void native_main_0202e300(void);

static inline void sendNB (const void * src, void * dst, u32 szByte)
{
    MI_CpuSend32(src, dst, szByte);
}
void native_main_0202e300 (void)
{
    if (native_data_main_020edf84.asyncFlag) {
        native_fn_0202e35c();
    }
    if (native_data_main_020edf84.buffer &&
        native_data_main_020edf84.buffer->idx > 0) {
        sendNB(&native_data_main_020edf84.buffer->data[0], (void *)&(*( REGType32v *) (0x04000000 + 0x400)) , native_data_main_020edf84.buffer->idx << 2);
        native_data_main_020edf84.buffer->idx = 0;
    }
}
void native_fn_0202e35c (void);
