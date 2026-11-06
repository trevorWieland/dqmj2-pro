typedef signed int s32;
typedef unsigned int u32;
typedef signed short s16;
extern u32 native_fn_0200235c(u32 numerator, s32 denominator);
extern const s16 native_data_020d7fe0[129];

u32 native_main_020028d8(s32 y, s32 x) {
    s32 numerator;
    s32 denominator;
    s32 offset;
    s32 positive;
    if (y > 0) {
        if (x > 0) {
            if (x > y) {
                numerator = y;
                denominator = x;
                offset = 0;
                positive = 1;
            } else if (x < y) {
                numerator = x;
                denominator = y;
                offset = 6434;
                positive = 0;
            } else {
                return 3217;
            }
        } else if (x < 0) {
            x = (s32)(0U - (u32)x);
            if (x < y) {
                numerator = x;
                denominator = y;
                offset = 6434;
                positive = 1;
            } else if (x > y) {
                numerator = y;
                denominator = x;
                offset = 12868;
                positive = 0;
            } else {
                return 9651;
            }
        } else {
            return 6434;
        }
    } else if (y < 0) {
        y = (s32)(0U - (u32)y);
        if (x < 0) {
            x = (s32)(0U - (u32)x);
            if (x > y) {
                numerator = y;
                denominator = x;
                offset = -12868;
                positive = 1;
            } else if (x < y) {
                numerator = x;
                denominator = y;
                offset = -6434;
                positive = 0;
            } else {
                return -9651;
            }
        } else if (x > 0) {
            if (x < y) {
                numerator = x;
                denominator = y;
                offset = -6434;
                positive = 1;
            } else if (x > y) {
                numerator = y;
                denominator = x;
                offset = 0;
                positive = 0;
            } else {
                return -3217;
            }
        } else {
            return -6434;
        }
    } else {
        if (x >= 0) {
            return 0;
        }
        return 12868;
    }
    if (denominator == 0) {
        return 0;
    }
    if (positive) {
        return (s16)(offset + native_data_020d7fe0[((s32)native_fn_0200235c((u32)numerator, denominator)) >> 5]);
    }
    return (s16)(offset - native_data_020d7fe0[((s32)native_fn_0200235c((u32)numerator, denominator)) >> 5]);
}
