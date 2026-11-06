typedef unsigned char u8;
typedef signed int s32;
__declspec(align(4)) extern u8 native_data_021c5a24[];

void native_main_02076508(s32 item)
{
    ((s32 *)(native_data_021c5a24 + 0x3D4))[native_data_021c5a24[0x7D4]] = item;
    native_data_021c5a24[0x7D4]++;
}
