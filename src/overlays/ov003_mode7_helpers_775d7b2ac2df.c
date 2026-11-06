typedef unsigned char u8;
typedef signed char s8;
typedef signed short s16;
typedef unsigned short u16;
typedef unsigned int u32;
typedef int s32;
typedef struct {s16 x,y;} Position;
typedef struct {u32 *root;void *callback;} Object;
typedef struct {u16 pad,pressed;} Input;
extern u8 data_ov003_021e07e0[];
typedef struct {u8 prefix[493];u8 first;} RosterHeader;
extern RosterHeader data_ov003_021e07f4;
extern char data_021c9698[];
extern void *func_ov003_021de854(u32);
extern Object *func_02049ad0(s8);
extern Object *func_02049ae4(void);
extern void func_02049ffc(u32);
extern void func_02049f4c(void *);
extern void func_020602ec(void *,s16,void *,s32,u32,u32);
extern void func_0204a724(s8,Position *,u32,u32,u32,u32,u32,u32);
extern void func_02065818(void *,s8,s8);
extern u32 func_02049f24(void);
extern void func_02049f30(void);
extern void func_02046af4(void *,u32,u32,u32,u32,u32);
extern void func_02049f14(u32);
extern void func_ov003_021dea38(u32,u32,u16,u32,u32,s32);
extern void func_ov003_021dfd18(u32);
extern void func_020853c8(void *,void *);
extern Input *func_0202a634(void);
extern void func_ov003_021df668(u32);
extern void func_ov003_021df6ac(void *);
extern void func_ov003_021df830(void *,s8,s8,s8,u32,u32);
extern void func_ov003_021dff60(void *);

void native_ov003_021dcaec(u8 *record,u32 index) {
    Position position={0,0};
    void *label;
    Object *object;
    if(index<data_ov003_021e07f4.first) label=func_ov003_021de854(7);else label=func_ov003_021de854(8);
    object=func_02049ad0(5);func_02049ffc(object->root[1]);func_02049f4c(object);position.x=24;func_020602ec(object->root,*(s16 *)(record+24),record,position.x,0,1);position.x=0;func_0204a724(5,&position,24,0,1,record[50],1,0);func_02065818(label,3,3);
}

void native_ov003_021dcbc4(void) {
    Object *current=func_02049ae4();
    u32 frame=func_02049f24();
    u32 selected;
    Object *object;
    u8 *detail;
    func_02049f30();selected=*(u32 *)((u8 *)&data_ov003_021e07f4+248);object=func_02049ad0((s8)(selected+8));detail=(u8 *)object->root[1];
    func_02046af4(data_021c9698,*(u32 *)(detail+104),detail[94],0,frame,255);func_02049f14(frame);func_ov003_021dea38(0,1,(u16)((u8)selected+8),1,1,87);func_ov003_021dfd18(0);
    if(current->root) func_020853c8(current->callback,current->root);
    *(u32 *)&data_ov003_021e07f4=5;
}

void native_ov003_021dcc8c(void) {
    Input *input=func_0202a634();
    if(input->pressed&0xFF7) {func_ov003_021df668(1);*(u32 *)&data_ov003_021e07f4=4;}
}

void native_ov003_021dccc4(u32 option) {data_ov003_021e07e0[1]=option;}

void native_ov003_021dccd4(u8 *cursor) {
    cursor[16]=7;func_ov003_021df6ac(cursor);func_ov003_021df830(cursor,(s8)data_ov003_021e07e0[0],(s8)(data_ov003_021e07e0[0]+8),(s8)(data_ov003_021e07e0[0]+15),28,28);func_ov003_021dff60(cursor);
}
