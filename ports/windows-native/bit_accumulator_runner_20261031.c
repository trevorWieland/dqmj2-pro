typedef unsigned int u32;
typedef signed int s32;
extern u32 native_main_020a771c(u32);
__declspec(dllimport) void *__stdcall GetStdHandle(s32);
__declspec(dllimport) s32 __stdcall ReadFile(void *,void *,u32,u32 *,void *);
__declspec(dllimport) s32 __stdcall WriteFile(void *,const void *,u32,u32 *,void *);
__declspec(dllimport) __declspec(noreturn) void __stdcall ExitProcess(u32);

static s32 read_all(void *handle,void *buffer,u32 size) {
    unsigned char *p=(unsigned char *)buffer;
    while(size) {
        u32 n=0;
        if(!ReadFile(handle,p,size,&n,0) || !n) return 0;
        p+=n;
        size-=n;
    }
    return 1;
}

static u32 mix(u32 digest,u32 value) {
    u32 i;
    for(i=0;i<4;i++) { digest=(digest^(value&255U))*16777619U;value>>=8; }
    return digest;
}

void j2p_entry(void) {
    void *input=GetStdHandle(-10);
    void *output=GetStdHandle(-11);
    u32 header[2],pair[2],receipt[8];
    u32 i,n,returned,failures=0,digest=2166136261U;
    if(!read_all(input,header,sizeof(header)) || header[0]!=0x4A324241U || header[1]!=1536) ExitProcess(2);
    for(i=0;i<header[1];i++) {
        if(!read_all(input,pair,sizeof(pair))) ExitProcess(3);
        returned=native_main_020a771c(pair[0]);
        failures+=(returned!=pair[1]);
        digest=mix(mix(digest,pair[0]),returned);
    }
    receipt[0]=0x4A324257U;
    receipt[1]=1;
    receipt[2]=header[1];
    receipt[3]=header[1];
    receipt[4]=failures;
    receipt[5]=digest;
    receipt[6]=sizeof(void *);
    receipt[7]=0;
    if(!WriteFile(output,receipt,sizeof(receipt),&n,0) || n!=sizeof(receipt)) ExitProcess(4);
    ExitProcess(failures!=0);
}
