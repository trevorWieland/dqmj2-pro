typedef unsigned char u8;
typedef unsigned int u32;
extern u8 native_data_021d4100[];
extern u32 native_fn_020642dc(void);
extern void native_fn_020620e8(u32, u32);
extern void native_fn_02089804(void);

void native_itcm_01ffbb44(void) {
    *(u32 *)(native_data_021d4100 + 0x14) = 1;
    switch (native_fn_020642dc() - 16) {
    case 9:
    case 10:
    case 11:
        native_fn_020620e8(20, 1);
        break;
    case 0:
    case 1:
    case 2:
    case 3:
    case 4:
    case 5:
    case 6:
    case 7:
    case 8:
        native_fn_02089804();
        break;
    }
}
