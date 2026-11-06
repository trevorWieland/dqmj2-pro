typedef unsigned int u32;
extern u32 native_primary_flags[];
extern u32 native_library_flags[];
int saved_20261029_primary_flag_get(int index) {
    return (native_primary_flags[index >> 5] >> (index & 31)) & 1;
}
int saved_20261029_primary_flag_set(int index,int value) {
    int previous = saved_20261029_primary_flag_get(index);
    if (value) native_primary_flags[index >> 5] |= 1U << (index & 31);
    else native_primary_flags[index >> 5] &= ~(1U << (index & 31));
    return previous;
}
int saved_20261029_library_flag_get(int index) {
    return (native_library_flags[index >> 5] >> (index & 31)) & 1;
}
int saved_20261029_library_aux_get(int index) {
    return (native_library_flags[(index + 64) >> 5] >> (index & 31)) & 1;
}
int saved_20261029_library_aux_set(int index,int value) {
    int previous = saved_20261029_library_aux_get(index);
    if (value) native_library_flags[(index + 64) >> 5] |= 1U << (index & 31);
    else native_library_flags[(index + 64) >> 5] &= ~(1U << (index & 31));
    return previous;
}
int saved_20261029_library_flag_set(int index,int value) {
    int previous = saved_20261029_library_flag_get(index);
    if (value) native_library_flags[index >> 5] |= 1U << (index & 31);
    else native_library_flags[index >> 5] &= ~(1U << (index & 31));
    if (value && !previous) {
        saved_20261029_library_aux_set(index,value);
        if (value) saved_20261029_primary_flag_set(76,1);
    }
    return previous;
}
