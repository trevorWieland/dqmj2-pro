/* ov000 row 0x0221208c: 144 bytes.
 *
 * What it does: 35 instructions; 6 call(s) to 0x021dfcd8, 0x02212104, 0x02040b44, +3 more; loops (back edge at +0x24); returns through pop {r4, r5, r6, r7, r8, r9, r10, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x8c -> constant 0x02240b54 (image word 0x02240b54)
 *   branch +0x34 -> +0x78
 *   branch +0x54 -> +0x78
 *   branch +0x60 -> +0x78
 *   back edge +0x80 -> +0x1c
 *   test +0x30 cmp r8, #0
 *   test +0x48 cmp r0, #0
 *   test +0x50 cmpne r1, #0
 *   test +0x5c cmp r0, #0
 *   test +0x7c cmp r7, #4
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0221208c; the literal pool and
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

extern void native_fn_021dfcd8(void);
extern void native_fn_02040b44(void);
extern void native_fn_02041200(void);
extern void native_fn_02040bdc(void);


asm u32 native_ov000_0221208c (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, lr}
    mov r9, #0
    mov r4, #12
    ldr r6, =0x02240b54
    mov r10, r0
    mov r7, r9
    mov r5, r4
ov000_0221208c_L1c:
    mov r0, r10
    mov r1, r7
    bl native_fn_021dfcd8
    mov r0, r0, lsl #16
    mov r8, r0, lsr #16
    cmp r8, #0
    ble ov000_0221208c_L78
    mov r0, r8
    mov r1, r6
    mov r2, r5
    bl native_fn_02040b44
    cmp r0, #0
    ldrne r1, [r0]
    cmpne r1, #0
    beq ov000_0221208c_L78
    bl native_fn_02041200
    cmp r0, #0
    beq ov000_0221208c_L78
    mov r0, r8
    mov r1, r6
    mov r2, r4
    bl native_fn_02040bdc
    add r9, r9, #1
ov000_0221208c_L78:
    add r7, r7, #1
    cmp r7, #4
    blt ov000_0221208c_L1c
    mov r0, r9
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, pc}
}
