typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef signed int s32;
_Static_assert(sizeof(void *)==4,"Four-byte pointer ABI required");
__declspec(dllimport) void __stdcall ExitProcess(u32);
__declspec(dllimport) void *__stdcall GetStdHandle(u32);
__declspec(dllimport) s32 __stdcall WriteFile(void *,const void *,u32,u32 *,void *);
extern u32 typed138(u32,u32,u32);
extern u32 retained138(u32,u32,u32);
extern u32 wrong138(u32,u32,u32);
extern u32 getter_actual138(u32);
extern u32 setter_actual138(u32,u32,u32);
typedef struct { u8 unknown_0[1]; s8 field_1; } Record_native_data_021b8ae0;
Record_native_data_021b8ae0 native_data_021b8ae0;
_Alignas(8) u8 native_data_021b8b10[128];
static u8 expected_rows[128];
static u32 family,expected_index,expected_value,expected_third,getter_calls,setter_calls,getter_bad,sdk_calls,sdk_bad,setter_bad;
static u32 actual[3],passed[3],rejected[3],other_fail[3],real_getter[3],sdk_total[3];
static u32 sdk_fail_total,setter_fail_total;
static u32 fingerprint=2166136261u;
static const u32 values[7]={0,1,127,128,255,0x80000000u,0xFFFFFFFFu};
static const u32 thirds[4]={0,1,0x12345678u,0xFFFFFFFFu};
static const u32 halves[4]={0,0x7FFF,0x8000,0xFFFF};

__declspec(noinline) u32 guarded_getter138(u32 index) {
    getter_calls++;
    if(index!=expected_index) { getter_bad++; return 0x6BADF00Du; }
    real_getter[family]++;
    return getter_actual138(index);
}
__declspec(noinline) u32 guarded_setter138(u32 index,u32 value,u32 third) {
    setter_calls++;
    if(index!=expected_index || value!=expected_value || third!=expected_third) setter_bad++;
    return setter_actual138(index,value,third);
}
__declspec(noinline) u32 sdk_callback138(void *row,u32 value,u32 third) {
    sdk_calls++;
    if(expected_index>=16 || row!=(void *)(native_data_021b8b10+8*expected_index) || value!=expected_value || third!=expected_third) sdk_bad++;
    return 0xDEADBEEFu;
}
__declspec(noinline) u32 host_status138(s8 value) {
    native_data_021b8ae0.field_1=value;
    return value==0;
}
static void one(u32 which,u32 index,u32 value,u32 third,u32 half,u32 previous,u32 seed) {
    u32 i,result,expected_return=0xFFFFFFFFu,expected_status=12,expected_sdk=0,good;
    family=which;expected_index=index;expected_value=value;expected_third=third;
    getter_calls=setter_calls=getter_bad=sdk_calls=sdk_bad=setter_bad=0;
    for(i=0;i<128;i++) native_data_021b8b10[i]=(u8)(i*29+seed);
    if(index<16) {
        native_data_021b8b10[index*8+4]=(u8)half;
        native_data_021b8b10[index*8+5]=(u8)(half>>8);
        native_data_021b8b10[index*8+6]=(u8)previous;
    }
    for(i=0;i<128;i++) expected_rows[i]=native_data_021b8b10[i];
    if(index<16) {
        expected_status=8;
        if((half&0x8000)==0) {
            expected_return=(u8)previous;
            expected_status=value>127?16:0;
            if(value<=127) { expected_rows[index*8+6]=(u8)value;expected_sdk=1; }
        }
    }
    native_data_021b8ae0.unknown_0[0]=0x7Bu;
    native_data_021b8ae0.field_1=0x5A;
    result=which==0?typed138(index,value,third):which==1?retained138(index,value,third):wrong138(index,value,third);
    actual[which]++;
    good=result==expected_return && getter_calls==1 && setter_calls==1 && setter_bad==0 && sdk_bad==0 && sdk_calls==expected_sdk && native_data_021b8ae0.unknown_0[0]==0x7Bu && (u8)native_data_021b8ae0.field_1==expected_status;
    for(i=0;i<128;i++) good&=native_data_021b8b10[i]==expected_rows[i];
    if(good && !getter_bad) passed[which]++;
    else if(getter_bad) rejected[which]++;
    else other_fail[which]++;
    sdk_total[which]+=sdk_calls;
    sdk_fail_total+=sdk_bad;setter_fail_total+=setter_bad;
    fingerprint=(fingerprint^result)*16777619u;
}
void j2p_entry(void) {
    u32 i,k,j,t,written=0,n=0,receipt[24];
    for(i=0;i<4096;i++) {
        u32 index=i&15,third=i%8==0?index:thirds[(i>>1)%4];
        for(k=0;k<3;k++) one(k,index,values[(i>>4)%7],third,halves[(i>>2)%4],(i>>4)&255,i+1);
        n++;
    }
    for(i=0;i<4;i++) for(j=0;j<7;j++) for(t=0;t<4;t++) {
        u32 index=i==0?16:i==1?17:i==2?0x80000000u:0xFFFFFFFFu;
        for(k=0;k<3;k++) one(k,index,values[j],thirds[t],0,255,n+1);
        n++;
    }
    receipt[0]=0x4A325346u;receipt[1]=1;receipt[2]=n;
    for(k=0;k<3;k++) { receipt[3+4*k]=actual[k];receipt[4+4*k]=passed[k];receipt[5+4*k]=rejected[k];receipt[6+4*k]=other_fail[k];receipt[15+k]=real_getter[k];receipt[18+k]=sdk_total[k]; }
    receipt[21]=fingerprint;receipt[22]=sdk_fail_total;receipt[23]=setter_fail_total;
    if(passed[0]!=n || rejected[0]!=0 || other_fail[0]!=0 || rejected[1]==0 || other_fail[1]!=0 || rejected[2]==0 || passed[2]==0 || other_fail[2]!=0) ExitProcess(80);
    if(!WriteFile(GetStdHandle((u32)-11),receipt,sizeof(receipt),&written,0) || written!=sizeof(receipt)) ExitProcess(81);
    ExitProcess(0);
}
