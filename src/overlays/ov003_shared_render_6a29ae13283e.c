typedef unsigned char u8;
typedef signed char s8;
typedef signed short s16;
typedef unsigned int u32;
typedef struct {u8 bytes[12];} Cell;
typedef struct {u8 prefix[16]; Cell cells[49];u32 offset;} Runtime;
typedef struct {s8 id;u8 count;} Entry;
extern u8 data_ov003_021e057c[];
extern char data_ov003_021e02c4[];
extern Entry data_ov003_021e014a[];
extern Runtime *func_02061944(void);
extern void func_0201d444(void *,const char *,...);
extern void func_0205ff80(void *);
extern void func_0205ff9c(void);
extern u32 func_02065730(void *,s8,u32,u32,u32);
extern u8 *func_02062a10(u32);
extern u8 *func_020c3948(u32);
extern u32 func_02044cdc(s16);
extern void func_02061c1c(s8,u32,u8,u32,u32,u32,u32);
extern void func_02045ed0(u32);
extern void func_02061de4(void *,s16,u32,u32,u32);
extern void func_ov003_021d9bd0(s8,u32,s8,u32);

void native_ov003_021d95a0(void) {
    s8 index;
    Runtime *runtime=func_02061944();
    char filename[32];
    u32 delta;
    func_0201d444(filename,data_ov003_021e02c4);
    func_0205ff80(filename);
    for(index=0;index<11;index++) {
        delta=func_02065730(&runtime->cells[index+1],data_ov003_021e014a[index].id,0,data_ov003_021e014a[index].count,runtime->offset);
        runtime->offset=runtime->offset+delta;
    }
    func_0205ff9c();
}

void native_ov003_021d9634(u32 *ids) {
    u8 index;
    u32 y;
    u8 *record;
    u32 count;
    func_02061c1c(6,3,3,26,2,0,0);
    y=6;
    for(index=0;index<3;index++) {
        switch(data_ov003_021e057c[1]) {
        case 1:record=func_02062a10(ids[index]);break;
        case 0:record=func_020c3948(ids[index]);break;
        }
        if(!record) count=0;
        else count=func_02044cdc(*(s16 *)(record+24));
        switch(count) {
        case 1:y=(u8)(y+3);break;
        case 2:y=(u8)(y+5);break;
        }
        func_02061c1c((s8)(index+7),7,(u8)y,11,2,0,0);
        func_02061c1c((s8)(index+10),19,(u8)y,5,2,0,0);
        func_02061c1c((s8)(index+13),10,(u8)(y+2),17,2,0,0);
        y=(u8)(y+(count==1?3:6));
    }
    func_02045ed0(1);
}

void native_ov003_021d97a4(u32 id) {
    Runtime *runtime=func_02061944();
    u8 *record=func_02062a10(id);
    if(record) func_02061de4(&runtime->cells[data_ov003_021e057c[0]+3],*(s16 *)(record+24),data_ov003_021e057c[0],1,0);
}

u8 native_ov003_021d97f8(u32 id,s8 *a,s8 *b,s8 *c,u32 flag) {
    u8 index;
    u8 *record;
    u32 count;
    func_02061944();
    switch(data_ov003_021e057c[1]) {
    case 1:record=func_02062a10(id);break;
    case 0:record=func_020c3948(id);break;
    }
    if(!record) return 0;
    count=func_02044cdc(*(s16 *)(record+24));
    index=0;
    do {
        func_ov003_021d9bd0((s8)(data_ov003_021e057c[0]+3+index),1,*a,flag);
        *a=*a+5;
        index++;
    } while(index<=count);
    if(count) *a+=2;
    else *a+=1;
    switch(count) {
    case 1:*b+=3;*c+=3;break;
    case 2:*b+=5;*c+=5;break;
    }
    func_ov003_021d9bd0((s8)(record[50]+6),7,*b,0);
    if(record[48]==100) func_ov003_021d9bd0(11,22,*c,0);
    if(count) {*b+=9;*c+=9;}
    else {*b+=6;*c+=6;}
    return index;
}
