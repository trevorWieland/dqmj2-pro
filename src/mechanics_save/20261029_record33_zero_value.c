typedef unsigned char u8;
typedef signed char s8;
typedef signed short s16;
typedef unsigned int u32;

typedef struct {
    u8 prefix[0x2E];
    s16 kind;
    u8 middle[0xF0];
    s16 first;
    s16 second;
    u8 tail[0xB];
    u8 marker;
} StateView;

typedef struct {
    u8 prefix[0x14C];
    s16 pairs[6][2];
    u8 middle[8];
    s8 state;
} TransferState;

extern TransferState *native_transfer_state(int side);
extern const u8 *native_transfer_enabled(void);
extern const u32 *native_transfer_flags(void);
extern StateView *native_state_view(int side, s8 index);

void preparation_record33_zero_value(int side) {
    TransferState *state;
    int all_front_nonpositive = 1;
    int index;
    state = native_transfer_state(side);
    if (*native_transfer_enabled() == 0)
        return;
    if (state->state != -1)
        return;
    if ((*native_transfer_flags() & 0x20000000) == 0)
        return;
    index = 0;
    do {
        StateView *view = native_state_view(side, index);
        if (view->kind != -1) {
            view->first = state->pairs[index][0];
            view->second = state->pairs[index][1];
            if (view->first > 0 && index < 3)
                all_front_nonpositive = 0;
            if (view->first == 0)
                view->marker = 1;
        }
        index++;
    } while (index < 6);
    if (all_front_nonpositive) {
        int second_index = 0;
        do {
            StateView *view = native_state_view(side, second_index);
            if (view->kind != -1) {
                view->first = 1;
                view->marker = 0;
            }
            second_index++;
        } while (second_index < 3);
    }
}
