/* ov001 row 0x0221f428: 184 bytes.
 *
 * What it does: 46 instructions; 8 call(s) to 0x021db8d0, 0x021dbe68, 0x0221f444, +5 more; loops (back edge at +0x20); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
 *
 * Decoded shape: loop with 8 calls (46 instructions, 8 calls, 2 branches, 8 back edges, 0 literal slots).
 *
 *   branch +0x28 -> +0x40
 *   back edge +0x4c -> +0x1c
 *   branch +0x64 -> +0x7c
 *   back edge +0x88 -> +0x58
 *   test +0x24 cmp r0, #0
 *   test +0x34 cmp r0, r5
 *   test +0x44 cmp r9, #3
 *   test +0x60 cmp r0, #0
 *   test +0x70 cmp r0, r6
 *   test +0x80 cmp r9, #3
 *   test +0xa8 cmp r4, r0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0221f428; the literal pool and
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

extern void ov001_record_is_active_021db8d0(void);
extern void native_fn_021dbe68(void);
extern void native_fn_021dbec8(void);


asm u32 native_ov001_0221f428 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    ldr r4, [r0, #0x8]
    mov r5, #0
    ldr r11, [r0, #0x4]
    mov r6, r5
    mov r9, r5
    mov r10, r4
ov001_0221f428_L1c:
    mov r0, r10
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_0221f428_L40
    mov r0, r10
    bl native_fn_021dbe68
    cmp r0, r5
    movge r5, r0
    movge r7, r9
ov001_0221f428_L40:
    add r9, r9, #1
    cmp r9, #3
    add r10, r10, #1088
    blt ov001_0221f428_L1c
    mov r5, r11
    mov r9, #0
ov001_0221f428_L58:
    mov r0, r5
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_0221f428_L7c
    mov r0, r5
    bl native_fn_021dbe68
    cmp r0, r6
    movge r6, r0
    movge r8, r9
ov001_0221f428_L7c:
    add r9, r9, #1
    cmp r9, #3
    add r5, r5, #1088
    blt ov001_0221f428_L58
    add r0, r7, r7, lsl #4
    add r0, r4, r0, lsl #6
    bl native_fn_021dbec8
    add r1, r8, r8, lsl #4
    mov r4, r0
    add r0, r11, r1, lsl #6
    bl native_fn_021dbec8
    cmp r4, r0
    movgt r0, #1
    movle r0, #0
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
