typedef unsigned char u8;
typedef signed char s8;
typedef unsigned int u32;
typedef struct { signed char active:1; signed char done:1; signed char changed:1; signed char started:1; signed char running:4; } Flags;
typedef struct { u8 prefix[200]; u32 allocation; s8 heap; u8 pad[4]; Flags flags; } Menu;
extern Menu data_ov003_021e058c;
extern u8 data_ov003_021e0464[];
extern u32 data_ov003_021e0468[];
extern u32 data_ov003_021e0474[];
extern u32 data_ov003_021e0480[];
extern u32 data_ov003_021e048c[];
extern void func_ov003_021d82f4(u32);
extern u8 func_ov003_021d85e4(u32,s8 *,s8 *,u32);
extern void func_0205fd18(void);
extern void func_ov003_021d8890(void);
extern void func_0202a498(s8,void *);
extern void func_0205fd4c(u32,u32);
extern void func_0205fd34(void *,u32);
extern u32 func_0205fd28(void *);
extern void func_0205fd0c(void *);


typedef signed short s16;
typedef struct {s16 x,y;} Position;
typedef struct {u8 bytes[12];} Cell;
typedef struct {u8 prefix[16];Cell cells[49];} Runtime;
extern Runtime *func_02061944(void);
extern void func_02065818(void *,u32,s8);
extern void func_020456ac(u32,u32,u32,u32,u32,u32);
extern void func_020622ec(u32,u32,u32);
extern u8 data_ov003_021e057c[];
extern u32 data_ov003_021e0580[];
extern void func_ov003_021d97a4(u32);
extern u8 func_ov003_021d97f8(u32,s8 *,s8 *,s8 *,u32);
extern void func_ov003_021d9c60(void);
extern u32 **func_02061dcc(s8);
extern void func_02049f4c(void *);
extern void func_02049ffc(u32);
extern void func_0204ab44(u32,Position *,u32,u32,u32,u32,u32);
extern u8 *func_02062a10(u32);
extern u8 *func_020c3948(u32);
extern u32 func_02044cdc(s16);
extern int func_020630b0(u32);
extern void func_020602ec(void *,s16,void *,u32,u32,u32);
extern void func_0204aaf0(s8,Position *,u32,u32,u32,u32,u32);
extern void func_0204ab98(s8,Position *,u32,void *,u32);
extern void func_0204a9d4(s8,Position *,u32,u32,u32,u32);
extern char data_ov003_021e02dc[];

void native_ov003_021d9984(u32 title,u32 *ids) {
    s8 index;
    u32 count;
    u8 *record;
    s8 cell;
    u8 offset;
    int limit;
    for(index=0;index<10;index++) func_02049f4c(func_02061dcc((s8)(index+6)));
    for(index=0;index<10;index++) func_02049ffc((*func_02061dcc((s8)(index+6)))[1]);
    {
        Position position={0,0};
        func_0204ab44(6,&position,20,0,title,1,1);
    }
    offset=0;
    for(index=0;index<3;index++) {
        switch(data_ov003_021e057c[1]) {
        case 1:record=func_02062a10(ids[index]);break;
        case 0:record=func_020c3948(ids[index]);break;
        }
        if(record) {
            count=func_02044cdc(*(s16 *)(record+24));
            func_020602ec(*func_02061dcc((s8)(offset+7)),*(s16 *)(record+24),record,0,0,1);
            cell=(s8)(offset+10);
            limit=func_020630b0(record[28]);
            { Position position={0,0};
            func_0204aaf0(cell,&position,5,1,1,1,1);
            position.x+=16;
            func_0204ab98(cell,&position,1,data_ov003_021e02dc,0);
            position.x+=8;
            if(record[48]!=100) func_0204a9d4(cell,&position,record[48]<limit?1:5,record[48],2,0);
            {
                Position marker={0,0};
                marker.x=0;
                func_0204aaf0((s8)(offset+13),&marker,0,1,record[50],1,1);
            }
            }
            offset=(u8)(offset+(count+1));
        }
    }
}

void native_ov003_021d9bd0(u32 id,u32 x,s8 y,u32 flag) {
    Runtime *runtime=func_02061944();
    u32 offset=id*12;
    Cell *cells=runtime->cells;
    switch(id) { case 3:case 4:case 5: {
        if(flag) native_ov003_021d9bd0(1,x,y,1);
        else native_ov003_021d9bd0(2,x,y,0);
        func_02065818((u8 *)cells+offset,x,y);
    break;} default:func_02065818((u8 *)cells+offset,x,y);break;}
}

void native_ov003_021d9c60(void) {
    func_020456ac(0,1,1,2,30,21);
    func_020456ac(0,2,1,2,30,21);
}

void native_ov003_021d9cb8(void) {
    s8 a=6,b=8,c=6;
    u8 index;
    for(index=0;index<3;index++) {
        func_ov003_021d97a4(data_ov003_021e0580[index]);
        if(data_ov003_021e058c.flags.started) {
            data_ov003_021e058c.flags.started=0;
            func_ov003_021d9c60();break;
        }
        data_ov003_021e057c[0]+=func_ov003_021d97f8(data_ov003_021e0580[index],&a,&b,&c,data_ov003_021e057c[1]);
    }
    data_ov003_021e058c.flags.changed=0;
    data_ov003_021e058c.flags.done=1;
}

void native_ov003_021d9d84(void) {
    data_ov003_021e058c.flags.active=0;
    if(data_ov003_021e058c.allocation) func_0202a498(data_ov003_021e058c.heap,(void *)data_ov003_021e058c.allocation);
    func_0205fd4c(0,0);
}

void native_ov003_021d9dc0(void) {
    if(!data_ov003_021e058c.flags.active) return;
    data_ov003_021e058c.flags.running=0;
    data_ov003_021e058c.flags.started=0;
    func_0205fd34(&data_ov003_021e058c,16);
    while(!func_0205fd28(&data_ov003_021e058c)) {
        data_ov003_021e058c.flags.running=0;
        data_ov003_021e058c.flags.started=0;
        func_0205fd0c(&data_ov003_021e058c);
    }
}
