typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef struct {volatile s8 timer;u8 pad[23];u32 current,phase,next,previous;} State;
typedef struct {void (*start)(void);u32 (*step)(void);void (*finish)(void);} Mode;
typedef struct {u16 unused,buttons;} Input;
extern State data_ov003_021e0690;
extern u32 data_ov003_021e06a8[];
extern u8 data_ov003_021e06b8[];
extern Mode data_ov003_021e0160[];
extern u32 func_0202a1e0(u32);
extern void func_ov003_021da898(void);
extern void func_02048e8c(void);
extern void func_ov003_021daa44(void);
extern void func_ov003_021daac4(void);
extern void func_020414c8(u32);
extern void func_020418b0(u32);
extern u32 func_020c3a00(void);
extern void func_020c39f0(u32);
extern void func_02048e74(void *,u32);
extern void *func_ov003_021dad9c(void);
extern void func_02048fcc(void *);
extern u32 func_02027400(void);
extern void func_ov003_021d79e4(u32);
extern void func_02041538(u32,u32,u32);
extern void func_ov003_021dff60(void);
extern u32 func_02041814(void);
extern u32 func_02062520(void);
extern u32 func_020653d0(void);
extern void func_ov003_021dea38(u32,u32,u32,u32,u32,int);
extern void func_ov003_021df6ac(void);
extern Input *func_0202a634(void);
extern void func_ov003_021df668(u32);
extern void func_ov003_021d7fa4(void);
extern void func_ov003_021d7878(u32);
extern u32 func_020c39e0(void);
extern void func_020c39d0(u32);
extern u32 func_020273c8(void);
extern void func_02045738(u32);
extern void func_0206258c(u32);
extern void func_020c40f4(u32);
extern void func_02041898(u32);
extern void func_020414b0(u32);
extern void func_0204176c(void);
extern void func_ov003_021de710(void);
extern void func_ov003_021dfbf4(void);
extern void func_ov003_021dacec(void);
extern void func_ov003_021daa0c(void);

u32 native_ov003_021da50c(void) {
    Mode *handlers;
    u32 *pending;
    u32 result=9;
    u32 again;
    u32 message;
    Input *input;
    pending=data_ov003_021e06a8;handlers=data_ov003_021e0160;
    do {
        volatile State *state=&data_ov003_021e0690;
        Mode *mode;
        u32 current;
        u32 phase;
        current=state->current;mode=&handlers[current];phase=state->phase;
        again=0;
        switch(phase) {
        case 0:mode->start();pending[1]=1;again=1;break;
        case 1: {
            u32 next=mode->step();
            if(next!=pending[0]) {pending[2]=next;pending[3]=pending[0];pending[1]=3;again=1;}
            break;
        }
        case 3:
            func_ov003_021dad9c();func_ov003_021dff60();
            if(func_02041814()==1) break;
            if(!func_02062520()) break;
            switch(pending[2]) {
            case 9:pending[1]=6;break;
            case 8:pending[1]=10;break;
            case 10:pending[1]=8;break;
            case 11:pending[1]=9;break;
            default:pending[1]=2;break;
            }
            again=1;break;
        case 2:
            mode->finish();func_02048fcc(data_ov003_021e06b8);pending[1]=0;pending[0]=pending[2];pending[2]=12;break;
        case 4:
            state->timer--;
            if(state->timer) break;
            switch(func_020653d0()) {
            case 0:state->timer=80;message=48;break;
            case 5:state->timer=5;message=50;break;
            default:state->timer=5;message=49;break;
            }
            func_ov003_021dea38(20,1,message,1,1,func_020653d0()==0?-1:87);func_020418b0(2);pending[1]=5;func_ov003_021dad9c();func_ov003_021df6ac();break;
        case 5:
            input=func_0202a634();func_ov003_021dad9c();func_ov003_021df6ac();
            if(state->timer==80) func_ov003_021d79e4(62);
            if(state->timer==0 && (input->buttons&0xFF7)) {
                func_ov003_021df668(0);func_ov003_021d7fa4();func_ov003_021d79e4(33);pending[1]=0;
            }
            state->timer--;
            if(state->timer<0) state->timer=0;
            break;
        case 6:func_ov003_021d7878(2);pending[1]=7;break;
        case 7:
            if(func_020c39e0()==3) {func_ov003_021df668(1);func_02041538(1,2,10);func_020c39d0(1);}
            if(func_020273c8()!=12) result=0;
            break;
        case 8:func_02045738(1);func_0206258c(0);func_020c40f4(1);func_020c39f0(2);result=3;break;
        case 9:func_02045738(1);func_0206258c(0);func_020c40f4(1);result=3;break;
        case 10:func_02041898(2);func_020414b0(63);func_ov003_021d7878(1);result=0;break;
        }
    } while(again);
    func_0204176c();
    return result;
}
