typedef unsigned int u32;
typedef signed int s32;
_Static_assert(sizeof(void *)==4,"Four-byte pointers required");
_Static_assert(sizeof(u32)==4,"Four-byte words required");
__declspec(dllimport) void __stdcall ExitProcess(u32 code);
__declspec(dllimport) void *__stdcall GetStdHandle(u32 handle);
__declspec(dllimport) s32 __stdcall ReadFile(void *handle,void *data,u32 bytes,u32 *read,void *overlapped);
__declspec(dllimport) s32 __stdcall WriteFile(void *handle,const void *data,u32 bytes,u32 *written,void *overlapped);
extern u32 native_main_02096cf8(u32 *record);
extern u32 native_main_02096d9c(u32 *record);
extern u32 native_main_02096d4c(u32 *record);
extern u32 native_main_02096d6c(u32 *record);
extern u32 native_main_02096d24(u32 *record);
extern u32 native_main_02096d04(u32 *record);
typedef u32 (*Reader)(u32 *record);
static Reader readers[6]={native_main_02096cf8,native_main_02096d9c,native_main_02096d4c,native_main_02096d6c,native_main_02096d24,native_main_02096d04};
static u32 expected[32][6];
static u32 records[64][3];
static u32 receipt[8]={0x4A325041u,4,64,32,0,0,2166136261u,0};

static void finish(u32 code) {
    u32 written;
    WriteFile(GetStdHandle((u32)-11),receipt,sizeof(receipt),&written,(void *)0);
    ExitProcess(code);
}

static void read_exact(void *destination,u32 bytes) {
    unsigned char *target=destination;
    u32 received;
    while (bytes) {
        if (!ReadFile(GetStdHandle((u32)-10),target,bytes,&received,(void *)0)||!received||received>bytes) finish(43);
        target+=received;
        bytes-=received;
    }
}

void j2p_entry(void) {
    u32 header[2];
    u32 index,flags,helper,word,result,byte;
    read_exact(header,sizeof(header));
    if (header[0]!=0x4A325047u||header[1]!=32) finish(44);
    read_exact(expected,sizeof(expected));
    for (index=0;index<64;++index) {
        for (flags=0;flags<32;++flags) {
            word=(((index*0x9E3779B9u)^0xA5A507FFu)&~(31u<<11))|(flags<<11);
            records[index][0]=word;
            records[index][1]=0x13579BDFu;
            records[index][2]=0xFEDCBA98u;
            for (helper=0;helper<6;++helper) {
                result=readers[helper](records[index]);
                ++receipt[4];
                if (result!=expected[flags][helper]||records[index][0]!=word||records[index][1]!=0x13579BDFu||records[index][2]!=0xFEDCBA98u) ++receipt[5];
                for (byte=0;byte<4;++byte) receipt[6]=(receipt[6]^((result>>(byte*8))&255))*16777619u;
            }
        }
    }
    finish(receipt[5]?42:0);
}
