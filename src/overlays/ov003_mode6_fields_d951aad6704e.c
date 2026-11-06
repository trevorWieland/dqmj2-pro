extern unsigned short data_ov003_021e0374[];
extern unsigned short data_ov003_021e035c[];
extern char data_ov003_021e037a[];
extern unsigned short data_ov003_021e0380[];
extern char data_ov003_021e0386[];
extern unsigned short data_ov003_021e0368[];
extern char data_ov003_021e0358[];
extern unsigned short data_ov003_021e0354[];
extern char data_ov003_021e036e[];
extern unsigned short data_ov003_021e0362[];
typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef int s32;
typedef struct {u8 enabled,page,limit,pad;u32 saved,result,phase;u32 gap[2];struct {u32 kind,a,b,c,d,e;} settings;} Panel;
typedef struct {u32 result,phase;} Mode;
typedef struct {void (*start)(void);void (*step)(void);} Callback;
typedef struct {u16 unused,pressed,pad,repeat;} Input;
extern Panel data_ov003_021e0a18;
extern Mode data_ov003_021e0a20;
extern Callback data_ov003_021e01cc[];
extern char data_ov003_021e0394[];
extern void func_02048e74(void *,u32);
extern s32 *func_ov003_021dad9c(void);
extern void func_02048fcc(void *);
extern void func_ov003_021dd22c(void);
extern u32 func_020c35fc(void);
extern void func_ov003_021dfccc(void);
extern void func_ov003_021dff60(void *);
extern void func_ov003_021df6ac(void *);
extern void func_ov003_021dd1b0(void);
extern u32 func_ov003_021de064(void);
extern void func_ov003_021df4b4(u32);
extern Input *func_0202a634(void);
extern void func_0205e7a8(s32,u32);
extern void func_ov003_021ded08(void *,u32,u32,u32,u32,u32,u32,u32);
extern void func_ov003_021dec40(void *,u32);
extern void func_020620b4(u32);
extern void func_02062358(u32);
extern void func_ov003_021deda4(void *,u32,void *,u32,u32,u32,u32);
extern void func_ov003_021dfd18(u32);

typedef struct {u32 kind,a,b,c,d,e;} Settings;
extern Settings data_ov003_021e0a30;
extern Settings *func_020c36ac(void);
extern void func_ov003_021da3e4(Settings *);
extern void func_ov003_021da3d0(void);
extern void func_020c35ec(u32);
extern void func_020c360c(u32);
extern void func_020c362c(u32);
extern void func_020c364c(u32);
extern void func_020c366c(u32);
extern void func_020c368c(u32);
extern void func_ov003_021deaf8(void *);
extern void func_ov003_021dea38(u32,u32,u16,u32,u32,s32);
extern unsigned short data_ov003_021e038c[];
extern char data_ov003_021e03a8[];

extern unsigned short data_ov003_021e039c[];
extern void func_02008e0c(const void *,void *,u32);

void native_ov003_021dd6c4(void) {
    s32 *cursor;Input *input;input=func_0202a634();cursor=func_ov003_021dad9c();func_ov003_021da3e4(&data_ov003_021e0a30);func_ov003_021da3d0();
    if(input->pressed&1){u8 selected=(u8)*cursor;switch(selected){
    case 0:data_ov003_021e0a18.page=2;break;case 1:data_ov003_021e0a18.page=3;break;case 2:data_ov003_021e0a18.page=4;break;case 3:data_ov003_021e0a18.page=5;break;case 4:data_ov003_021e0a18.page=6;break;}
        if(selected==5){func_02008e0c(&data_ov003_021e0a30,func_020c36ac(),24);func_020c35ec(3);func_020c360c(data_ov003_021e0a18.settings.a);func_020c362c(data_ov003_021e0a18.settings.b);func_020c364c(data_ov003_021e0a18.settings.c);func_020c366c(data_ov003_021e0a18.settings.d);func_020c368c(data_ov003_021e0a18.settings.e);data_ov003_021e0a18.phase=4;}
        else {func_ov003_021da3d0();data_ov003_021e0a18.phase=1;}
        func_0205e7a8(-1,82);return;
    }
    if(input->pressed&2){func_02008e0c(func_020c36ac(),&data_ov003_021e0a30,24);data_ov003_021e0a18.page=0;data_ov003_021e0a18.phase=1;data_ov003_021e0a18.enabled=3;func_0205e7a8(-1,83);return;}
    if(input->pressed&0x800){u8 selected=(u8)*cursor;func_ov003_021deaf8(cursor);func_ov003_021dea38(20,1,data_ov003_021e039c[selected],1,1,87);data_ov003_021e0a18.phase=3;}
}

void native_ov003_021dd8a4(void) {
    func_ov003_021dad9c();func_ov003_021df4b4(4);data_ov003_021e0a18.limit=2;data_ov003_021e0a18.enabled=func_020c36ac()->a;func_ov003_021ded08(func_ov003_021dad9c(),33,16,3,7,28,2,2);func_ov003_021deda4(func_ov003_021dad9c(),3,data_ov003_021e036e,2,10,28,data_ov003_021e0a18.enabled);func_ov003_021dfd18(1);
}

void native_ov003_021dd94c(void) {
    Input *input=func_0202a634();s32 *cursor=func_ov003_021dad9c();
    if(input->pressed&1){data_ov003_021e0a18.settings.a=*cursor;data_ov003_021e0a18.page=1;data_ov003_021e0a18.enabled=0;data_ov003_021e0a18.phase=1;func_0205e7a8(-1,82);return;}
    if(input->pressed&2){data_ov003_021e0a18.page=1;data_ov003_021e0a18.enabled=0;data_ov003_021e0a18.phase=1;func_0205e7a8(-1,83);return;}
    if(input->pressed&0x800){u8 selected=(u8)*cursor;func_ov003_021deaf8(cursor);func_ov003_021dea38(20,1,data_ov003_021e0362[selected],1,1,87);data_ov003_021e0a18.phase=3;}
}

void native_ov003_021dda30(void) {
    func_ov003_021dad9c();func_ov003_021df4b4(4);data_ov003_021e0a18.limit=1;data_ov003_021e0a18.enabled=func_020c36ac()->b;func_ov003_021ded08(func_ov003_021dad9c(),34,16,3,7,28,2,2);func_ov003_021deda4(func_ov003_021dad9c(),2,data_ov003_021e0358,2,10,28,data_ov003_021e0a18.enabled);func_ov003_021dfd18(1);
}

void native_ov003_021ddad8(void) {
    Input *input=func_0202a634();s32 *cursor=func_ov003_021dad9c();
    if(input->pressed&1){data_ov003_021e0a18.settings.b=*cursor;data_ov003_021e0a18.page=1;data_ov003_021e0a18.enabled=1;func_ov003_021da3d0();data_ov003_021e0a18.phase=1;func_0205e7a8(-1,82);return;}
    if(input->pressed&2){data_ov003_021e0a18.page=1;data_ov003_021e0a18.enabled=1;data_ov003_021e0a18.phase=1;func_0205e7a8(-1,83);return;}
    if(input->pressed&0x800){u8 selected=(u8)*cursor;func_ov003_021deaf8(cursor);func_ov003_021dea38(20,1,data_ov003_021e0354[selected],1,1,87);data_ov003_021e0a18.phase=3;}
}

void native_ov003_021ddbc0(void) {
    func_ov003_021dad9c();func_ov003_021df4b4(4);data_ov003_021e0a18.limit=2;data_ov003_021e0a18.enabled=func_020c36ac()->c;func_ov003_021ded08(func_ov003_021dad9c(),35,16,3,7,28,2,2);func_ov003_021deda4(func_ov003_021dad9c(),3,data_ov003_021e0386,2,10,28,data_ov003_021e0a18.enabled);func_ov003_021dfd18(1);
}

void native_ov003_021ddc68(void) {
    Input *input=func_0202a634();s32 *cursor=func_ov003_021dad9c();
    if(input->pressed&1){data_ov003_021e0a18.settings.c=*cursor;data_ov003_021e0a18.page=1;data_ov003_021e0a18.enabled=2;data_ov003_021e0a18.phase=1;func_0205e7a8(-1,82);return;}
    if(input->pressed&2){data_ov003_021e0a18.page=1;data_ov003_021e0a18.enabled=2;data_ov003_021e0a18.phase=1;func_0205e7a8(-1,83);return;}
    if(input->pressed&0x800){u8 selected=(u8)*cursor;func_ov003_021deaf8(cursor);func_ov003_021dea38(20,1,data_ov003_021e0368[selected],1,1,87);data_ov003_021e0a18.phase=3;}
}

void native_ov003_021ddd4c(void) {
    func_ov003_021dad9c();func_ov003_021df4b4(4);data_ov003_021e0a18.limit=2;data_ov003_021e0a18.enabled=func_020c36ac()->d;func_ov003_021ded08(func_ov003_021dad9c(),36,16,3,7,28,2,2);func_ov003_021deda4(func_ov003_021dad9c(),3,data_ov003_021e037a,2,10,28,data_ov003_021e0a18.enabled);func_ov003_021dfd18(1);
}

void native_ov003_021dddf4(void) {
    Input *input=func_0202a634();s32 *cursor=func_ov003_021dad9c();
    if(input->pressed&1){data_ov003_021e0a18.settings.d=*cursor;data_ov003_021e0a18.page=1;data_ov003_021e0a18.enabled=3;data_ov003_021e0a18.phase=1;func_0205e7a8(-1,82);return;}
    if(input->pressed&2){data_ov003_021e0a18.page=1;data_ov003_021e0a18.enabled=3;data_ov003_021e0a18.phase=1;func_0205e7a8(-1,83);return;}
    if(input->pressed&0x800){u8 selected=(u8)*cursor;func_ov003_021deaf8(cursor);func_ov003_021dea38(20,1,data_ov003_021e0374[selected],1,1,87);data_ov003_021e0a18.phase=3;}
}

void native_ov003_021dded8(void) {
    func_ov003_021dad9c();func_ov003_021df4b4(4);data_ov003_021e0a18.limit=2;data_ov003_021e0a18.enabled=func_020c36ac()->e;func_ov003_021ded08(func_ov003_021dad9c(),37,16,3,7,28,2,2);func_ov003_021deda4(func_ov003_021dad9c(),3,data_ov003_021e035c,2,10,28,data_ov003_021e0a18.enabled);func_ov003_021dfd18(1);
}

void native_ov003_021ddf80(void) {
    Input *input=func_0202a634();s32 *cursor=func_ov003_021dad9c();
    if(input->pressed&1){data_ov003_021e0a18.settings.e=*cursor;data_ov003_021e0a18.page=1;data_ov003_021e0a18.enabled=4;data_ov003_021e0a18.phase=1;func_0205e7a8(-1,82);return;}
    if(input->pressed&2){data_ov003_021e0a18.page=1;data_ov003_021e0a18.enabled=4;data_ov003_021e0a18.phase=1;func_0205e7a8(-1,83);return;}
    if(input->pressed&0x800){u8 selected=(u8)*cursor;func_ov003_021deaf8(cursor);func_ov003_021dea38(20,1,data_ov003_021e0380[selected],1,1,87);data_ov003_021e0a18.phase=3;}
}
