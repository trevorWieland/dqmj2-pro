typedef unsigned short int u16;
typedef unsigned long u32;
typedef signed short int s16;
typedef volatile u16 vu16;
typedef volatile u32 vu32;
typedef volatile s16 vs16;
void native_fn_020072d0(void * startAddr, u32 nBytes);
typedef struct SNDSharedWork {
	vu32 finishCommandTag;
	vu32 playerStatus;
	vu16 channelStatus;
	vu16 captureStatus;
	vu32 padding[5];
	struct {
		vs16 variable[16 ];
		vu32 tickCounter;
	} player[16 ];
	vs16 globalVariable[16 ];
} SNDSharedWork;
extern SNDSharedWork * native_data_main_020e52c0;
u32 native_main_02009dbc(void);
SNDSharedWork * native_data_main_020e52c0;
u32 native_main_02009dbc (void)
{
    ((void) 0) ;
    native_fn_020072d0((void *)&native_data_main_020e52c0->finishCommandTag,
                       sizeof(native_data_main_020e52c0->finishCommandTag));
    return native_data_main_020e52c0->finishCommandTag;
}
