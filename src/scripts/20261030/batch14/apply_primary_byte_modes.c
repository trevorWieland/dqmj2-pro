#include "scr_byte_mode.h"
void apply_primary_byte_modes(float saved_input)
{
    bool enabled = get_primary_flag(207);
    if (enabled == false) {
        select_context_byte_mode(2, 0);
    }
    enabled = get_primary_flag(208);
    if (enabled == false) {
        select_context_byte_mode(3, 0);
    }
    enabled = get_primary_flag(209);
    if (enabled == false) {
        select_context_byte_mode(4, 0);
    }
    enabled = get_primary_flag(210);
    if (enabled == false) {
        select_context_byte_mode(5, 0);
    }
    enabled = get_primary_flag(212);
    if (enabled == false) {
        select_context_byte_mode(8, 0);
    }
    enabled = get_primary_flag(211);
    if (enabled == false) {
        select_context_byte_mode(7, 0);
    }
}
