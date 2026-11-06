typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef int s32;
typedef struct {u8 enabled,page,limit,pad;u32 saved,result,phase;} Panel;
typedef struct {u32 result,phase;} Mode;
typedef struct {void (*start)(void);void (*step)(void);} Callback;
typedef struct {u16 unused,pressed,pad,repeat;} Input;
extern Panel data_ov003_021e0a18;
extern Mode data_ov003_021e0a20;
extern Callback data_ov003_021e01cc[];
extern char data_ov003_021e0394[];
extern char data_ov003_021e03a8[];
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

void native_ov003_021dd074(void) {
    func_02048e74(&data_ov003_021e0a20,6);func_02048fcc(func_ov003_021dad9c());data_ov003_021e0a18.phase=0;
}

void native_ov003_021dd19c(void) {func_ov003_021df4b4(1);func_ov003_021dfccc();}

void native_ov003_021dd1b0(void) {
    Input *input=func_0202a634();s32 *cursor=func_ov003_021dad9c();
    if(input->repeat&64){if(*cursor>0)*cursor=*cursor-1;else *cursor=data_ov003_021e0a18.limit;func_0205e7a8(-1,85);}
    else if(input->repeat&128){if(*cursor<data_ov003_021e0a18.limit)*cursor=*cursor+1;else *cursor=0;func_0205e7a8(-1,85);}
}

void native_ov003_021dd22c(void) {
    func_ov003_021ded08(func_ov003_021dad9c(),4,16,1,3,30,2,0);func_ov003_021dec40(func_ov003_021dad9c(),1);func_020620b4(39);func_02062358(1);
}

void native_ov003_021dd28c(void) {
    s32 *cursor=func_ov003_021dad9c();func_ov003_021df4b4(3);data_ov003_021e0a18.limit=3;func_ov003_021deda4(cursor,4,data_ov003_021e0394,2,6,28,data_ov003_021e0a18.enabled);func_ov003_021dfd18(1);data_ov003_021e0a18.saved=0;
}

void native_ov003_021dd5f4(void) {
    s32 *cursor=func_ov003_021dad9c();data_ov003_021e0a18.limit=5;
    if(data_ov003_021e0a18.saved)func_ov003_021df4b4(3);else func_ov003_021df4b4(4);
    if(data_ov003_021e0a18.saved){func_ov003_021ded08(cursor,45,16,2,5,29,2,1);data_ov003_021e0a18.saved=0;}
    func_ov003_021deda4(cursor,6,data_ov003_021e03a8,2,8,28,data_ov003_021e0a18.enabled);func_ov003_021dfd18(1);
}
