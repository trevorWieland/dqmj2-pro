typedef struct Port { unsigned char prefix[0x36]; volatile unsigned short mask; } Port;
extern Port native_utility_child_arm9_data_0202cc50;
void native_utility_child_arm9_main_0200fc04(unsigned int mask) { while (native_utility_child_arm9_data_0202cc50.mask & mask) {} }
