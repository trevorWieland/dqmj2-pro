/* ov001 row 0x0220ebf4: 180 bytes.
 *
 * What it does: 45 instructions; 8 call(s) to 0x021dcda8, 0x02209490, 0x0207b674, +5 more; loops (back edge at +0x14); returns through pop {r3, r4, r5, r6, r7, pc}
 *
 * Decoded shape: loop with 8 calls (45 instructions, 8 calls, 1 branch, 6 back edges, 0 literal slots).
 *
 *   branch +0x44 -> +0xac
 *   branch +0x4c -> +0xac
 *   test +0x18 cmp r0, #0
 *   test +0x40 cmp r0, #0
 *   test +0x48 cmp r4, #0
 *   test +0xa0 cmp r0, #0
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0220ebf4; the literal pool and
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

extern void native_fn_021dcda8(void);
extern void native_fn_02209490(void);
extern void native_fn_0207b674(void);
extern void native_fn_0220e910(void);
extern void native_fn_0220e3a8(void);
extern void native_fn_021d908c(void);
extern void native_fn_02210ad0(void);


asm u32 native_ov001_0220ebf4 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    mov r6, r1
    mov r7, r0
    mov r0, r6
    mov r4, r2
    bl native_fn_021dcda8
    cmp r0, #0
    movne r0, #0
    ldmneia sp!, {r3, r4, r5, r6, r7, pc}
    add r0, r6, #556
    bl native_fn_02209490
    ldr r1, [r7, #0x1e8]
    mov r5, r0
    add r1, r1, #70
    mov r0, #68
    bl native_fn_0207b674
    cmp r0, #0
    ble ov001_0220ebf4_Lac
    cmp r4, #0
    bne ov001_0220ebf4_Lac
    ldrb r0, [r6, #0x31e]
    mov r1, #12
    mov r2, r1
    bl native_fn_0220e910
    ldr r1, [r6, #0x1e8]
    mov r4, r0
    ldrb r3, [r1, #0x92]
    mov r2, #0
    mov r0, r7
    mov r1, #12
    str r2, [sp]
    bl native_fn_0220e3a8
    mov r1, r0
    mov r0, r4
    mov r2, r5
    bl native_fn_021d908c
    mov r2, r0
    mov r0, r7
    mov r1, #100
    bl native_fn_02210ad0
    cmp r0, #0
    movne r0, #1
    ldmneia sp!, {r3, r4, r5, r6, r7, pc}
ov001_0220ebf4_Lac:
    mov r0, #0
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
