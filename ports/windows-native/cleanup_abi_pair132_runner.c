typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef signed int s32;
_Static_assert(sizeof(void *)==4,"Four-byte pointer ABI required");
__declspec(dllimport) void __stdcall ExitProcess(u32);
__declspec(dllimport) void *__stdcall GetStdHandle(u32);
__declspec(dllimport) s32 __stdcall WriteFile(void *,const void *,u32,u32 *,void *);
extern u32 typed_first132(void *,u32);
extern u32 retained_first132(void *,u32);
extern u32 wrong_first132(void *,u32);
extern u32 typed_second132(void *);
extern u32 retained_second132(void *);
extern u32 wrong_second132(void *);
_Alignas(4) static u8 storage[160];
static u8 *object;
static u32 family,argument,stage,bad,cleanup_bad;
static const u32 basis[4]={0,1,0x80000000u,0xFFFFFFFFu};
static u32 receipt[20]={0x4A324150u,1,0,0,0,0,0,0,0,0,0,0,0,0,2166136261u,0,0,0,0,0};

__declspec(noinline) u32 native_fn_020850a0(void *pointer) {
    bad |= stage++!=0;
    if(pointer!=object){++cleanup_bad;bad=1;return 0;}
    if(*(u32 *)(object+0x64)) *(u32 *)(object+0x64)=0;
    return 0;
}
__declspec(noinline) u32 native_fn_02087e44(u32 pointer,u32 mode) {
    bad |= stage++!=1 || pointer!=*(u32 *)(object+0x44) || mode!=0;
    return 0xFFFFFFFFu;
}
__declspec(noinline) u32 native_fn_020852b0(void *pointer,u32 word) {
    u8 *p=(u8 *)pointer;
    bad |= family!=0 || stage++!=2 || p!=object+0x3C || word!=argument;
    p[0]=0;p[1]=0;*(u16 *)(p+2)=0;*(u32 *)(p+0x2C)=word;
    return (u32)p;
}
__declspec(noinline) u32 native_fn_02085270(void *pointer,s32 first,s32 second) {
    u8 *p=(u8 *)pointer;
    bad |= family!=0 || stage++!=3 || p!=object+0x3C || first!=0 || second!=0;
    *(u16 *)(p+0x34)=(u16)first;*(u16 *)(p+0x36)=(u16)second;
    return (u32)p;
}
__declspec(noinline) u32 native_fn_02086b14(void *pointer,u32 mode) {
    u8 *p=(u8 *)pointer;
    bad |= stage++!=(family?2:4) || p!=object || mode!=(family?3:16);
    *(u32 *)(p+0x10)=*(u32 *)(p+0xC);*(u32 *)(p+0xC)=mode;
    return (u32)p;
}
static void finish(u32 code) {
    u32 written;
    WriteFile(GetStdHandle((u32)-11),receipt,sizeof(receipt),&written,(void *)0);
    ExitProcess(code);
}
static void run_case(u32 which,u32 version,u32 handle,u32 scalar,u32 mode,u32 flags,u32 seed) {
    u8 expected[160];
    u32 i,result,failed;
    family=which;object=storage+16;argument=basis[scalar];
    for(i=0;i<160;++i) storage[i]=expected[i]=(u8)(i*37+seed);
    *(u32 *)(object+0x64)=handle;*(u32 *)(object+0x44)=basis[(scalar+1)%4];
    *(u32 *)(object+0xC)=basis[mode];*(u32 *)(object+0x18)=basis[flags];
    for(i=0;i<160;++i) expected[i]=storage[i];
    *(u32 *)(expected+16+0x64)=0;
    if(!family){*(u32 *)(expected+16+0x3C)=0;*(u32 *)(expected+16+0x68)=argument;*(u16 *)(expected+16+0x70)=0;*(u16 *)(expected+16+0x72)=0;}
    *(u32 *)(expected+16+0x18)=basis[flags]|(family?8:2);
    *(u32 *)(expected+16+0x10)=basis[mode];*(u32 *)(expected+16+0xC)=family?3:16;
    stage=bad=cleanup_bad=0;
    if(!family){
        if(version==0) result=typed_first132(object,argument);
        else if(version==1) result=retained_first132(object,argument);
        else result=wrong_first132(object,argument);
    }else{
        if(version==0) result=typed_second132(object);
        else if(version==1) result=retained_second132(object);
        else result=wrong_second132(object);
    }
    failed=bad || stage!=(family?3:5) || result!=(family?1:(u32)object);
    for(i=0;i<160;++i) failed |= storage[i]!=expected[i];
    if(version==0){++receipt[2];receipt[3]+=failed==0;receipt[10]+=stage==(family?3:5);receipt[13]+=failed!=0;++receipt[16+family];for(i=0;i<160;++i) receipt[14]=(receipt[14]^storage[i])*16777619u;}
    else if(version==1){++receipt[4];receipt[5]+=failed!=0;receipt[6]+=failed==0;receipt[11]+=cleanup_bad;receipt[18+family]+=failed!=0;}
    else{++receipt[7];receipt[8]+=failed!=0;receipt[9]+=failed==0;receipt[12]+=cleanup_bad;}
}
void j2p_entry(void) {
    u32 which,version,handle,scalar,mode,flags,seed;
    for(which=0;which<2;++which)
        for(version=0;version<3;++version)
            for(handle=0;handle<2;++handle)
                for(scalar=0;scalar<4;++scalar)
                    for(mode=0;mode<4;++mode)
                        for(flags=0;flags<4;++flags)
                            for(seed=0;seed<2;++seed)
                                run_case(which,version,handle?0x12345678u:0,scalar,mode,flags,seed?255:0);
    receipt[15]=receipt[2]!=512 || receipt[3]!=512 || receipt[4]!=512 || receipt[7]!=512 || receipt[8]!=256 || receipt[9]!=256 || receipt[12]!=256 || receipt[13] || receipt[16]!=256 || receipt[17]!=256;
    finish(receipt[15]?42:0);
}
