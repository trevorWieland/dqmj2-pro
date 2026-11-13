/* ov000 row 0x021ff4cc: 280 bytes.
 *
 * What it does: 66 instructions; 19 call(s) to 0x02215698, 0x02062aa0, 0x02062ad0, +16 more; loops (back edge at +0x08); returns through pop {r4, r5, r6, pc}; 4 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x108 -> constant 0x02237778 (image word 0x02237778)
 *   pool +0x10c -> constant 0x02237780 (image word 0x02237780)
 *   pool +0x110 -> constant 0x02237870 (image word 0x02237870)
 *   pool +0x114 -> constant 0x02237960 (image word 0x02237960)
 *   back edge +0x30 -> +0x20
 *   branch +0x48 -> +0x80
 *   branch +0x50 -> +0x60
 *   branch +0x5c -> +0x68
 *   back edge +0x7c -> +0x4c
 *   test +0x2c cmp r3, #6
 *   test +0x44 cmp r0, #0
 *   test +0x4c cmp r5, r4
 *   test +0x78 cmp r5, r0
 *   0 block transfer(s), 8 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021ff4cc; the literal pool and
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

extern void ov000_display_context_02215698(void);
extern void native_fn_02062aa0(void);
extern void native_fn_02062ad0(void);
extern void native_fn_02062a50(void);
extern void native_fn_02062a88(void);
extern void native_fn_020620b4(void);
extern void native_fn_02008c58(void);
extern void native_fn_022162e4(void);
extern void native_fn_02215a14(void);
extern void native_fn_022013b4(void);
extern void native_fn_022179fc(void);
extern void native_fn_02217ac8(void);
extern void native_fn_0220155c(void);
extern void native_fn_021ff6bc(void);


asm u32 native_ov000_021ff4cc (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    bl ov000_display_context_02215698
    bl native_fn_02062aa0
    mov r4, r0
    bl native_fn_02062ad0
    mov r3, #0
    ldr r2, =0x02237778
    mov r5, r3
ov000_021ff4cc_L20:
    add r1, r2, r3, lsl #2
    add r3, r3, #1
    str r5, [r1, #0x5f8]
    cmp r3, #6
    blt ov000_021ff4cc_L20
    add r1, r4, r0
    ldr r6, =0x02237778
    and r0, r1, #255
    strb r1, [r6, #0x5e6]
    cmp r0, #0
    ble ov000_021ff4cc_L80
ov000_021ff4cc_L4c:
    cmp r5, r4
    bge ov000_021ff4cc_L60
    mov r0, r5
    bl native_fn_02062a50
    b ov000_021ff4cc_L68
ov000_021ff4cc_L60:
    sub r0, r5, r4
    bl native_fn_02062a88
ov000_021ff4cc_L68:
    add r1, r6, r5, lsl #2
    str r0, [r1, #0x5f8]
    ldrb r0, [r6, #0x5e6]
    add r5, r5, #1
    cmp r5, r0
    blt ov000_021ff4cc_L4c
ov000_021ff4cc_L80:
    mov r0, #1
    bl native_fn_020620b4
    ldr r3, =0x02237778
    mov r0, #0
    ldr r1, =0x02237780
    str r0, [r3]
    mov r4, #9
    mov r2, #240
    str r4, [r3, #0x4]
    bl native_fn_02008c58
    ldr r1, =0x02237870
    mov r0, #0
    mov r2, #240
    bl native_fn_02008c58
    ldr r1, =0x02237960
    mov r0, #0
    mov r2, #240
    bl native_fn_02008c58
    bl native_fn_022162e4
    bl native_fn_02215a14
    bl native_fn_022013b4
    bl native_fn_022179fc
    mov r0, #0
    bl native_fn_02217ac8
    bl native_fn_0220155c
    mov r2, #127
    ldr r0, =0x02237778
    mov r1, #0
    strb r2, [r0, #0x5e7]
    strb r1, [r0, #0x5e8]
    str r1, [r0, #0x5f4]
    bl native_fn_021ff6bc
    mov r0, #0
    ldmia sp!, {r4, r5, r6, pc}
}
