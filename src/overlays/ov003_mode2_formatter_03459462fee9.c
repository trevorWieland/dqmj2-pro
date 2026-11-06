typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef int s32;
typedef struct {u32 result,phase;} Mode;
typedef struct {u16 unused,pressed,pad,repeat;} Input;
extern Mode data_ov003_021e0a08;
extern Mode data_ov003_021e0a08_alias1;
extern char data_ov003_021e0350[];
extern void func_02048e74(void *,u32);
extern s32 *func_ov003_021dad9c(void);
extern u32 func_ov003_021dada8(void);
extern void func_02048fcc(void *);
extern void func_ov003_021dce68(void);
extern void func_ov003_021dcf60(void);
extern void func_ov003_021dff60(void *);
extern void func_ov003_021df6ac(void *);
extern u32 func_02041814(void);
extern void func_ov003_021df4b4(u32);
extern void func_ov003_021dfccc(void);
extern void func_ov003_021ded08(void *,u32,u32,u32,u32,u32,u32,u32);
extern void func_ov003_021deda4(void *,u32,void *,u32,u32,u32,u32);
extern void func_ov003_021dfd18(u32);
extern void func_020620e8(u32,u32);
extern u32 func_02041944(void);
extern void func_02041538(u32,u32,u32);
extern Input *func_0202a634(void);
extern void func_0205e7a8(s32,u32);
extern void func_020c356c(u32);
extern void func_020c39f0(u32);
extern void func_02061260(u32);

void native_ov003_021dce68(void) {
    s32 *cursor;
    if(func_ov003_021dada8()!=1){func_ov003_021ded08(func_ov003_021dad9c(),2,16,1,3,30,2,0);}
    func_ov003_021ded08(func_ov003_021dad9c(),12,16,2,5,29,2,1);
    cursor=func_ov003_021dad9c();func_ov003_021deda4(cursor,2,data_ov003_021e0350,2,8,28,*func_ov003_021dad9c());func_ov003_021dfd18(1);
    if(func_ov003_021dada8()!=1)func_020620e8(37,1);
    if(func_02041944())func_02041538(0,2,10);
}
