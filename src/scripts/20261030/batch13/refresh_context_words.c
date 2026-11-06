#include "scr_context_words.h"
void refresh_context_words(void)
{
    reset_context_words();
    float state = get_numeric_state(0);
    if (state == 2) {
        state = get_numeric_state(3);
        if (state <= 6) {
            set_context_word(2, 0);
        } else {
            {
                set_context_word(2, 10800);
            }
        }
    } else {
        if (state == 3) {
            set_context_word(1, 10800);
        }
    }
    bool enabled = get_primary_flag(209);
    if (enabled == false) {
        set_context_word(3, 0);
    }
    enabled = get_primary_flag(210);
    if (enabled == false) {
        set_context_word(6, 0);
    }
    enabled = get_primary_flag(212);
    if (enabled == false) {
        set_context_word(4, 0);
    }
    enabled = get_primary_flag(211);
    if (enabled == false) {
        set_context_word(5, 0);
    }
    state = get_numeric_state(20);
    if (state <= 28) {
        set_context_word(15, 0);
    }
}
