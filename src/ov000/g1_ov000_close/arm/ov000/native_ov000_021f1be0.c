/* ov000 row 0x021f1be0: 1064 bytes.
 *
 * What it does: 256 instructions and 19 call(s), then a 7-entry dispatch through an inline branch table at 0x021f1c30 (dispatch word at 0x021f1c28)
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

extern void native_fn_02008d78(void);
extern void native_fn_021f35c8(void);
extern void native_fn_02044d84(void);
extern void native_fn_021f3580(void);
extern void native_fn_020449d4(void);
extern void native_fn_02044fcc(void);
extern void native_fn_020635d4(void);
extern void native_fn_021f35dc(void);
extern void native_fn_0207aa98(void);
extern void native_fn_021f359c(void);
extern void native_fn_021f35b0(void);
extern void native_fn_021f27b8(void);
extern void native_fn_021f1bd4(void);
extern void native_fn_021f18cc(void);
extern void native_fn_021f1968(void);
extern void native_fn_021f19e4(void);
extern void native_fn_021f1a5c(void);
extern void native_fn_021f1a98(void);
extern void native_fn_021f1ad4(void);
extern void native_fn_021f1b18(void);
extern void native_fn_021f1b54(void);
extern void native_fn_021f1b90(void);


asm u32 native_ov000_021f1be0 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #16
    ldr r3, [pc, #0x3f0]
    mov r5, r1
    ldr r2, [r3, #0x8]
    add r4, sp, #4
    mov r1, #0
    str r1, [r4]
    str r1, [r4, #0x4]
    str r1, [r4, #0x8]
    add r2, r2, #6400
    strh r1, [r2, #24]
    ldr r2, [r3, #0x8]
    mov r4, r0
    add r0, r2, #268
    mov r2, #6144
    bl native_fn_02008d78
    cmp r4, #6
    addls pc, pc, r4, lsl #2
    b L_021f1f9c
    dcd 0xea0000d9
    dcd 0xea000004
    dcd 0xea000003
    dcd 0xea000068
    dcd 0xea000067
    dcd 0xea00009e
    dcd 0xea00009d
    cmp r5, #8
    addls pc, pc, r5, lsl #2
    b L_021f1cbc
    b L_021f1cbc
    b L_021f1c7c
    b L_021f1c84
    b L_021f1c8c
    b L_021f1c94
    b L_021f1c9c
    b L_021f1ca4
    b L_021f1cac
    b L_021f1cb4
L_021f1c7c:
    mov r8, #1
    b L_021f1cc0
L_021f1c84:
    mov r8, #2
    b L_021f1cc0
L_021f1c8c:
    mov r8, #3
    b L_021f1cc0
L_021f1c94:
    mov r8, #4
    b L_021f1cc0
L_021f1c9c:
    mov r8, #5
    b L_021f1cc0
L_021f1ca4:
    mov r8, #6
    b L_021f1cc0
L_021f1cac:
    mov r8, #7
    b L_021f1cc0
L_021f1cb4:
    mov r8, #8
    b L_021f1cc0
L_021f1cbc:
    mov r8, #0
L_021f1cc0:
    bl native_fn_021f35c8
    str r0, [sp]
    cmp r0, #0
    mov r10, #0
    bls L_021f1dc4
L_021f1cd4:
    mov r0, r10
    bl native_fn_02044d84
    rsbs r6, r0, #2
    mov r5, #0
    bmi L_021f1dac
    ldr r4, [pc, #0x2f0]
    mov r9, r5
    mov r11, r5
L_021f1cf4:
    mov r0, r10
    mov r1, r11
    mov r7, r10
    bl native_fn_021f3580
    cmp r0, #15
    beq L_021f1d9c
    cmp r8, #0
    beq L_021f1d34
    mov r0, r10
    bl native_fn_020449d4
    ldrh r0, [r0, #4]
    mov r0, r0, lsl #24
    mov r0, r0, lsr #28
    and r0, r0, #255
    cmp r8, r0
    bne L_021f1d9c
L_021f1d34:
    mov r0, r10
    mov r1, r5
    bl native_fn_02044fcc
    cmp r0, #0
    beq L_021f1d70
    mov r0, r10
    mov r1, r5
    bl native_fn_020635d4
    cmp r0, #0
    bne L_021f1d9c
    mov r0, r10
    mov r1, r5
    bl native_fn_02044fcc
    mov r7, r0
    b L_021f1d74
L_021f1d70:
    orr r7, r7, r9
L_021f1d74:
    ldr r1, [r4, #0x8]
    add r0, r1, #6400
    ldrh r0, [r0, #24]
    add r0, r1, r0, lsl #2
    str r7, [r0, #0x10c]
    ldr r0, [r4, #0x8]
    add r0, r0, #6400
    ldrh r1, [r0, #24]
    add r1, r1, #1
    strh r1, [r0, #24]
L_021f1d9c:
    add r5, r5, #1
    cmp r5, r6
    add r9, r9, #65536
    ble L_021f1cf4
L_021f1dac:
    add r0, r10, #1
    mov r1, r0, lsl #16
    ldr r0, [sp]
    mov r10, r1, lsr #16
    cmp r0, r1, lsr #16
    bhi L_021f1cd4
L_021f1dc4:
    ldr r2, [pc, #0x218]
    ldr r1, [pc, #0x218]
    ldr r0, [pc, #0x218]
    str r2, [sp, #0x4]
    str r1, [sp, #0x8]
    str r0, [sp, #0xc]
    mov r0, #2
    b L_021f1fa4
    cmp r5, #0
    beq L_021f1e10
    cmp r5, #1
    beq L_021f1e00
    cmp r5, #2
    beq L_021f1e08
    b L_021f1e10
L_021f1e00:
    mov r5, #1
    b L_021f1e14
L_021f1e08:
    mov r5, #2
    b L_021f1e14
L_021f1e10:
    mov r5, #0
L_021f1e14:
    bl native_fn_021f35dc
    movs r6, r0
    mov r4, #0
    beq L_021f1ea4
    ldr r7, [pc, #0x1b4]
L_021f1e28:
    mov r0, r4
    bl native_fn_0207aa98
    cmp r0, #0
    beq L_021f1ea4
    mov r0, r4
    bl native_fn_021f359c
    ldrb r0, [r0, #0x2]
    cmp r0, #0
    beq L_021f1e90
    cmp r5, #0
    beq L_021f1e68
    mov r0, r4
    bl native_fn_021f359c
    ldrb r0, [r0, #0x2]
    cmp r5, r0
    bne L_021f1e90
L_021f1e68:
    ldr r1, [r7, #0x8]
    add r0, r1, #6400
    ldrh r0, [r0, #24]
    add r0, r1, r0, lsl #2
    str r4, [r0, #0x10c]
    ldr r0, [r7, #0x8]
    add r0, r0, #6400
    ldrh r1, [r0, #24]
    add r1, r1, #1
    strh r1, [r0, #24]
L_021f1e90:
    add r0, r4, #1
    mov r0, r0, lsl #16
    cmp r6, r0, lsr #16
    mov r4, r0, lsr #16
    bhi L_021f1e28
L_021f1ea4:
    ldr r2, [pc, #0x144]
    ldr r1, [pc, #0x144]
    ldr r0, [pc, #0x144]
    str r2, [sp, #0x4]
    str r1, [sp, #0x8]
    str r0, [sp, #0xc]
    mov r0, #4
    b L_021f1fa4
    cmp r5, #3
    addls pc, pc, r5, lsl #2
    b L_021f1ef8
    b L_021f1ef8
    b L_021f1ee0
    b L_021f1ee8
    b L_021f1ef0
L_021f1ee0:
    mov r5, #1
    b L_021f1efc
L_021f1ee8:
    mov r5, #2
    b L_021f1efc
L_021f1ef0:
    mov r5, #3
    b L_021f1efc
L_021f1ef8:
    mov r5, #0
L_021f1efc:
    bl native_fn_021f35dc
    movs r6, r0
    mov r4, #0
    beq L_021f1f7c
    ldr r7, [pc, #0xcc]
L_021f1f10:
    mov r0, r4
    bl native_fn_021f35b0
    ldrb r0, [r0, #0x2]
    cmp r0, #0
    beq L_021f1f68
    cmp r5, #0
    beq L_021f1f40
    mov r0, r4
    bl native_fn_021f35b0
    ldrb r0, [r0, #0x2]
    cmp r5, r0
    bne L_021f1f68
L_021f1f40:
    ldr r1, [r7, #0x8]
    add r0, r1, #6400
    ldrh r0, [r0, #24]
    add r0, r1, r0, lsl #2
    str r4, [r0, #0x10c]
    ldr r0, [r7, #0x8]
    add r0, r0, #6400
    ldrh r1, [r0, #24]
    add r1, r1, #1
    strh r1, [r0, #24]
L_021f1f68:
    add r0, r4, #1
    mov r0, r0, lsl #16
    cmp r6, r0, lsr #16
    mov r4, r0, lsr #16
    bhi L_021f1f10
L_021f1f7c:
    ldr r2, [pc, #0x78]
    ldr r1, [pc, #0x78]
    ldr r0, [pc, #0x78]
    str r2, [sp, #0x4]
    str r1, [sp, #0x8]
    str r0, [sp, #0xc]
    mov r0, #6
    b L_021f1fa4
L_021f1f9c:
    add sp, sp, #16
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
L_021f1fa4:
    bl native_fn_021f27b8
    add r1, sp, #4
    ldr r3, [r1, r0, lsl #2]
    cmp r3, #0
    addeq sp, sp, #16
    ldmeqia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    ldr r0, [pc, #0x1c]
    mov r2, #4
    ldr r4, [r0, #0x8]
    add r0, r4, #6400
    ldrh r1, [r0, #24]
    add r0, r4, #268
    bl native_fn_021f1bd4
    add sp, sp, #16
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    dcd 0x02236d98
    dcd native_fn_021f18cc
    dcd native_fn_021f1968
    dcd native_fn_021f19e4
    dcd native_fn_021f1a5c
    dcd native_fn_021f1a98
    dcd native_fn_021f1ad4
    dcd native_fn_021f1b18
    dcd native_fn_021f1b54
    dcd native_fn_021f1b90
}
