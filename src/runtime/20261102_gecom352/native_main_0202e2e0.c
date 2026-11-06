typedef unsigned long u32;
typedef struct NNSG3dGeBuffer_ {
    u32 idx;
    u32 data[192 ];
} NNSG3dGeBuffer;
typedef struct { NNSG3dGeBuffer *buffer; volatile int asyncFlag; } OriginalGecomState;
extern OriginalGecomState native_data_main_020edf84;


void native_main_0202e2e0(NNSG3dGeBuffer * p);
void native_main_0202e2e0 (NNSG3dGeBuffer * p)
{
    ((void) 0) ;
    if (native_data_main_020edf84.buffer == ((void *)0) ) {
        p->idx = 0;
        native_data_main_020edf84.buffer = p;
    }
}
