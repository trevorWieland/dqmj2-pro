/* ov001 row 0x02211bc4: 296 bytes.
 *
 * What it does: 73 instructions; 9 call(s) to 0x02211918, 0x02211cdc, 0x0205f98c, +6 more; loops (back edge at +0x08); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 9 calls (73 instructions, 9 calls, 0 branches, 6 back edges, 1 literal slot).
 *
 *   pool +0x124 -> native_data_0222e10c (image word 0x0222e10c)
 *   branch +0x2c -> +0x118
 *   branch +0x60 -> +0x94
 *   branch +0x7c -> +0x94
 *   back edge +0x114 -> +0x34
 *   test +0x20 cmp r1, #1
 *   test +0x48 cmp r1, #15
 *   test +0x5c cmp r7, #10
 *   test +0x64 cmp r1, #55
 *   test +0x78 cmp r7, #10
 *   test +0x80 cmp r1, #109
 *   test +0x110 cmp r4, r0
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02211bc4; the literal pool and
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

extern void native_fn_02211918(void);
extern u8 native_data_0222e10c[];
extern void native_fn_0205f98c(void);
extern void native_fn_02048a60(void);
extern void native_fn_02048a94(void);
extern void native_fn_02048a9c(void);


asm u32 native_ov001_02211bc4 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    mov r10, r0
    bl native_fn_02211918
    ldrsh r2, [r10, #22]
    ldrb r1, [r10, #0x22]
    mov r5, r0
    and r9, r2, #255
    add r0, r9, r1
    cmp r1, #1
    and r8, r0, #255
    mov r4, #1
    bls ov001_02211bc4_L118
    ldr r11, =native_data_0222e10c
ov001_02211bc4_L34:
    ldr r0, [r10, #0x1c]
    mov r1, r4
    bl native_fn_0205f98c
    mov r6, r0
    ldrb r1, [r6, #0x4]
    cmp r1, #15
    movhs r0, #15
    movlo r0, #5
    sub r0, r1, r0
    and r7, r0, #255
    cmp r7, #10
    blo ov001_02211bc4_L94
    cmp r1, #55
    movhs r0, #55
    movlo r0, #45
    sub r0, r1, r0
    and r7, r0, #255
    cmp r7, #10
    blo ov001_02211bc4_L94
    cmp r1, #109
    movhs r0, #109
    movlo r0, #99
    sub r0, r1, r0
    and r7, r0, #255
ov001_02211bc4_L94:
    mov r0, r6
    mov r1, r5
    mov r2, r8
    bl native_fn_02048a60
    ldrb r1, [r10, #0x20]
    mov r0, r6
    sub r1, r1, #1
    and r1, r1, #255
    bl native_fn_02048a94
    ldrb r1, [r10, #0x21]
    mov r0, r6
    bl native_fn_02048a9c
    ldr r1, [r6, #0x7c]
    sub r0, r4, #1
    orr r1, r1, #2
    ldrb r2, [r11, r7]
    str r1, [r6, #0x7c]
    mov r0, r0, lsl #2
    strh r0, [r6, #130]
    mov r0, #2
    strb r0, [r6, #0x88]
    add r0, r4, #1
    add r2, r5, r2
    ldrb r1, [r10, #0x22]
    and r4, r0, #255
    and r5, r2, #255
    add r0, r1, #1
    rsb r0, r0, #0
    strh r0, [r6, #142]
    str r9, [r6, #0x84]
    ldrb r0, [r10, #0x22]
    cmp r4, r0
    blo ov001_02211bc4_L34
ov001_02211bc4_L118:
    mov r0, #60
    strh r0, [r10, #38]
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
