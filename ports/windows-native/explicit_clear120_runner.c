typedef unsigned char u8;
typedef unsigned int u32;
typedef signed int s32;
_Static_assert(sizeof(void *) == 4, "Four-byte pointer ABI required");
__declspec(dllimport) void __stdcall ExitProcess(u32);
__declspec(dllimport) void *__stdcall GetStdHandle(u32);
__declspec(dllimport) s32 __stdcall WriteFile(void *, const void *, u32, u32 *, void *);
extern u32 native_main_020bf5c0(u32);
extern u32 native_main_0207cdb8(u32);
extern u32 retained_main_020bf5c0(u32);
extern u32 retained_main_0207cdb8(u32);
_Alignas(4) u8 native_data_021d4bec[32];
_Alignas(4) u8 native_data_021c67a8[16];
static u32 expected_selector;
static u32 expected_pointer;
static u32 helper_result;
static u32 helper_calls;
static u32 helper_bad;
static u32 receipt[12] = {0x4A324346u, 1, 0, 0, 0, 0, 0, 0, 0, 0, 2166136261u, 0};
static const u32 selectors[16] = {0,1,2,15,16,127,128,255,65535,65536,0x7FFFFFFFu,0x80000000u,0xFFFFFF80u,0xFFFFFFFEu,0xFFFFFFFFu,0x12345678u};
static const u32 pointers[8] = {0,1,2,32,0x12345678u,0x76543210u,0x80000000u,0xFFFFFFFFu};
static const u32 returns[4] = {0,1,0x80000000u,0xFFFFFFFFu};

__declspec(noinline) u32 native_fn_0202a498(u32 selector, u32 pointer) {
    ++helper_calls;
    helper_bad |= selector != expected_selector || pointer != expected_pointer;
    return helper_result;
}

static void finish(u32 code) {
    u32 written;
    WriteFile(GetStdHandle((u32)-11), receipt, sizeof(receipt), &written, (void *)0);
    ExitProcess(code);
}

static void run_case(u32 kind, u32 legacy, u32 selector, u32 pointer, u32 result, u32 seed) {
    u32 i, got, expected_return, bad;
    u8 first_expected[32], second_expected[16];
    for (i=0;i<32;++i) native_data_021d4bec[i]=first_expected[i]=(u8)(i*37+seed);
    for (i=0;i<16;++i) native_data_021c67a8[i]=second_expected[i]=(u8)(i*43+seed);
    *(u32 *)(native_data_021d4bec+8)=*(u32 *)(first_expected+8)=pointer;
    *(u32 *)native_data_021c67a8=*(u32 *)second_expected=pointer;
    expected_selector=selector;
    expected_pointer=pointer;
    helper_result=result;
    helper_calls=helper_bad=0;
    if (pointer) {
        if (kind) *(u32 *)second_expected=0;
        else *(u32 *)(first_expected+8)=0;
    }
    if (legacy) got=kind ? retained_main_0207cdb8(selector) : retained_main_020bf5c0(selector);
    else got=kind ? native_main_0207cdb8(selector) : native_main_020bf5c0(selector);
    expected_return=pointer ? (kind ? (u32)native_data_021c67a8 : (u32)native_data_021d4bec) : selector;
    bad=helper_bad || helper_calls!=(pointer!=0) || got!=expected_return;
    for (i=0;i<32;++i) bad |= native_data_021d4bec[i]!=first_expected[i];
    for (i=0;i<16;++i) bad |= native_data_021c67a8[i]!=second_expected[i];
    if (legacy) {
        ++receipt[4];
        receipt[5]+=bad!=0;
        receipt[6]+=bad==0;
        receipt[8]+=helper_calls;
    } else {
        ++receipt[2];
        receipt[3]+=bad==0;
        receipt[7]+=helper_calls;
        for (i=0;i<32;++i) receipt[10]=(receipt[10]^native_data_021d4bec[i])*16777619u;
        for (i=0;i<16;++i) receipt[10]=(receipt[10]^native_data_021c67a8[i])*16777619u;
        if (bad) ++receipt[9];
    }
}

void j2p_entry(void) {
    u32 kind, legacy, s, p, r, seed;
    for (kind=0;kind<2;++kind)
        for (legacy=0;legacy<2;++legacy)
            for (s=0;s<16;++s)
                for (p=0;p<8;++p)
                    for (r=0;r<4;++r)
                        for (seed=0;seed<2;++seed)
                            run_case(kind,legacy,selectors[s],pointers[p],returns[r],seed?255:0);
    if (receipt[2]!=2048 || receipt[3]!=2048 || receipt[4]!=2048 || receipt[5]!=1792 || receipt[6]!=256 || receipt[7]!=1792 || receipt[8]!=1792 || receipt[9]) finish(42);
    finish(0);
}
