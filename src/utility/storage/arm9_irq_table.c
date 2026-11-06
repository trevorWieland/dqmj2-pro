typedef void (*UtilityIrqHandler)(void);
extern void native_utility_child_arm9_handler_02008f65(void);
extern void native_utility_child_arm9_handler_02008f71(void);
extern void native_utility_child_arm9_handler_02008f7d(void);
extern void native_utility_child_arm9_handler_02008f89(void);
extern void native_utility_child_arm9_handler_02008f95(void);
extern void native_utility_child_arm9_handler_02008fa1(void);
extern void native_utility_child_arm9_handler_02008fad(void);
extern void native_utility_child_arm9_handler_02008fb9(void);
extern void native_utility_child_arm9_handler_02009025(void);
UtilityIrqHandler native_utility_child_arm9_dtcm_027e0000[24] = {
    native_utility_child_arm9_handler_02009025,
    native_utility_child_arm9_handler_02009025,
    native_utility_child_arm9_handler_02009025,
    native_utility_child_arm9_handler_02008f89,
    native_utility_child_arm9_handler_02008f7d,
    native_utility_child_arm9_handler_02008f71,
    native_utility_child_arm9_handler_02008f65,
    native_utility_child_arm9_handler_02009025,
    native_utility_child_arm9_handler_02008fb9,
    native_utility_child_arm9_handler_02008fad,
    native_utility_child_arm9_handler_02008fa1,
    native_utility_child_arm9_handler_02008f95,
    native_utility_child_arm9_handler_02009025,
    native_utility_child_arm9_handler_02009025,
    native_utility_child_arm9_handler_02009025,
    native_utility_child_arm9_handler_02009025,
    native_utility_child_arm9_handler_02009025,
    native_utility_child_arm9_handler_02009025,
    native_utility_child_arm9_handler_02009025,
    native_utility_child_arm9_handler_02009025,
    native_utility_child_arm9_handler_02009025,
    native_utility_child_arm9_handler_02009025,
    0,
    0,
};
