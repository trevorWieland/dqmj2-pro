typedef unsigned int size_t;
typedef long ptrdiff_t;
typedef long long intmax_t;
typedef unsigned short wchar_t;
typedef char *va_list;
enum justification_options { left_justification, right_justification, zero_fill };
enum sign_options { only_minus, sign_always, space_holder };
enum argument_options {
    normal_argument,
    char_argument,
    short_argument,
    long_argument,
    long_long_argument,
    wchar_argument,
    intmax_argument,
    size_t_argument,
    ptrdiff_argument,
    long_double_argument,
};
typedef struct {
    unsigned char justification_options;
    unsigned char sign_options;
    unsigned char precision_specified;
    unsigned char alternate_form;
    unsigned char argument_options;
    unsigned char conversion_char;
    int field_width;
    int precision;
} print_format;
typedef char NdsFormatterAbiRequired[(sizeof(void *) == 4 && sizeof(long) == 4 && sizeof(ptrdiff_t) == 4 && sizeof(long double) == 8 && sizeof(wchar_t) == 2 && sizeof(print_format) == 16) ? 1 : -1];
extern wchar_t native_data_020dd11c[];
extern char native_data_020dd120[];
extern const char *native_fn_0201b338(const char *, va_list *, print_format *);
extern char *native_fn_0201b8c8(long, char *, print_format);
extern char *native_fn_0201bb14(long long, char *, print_format);
extern char *native_fn_0201c410(long double, char *, print_format);
extern char *native_fn_0201be10(long double, char *, print_format);
extern unsigned int native_fn_0201b124(char *, const wchar_t *, unsigned int);
extern unsigned int native_fn_0201d69c(const char *);
extern char *native_fn_0201d948(const char *, int);
extern void *native_fn_0201b21c(const void *, int, unsigned int);
int native_main_0201cb74(unsigned int (*WriteProc)(void*, const char*, size_t), void* WriteProcArg,
                        const char* format_str, va_list arg
                       )
{
    int num_chars, chars_written, field_width;
    const char* format_ptr;
    const char* curr_format;
    print_format format;
    signed long long_num;
    signed long long long_long_num;
    long double long_double_num;
    char buff[512];
    char* buff_ptr;
    char* string_end;
    char fill_char = ' ';
    format_ptr = format_str;
    chars_written = 0;
    while (*format_ptr) {
        if (!(curr_format = native_fn_0201d948(format_ptr, '%'))) {
            num_chars = native_fn_0201d69c(format_ptr);
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
        format_ptr = native_fn_0201b338(format_ptr, &arg, &format);
        switch (format.conversion_char) {
        case 'd':
        case 'i':
            if (format.argument_options == long_argument) {
                long_num = (*(signed long *)((arg += sizeof(signed long)) - sizeof(signed long)));
            } else if (format.argument_options == long_long_argument) {
                long_long_num = (*(signed long long *)((arg += sizeof(signed long long)) - sizeof(signed long long)));
            }
            else if (format.argument_options == intmax_argument) {
                long_long_num = (*(intmax_t *)((arg += sizeof(intmax_t)) - sizeof(intmax_t)));
            }
            else if (format.argument_options == size_t_argument) {
                long_num = (*(size_t *)((arg += sizeof(size_t)) - sizeof(size_t)));
            }
            else if (format.argument_options == ptrdiff_argument) {
                long_num = (*(ptrdiff_t *)((arg += sizeof(ptrdiff_t)) - sizeof(ptrdiff_t)));
            }
            else {
                long_num = (*(int *)((arg += sizeof(int)) - sizeof(int)));
            }
            if (format.argument_options == short_argument) {
                long_num = (signed short)long_num;
            }
            if (format.argument_options == char_argument) {
                long_num = (signed char)long_num;
            }
            if ((format.argument_options == long_long_argument)
                || format.argument_options == intmax_argument
               )
            {
                if ((buff_ptr = native_fn_0201bb14(long_long_num, buff + 512, format)) != 0) {
                } else {
                    goto conversion_error;
                }
            } else {
                if (!(buff_ptr = native_fn_0201b8c8(long_num, buff + 512, format))) {
                    goto conversion_error;
                }
            }
            num_chars = buff + 512 - 1 - buff_ptr;
            break;
        case 'o':
        case 'u':
        case 'x':
        case 'X':
            if (format.argument_options == long_argument) {
                long_num = (*(unsigned long *)((arg += sizeof(unsigned long)) - sizeof(unsigned long)));
            } else if (format.argument_options == long_long_argument) {
                long_long_num = (*(signed long long *)((arg += sizeof(signed long long)) - sizeof(signed long long)));
            }
            else if (format.argument_options == intmax_argument) {
                long_long_num = (*(intmax_t *)((arg += sizeof(intmax_t)) - sizeof(intmax_t)));
            }
            else if (format.argument_options == size_t_argument) {
                long_num = (*(size_t *)((arg += sizeof(size_t)) - sizeof(size_t)));
            }
            else if (format.argument_options == ptrdiff_argument) {
                long_num = (*(ptrdiff_t *)((arg += sizeof(ptrdiff_t)) - sizeof(ptrdiff_t)));
            }
            else {
                long_num = (*(unsigned int *)((arg += sizeof(unsigned int)) - sizeof(unsigned int)));
            }
            if (format.argument_options == short_argument) {
                long_num = (unsigned short)long_num;
            }
            if (format.argument_options == char_argument) {
                long_num = (unsigned char)long_num;
            }
            if ((format.argument_options == long_long_argument)
                || format.argument_options == intmax_argument
               )
            {
                if ((buff_ptr = native_fn_0201bb14(long_long_num, buff + 512, format)) != 0) {
                } else {
                    goto conversion_error;
                }
            } else {
                if (!(buff_ptr = native_fn_0201b8c8(long_num, buff + 512, format))) {
                    goto conversion_error;
                }
            }
            num_chars = buff + 512 - 1 - buff_ptr;
            break;
        case 'f':
        case 'F':
        case 'e':
        case 'E':
        case 'g':
        case 'G':
            if (format.argument_options == long_double_argument) {
                long_double_num = (*(long double *)((arg += sizeof(long double)) - sizeof(long double)));
            } else {
                long_double_num = (*(double *)((arg += sizeof(double)) - sizeof(double)));
            }
            if (!(buff_ptr = native_fn_0201c410(long_double_num, buff + 512, format))) {
                goto conversion_error;
            }
            num_chars = buff + 512 - 1 - buff_ptr;
            break;
        case 'a':
        case 'A':
            if (format.argument_options == long_double_argument) {
                long_double_num = (*(long double *)((arg += sizeof(long double)) - sizeof(long double)));
            } else {
                long_double_num = (*(double *)((arg += sizeof(double)) - sizeof(double)));
            }
            if (!(buff_ptr = native_fn_0201be10(long_double_num, buff + 512, format))) {
                goto conversion_error;
            }
            num_chars = buff + 512 - 1 - buff_ptr;
            break;
        case 's':
            if (format.argument_options == wchar_argument) {
                wchar_t* wcs_ptr = (*(wchar_t* *)((arg += sizeof(wchar_t*)) - sizeof(wchar_t*)));
                if (wcs_ptr == 0) {
                    wcs_ptr = native_data_020dd11c;
                }
                if ((num_chars = native_fn_0201b124(buff, wcs_ptr, sizeof(buff))) < 0) {
                    goto conversion_error;
                }
                buff_ptr = &buff[0];
            } else {
                buff_ptr = (*(char* *)((arg += sizeof(char*)) - sizeof(char*)));
            }
            if (buff_ptr == 0) {
                buff_ptr = native_data_020dd120;
            }
            if (format.alternate_form) {
                num_chars = (unsigned char)*buff_ptr++;
                if (format.precision_specified && num_chars > format.precision) {
                    num_chars = format.precision;
                }
            } else if (format.precision_specified) {
                num_chars = format.precision;
                if ((string_end = (char*)native_fn_0201b21c((unsigned char*)buff_ptr, 0, num_chars)) != 0) {
                    num_chars = string_end - buff_ptr;
                }
            } else {
                num_chars = native_fn_0201d69c(buff_ptr);
            }
            break;
        case 'n':
            buff_ptr = (*(char* *)((arg += sizeof(char*)) - sizeof(char*)));
            switch (format.argument_options) {
            case normal_argument:
                *(int*)buff_ptr = chars_written;
                break;
            case short_argument:
                *(signed short*)buff_ptr = chars_written;
                break;
            case long_argument:
                *(signed long*)buff_ptr = chars_written;
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
                *(signed long long*)buff_ptr = chars_written;
                break;
            }
            continue;
        case 'c':
            buff_ptr = buff;
            *buff_ptr = (*(int *)((arg += sizeof(int)) - sizeof(int)));
            num_chars = 1;
            break;
        case '%':
            buff_ptr = buff;
            *buff_ptr = '%';
            num_chars = 1;
            break;
        case 0xFF:
        default:
        conversion_error:
            num_chars = native_fn_0201d69c(curr_format);
            chars_written += num_chars;
            if (num_chars && !(*WriteProc)(WriteProcArg, curr_format, num_chars)) {
                return -1;
            }
            return chars_written;
            break;
        }
        field_width = num_chars;
        if (format.justification_options != left_justification) {
            fill_char = (format.justification_options == zero_fill) ? '0' : ' ';
            if (((*buff_ptr == '+') || (*buff_ptr == '-') || (*buff_ptr == ' ')) &&
                (fill_char == '0'))
            {
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
                char blank = ' ';
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
