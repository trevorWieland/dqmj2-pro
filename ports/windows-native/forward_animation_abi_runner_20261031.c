typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef signed int s32;
extern u32 native_main_0204106c(void *,const void *,u32);
__declspec(dllimport) void *__stdcall GetStdHandle(s32);
__declspec(dllimport) s32 __stdcall ReadFile(void *,void *,u32,u32 *,void *);
__declspec(dllimport) s32 __stdcall WriteFile(void *,const void *,u32,u32 *,void *);
__declspec(dllimport) __declspec(noreturn) void __stdcall ExitProcess(u32);
_Alignas(4) static u8 destination[0x1800];
_Alignas(4) static u8 file[0x3400];
_Alignas(4) static u32 holders[2];
static u32 header[2];
static u32 profile[5];
static u8 golden[0x1800];
static u32 failures;
static u32 consumed;
static u32 digest=2166136261U;

void *memset(void *target,s32 value,u32 size) {
    volatile u8 *p=(volatile u8 *)target;
    u32 i;
    for(i=0;i<size;i++) p[i]=(u8)value;
    return target;
}

static void put(u8 *p,u32 value) { *(u32 *)p=value; }
static void half(u8 *p,u16 value) { *(u16 *)p=value; }
static void check(s32 value) { if(!value) failures++; }
static void mix(u32 value) {
    u32 i;
    for(i=0;i<4;i++) { digest=(digest^(value&255U))*16777619U;value>>=8; }
}

u32 native_fn_02028b64(void *out,const void *holder,u32 index) {
    u8 *dest=(u8 *)out;
    const u8 *source=*(u8 *const *)holder;
    const u8 *resource;
    const u8 *entry;
    const u8 *node;
    u32 i;
    check(out==destination+16+profile[2]);
    check(holder==holders+profile[3]/4);
    check(index==profile[1]);
    consumed++;
    memset(dest,0,256);
    resource=source+*(const u32 *)(source+*(const u16 *)(source+12));
    if(index>=resource[9]) return 0;
    entry=resource+8+*(const u16 *)(resource+14);
    entry+=4+index*(*(const u16 *)entry);
    node=resource+*(const u32 *)entry;
    for(i=0;i<16;i++) dest[12+i]=node[i];
    put(dest+0x7C,0x1000);
    put(dest+0x80,0x1000);
    put(dest+0x84,0x1000);
    put(dest+0x70,0);
    put(dest+0x74,0);
    put(dest+0x78,0);
    put(dest+0x88,0);
    put(dest+0x8C,0);
    put(dest+0x90,0);
    dest[9]=1;
    put(dest+0xF4,0xFFFFFFFFU);
    dest[8]=1;
    return 1;
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
    u32 i,j,returned;
    u8 *resource=file+0x100;
    memset(destination,0xA5,sizeof(destination));
    memset(file,0xA5,sizeof(file));
    half(file+12,0x20);
    put(file+0x20,0x100);
    resource[9]=(u8)profile[0];
    half(resource+14,0x20);
    half(resource+0x28,4);
    for(i=0;i<255;i++) {
        put(resource+0x2C+4*i,0x900+32*i);
        for(j=0;j<32;j++) resource[0x900+32*i+j]=(u8)(i+j);
    }
    holders[0]=(u32)file;
    holders[1]=(u32)file;
    returned=native_main_0204106c(destination+16+profile[2],holders+profile[3]/4,profile[1]);
    check(returned==profile[4]);
    for(i=0;i<sizeof(destination);i++) check(destination[i]==golden[i]);
    mix(returned);
    mix(profile[1]);
    mix(consumed);
}

void j2p_entry(void) {
    void *input=GetStdHandle(-10);
    void *output=GetStdHandle(-11);
    u32 i,n,receipt[8];
    if(!read_all(input,header,sizeof(header)) || header[0]!=0x4A324146U || header[1]!=384) ExitProcess(2);
    for(i=0;i<header[1];i++) {
        if(!read_all(input,profile,sizeof(profile)) || !read_all(input,golden,sizeof(golden))) ExitProcess(3);
        run_case();
    }
    receipt[0]=0x4A324157U;
    receipt[1]=1;
    receipt[2]=header[1];
    receipt[3]=consumed;
    receipt[4]=failures;
    receipt[5]=digest;
    receipt[6]=sizeof(void *);
    receipt[7]=0;
    if(!WriteFile(output,receipt,sizeof(receipt),&n,0) || n!=sizeof(receipt)) ExitProcess(4);
    ExitProcess(failures!=0);
}
