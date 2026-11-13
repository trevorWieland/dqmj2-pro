/* ov000 row 0x02201608: 416 bytes.
 *
 * What it does: 96 instructions; 18 call(s) to 0x02215698, 0x020620b4, 0x02008c58, +15 more; loops (back edge at +0x30); returns through pop {r3, r4, r5, r6, r7, r8, pc}; 8 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x180 -> constant 0x02237d94 (image word 0x02237d94)
 *   pool +0x184 -> constant 0x02237d9c (image word 0x02237d9c)
 *   pool +0x188 -> constant 0x02237f7c (image word 0x02237f7c)
 *   pool +0x18c -> native_data_0222f4cc (image word 0x0222f4cc)
 *   pool +0x190 -> native_data_0222f514 (image word 0x0222f514)
 *   pool +0x194 -> constant 0x020dae90 (image word 0x020dae90)
 *   pool +0x198 -> constant 0x020dae88 (image word 0x020dae88)
 *   pool +0x19c -> constant 0x02237d90 (image word 0x02237d90)
 *   back edge +0x30 -> +0x18
 *   back edge +0x90 -> +0x7c
 *   branch +0xc4 -> +0xd8
 *   back edge +0xe4 -> +0xa8
 *   back edge +0x11c -> +0xf8
 *   test +0x8c cmp r4, #12
 *   test +0xc0 cmp r0, #127
 *   test +0xe0 cmp r4, #4
 *   test +0x104 cmp r0, #0
 *   test +0x118 cmp r7, #12
 *   0 block transfer(s), 14 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02201608; the literal pool and
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
extern void native_fn_020620b4(void);
extern void native_fn_02008c58(void);
extern void native_fn_022162e4(void);
extern void native_fn_020632d0(void);
extern u8 native_data_0222f4cc[];
extern void native_fn_022015fc(void);
extern void native_fn_02215a14(void);
extern void native_fn_02202568(void);
extern void native_fn_022179fc(void);
extern void native_fn_02217ac8(void);
extern void native_fn_02201a60(void);
extern void native_fn_02202708(void);
extern u8 native_data_0222f514[];
extern void native_fn_0205db90(void);
extern void native_fn_0205d9e8(void);


asm u32 native_ov000_02201608 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, lr}
    sub sp, sp, #36
    bl ov000_display_context_02215698
    add r2, sp, #4
    mov r1, #8
    mov r0, #0
ov000_02201608_L18:
    strb r0, [r2]
    strb r0, [r2, #0x1]
    strb r0, [r2, #0x2]
    strb r0, [r2, #0x3]
    add r2, r2, #4
    subs r1, r1, #1
    bne ov000_02201608_L18
    ldr r1, =0x02237d94
    mov r0, #0
    str r0, [r1]
    bl native_fn_020620b4
    ldr r3, =0x02237d94
    mov r4, #7
    ldr r1, =0x02237d9c
    mov r0, #0
    mov r2, #240
    str r4, [r3, #0x4]
    bl native_fn_02008c58
    ldr r1, =0x02237f7c
    mov r0, #0
    mov r2, #4
    bl native_fn_02008c58
    ldr r2, =0x02237d94
    mov r4, #0
    mov r3, #127
ov000_02201608_L7c:
    add r0, r4, #1
    add r1, r2, r4
    and r4, r0, #255
    strb r3, [r1, #0x1ec]
    cmp r4, #12
    blo ov000_02201608_L7c
    bl native_fn_022162e4
    ldr r6, =0x02237d94
    mov r4, #0
    strb r4, [r6, #0x1f8]
    mov r5, #127
ov000_02201608_La8:
    add r1, r4, #12
    add r8, r6, r4
    mov r0, r4
    strb r5, [r8, #0x1e8]
    and r7, r1, #255
    bl native_fn_020632d0
    cmp r0, #127
    beq ov000_02201608_Ld8
    strb r7, [r8, #0x1e8]
    ldrb r0, [r6, #0x1f8]
    add r0, r0, #1
    strb r0, [r6, #0x1f8]
ov000_02201608_Ld8:
    add r0, r4, #1
    and r4, r0, #255
    cmp r4, #4
    blo ov000_02201608_La8
    ldr r6, =0x02237d94
    ldr r5, =native_data_0222f4cc
    mov r7, #0
    mov r4, #6
ov000_02201608_Lf8:
    mla r0, r7, r4, r5
    ldrh r0, [r0, #4]
    bl native_fn_022015fc
    cmp r0, #0
    strneb r7, [r6, #0x1ec]
    add r0, r7, #1
    and r7, r0, #255
    addne r6, r6, #1
    cmp r7, #12
    blo ov000_02201608_Lf8
    bl native_fn_02215a14
    bl native_fn_02202568
    bl native_fn_022179fc
    mov r0, #0
    bl native_fn_02217ac8
    bl native_fn_02201a60
    mov r0, #1
    bl native_fn_02202708
    ldr r1, =native_data_0222f514
    add r0, sp, #4
    mvn r2, #0
    bl native_fn_0205db90
    mov r0, #4
    str r0, [sp]
    ldr r2, =0x020dae90
    ldr r3, =0x020dae88
    mov r0, #2
    add r1, sp, #4
    bl native_fn_0205d9e8
    ldr r1, =0x02237d90
    str r0, [r1]
    mov r0, #0
    add sp, sp, #36
    ldmia sp!, {r3, r4, r5, r6, r7, r8, pc}
}
