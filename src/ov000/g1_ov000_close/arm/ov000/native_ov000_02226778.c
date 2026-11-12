/* ov000 row 0x02226778: 524 bytes.
 *
 * What it does: 129 instructions and 18 call(s), then a 17-entry dispatch through an inline branch table at 0x022267a0 (dispatch word at 0x02226798)
 *
 * Carrier: mwccarm asm with dcd data runs.
 * The measured extent is code plus data inside the function. The data
 * runs are emitted as data, not decoded as instructions; every
 * instruction, branch target, pool word and table entry is read from
 * the image.
 *
 * Unknowns: the field roles, the meaning of the table entries and every callee contract are not established by byte identity; the dispatch range and the table bounds are measured.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_0202a634(void);
extern void native_fn_022256e4(void);
extern void native_fn_022256fc(void);
extern void native_fn_02227ccc(void);
extern void native_fn_0222558c(void);
extern void native_fn_02225434(void);
extern void native_fn_02062520(void);


asm u32 native_ov000_02226778 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    ldr r4, [pc, #0x1f8]
    bl native_fn_0202a634
    ldr r1, [pc, #0x1f4]
    mov r0, #0
    ldrsb r1, [r1, #24]
    sub r1, r1, #10
    cmp r1, #16
    addls pc, pc, r1, lsl #2
    b L_02226834
    dcd 0xea000016
    dcd 0xea00000e
    dcd 0xea000014
    dcd 0xea000013
    dcd 0xea000012
    dcd 0xea00000a
    dcd 0xea00001d
    dcd 0xea00001c
    dcd 0xea00001b
    dcd 0xea00001a
    dcd 0xea000019
    dcd 0xea000018
    dcd 0xea00000d
    dcd 0xea00000c
    dcd 0xea000012
    dcd 0xea000011
    dcd 0xea000010
    mov r0, #19
    bl native_fn_022256e4
    cmp r0, #0
    bne L_0222683c
    mov r0, #65
    bl native_fn_022256fc
    b L_0222683c
    mov r0, #65
    bl native_fn_022256e4
    b L_0222683c
    mov r0, #20
    bl native_fn_022256e4
    cmp r0, #0
    bne L_0222683c
    mov r0, #66
    bl native_fn_022256fc
    b L_0222683c
    mov r0, #66
    bl native_fn_022256e4
    b L_0222683c
L_02226834:
    mov r1, #127
    strb r1, [r4, #0x18c]
L_0222683c:
    cmp r0, #0
    moveq r1, #127
    moveq r0, #0
    streqb r1, [r4, #0x18c]
    beq L_0222685c
    ldrb r1, [r0]
    strb r1, [r4, #0x18c]
    ldrb r0, [r0, #0x1]
L_0222685c:
    strb r0, [r4, #0x192]
    ldr r0, [pc, #0x118]
    ldrsb r0, [r0, #24]
    cmp r0, #9
    addls pc, pc, r0, lsl #2
    b L_02226908
    b L_0222689c
    b L_0222689c
    b L_0222689c
    b L_0222689c
    b L_022268e8
    b L_022268e8
    b L_022268e8
    b L_02226908
    b L_02226908
    b L_022268e8
L_0222689c:
    bl native_fn_02227ccc
    cmp r0, #0
    mov r0, #0
    mov r1, r0
    beq L_022268cc
    bl native_fn_0222558c
    cmp r0, #0
    bne L_02226908
    mov r0, #1
    mov r1, r0
    bl native_fn_0222558c
    b L_02226908
L_022268cc:
    bl native_fn_02225434
    cmp r0, #0
    bne L_02226908
    mov r0, #1
    mov r1, r0
    bl native_fn_02225434
    b L_02226908
L_022268e8:
    bl native_fn_02227ccc
    cmp r0, #0
    mov r0, #1
    mov r1, #0
    beq L_02226904
    bl native_fn_0222558c
    b L_02226908
L_02226904:
    bl native_fn_02225434
L_02226908:
    ldr r0, [pc, #0x70]
    mov r5, #0
    ldrsb r0, [r0, #24]
    cmp r0, #20
    bne L_02226944
    bl native_fn_02062520
    cmp r0, #0
    beq L_02226944
    ldr r0, [pc, #0x50]
    ldrb r0, [r0, #0x20]
    add r0, r0, #21
    mov r0, r0, lsl #16
    mov r0, r0, lsr #16
    bl native_fn_022256e4
    mov r5, r0
L_02226944:
    ldr r1, [pc, #0x34]
    cmp r5, #0
    ldrneb r0, [r5]
    ldrsb r1, [r1, #24]
    strneb r0, [r4, #0x18f]
    mov r0, #0
    cmp r1, #27
    bne L_0222696c
    mov r0, #64
    bl native_fn_022256e4
L_0222696c:
    cmp r0, #0
    ldrneb r0, [r0]
    strneb r0, [r4, #0x193]
    ldmia sp!, {r3, r4, r5, pc}
    dcd 0x02246aa8
    dcd 0x022468b8
}
