#include "scr_registered_flags.h"
extern float registered_key_0;
extern float registered_key_1;
extern float registered_key_2;
extern float registered_key_3;
extern float registered_key_4;
extern float registered_key_5;
extern float registered_key_6;
extern float registered_key_7;
extern float registered_key_8;
extern float registered_key_9;
extern float registered_flag_0;
extern float registered_flag_1;
extern float registered_flag_2;
extern float registered_flag_3;
extern float registered_flag_4;
extern float registered_flag_5;
extern float registered_flag_6;
extern float registered_flag_7;
extern float registered_flag_8;
extern float registered_flag_9;
float apply_registered_primary(float candidate)
{
    float flag_index = -1;
    bool enabled;
    if (candidate == registered_key_0) {
        flag_index = registered_flag_0;
    } else {
        if (candidate == registered_key_1) {
            flag_index = registered_flag_1;
        } else {
            if (candidate == registered_key_2) {
                flag_index = registered_flag_2;
            } else {
                if (candidate == registered_key_3) {
                    flag_index = registered_flag_3;
                } else {
                    if (candidate == registered_key_4) {
                        flag_index = registered_flag_4;
                    } else {
                        if (candidate == registered_key_5) {
                            flag_index = registered_flag_5;
                        } else {
                            if (candidate == registered_key_6) {
                                flag_index = registered_flag_6;
                            } else {
                                if (candidate == registered_key_7) {
                                    flag_index = registered_flag_7;
                                } else {
                                    if (candidate == registered_key_8) {
                                        flag_index = registered_flag_8;
                                    } else {
                                        if (candidate == registered_key_9) {
                                            flag_index = registered_flag_9;
                                        } else {
                                            {
                                                candidate = -1;
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    if (candidate != -1) {
        enabled = get_primary_flag(flag_index);
        if (enabled == false) {
            set_primary_flag(flag_index, true);
        } else {
            {
                flag_index = -1;
            }
        }
    }
    return candidate;
}
