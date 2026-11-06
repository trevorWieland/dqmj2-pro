typedef unsigned char u8;typedef unsigned int u32;typedef signed int s32;typedef unsigned long long u64;typedef signed long long s64;
typedef struct{u32 x,y;u8*state;u32 size;}Stream;
extern void native_ov006_021ed86c(Stream*,const u8*,u32,u32);
extern void native_ov006_021ed8d0(Stream*,u8*,const u8*,u32);
extern u32 native_ov006_021ed8fc(Stream*);
extern u32 native_ov006_021ed964(u32,const u8*,s32,u32,u32*);
extern void native_ov006_021ed99c(s32,u32*);
extern void native_ov006_021f08fc(const u8*,const u8*,u8*);
