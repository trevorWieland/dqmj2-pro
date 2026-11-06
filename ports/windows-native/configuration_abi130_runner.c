typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef signed int s32;
_Static_assert(sizeof(void *) == 4, "Four-byte pointers required");
__declspec(dllimport) void __stdcall ExitProcess(u32);
__declspec(dllimport) void *__stdcall GetStdHandle(u32);
__declspec(dllimport) s32 __stdcall WriteFile(void *, const void *, u32, u32 *, void *);
extern u32 typed_configuration130(void *,u32,u32,u32);
extern u32 retained_configuration130(void *,u32,u32,u32);
extern u32 wrong_configuration130(void *,u32,u32,u32);
_Alignas(4) static u8 storage[160];
static u8 *object;
static u32 arguments[3],lookup_word,stage,bad,cleanup_bad;
static const u32 basis[4]={0,1,0x80000000u,0xFFFFFFFFu};
static u32 receipt[16]={0x4A324143u,1,0,0,0,0,0,0,0,0,0,0,0,0,2166136261u,0};

__declspec(noinline) u32 native_fn_020850a0(void *pointer) {
    bad |= stage++ != 0;
    if (pointer != object) { ++cleanup_bad;bad=1;return 0; }
    if (*(u32 *)(object+0x64)) *(u32 *)(object+0x64)=0;
    return 0;
}

__declspec(noinline) u32 native_fn_02087e44(u32 pointer,u32 mode) {
    bad |= stage++ != 1 || pointer!=*(u32 *)(object+0x44) || mode!=0;
    return 0xFFFFFFFFu;
}

__declspec(noinline) u32 native_fn_02085284(void *pointer,u32 first,u32 second,u32 third) {
    u8 *p=(u8 *)pointer;
    bad |= stage++ != 2 || p!=object+0x3C || first!=arguments[0] || second!=arguments[1] || third!=arguments[2];
    p[0]=(u8)first;p[1]=(u8)second;*(u16 *)(p+2)=(u16)third;*(u32 *)(p+0x2C)=lookup_word;
    return lookup_word;
}

__declspec(noinline) u32 native_fn_02085270(void *pointer,s32 first,s32 second) {
    u8 *p=(u8 *)pointer;
    bad |= stage++ != 3 || p!=object+0x3C || first!=8 || second!=0;
    *(u16 *)(p+0x34)=(u16)first;*(u16 *)(p+0x36)=(u16)second;
    return (u32)p;
}

__declspec(noinline) u32 native_fn_02086b14(void *pointer,u32 mode) {
    u8 *p=(u8 *)pointer;
    bad |= stage++ != 4 || p!=object || mode!=16;
    *(u32 *)(p+0x10)=*(u32 *)(p+0xC);*(u32 *)(p+0xC)=mode;
    return (u32)p;
}

static void finish(u32 code) {
    u32 written;
    WriteFile(GetStdHandle((u32)-11),receipt,sizeof(receipt),&written,(void *)0);
    ExitProcess(code);
}

static void run_case(u32 kind,u32 handle,u32 rotation,u32 mode,u32 flags,u32 lookup,u32 seed) {
    u8 expected[160];
    u32 i,result,failed;
    object=storage+16;
    for(i=0;i<160;++i) storage[i]=expected[i]=(u8)(i*37+seed);
    for(i=0;i<3;++i) arguments[i]=basis[(rotation+i)%4];
    *(u32 *)(object+0x64)=handle;
    *(u32 *)(object+0x44)=basis[(rotation+1)%4];
    *(u32 *)(object+0xC)=basis[mode];
    *(u32 *)(object+0x18)=basis[flags];
    for(i=0;i<160;++i) expected[i]=storage[i];
    *(u32 *)(expected+16+0x64)=0;
    expected[16+0x3C]=(u8)arguments[0];expected[16+0x3D]=(u8)arguments[1];
    *(u16 *)(expected+16+0x3E)=(u16)arguments[2];
    lookup_word=basis[lookup];*(u32 *)(expected+16+0x68)=lookup_word;
    *(u16 *)(expected+16+0x70)=8;*(u16 *)(expected+16+0x72)=0;
    *(u32 *)(expected+16+0x18)=basis[flags]|2;
    *(u32 *)(expected+16+0x10)=basis[mode];*(u32 *)(expected+16+0xC)=16;
    stage=bad=cleanup_bad=0;
    if(kind==0) result=typed_configuration130(object,arguments[0],arguments[1],arguments[2]);
    else if(kind==1) result=retained_configuration130(object,arguments[0],arguments[1],arguments[2]);
    else result=wrong_configuration130(object,arguments[0],arguments[1],arguments[2]);
    failed=bad || stage!=5 || result!=(u32)object;
    for(i=0;i<160;++i) failed |= storage[i]!=expected[i];
    if(kind==0) {
        ++receipt[2];receipt[3]+=failed==0;receipt[10]+=stage==5;receipt[13]+=failed!=0;
        for(i=0;i<160;++i) receipt[14]=(receipt[14]^storage[i])*16777619u;
    } else if(kind==1) {++receipt[4];receipt[5]+=failed!=0;receipt[6]+=failed==0;receipt[11]+=cleanup_bad;}
    else {++receipt[7];receipt[8]+=failed!=0;receipt[9]+=failed==0;receipt[12]+=cleanup_bad;}
}

void j2p_entry(void) {
    u32 kind,handle,rotation,mode,flags,lookup,seed;
    for(kind=0;kind<3;++kind)
        for(handle=0;handle<2;++handle)
            for(rotation=0;rotation<4;++rotation)
                for(mode=0;mode<4;++mode)
                    for(flags=0;flags<4;++flags)
                        for(lookup=0;lookup<4;++lookup)
                            for(seed=0;seed<2;++seed)
                                run_case(kind,handle?0x12345678u:0,rotation,mode,flags,lookup,seed?255:0);
    receipt[15]=receipt[2]!=1024 || receipt[3]!=1024 || receipt[4]!=1024 || receipt[7]!=1024 || receipt[8]!=512 || receipt[9]!=512 || receipt[12]!=512 || receipt[13]!=0;
    finish(receipt[15]?42:0);
}
