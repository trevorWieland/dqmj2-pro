typedef unsigned int u32;
typedef unsigned long long u64;
extern u64 native_fn_02007a9c(void);
extern void native_fn_02008c28(const void *, void *, u32);
extern unsigned char native_data_021e6e24[];
typedef struct State {
    u32 first;
    u32 second;
    u32 third;
    u32 fourth;
    unsigned char payload[64];
} State;
void native_ov005_021d87b4(State *state)
{
    state->first = native_fn_02007a9c() & 3;
    state->second = (native_fn_02007a9c() >> 2) & 3;
    state->third = 0;
    state->fourth = 0;
    native_fn_02008c28(native_data_021e6e24, state->payload, 64);
}
