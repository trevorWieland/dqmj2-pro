typedef unsigned char u8;
typedef unsigned int u32;
typedef signed int s32;
extern u32 native_main_020ac404(void **,u32);
__declspec(dllimport) void *__stdcall GetStdHandle(s32);
__declspec(dllimport) s32 __stdcall ReadFile(void *,void *,u32,u32 *,void *);
__declspec(dllimport) s32 __stdcall WriteFile(void *,const void *,u32,u32 *,void *);
__declspec(dllimport) __declspec(noreturn) void __stdcall ExitProcess(u32);
u8 native_data_020e0768[4];
u8 native_data_020e05ec[4];
u8 native_data_020e05f8[4];
u8 native_data_020e0604[4];
u8 native_data_020e0614[4];
u8 native_data_020e061c[4];
_Alignas(4) static u8 contexts[2][0x600];
_Alignas(4) static u8 nodes[2][64];
static void *holder;
static u32 header[2],profile[9],failures,digest=2166136261U,format_count,failed_cases,failed_int_min;
static u8 golden[0xC80];

void *memset(void *target,s32 value,u32 size) {
    volatile u8 *p=(volatile u8 *)target;
    u32 i;
    for(i=0;i<size;i++) p[i]=(u8)value;
    return target;
}

static void put(u8 *p,u32 v) { *(u32 *)p=v; }
static void check(s32 v) { if(!v) failures++; }
static void mix(u32 v) {
    u32 i;
    for(i=0;i<4;i++) { digest=(digest^(v&255U))*16777619U;v>>=8; }
}

static u32 normalized(const void *p) {
    if(p==native_data_020e0768) return 0x020E0768;
    if(p==native_data_020e05ec) return 0x020E05EC;
    if(p==native_data_020e05f8) return 0x020E05F8;
    if(p==native_data_020e0604) return 0x020E0604;
    if(p==native_data_020e0614) return 0x020E0614;
    if(p==native_data_020e061c) return 0x020E061C;
    return (u32)p;
}

u32 native_fn_020b0a50(void **root,u32 selector,void **out) {
    check(root==&holder && selector==profile[7] && holder==contexts[0]);
    *out=nodes[profile[5]];
    if(profile[6]) holder=contexts[1];
    return profile[0];
}

u32 native_fn_020ac6f4(void **root,void *dest,const void *value) {
    check(root==&holder && dest==(u8 *)holder+0x210);
    put((u8 *)dest+4*format_count++,normalized(value));
    return 0xAB123456U;
}

u32 native_fn_020ac710(void **root,void *dest,s32 value) {
    check(root==&holder && dest==(u8 *)holder+0x210);
    put((u8 *)dest+4*format_count++,(u32)value);
    return 0xAB123456U;
}

u32 native_fn_020b2a38(s32 root,u32 value,u32 extent) {
    check((u32)root==(u32)holder && extent==256);
    put((u8 *)(u32)root+0x210+4*format_count++,normalized((void *)value));
    return 0xAB123456U;
}

u32 native_fn_020a929c(u32 value) {
    check(value==profile[1]);
    return 0xAB123456U;
}

u32 native_fn_020b0b48(void **root,void *node) {
    check(root==&holder && node==nodes[profile[5]]);
    return 0xAB123456U;
}

static s32 read_all(void *handle,void *buffer,u32 size) {
    u8 *p=(u8 *)buffer;
    while(size) {
        u32 n=0;
        if(!ReadFile(handle,p,size,&n,0) || !n) return 0;
        p+=n;
        size-=n;
    }
    return 1;
}

static void run_case(void) {
    u32 i,j,returned,before=failures;
    static const u32 offsets[4]={0x10,8,12,0x1C};
    memset(contexts,0xA5,sizeof(contexts));
    memset(nodes,0xA5,sizeof(nodes));
    holder=contexts[0];
    format_count=0;
    put(contexts[0]+0x100,profile[3]);
    put(contexts[1]+0x100,1);
    put(contexts[0]+0x198,0x12345678);
    put(contexts[1]+0x198,0x87654321);
    for(i=0;i<2;i++) {
        put(nodes[i],i==0?0x13579BDF:0xFEDCBA98);
        put(nodes[i]+0x14,profile[1]);
        put(nodes[i]+0x18,profile[2]);
        for(j=0;j<4;j++) put(nodes[i]+offsets[j],profile[4]&(1U<<j)?0x100:0);
    }
    returned=native_main_020ac404(&holder,profile[7]);
    check(returned==profile[8]);
    check(holder==contexts[profile[6]?1:0]);
    for(i=0;i<0x600;i++) check(contexts[0][i]==golden[i]);
    for(i=0;i<0x600;i++) check(contexts[1][i]==golden[0x600+i]);
    for(i=0;i<64;i++) check(nodes[0][i]==golden[0xC00+i]);
    for(i=0;i<64;i++) check(nodes[1][i]==golden[0xC40+i]);
    if(failures!=before) { failed_cases++;if(profile[2]==0x80000000U) failed_int_min++; }
    mix(returned);
    mix(*(u32 *)(nodes[profile[5]]+0x18));
    mix(*(u32 *)(nodes[profile[5]]+0x14));
    mix(format_count);
}

void j2p_entry(void) {
    void *input=GetStdHandle(-10),*output=GetStdHandle(-11);
    u32 i,n,receipt[10];
    if(!read_all(input,header,sizeof(header)) || header[0]!=0x4A324C4EU || header[1]!=840) ExitProcess(2);
    for(i=0;i<header[1];i++) {
        if(!read_all(input,profile,sizeof(profile)) || !read_all(input,golden,sizeof(golden))) ExitProcess(3);
        run_case();
    }
    receipt[0]=0x4A324C57U;
    receipt[1]=1;
    receipt[2]=header[1];
    receipt[3]=header[1];
    receipt[4]=failures;
    receipt[5]=digest;
    receipt[6]=sizeof(void *);
    receipt[7]=failed_cases;
    receipt[8]=failed_int_min;
    receipt[9]=0;
    if(!WriteFile(output,receipt,sizeof(receipt),&n,0) || n!=sizeof(receipt)) ExitProcess(4);
    ExitProcess(failures!=0);
}
