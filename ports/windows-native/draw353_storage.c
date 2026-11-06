typedef unsigned char u8;
typedef signed char s8;
typedef signed int s32;
typedef unsigned int u32;
u8 native_data_021b9bd4[0x280];
u8 native_data_02102a18[0x1000];
u32 draw_seen_index;
u32 draw_seen_selector;
u32 draw_helper_calls;
u32 draw_lower_calls;
u32 draw_words[11];
extern u32 draw_real_61dcc(s32);
extern u32 draw_real_49ad0(s32);
u32 native_fn_02061dcc(s32 index) {
    draw_seen_index = (u32)index;
    draw_helper_calls++;
    return draw_real_61dcc(index);
}
u32 native_fn_02049ad0(s32 selector) {
    draw_seen_selector = (u32)selector;
    return draw_real_49ad0(selector);
}
u32 native_fn_02049be4(u32 a0,u32 a1,u32 a2,u32 a3,u32 a4,u32 a5,u32 a6,u32 a7,u32 a8,u32 a9,u32 a10) {
    draw_words[0]=a0;draw_words[1]=a1;draw_words[2]=a2;draw_words[3]=a3;draw_words[4]=a4;draw_words[5]=a5;
    draw_words[6]=a6;draw_words[7]=a7;draw_words[8]=a8;draw_words[9]=a9;draw_words[10]=a10;
    draw_lower_calls++;
    return 0xDA010203U;
}
void draw_reset(s32 left,s32 right,s32 mode) {
    u32 i;
    for(i=0;i<0x280;i++) native_data_021b9bd4[i]=0xA5;
    *(s32 *)(native_data_021b9bd4+0x25C)=left;
    *(s32 *)(native_data_021b9bd4+0x260)=right;
    native_data_021b9bd4[0x268]=(u8)mode;
    draw_seen_index=draw_seen_selector=0xA5A5A5A5U;
    draw_helper_calls=draw_lower_calls=0;
    for(i=0;i<11;i++) draw_words[i]=0xC7C7C7C7U;
}
