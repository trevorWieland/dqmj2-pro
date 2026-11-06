static inline s16 DecodeAdpcm (int code, AdpcmState * state)
{
    int step;
    int sample;
    int index;
    int d;
    sample = state->prevSample;
    index = state->prevIndex;
    step = native_data_020d91b0[ index ];
    d = step >> 3;
    if (code & 4) d += step;
    if (code & 2) d += step >> 1;
    if (code & 1) d += step >> 2;
    if (code & 8) {
        sample -= d;
        if (sample < -32768) sample = -32768;
    } else {
        sample += d;
        if (sample > 32767) sample = 32767;
    }
    index += native_data_020d91a0[ code ];
    if (index < 0) index = 0;
    else if (index > 89 - 1) index = 89 - 1;
    state->prevSample = (s16)sample;
    state->prevIndex = (u8)index;
    return (s16)sample;
}

void native_fn_0203aa0c (NNSSndStrmPlayer * player);

typedef struct J2StreamGlobals {int initialized;struct NNSSndStrmThread *prepareThread;u8 *decodeBuffer;} J2StreamGlobals;

extern J2StreamGlobals native_data_020f4c84;
