/* ov001 row 0x0222c1c0: 188 bytes.
 *
 * What it does: 47 instructions; 9 call(s) to 0x0207afec, 0x021db438, 0x021db8d0, +6 more; loops (back edge at +0x0c); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
 *
 * Decoded shape: loop with 9 calls (47 instructions, 9 calls, 1 branch, 9 back edges, 0 literal slots).
 *
 *   branch +0x44 -> +0xa8
 *   back edge +0xb4 -> +0x38
 *   test +0x40 cmp r0, #0
 *   test +0xac cmp r10, #3
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0222c1c0; the literal pool and
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

extern void native_fn_0207afec(void);
extern void ov001_side_slot_record_021db438(void);
extern void ov001_record_is_active_021db8d0(void);
extern void native_fn_021d9494(void);
extern void native_fn_021f0950(void);
extern void native_fn_021f0f0c(void);
extern void native_fn_021ee7d4(void);
extern void native_fn_022024d4(void);


asm u32 native_ov001_0222c1c0 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    mov r8, r1
    mov r7, r0
    bl native_fn_0207afec
    mov r4, r0
    mov r0, r8
    mov r1, #0
    bl ov001_side_slot_record_021db438
    mov r1, r7, lsl #16
    mov r10, #0
    mov r5, r0
    mov r6, r1, asr #16
    and r8, r8, #255
    mov r11, r10
ov001_0222c1c0_L38:
    mov r0, r5
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_0222c1c0_La8
    mov r0, r5
    mov r1, r11
    mov r2, r11
    bl native_fn_021d9494
    mov r0, #0
    ldrb r9, [r4, #0x1e]
    mov r2, r0
    mov r1, r5
    mov r3, r6
    str r2, [sp]
    bl native_fn_021f0950
    mov r1, r0
    mov r0, r5
    mov r2, r7
    bl native_fn_021f0f0c
    mov r2, r9
    mov r9, r0
    mov r0, r5
    mov r1, r9
    bl native_fn_021ee7d4
    rsb r2, r9, #0
    mov r0, r8
    and r1, r10, #255
    bl native_fn_022024d4
ov001_0222c1c0_La8:
    add r10, r10, #1
    cmp r10, #3
    add r5, r5, #1088
    blt ov001_0222c1c0_L38
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
