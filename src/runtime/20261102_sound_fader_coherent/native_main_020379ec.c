typedef unsigned int u32;
    typedef signed long long int s64;
typedef struct NNSSndFader {
    int origin;
    int target;
    int counter;
    int frame;
} NNSSndFader;
u32 native_main_020379ec (u32 raw)
{
    const NNSSndFader * fader = (const NNSSndFader *)raw;
    s64 value;
    ((void) 0) ;
    if (fader->counter >= fader->frame) {
        return fader->target;
    }
    value = (fader->target - fader->origin)
            * fader->counter / fader->frame
            + fader->origin;
    return (u32)(int)value;
}
