#include "context000.h"

unsigned long native_main_0201ed2c(int base, int max_width, int (*ReadProc)(void *, int, int), void *ReadProcArg, int* chars_scanned, int* negative, int* overflow) {
    int scan_state = start;
    int count = 0;
    int spaces = 0;
    unsigned long value = 0;
    unsigned long value_max = 0;
    int c;
    *negative = *overflow = 0;
    if (base < 0 || base == 1 || base > 36 || max_width < 1) {
        scan_state = failure;
    }
    else {
        c = (count++, (*ReadProc)(ReadProcArg, 0, 0)) ;
    }
    if (base != 0) {
        value_max = 0xffffffffUL / base;
    }
    while (count <= max_width && c != -1 && !(scan_state & (finished | failure)) ) {
        switch (scan_state) {
            case start:
                if (isspace(c)) {
                    c = (count++, (*ReadProc)(ReadProcArg, 0, 0)) ;
                    count--;
                    spaces++;
                    break;
                }
                if (c == '+') {
                    c = (count++, (*ReadProc)(ReadProcArg, 0, 0)) ;
                }
                else if (c == '-') {
                    c = (count++, (*ReadProc)(ReadProcArg, 0, 0)) ;
                    *negative = 1;
                }
                scan_state = check_for_zero;
                break;
            case check_for_zero:
                if (base == 0 || base == 16) {
                    if (c == '0') {
                        scan_state = leading_zero;
                        c = (count++, (*ReadProc)(ReadProcArg, 0, 0)) ;
                        break;
                    }
                }
                scan_state = need_digit;
                break;
            case 4:
                if (c == 'X' || c == 'x') {
                    base = 16;
                    scan_state = need_digit;
                    c = (count++, (*ReadProc)(ReadProcArg, 0, 0)) ;
                    break;
                }
                if (base == 0) {
                    base = 8;
                }
                scan_state = digit_loop;
                break;
            case need_digit:
            case digit_loop:
                if (base == 0) {
                    base = 10;
                }
                if (!value_max) {
                    value_max = 0xffffffffUL / base;
                }
                if (isdigit(c)) {
                    if ((c -= '0') >= base) {
                        if (scan_state == digit_loop) {
                            scan_state = finished;
                        }
                        else {
                            scan_state = failure;
                        }
                        c += '0';
                        break;
                    }
                }
                else if (!isalpha(c) || (toupper(c) - 'A' + 10) >= base) {
                    if (scan_state == digit_loop) {
                        scan_state = finished;
                    }
                    else {
                        scan_state = failure;
                    }
                    break;
                }
                else {
                    c = toupper(c) - 'A' + 10;
                }
                if (value > value_max) {
                    *overflow = 1;
                }
                value *= base;
                if (c > (0xffffffffUL - value)) {
                    *overflow = 1;
                }
                value += c;
                scan_state = digit_loop;
                c = (count++, (*ReadProc)(ReadProcArg, 0, 0)) ;
                break;
        }
    }
    if (!(scan_state & (leading_zero | digit_loop | finished)) ) {
        count = 0;
        value = 0;
        *chars_scanned = 0;
    }
    else {
        count--;
        *chars_scanned = count + spaces;
    }
    (*ReadProc)(ReadProcArg, c, 1) ;
    return value;
}
