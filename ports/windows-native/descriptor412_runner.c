typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef signed int s32;
__declspec(dllimport) void __stdcall ExitProcess(u32);
__declspec(dllimport) void *__stdcall GetStdHandle(s32);
__declspec(dllimport) s32 __stdcall ReadFile(void *,void *,u32,u32 *,void *);
__declspec(dllimport) s32 __stdcall WriteFile(void *,const void *,u32,u32 *,void *);
_Alignas(4) u8 native_data_020f69ec[8];
_Alignas(4) static u8 table[3200];
static u32 seen_index,seen_scaled,seen_final_index,seen_level;
static u32 lookup_calls,scale_calls,final_calls;
u32 descriptor_lookup_impl(s32);
u32 descriptor_scale_impl(s32,s32);
u32 native_fn_020449d4(s32 index) {
    seen_index=(u32)index;
    lookup_calls++;
    return descriptor_lookup_impl(index);
}
u32 native_fn_02044e18(s32 value,s32 level) {
    scale_calls++;
    return descriptor_scale_impl(value,level);
}
u32 native_fn_0207b790(u32 value,u32 index,u32 level) {
    seen_scaled=value;
    seen_final_index=index;
    seen_level=level;
    final_calls++;
    return value^(index*0x13579B)^(level*0x2468AD);
}
u32 native_main_02044e44(u32,u32);
u32 native_main_02044e80(u32,u32);
u32 native_main_02044ebc(u32,u32);
u32 native_main_02044ef8(u32,u32);
u32 native_main_02044f34(u32,u32);
u32 native_main_02044f70(u32,u32);
static u32 (*const functions[6])(u32,u32)={
    native_main_02044e44,native_main_02044e80,native_main_02044ebc,
    native_main_02044ef8,native_main_02044f34,native_main_02044f70
};
static s32 read_exact(void *out,u32 size) {
    u8 *pointer=(u8 *)out;
    while(size) {
        u32 got=0;
        if(!ReadFile(GetStdHandle(-10),pointer,size,&got,0)||!got)return 0;
        pointer+=got;
        size-=got;
    }
    return 1;
}
void j2p_entry(void) {
    u32 header[2],i,index,column,errors=0,hash=2166136261;
    if(!read_exact(header,8)||header[0]!=0x4A324411||header[1]!=1152)ExitProcess(90);
    for(i=0;i<3200;i++)table[i]=(u8)(i*43+19);
    for(index=0;index<32;index++) {
        for(column=0;column<6;column++) {
            u32 field=1+(index*37+column*17)%999;
            table[index*100+0x10+column*2]=(u8)field;
            table[index*100+0x11+column*2]=(u8)(field>>8);
        }
    }
    *(u32 *)(native_data_020f69ec+4)=(u32)table;
    for(i=0;i<header[1];i++) {
        u32 row[6],result;
        if(!read_exact(row,24)||row[0]>=6)ExitProcess(91);
        seen_index=seen_scaled=seen_final_index=seen_level=0xFFFFFFFF;
        result=functions[row[0]](row[1],row[2]);
        if(result!=row[3]||seen_index!=row[1]||seen_scaled!=row[4]||seen_final_index!=row[1]||seen_level!=row[2])errors++;
        hash=(hash^result)*16777619;
        hash=(hash^seen_index)*16777619;
        hash=(hash^seen_scaled)*16777619;
    }
    {
        u32 out[8]={0x4A324412,1,header[1],errors,lookup_calls,scale_calls,final_calls,hash};
        u32 written=0;
        if(!WriteFile(GetStdHandle(-11),out,32,&written,0)||written!=32)ExitProcess(92);
    }
    ExitProcess(errors?42:0);
}
