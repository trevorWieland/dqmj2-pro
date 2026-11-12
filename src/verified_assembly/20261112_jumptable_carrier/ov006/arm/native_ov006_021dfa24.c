/* ov006 row 0x021dfa24: 784 bytes.
 *
 * What it does: switch dispatch through an inline table
 *
 * Carrier: mwccarm asm with dcd data runs.
 * The measured extent is code plus data inside the function. The data
 * runs are emitted as data, not decoded as instructions; every
 * instruction, branch target, pool word and table entry is read from
 * the image.
 *
 * Unknowns: the field roles and the meaning of the table entries are not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_020bad00(void);
extern void native_fn_020c225c(void);
extern void native_fn_021dffb8(void);
extern void native_fn_020bad50(void);
extern void native_fn_020badcc(void);
extern void native_fn_02008e0c(void);
extern void native_fn_021df92c(void);
extern void native_fn_021df948(void);


asm u32 native_ov006_021dfa24 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    ldr r2, [pc, #0x2e8]
    ldr r0, [r2, #0x48]
    cmp r0, #7
    addls pc, pc, r0, lsl #2
    b L_021dfd10
    dcd 0xea0000b3
    dcd 0xea000005
    dcd 0xea000016
    dcd 0xea00002d
    dcd 0xea000077
    dcd 0xea0000ae
    dcd 0xea0000a2
    dcd 0xea0000a8
    ldr r0, [r2, #0x44]
    cmp r0, #0
    subgt r0, r0, #1
    strgt r0, [r2, #0x44]
    bgt L_021dfd10
    ldr r1, [pc, #0x2a4]
    ldr r3, [pc, #0x2a4]
    mov r0, #1
    mov r2, #16
    bl native_fn_020bad00
    cmp r0, #0
    bne L_021dfa94
    mov r0, #805306368
    bl native_fn_020c225c
L_021dfa94:
    ldr r0, [pc, #0x27c]
    mov r1, #2
    str r1, [r0, #0x48]
    b L_021dfd10
    ldr r3, [r2, #0x14]
    ldr r0, [pc, #0x274]
    add r1, r3, #1
    str r1, [r2, #0x14]
    cmp r3, r0
    ble L_021dfac4
    mov r0, #-1610612736
    bl native_fn_020c225c
L_021dfac4:
    ldr r0, [pc, #0x24c]
    ldr r1, [r0, #0xc]
    cmp r1, #1
    bne L_021dfd10
    ldr r1, [r0, #0x34]
    cmp r1, #0
    beq L_021dfaf8
    mov r1, #5
    str r1, [r0, #0x44]
    mov r1, #3
    str r1, [r0, #0x48]
    mov r0, #1
    ldmia sp!, {r3, pc}
L_021dfaf8:
    mov r1, #7
    str r1, [r0, #0x48]
    b L_021dfd10
    ldr r0, [r2, #0x44]
    cmp r0, #0
    subgt r0, r0, #1
    strgt r0, [r2, #0x44]
    bgt L_021dfd10
    ldr r0, [r2, #0x70]
    cmp r0, #4
    addls pc, pc, r0, lsl #2
    b L_021dfb5c
    b L_021dfb6c
    b L_021dfb3c
    b L_021dfb3c
    b L_021dfb5c
    b L_021dfb4c
L_021dfb3c:
    mov r0, #156
    bl native_fn_021dffb8
    mov r0, #0
    ldmia sp!, {r3, pc}
L_021dfb4c:
    mov r0, #31
    bl native_fn_021dffb8
    mov r0, #0
    ldmia sp!, {r3, pc}
L_021dfb5c:
    mov r0, #29
    bl native_fn_021dffb8
    mov r0, #0
    ldmia sp!, {r3, pc}
L_021dfb6c:
    mov r0, #0
    str r0, [r2, #0xc]
    ldr r0, [r2, #0x3c]
    cmp r0, #3
    addls pc, pc, r0, lsl #2
    b L_021dfc18
    b L_021dfb94
    b L_021dfbcc
    b L_021dfbf4
    b L_021dfba4
L_021dfb94:
    mov r0, #5
    str r0, [r2, #0x48]
    mov r0, #1
    ldmia sp!, {r3, pc}
L_021dfba4:
    ldr r0, [r2, #0x28]
    ldr r1, [r2, #0x30]
    ldr r2, [r2, #0x20]
    ldr r3, [pc, #0x168]
    bl native_fn_020bad00
    cmp r0, #0
    bne L_021dfc18
    mov r0, #805306368
    bl native_fn_020c225c
    b L_021dfc18
L_021dfbcc:
    ldr r0, [r2, #0x28]
    ldr r2, [r2, #0x20]
    ldr r1, [pc, #0x14c]
    ldr r3, [pc, #0x140]
    bl native_fn_020bad50
    cmp r0, #0
    bne L_021dfc18
    mov r0, #805306368
    bl native_fn_020c225c
    b L_021dfc18
L_021dfbf4:
    ldr r0, [r2, #0x28]
    ldr r1, [r2, #0x30]
    ldr r2, [r2, #0x20]
    ldr r3, [pc, #0x124]
    bl native_fn_020badcc
    cmp r0, #0
    bne L_021dfc18
    mov r0, #805306368
    bl native_fn_020c225c
L_021dfc18:
    ldr r0, [pc, #0xf8]
    mov r1, #4
    str r1, [r0, #0x48]
    mov r1, #0
    str r1, [r0, #0x14]
    b L_021dfd10
    ldr r3, [r2, #0x14]
    ldr r0, [pc, #0xe8]
    add r1, r3, #1
    str r1, [r2, #0x14]
    cmp r3, r0
    ble L_021dfc50
    mov r0, #-1610612736
    bl native_fn_020c225c
L_021dfc50:
    ldr r1, [pc, #0xc0]
    ldr r0, [r1, #0xc]
    cmp r0, #1
    bne L_021dfd10
    ldr r0, [r1, #0x34]
    cmp r0, #0
    ldr r0, [r1, #0x3c]
    beq L_021dfcb0
    cmp r0, #1
    bne L_021dfc9c
    ldr r2, [r1, #0x20]
    ldr r0, [pc, #0xac]
    sub r2, r2, #12
    str r2, [r1, #0x20]
    ldr r1, [r1, #0x30]
    bl native_fn_02008e0c
    ldr r0, [pc, #0x90]
    mov r1, #0
    strb r1, [r0, #0xc]
L_021dfc9c:
    ldr r0, [pc, #0x74]
    mov r1, #5
    str r1, [r0, #0x48]
    mov r0, #1
    ldmia sp!, {r3, pc}
L_021dfcb0:
    cmp r0, #1
    beq L_021dfcc8
    cmp r0, #2
    beq L_021dfcd8
    cmp r0, #3
    bne L_021dfd10
L_021dfcc8:
    ldr r0, [pc, #0x48]
    mov r1, #6
    str r1, [r0, #0x48]
    b L_021dfd10
L_021dfcd8:
    mov r0, #7
    str r0, [r1, #0x48]
    b L_021dfd10
    ldr r0, [r2, #0x38]
    add r0, r0, #1
    str r0, [r2, #0x38]
    cmp r0, #60
    movgt r0, #7
    strgt r0, [r2, #0x48]
    b L_021dfd10
    mov r0, #29
    bl native_fn_021dffb8
    mov r0, #0
    ldmia sp!, {r3, pc}
L_021dfd10:
    mov r0, #1
    ldmia sp!, {r3, pc}
    dcd 0x0220f594
    dcd 0x0220f604
    dcd native_fn_021df92c
    dcd 0x000001c2
    dcd 0x0220f828
    dcd native_fn_021df948
    dcd 0x0220f834
}
