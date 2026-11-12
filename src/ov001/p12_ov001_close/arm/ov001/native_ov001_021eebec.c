/* ov001 row 0x021eebec: 144 bytes.
 *
 * What it does: 36 instructions; 6 call(s) to 0x0205d53c, 0x0205d750, 0x0205cedc, +3 more; loops (back edge at +0x04); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
 *
 * Decoded shape: loop with 6 calls (36 instructions, 6 calls, 2 branches, 6 back edges, 0 literal slots).
 *
 *   branch +0x38 -> +0x78
 *   branch +0x60 -> +0x78
 *   back edge +0x84 -> +0x30
 *   test +0x34 cmp r0, #3
 *   test +0x5c cmp r0, #0
 *   test +0x7c cmp r9, #32
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021eebec; the literal pool and
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

extern void native_fn_0205d53c(void);
extern void native_fn_0205d750(void);
extern void native_fn_0205cedc(void);
extern void native_fn_0205d7fc(void);
extern void native_fn_021d78a4(void);


asm u32 native_ov001_021eebec (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    bl native_fn_0205d53c
    mov r0, #0
    bl native_fn_0205d750
    mov r9, #0
    mov r6, #1
    mov r10, r0
    mov r5, #1440
    mov r4, #70
    mov r11, #24576
    mov r8, r6
    mov r7, r9
ov001_021eebec_L30:
    ldrb r0, [r10]
    cmp r0, #3
    bne ov001_021eebec_L78
    mov r0, r9
    bl native_fn_0205cedc
    mov r1, r0
    mov r0, r9
    mov r2, r1, asr #12
    mov r1, r8
    mov r3, r7
    bl native_fn_0205d7fc
    cmp r0, #0
    beq ov001_021eebec_L78
    mov r0, r6
    mov r1, r5
    mov r2, r4
    mov r3, r11
    bl native_fn_021d78a4
ov001_021eebec_L78:
    add r9, r9, #1
    cmp r9, #32
    add r10, r10, #284
    blt ov001_021eebec_L30
    mov r0, #1
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
