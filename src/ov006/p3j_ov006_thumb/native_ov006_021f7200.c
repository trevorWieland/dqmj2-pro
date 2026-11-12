typedef unsigned char u8;
typedef unsigned int u32;

extern void ov006_main_loop_set_callback_021f52cc(void *);
extern u8 native_data_0221c0bc[];

void native_ov006_021f7200(void) {
    native_data_0221c0bc[0] = native_data_0221c0bc[0] + 1;
    if (native_data_0221c0bc[0] >= 0x78) {
        ov006_main_loop_set_callback_021f52cc((void *)0x021f7195);
    }
}
