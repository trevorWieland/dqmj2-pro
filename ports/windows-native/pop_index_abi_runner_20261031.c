typedef unsigned char u8;
typedef signed char s8;
typedef unsigned int u32;
typedef signed int s32;
typedef struct { u8 unknown_0[4]; s32 field_4; s32 field_8; } Root;
extern Root native_data_021d6840;
extern Root native_data_021d64cc;
extern u8 native_data_021d6873[];
extern u8 native_data_021d64ff[];
extern u32 native_main_020cd5bc(s32);
extern u32 native_main_020cab98(s32);
__declspec(dllimport) void *__stdcall GetStdHandle(s32);
__declspec(dllimport) s32 __stdcall ReadFile(void *,void *,u32,u32 *,void *);
__declspec(dllimport) s32 __stdcall WriteFile(void *,const void *,u32,u32 *,void *);
__declspec(dllimport) __declspec(noreturn) void __stdcall ExitProcess(u32);
Root native_data_021d6840;
Root native_data_021d64cc;
u8 native_data_021d6873[64];
u8 native_data_021d64ff[64];
_Alignas(4) static u8 descriptors[384][12];
_Alignas(4) static u8 handles[384][16];
_Alignas(4) static u8 assets[384][128];
static u32 profile[12];
static u32 failures;
static u32 free_calls;
static u32 ui_calls;
static u32 digest=2166136261U;

void *memset(void *target,s32 value,u32 length) {
    volatile u8 *p=(volatile u8 *)target;
    u32 i;
    for(i=0;i<length;i++) p[i]=(u8)value;
    return target;
}

static u32 word(const u8 *p) { return *(const u32 *)p; }
static void put(u8 *p,u32 value) { *(u32 *)p=value; }
static void check(s32 truth) { if(!truth) failures++; }
static void mix(u32 value) {
    u32 i;
    for(i=0;i<4;i++) { digest=(digest^(value&255U))*16777619U; value>>=8; }
}

u32 native_fn_02049ad0(s32 index) {
    check(index>=-128 && index<=255);
    if(index<-128 || index>255) ExitProcess(4);
    return (u32)descriptors[index+128];
}

u32 native_fn_0206db90(s32 category) {
    check(category==(s32)(s8)profile[2]);
    return profile[3];
}

u32 native_fn_02045dc4(u32 a0,u32 a1,u32 a2,u32 a3,u32 a4,u32 a5) {
    check(a0==1 && a1==77 && a2==profile[10] && a3==128 && a4==255 && a5==0);
    ui_calls++;
    return 0xF1234567U;
}

u32 native_fn_0205ff4c(void *handle) {
    check((u32)handle==(u32)handles[(s32)profile[1]+128]);
    free_calls++;
    return 0xF1234567U;
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
    s32 selected=(s32)profile[1]+128;
    Root *state=profile[0]?&native_data_021d64cc:&native_data_021d6840;
    Root *other=profile[0]?&native_data_021d6840:&native_data_021d64cc;
    memset(&native_data_021d6840,0xA5,sizeof(Root));
    memset(&native_data_021d64cc,0xA5,sizeof(Root));
    state->field_4=1000;
    state->field_8=1;
    memset(descriptors,0xA5,sizeof(descriptors));
    memset(handles,0xA5,sizeof(handles));
    memset(assets,0xA5,sizeof(assets));
    memset(native_data_021d6873,0x3D,64);
    memset(native_data_021d64ff,0x3D,64);
    native_data_021d6873[0]=77;
    native_data_021d64ff[0]=77;
    for(i=0;i<384;i++) {
        put(descriptors[i],(u32)handles[i]);
        descriptors[i][5]=(u8)profile[2];
        descriptors[i][6]=127;
        put(handles[i]+4,(u32)assets[i]);
        assets[i][0x1E]=(u8)profile[8];
        assets[i][0x1F]=(u8)profile[9];
        assets[i][0x5C]=(u8)profile[10];
        assets[i][0x5D]=128;
        assets[i][0x5E]=255;
        assets[i][0x5F]=0;
    }
    free_calls=0;
    ui_calls=0;
    returned=profile[0]?native_main_020cab98((s32)profile[1]):native_main_020cd5bc((s32)profile[1]);
    check(returned==profile[4]);
    check((u32)state->field_4==profile[5] && (u32)state->field_8==profile[6]);
    check(descriptors[selected][6]==profile[7]);
    check(ui_calls==profile[11] && free_calls==1);
    check((u32)other->field_4==0xA5A5A5A5U && (u32)other->field_8==0xA5A5A5A5U);
    for(i=0;i<384;i++) {
        check(word(descriptors[i])==(i==(u32)selected?0:(u32)handles[i]));
        check(descriptors[i][5]==(u8)profile[2]);
        check(descriptors[i][6]==(i==(u32)selected?255:127));
        for(j=4;j<12;j++) if(j!=5 && j!=6) check(descriptors[i][j]==0xA5);
        check(word(handles[i]+4)==(u32)assets[i]);
    }
    mix(returned);mix((u32)state->field_4);mix((u32)state->field_8);mix(descriptors[selected][6]);mix(ui_calls);mix(free_calls);
}

void j2p_entry(void) {
    u32 header[2],i,written,receipt[8];
    void *input=GetStdHandle(-10);
    check(sizeof(void *)==4 && sizeof(u32)==4);
    if(!read_all(input,header,8) || header[0]!=0x4A32504FU || header[1]>4096) ExitProcess(2);
    for(i=0;i<header[1];i++) {
        if(!read_all(input,profile,sizeof(profile))) ExitProcess(3);
        run_case();
    }
    receipt[0]=0x4A325049U;receipt[1]=1;receipt[2]=header[1];receipt[3]=i;
    receipt[4]=failures;receipt[5]=digest;receipt[6]=4;receipt[7]=0;
    WriteFile(GetStdHandle(-11),receipt,sizeof(receipt),&written,0);
    ExitProcess(failures?1:0);
}
