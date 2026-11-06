#include "context000.h"

int native_main_02020890(void *(*WriteProc)(void *, const wchar_t *, size_t), void *WriteProcArg, const wchar_t * format_str, va_list arg) {
    int num_chars, chars_written, field_width;
    const wchar_t* format_ptr;
    const wchar_t* curr_format;
    print_format format;
    long long_num;
    long long long_long_num;
    long double long_double_num;
    wchar_t buff[512];
    wchar_t* buff_ptr;
    wchar_t* string_end;
    char* cstring_end;
    wchar_t fill_char = L' ';
    char* strptr;
    format_ptr = format_str;
    chars_written = 0;
    while (*format_ptr) {
        if (!(curr_format = native_fn_020212c4(format_ptr, L'%'))) {
            num_chars = native_fn_02021258(format_ptr);
            chars_written += num_chars;
            if (num_chars && !(*WriteProc)(WriteProcArg, format_ptr, num_chars)) {
                return -1;
            }
            break;
        }
        num_chars = curr_format - format_ptr;
        chars_written += num_chars;
        if (num_chars && !(*WriteProc)(WriteProcArg, format_ptr, num_chars)) {
            return -1;
        }
        format_ptr = curr_format;
        format_ptr = native_fn_0201f2c0(format_ptr, &arg, &format);
        switch (format.conversion_char) {
            case L'd':
            case L'i':
                if (format.argument_options == long_argument) {
                    long_num = (*( long *)((arg += ((sizeof( long)+3)&~3)) - ((sizeof( long)+3)&~3))) ;
                }
                else if (format.argument_options == long_long_argument) {
                    long_long_num = (*( long long *)((arg += ((sizeof( long long)+3)&~3)) - ((sizeof( long long)+3)&~3))) ;
                }
                else if (format.argument_options == intmax_argument) {
                    long_long_num = (*( intmax_t *)((arg += ((sizeof( intmax_t)+3)&~3)) - ((sizeof( intmax_t)+3)&~3))) ;
                }
                else if (format.argument_options == size_t_argument) {
                    long_num = (*( size_t *)((arg += ((sizeof( size_t)+3)&~3)) - ((sizeof( size_t)+3)&~3))) ;
                }
                else if (format.argument_options == ptrdiff_argument) {
                    long_num = (*( ptrdiff_t *)((arg += ((sizeof( ptrdiff_t)+3)&~3)) - ((sizeof( ptrdiff_t)+3)&~3))) ;
                }
                else {
                    long_num = (*( int *)((arg += ((sizeof( int)+3)&~3)) - ((sizeof( int)+3)&~3))) ;
                }
                if (format.argument_options == short_argument) {
                    long_num = (short)long_num;
                }
                if ((format.argument_options == long_long_argument) || (format.argument_options == intmax_argument)) {
                    if (!(buff_ptr = native_fn_0201fa88(long_long_num, buff + 512, format))) {
                        goto conversion_error;
                    }
                }
                else {
                    if (!(buff_ptr = native_fn_0201f838(long_num, buff + 512, format))) {
                        goto conversion_error;
                    }
                }
                num_chars = buff + 512 - 1 - buff_ptr;
                break;
            case L'o':
            case L'u':
            case L'x':
            case L'X':
                if (format.argument_options == long_argument) {
                    long_num = (*( unsigned long *)((arg += ((sizeof( unsigned long)+3)&~3)) - ((sizeof( unsigned long)+3)&~3))) ;
                }
                else if (format.argument_options == long_long_argument) {
                    long_long_num = (*( long long *)((arg += ((sizeof( long long)+3)&~3)) - ((sizeof( long long)+3)&~3))) ;
                }
                else if (format.argument_options == intmax_argument) {
                    long_long_num = (*( intmax_t *)((arg += ((sizeof( intmax_t)+3)&~3)) - ((sizeof( intmax_t)+3)&~3))) ;
                }
                else if (format.argument_options == size_t_argument) {
                    long_num = (*( size_t *)((arg += ((sizeof( size_t)+3)&~3)) - ((sizeof( size_t)+3)&~3))) ;
                }
                else if (format.argument_options == ptrdiff_argument) {
                    long_num = (*( ptrdiff_t *)((arg += ((sizeof( ptrdiff_t)+3)&~3)) - ((sizeof( ptrdiff_t)+3)&~3))) ;
                }
                else {
                    long_num = (*( unsigned int *)((arg += ((sizeof( unsigned int)+3)&~3)) - ((sizeof( unsigned int)+3)&~3))) ;
                }
                if (format.argument_options == short_argument) {
                    long_num = (unsigned short)long_num;
                }
                if ((format.argument_options == long_long_argument) || (format.argument_options == intmax_argument)) {
                    if (!(buff_ptr = native_fn_0201fa88(long_long_num, buff + 512, format))) {
                        goto conversion_error;
                    }
                }
                else {
                    if (!(buff_ptr = native_fn_0201f838(long_num, buff + 512, format))) {
                        goto conversion_error;
                    }
                }
                num_chars = buff + 512 - 1 - buff_ptr;
                break;
            case L'f':
            case L'F':
            case L'e':
            case L'E':
            case L'g':
            case L'G':
                if (format.argument_options == long_double_argument) {
                    long_double_num = (*( long double *)((arg += ((sizeof( long double)+3)&~3)) - ((sizeof( long double)+3)&~3))) ;
                }
                else {
                    long_double_num = (*( double *)((arg += ((sizeof( double)+3)&~3)) - ((sizeof( double)+3)&~3))) ;
                }
                if (!(buff_ptr = native_fn_02020244(long_double_num, buff + 512, format))) {
                    goto conversion_error;
                }
                num_chars = buff + 512 - 1 - buff_ptr;
                break;
            case 'a':
            case 'A':
                if (format.argument_options == long_double_argument) {
                    long_double_num = (*( long double *)((arg += ((sizeof( long double)+3)&~3)) - ((sizeof( long double)+3)&~3))) ;
                }
                else {
                    long_double_num = (*( double *)((arg += ((sizeof( double)+3)&~3)) - ((sizeof( double)+3)&~3))) ;
                }
                if (!(buff_ptr = native_fn_0201fd88(long_double_num, buff + 512, format))) {
                    goto conversion_error;
                }
                num_chars = buff + 512 - 1 - buff_ptr;
                break;
            case L's':
                if (format.argument_options == wchar_argument) {
                    buff_ptr = (*( wchar_t * *)((arg += ((sizeof( wchar_t *)+3)&~3)) - ((sizeof( wchar_t *)+3)&~3))) ;
                    if(0 && buff_ptr == ((void *)0) ){
                        __msl_runtime_constraint_violation_s(((void *)0) , ((void *)0) , -1);
                        return -1;
                    }
                    if (buff_ptr == ((void *)0) ) {
                        buff_ptr = native_data_020dd184;
                    }
                    if (format.alternate_form)
                    {
                        num_chars = (unsigned char) *buff_ptr++;
                        if (format.precision_specified && num_chars > format.precision)
                            num_chars = format.precision;
                    }
                    else if (format.precision_specified)
                    {
                        num_chars = format.precision;
                        if ((string_end = (wchar_t *)native_fn_0201f298(buff_ptr, 0, num_chars)) != 0) {
                            num_chars = string_end - buff_ptr;
                        }
                    }
                    else
                        num_chars = native_fn_02021258(buff_ptr);
                }
                else {
                    strptr = (*( char * *)((arg += ((sizeof( char *)+3)&~3)) - ((sizeof( char *)+3)&~3))) ;
                    if(0 && strptr == ((void *)0) ){
                        __msl_runtime_constraint_violation_s(0,0,-1);
                        return -1;
                    }
                    if (strptr == ((void *)0) ) {
                          strptr = native_data_020dd188;
                    }
                    if (format.alternate_form) {
                        num_chars = (unsigned char) *buff_ptr++;
                        if (format.precision_specified && num_chars > format.precision) {
                            num_chars = format.precision;
                        }
                    }
                    else if (format.precision_specified) {
                        num_chars = format.precision;
                        if ((cstring_end = (char *) native_fn_0201b21c(strptr, 0, num_chars)) != 0) {
                            num_chars = cstring_end - strptr;
                        }
                    }
                    else
                        num_chars = native_fn_0201d69c(strptr);
                      if ((num_chars = native_fn_0201b09c(buff, strptr, num_chars)) < 0)
                        goto conversion_error;
                    buff_ptr = &buff[0];
                }
                break;
            case 'n':
                if(0){
                    __msl_runtime_constraint_violation_s(0,0,-1);
                    return -1;
                }
                buff_ptr = (*( wchar_t * *)((arg += ((sizeof( wchar_t *)+3)&~3)) - ((sizeof( wchar_t *)+3)&~3))) ;
                switch (format.argument_options) {
                    case normal_argument:
                        *(int*)buff_ptr = chars_written;
                        break;
                    case short_argument:
                        *(short*)buff_ptr = chars_written;
                        break;
                    case long_argument:
                        *(long*)buff_ptr = chars_written;
                        break;
                    case intmax_argument:
                        *(intmax_t*)buff_ptr = chars_written;
                        break;
                    case size_t_argument:
                        *(size_t*)buff_ptr = chars_written;
                        break;
                    case ptrdiff_argument:
                        *(ptrdiff_t*)buff_ptr = chars_written;
                        break;
                    case long_long_argument:
                        *(long long*)buff_ptr = chars_written;
                        break;
                }
                continue;
            case L'c':
                buff_ptr = buff;
                if (format.argument_options == wchar_argument) {
                    *buff_ptr = (*( int *)((arg += ((sizeof( int)+3)&~3)) - ((sizeof( int)+3)&~3))) ;
                    num_chars = 1;
                }
                else {
                    char chint = (*( int *)((arg += ((sizeof( int)+3)&~3)) - ((sizeof( int)+3)&~3))) ;
                    num_chars = native_fn_0201b018(buff, &chint, 1);
                }
                break;
            case L'%':
                buff_ptr = buff;
                *buff_ptr = '%';
                num_chars = 1;
                break;
            case 0xFFFF:
            default:
                conversion_error:
                    num_chars = native_fn_02021258(curr_format);
                    chars_written += num_chars;
                    if (num_chars && !(*WriteProc)(WriteProcArg, curr_format, num_chars)) {
                        return -1;
                    }
                    return chars_written;
                    break;
        }
        field_width = num_chars;
        if (format.justification_options != left_justification) {
            fill_char = (format.justification_options == zero_fill) ? L'0' : L' ';
            if (((*buff_ptr == L'+') || (*buff_ptr == L'-') || (*buff_ptr == L' ')) && (fill_char == L'0')) {
                if ((*WriteProc)(WriteProcArg, buff_ptr, 1) == 0) {
                    return -1;
                }
                ++buff_ptr;
                num_chars--;
            }
            while (field_width < format.field_width) {
                if ((*WriteProc)(WriteProcArg, &fill_char, 1) == 0) {
                    return -1;
                }
                ++field_width;
            }
        }
        if (num_chars && !(*WriteProc)(WriteProcArg, buff_ptr, num_chars)) {
            return -1;
        }
        if (format.justification_options == left_justification) {
            while (field_width < format.field_width) {
                wchar_t blank = L' ';
                if ((*WriteProc)(WriteProcArg, &blank, 1) == 0) {
                    return -1;
                }
                ++field_width;
            }
        }
        chars_written += field_width;
    }
    return chars_written;
}
