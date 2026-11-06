typedef unsigned char u8;
typedef unsigned int u32;

typedef struct {
    u8 prefix[0x14];
    u32 status;
} Result;

typedef struct State State;
typedef u32 (*Operation)(State *, u32, u32, u32);

struct State {
    u8 prefix[0x1C];
    u32 flags;
    u8 gap[4];
    Result *result;
    u8 gap2[0x28];
    Operation operation;
};

typedef struct {
    State *state;
    u32 offset;
} Cursor;

extern u32 native_fn_02007ff4(void);
extern u32 native_fn_02008008(u32);
extern void native_fn_020068d4(void *);

u32 native_main_0200a81c(Cursor *cursor, u32 value, u32 length) {
    State *state = cursor->state;
    u32 status;
    state->flags |= 0x200;
    status = state->operation(state, value, cursor->offset, length);
    switch (status) {
    case 0:
    case 1:
        state->flags &= ~0x200U;
        break;
    case 6: {
        u32 irq = native_fn_02007ff4();
        u32 waiting;
        if (state->flags & 0x200) {
            waiting = 1;
        } else {
            waiting = 0;
        }
        if (waiting != 0) {
            do {
                native_fn_020068d4((u8 *)state + 0xC);
                if (state->flags & 0x200) {
                    waiting = 1;
                } else {
                    waiting = 0;
                }
            } while (waiting != 0);
        }
        native_fn_02008008(irq);
        status = state->result->status;
        break;
    }
    }
    cursor->offset += length;
    return status;
}
