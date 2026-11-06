typedef unsigned char u8;
typedef unsigned int u32;
typedef struct { u8 *buffer; u32 capacity; u32 written; } Output;
typedef u32 (*Writer)(Output *, const u8 *, u32);
extern u32 format_write(Output *, const u8 *, u32);
extern int format_core(Writer, Output *, const u8 *, void *);
int native_main_0201d3dc(u8 *buffer, u32 capacity, const u8 *format, void *arguments) {
    Output output;
    int result;
    output.buffer = buffer;
    output.capacity = capacity;
    output.written = 0;
    result = format_core(format_write, &output, format, arguments);
    if (buffer != 0) {
        if ((u32)result < capacity) buffer[result] = 0;
        else if (capacity != 0) *(buffer + capacity - 1) = 0;
    }
    return result;
}
