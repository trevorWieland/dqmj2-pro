/* ov000 row 0x02224060: 772 bytes.
 *
 * What it does: 193 instructions and 24 call(s), then a 8-entry dispatch through an inline branch table at 0x022242c0 (dispatch word at 0x022242b8)
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

extern void native_fn_01ffb4ec(void);
extern void native_fn_01ffa010(void);
extern void native_fn_01ffa8d8(void);
extern void native_fn_01ffa394(void);
extern void native_fn_01ffa5fc(void);


asm u32 native_ov000_02224060 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #32
    mov r8, #0
    mov r6, r8
    add r5, sp, #0
    mvn r4, #1
L_02224078:
    and r0, r8, #255
    bl native_fn_01ffb4ec
    str r6, [r5, r8, lsl #2]
    add r8, r8, #1
    strb r4, [r0, #0x16c]
    cmp r8, #8
    blt L_02224078
    bl native_fn_01ffa010
    ldrb r0, [r0]
    cmp r0, #0
    beq L_022240b8
    cmp r0, #1
    beq L_022240c0
    cmp r0, #2
    moveq r7, #1
    b L_022240c4
L_022240b8:
    mov r7, #4
    b L_022240c4
L_022240c0:
    mov r7, #2
L_022240c4:
    mov r8, #0
    bl native_fn_01ffa8d8
    cmp r0, #0
    ble L_02224214
    mov r11, #1
    mvn r4, #0
    add r5, sp, #0
    mov r10, r11
L_022240e4:
    ldr r0, [r5, r8, lsl #2]
    cmp r0, #1
    beq L_02224204
    and r0, r8, #255
    bl native_fn_01ffb4ec
    mov r9, r0
    mov r0, r8
    bl native_fn_01ffa394
    cmp r0, #0
    bne L_0222418c
    add r0, r9, #256
    ldrsb r0, [r0, #100]
    bl native_fn_01ffa394
    cmp r0, #0
    bne L_02224204
    ldrb r0, [r9, #0x164]
    bl native_fn_01ffb4ec
    add r1, r9, #256
    ldrsb r1, [r1, #100]
    ldr r1, [r5, r1, lsl #2]
    cmp r1, #0
    bne L_02224170
    ldrb r2, [r9, #0x167]
    ldrb r1, [r0, #0x167]
    cmp r2, r1
    bhs L_02224160
    ldrb r1, [r9, #0x166]
    orr r1, r1, r7
    strb r1, [r9, #0x166]
    strb r4, [r9, #0x16c]
    b L_02224170
L_02224160:
    ldrb r1, [r0, #0x166]
    orr r1, r1, r7
    strb r1, [r0, #0x166]
    strb r4, [r0, #0x16c]
L_02224170:
    add r1, r9, #256
    add r0, r0, #256
    ldrsb r1, [r1, #100]
    ldrsb r0, [r0, #100]
    str r10, [r5, r1, lsl #2]
    str r10, [r5, r0, lsl #2]
    b L_02224204
L_0222418c:
    mov r0, r8
    mov r1, #8
    bl native_fn_01ffa5fc
    mov r6, r0
    ldrb r0, [r6]
    cmp r0, #0
    bne L_022241bc
    ldrb r0, [r9, #0x166]
    str r11, [r5, r8, lsl #2]
    orr r0, r0, r7
    strb r0, [r9, #0x166]
    strb r4, [r9, #0x16c]
L_022241bc:
    add r0, r9, #256
    ldrsb r0, [r0, #100]
    bl native_fn_01ffa394
    cmp r0, #0
    bne L_02224204
    ldrb r0, [r9, #0x164]
    bl native_fn_01ffb4ec
    ldrb r1, [r6]
    cmp r1, #0
    beq L_022241f4
    ldrb r1, [r0, #0x166]
    orr r1, r1, r7
    strb r1, [r0, #0x166]
    strb r4, [r0, #0x16c]
L_022241f4:
    add r0, r9, #256
    ldrsb r1, [r0, #100]
    mov r0, #1
    str r0, [r5, r1, lsl #2]
L_02224204:
    add r8, r8, #1
    bl native_fn_01ffa8d8
    cmp r8, r0
    blt L_022240e4
L_02224214:
    mov r8, #0
    bl native_fn_01ffa8d8
    cmp r0, #0
    ble L_02224344
    mov r11, #2
    mov r10, #1
    mov r4, #4
    mov r5, #3
    mov r6, r11
    mov r7, r10
L_0222423c:
    and r0, r8, #255
    bl native_fn_01ffb4ec
    mov r9, r0
    bl native_fn_01ffa8d8
    cmp r0, #4
    bne L_022242a0
    bl native_fn_01ffa010
    ldrb r0, [r0]
    cmp r0, #1
    bne L_02224334
    ldrb r0, [r9, #0x166]
    cmp r0, #2
    beq L_02224290
    cmp r0, #4
    beq L_02224288
    cmp r0, #6
    bne L_02224298
    strb r7, [r9, #0x16c]
    b L_02224334
L_02224288:
    strb r6, [r9, #0x16c]
    b L_02224334
L_02224290:
    strb r5, [r9, #0x16c]
    b L_02224334
L_02224298:
    strb r4, [r9, #0x16c]
    b L_02224334
L_022242a0:
    bl native_fn_01ffa010
    ldrb r0, [r0]
    cmp r0, #2
    bne L_02224334
    ldrb r0, [r9, #0x166]
    cmp r0, #7
    addls pc, pc, r0, lsl #2
    b L_0222432c
    dcd 0xea000019
    dcd 0xea000015
    dcd 0xea000011
    dcd 0xea00000d
    dcd 0xea000009
    dcd 0xea000005
    dcd 0xea000002
    dcd 0xeaffffff
    strb r10, [r9, #0x16c]
    b L_02224334
    strb r11, [r9, #0x16c]
    b L_02224334
    mov r0, #3
    strb r0, [r9, #0x16c]
    b L_02224334
    mov r0, #4
    strb r0, [r9, #0x16c]
    b L_02224334
    mov r0, #5
    strb r0, [r9, #0x16c]
    b L_02224334
    mov r0, #6
    strb r0, [r9, #0x16c]
    b L_02224334
    mov r0, #7
    strb r0, [r9, #0x16c]
    b L_02224334
L_0222432c:
    mov r0, #8
    strb r0, [r9, #0x16c]
L_02224334:
    add r8, r8, #1
    bl native_fn_01ffa8d8
    cmp r8, r0
    blt L_0222423c
L_02224344:
    mov r4, #0
L_02224348:
    and r0, r4, #255
    bl native_fn_01ffb4ec
    add r4, r4, #1
    cmp r4, #8
    blt L_02224348
    add sp, sp, #32
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
