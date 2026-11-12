/* ov001 row 0x021dc6a4: 528 bytes.
 *
 * What it does: 128 instructions; 21 call(s) to 0x02044424, 0x021db8d0, 0x021db9e0, +18 more; loops (back edge at +0x2c); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 4 literal slot(s) in the extent
 *
 * Decoded shape: loop with 21 calls (128 instructions, 21 calls, 6 branches, 21 back edges, 4 literal slots).
 *
 *   pool +0x200 -> constant 0x02236f6c (image word 0x02236f6c)
 *   pool +0x204 -> constant 0x022362ac (image word 0x022362ac)
 *   pool +0x208 -> constant 0x022355ec (image word 0x022355ec)
 *   pool +0x20c -> constant 0x02237c2c (image word 0x02237c2c)
 *   branch +0x58 -> +0x8c
 *   branch +0x98 -> +0xcc
 *   branch +0xd4 -> +0x158
 *   branch +0xe4 -> +0x118
 *   branch +0x124 -> +0x158
 *   back edge +0x178 -> +0x4c
 *   branch +0x1cc -> +0x1f4
 *   test +0x54 cmp r0, #0
 *   test +0x94 cmp r0, #0
 *   test +0xd0 cmp r0, #0
 *   test +0xe0 cmp r0, #0
 *   test +0x120 cmp r0, #0
 *   test +0x168 cmp r0, #3
 *   test +0x180 cmp r4, r0
 *   test +0x1a8 cmp r1, r2
 *   test +0x1c8 cmp r0, #0
 *   test +0x1e0 cmp r1, r0
 *   0 block transfer(s), 9 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021dc6a4; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: byte identity fixes the instruction stream, not the field, block and callee semantics behind the addresses and strides it touches.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_02044424(void);
extern void ov001_record_is_active_021db8d0(void);
extern void native_fn_021db9e0(void);
extern void native_fn_021dbcbc(void);
extern void native_fn_021dbd24(void);
extern void native_fn_0204459c(void);
extern void native_fn_01ffa824(void);
extern void native_fn_01ffa84c(void);


asm u32 native_ov001_021dc6a4 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #16
    mov r0, #0
    str r0, [sp, #0x8]
    ldr r4, [sp, #0x8]
    mov r0, #67108864
    mov r1, r4
    mov r11, r4
    str r1, [sp, #0x4]
    mov r6, r4
    mov r5, r4
    bl native_fn_02044424
    str r0, [sp]
    mov r0, #0
    ldr r7, =0x02236f6c
    ldr r8, =0x022362ac
    ldr r9, =0x022355ec
    ldr r10, =0x02237c2c
    str r0, [sp, #0xc]
ov001_021dc6a4_L4c:
    mov r0, r7
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_021dc6a4_L8c
    mov r0, r7
    bl native_fn_021db9e0
    add r0, r0, #1
    add r4, r4, r0
    mov r0, r7
    bl native_fn_021dbcbc
    ldr r1, [sp, #0x4]
    add r0, r1, r0
    str r0, [sp, #0x4]
    mov r0, r7
    bl native_fn_021dbd24
    add r5, r5, r0
ov001_021dc6a4_L8c:
    mov r0, r8
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_021dc6a4_Lcc
    mov r0, r8
    bl native_fn_021db9e0
    add r1, r0, #1
    ldr r0, [sp, #0x8]
    add r0, r0, r1
    str r0, [sp, #0x8]
    mov r0, r8
    bl native_fn_021dbcbc
    add r11, r11, r0
    mov r0, r8
    bl native_fn_021dbd24
    add r6, r6, r0
ov001_021dc6a4_Lcc:
    ldr r0, [sp]
    cmp r0, #0
    bne ov001_021dc6a4_L158
    mov r0, r9
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_021dc6a4_L118
    mov r0, r9
    bl native_fn_021db9e0
    add r0, r0, #1
    add r4, r4, r0
    mov r0, r9
    bl native_fn_021dbcbc
    ldr r1, [sp, #0x4]
    add r0, r1, r0
    str r0, [sp, #0x4]
    mov r0, r9
    bl native_fn_021dbd24
    add r5, r5, r0
ov001_021dc6a4_L118:
    mov r0, r10
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_021dc6a4_L158
    mov r0, r10
    bl native_fn_021db9e0
    add r1, r0, #1
    ldr r0, [sp, #0x8]
    add r0, r0, r1
    str r0, [sp, #0x8]
    mov r0, r10
    bl native_fn_021dbcbc
    add r11, r11, r0
    mov r0, r10
    bl native_fn_021dbd24
    add r6, r6, r0
ov001_021dc6a4_L158:
    ldr r0, [sp, #0xc]
    add r7, r7, #1088
    add r0, r0, #1
    str r0, [sp, #0xc]
    cmp r0, #3
    add r8, r8, #1088
    add r9, r9, #1088
    add r10, r10, #1088
    blt ov001_021dc6a4_L4c
    ldr r0, [sp, #0x8]
    cmp r4, r0
    addgt sp, sp, #16
    movgt r0, #8
    ldmgtia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    addlt sp, sp, #16
    movlt r0, #9
    ldmltia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    ldr r0, [sp, #0x4]
    mul r2, r11, r5
    mul r1, r0, r6
    cmp r1, r2
    addlt sp, sp, #16
    movlt r0, #8
    ldmltia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    addgt sp, sp, #16
    movgt r0, #9
    ldmgtia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    bl native_fn_0204459c
    cmp r0, #0
    beq ov001_021dc6a4_L1f4
    bl native_fn_01ffa824
    mov r4, r0
    bl native_fn_01ffa84c
    and r1, r4, #255
    cmp r1, r0
    movlo r0, #8
    add sp, sp, #16
    movhs r0, #9
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
ov001_021dc6a4_L1f4:
    mov r0, #5
    add sp, sp, #16
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
