/* ov001 row 0x021d8498: 316 bytes.
 *
 * What it does: 71 instructions; 13 call(s) to 0x021d8ce0, 0x0201d444, 0x0202a8e0, +10 more; loops (back edge at +0x20); returns through pop {r3, r4, r5, r6, pc}; 8 literal slot(s) in the extent
 *
 * Decoded shape: loop with 13 calls (71 instructions, 13 calls, 7 branches, 11 back edges, 8 literal slots).
 *
 *   pool +0x11c -> native_data_0222e960 (image word 0x0222e960)
 *   pool +0x120 -> constant 0x02231720 (image word 0x02231720)
 *   pool +0x124 -> constant 0x022314bc (image word 0x022314bc)
 *   pool +0x128 -> native_data_0222e96c (image word 0x0222e96c)
 *   pool +0x12c -> constant 0x02231514 (image word 0x02231514)
 *   pool +0x130 -> native_fn_021d845c (image word 0x021d845c)
 *   pool +0x134 -> constant 0x00007fff (image word 0x00007fff)
 *   pool +0x138 -> constant 0x022315bc (image word 0x022315bc)
 *   branch +0x34 -> +0x110
 *   branch +0x3c -> +0x110
 *   branch +0x54 -> +0x110
 *   branch +0x6c -> +0x110
 *   branch +0x98 -> +0x110
 *   branch +0xb0 -> +0x104
 *   branch +0xc8 -> +0xf8
 *   test +0x38 cmp r2, #5120
 *   test +0x50 cmp r0, #0
 *   test +0x68 cmp r0, #0
 *   test +0xac cmp r0, #0
 *   test +0xc4 cmp r0, #0
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021d8498; the literal pool and
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

extern void native_fn_021d8ce0(void);
extern u8 native_data_0222e960[];
extern void native_fn_0201d444(void);
extern void native_fn_0202a8e0(void);
extern void native_fn_0202a818(void);
extern void native_fn_02040e0c(void);
extern u8 native_data_0222e96c[];
extern void native_fn_0203cc3c(void);
extern void native_fn_02040fb0(void);
extern void native_fn_0204106c(void);
extern void native_fn_021d845c(void);
extern void native_fn_02029284(void);
extern void native_fn_020410f0(void);
extern void native_fn_0203cf9c(void);


asm u32 native_ov001_021d8498 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, lr}
    sub sp, sp, #36
    mov r6, r0
    mov r4, #0
    bl native_fn_021d8ce0
    mov r2, r0
    ldr r1, =native_data_0222e960
    add r0, sp, #4
    bl native_fn_0201d444
    add r0, sp, #4
    bl native_fn_0202a8e0
    movs r2, r0
    ldr r5, =0x02231720
    beq ov001_021d8498_L110
    cmp r2, #5120
    bhs ov001_021d8498_L110
    add r0, sp, #4
    mov r1, r5
    mov r3, r4
    bl native_fn_0202a818
    cmp r0, #0
    beq ov001_021d8498_L110
    ldr r0, =0x022314bc
    mov r1, r5
    mov r2, #1
    bl native_fn_02040e0c
    cmp r0, #0
    beq ov001_021d8498_L110
    mov r0, r6
    bl native_fn_021d8ce0
    mov r2, r0
    ldr r1, =native_data_0222e96c
    add r0, sp, #4
    bl native_fn_0201d444
    add r0, sp, #4
    mov r1, #1
    bl native_fn_0203cc3c
    movs r5, r0
    beq ov001_021d8498_L110
    ldr r0, =0x022314bc
    mov r1, r5
    mov r2, #1
    bl native_fn_02040fb0
    cmp r0, #0
    beq ov001_021d8498_L104
    ldr r0, =0x02231514
    ldr r1, =0x022314bc
    mov r2, r4
    bl native_fn_0204106c
    cmp r0, #0
    beq ov001_021d8498_Lf8
    ldr r12, =0x022314bc
    ldr r0, =0x02231514
    ldr r3, =native_fn_021d845c
    mov r1, #4
    mov r2, #2
    str r12, [sp]
    bl native_fn_02029284
    ldr r1, =0x00007fff
    ldr r0, =0x022315bc
    mov r4, #1
    strh r1, [r0, #92]
ov001_021d8498_Lf8:
    ldr r0, =0x022314bc
    mov r1, #0
    bl native_fn_020410f0
ov001_021d8498_L104:
    mov r1, r5
    mov r0, #1
    bl native_fn_0203cf9c
ov001_021d8498_L110:
    mov r0, r4
    add sp, sp, #36
    ldmia sp!, {r3, r4, r5, r6, pc}
}
