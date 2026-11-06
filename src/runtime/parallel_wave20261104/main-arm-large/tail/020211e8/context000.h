typedef unsigned int size_t;

typedef unsigned short wchar_t;

typedef char *va_list;

typedef struct {wchar_t *text;size_t capacity;size_t written;} Output;

void *native_fn_02021180(void *,const wchar_t *,size_t);

int native_fn_02020890(void *(*)(void *,const wchar_t *,size_t),void *,const wchar_t *,va_list);
