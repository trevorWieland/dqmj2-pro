/* main row 0x0202654c: 1348 bytes.
 *
 * What it does: normalises a soft-float quotient through a 256-byte reciprocal table
 *
 * Carrier: mwccarm asm with dcd data runs.
 * The measured extent is code plus data inside the function. The data
 * runs are emitted as data, not decoded as instructions; every
 * instruction, branch target, pool word and table entry is read from
 * the image.
 *
 * Unknowns: the reciprocal table's producer and every call-site contract; the table content and bounds are measured.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;




asm u32 native_main_0202654c (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    ldr lr, [pc, #0x534]
    eor r4, r1, r3
    ands r12, lr, r1, lsr #19
    cmpne r12, lr
    beq L_020268f8
    bic r1, r1, lr, lsl #20
    orr r1, r1, #1048576
    add r12, r12, r4, lsr #31
L_02026570:
    ands r4, lr, r3, lsr #19
    cmpne r4, lr
    beq L_02026990
    bic r3, r3, lr, lsl #20
    orr r3, r3, #1048576
L_02026584:
    sub r12, r12, r4
    cmp r1, r3
    cmpeq r0, r2
    bhs L_020265a0
    adds r0, r0, r0
    adc r1, r1, r1
    sub r12, r12, #2
L_020265a0:
    sub r4, pc, #36
    ldrb lr, [r4, r3, lsr #12]
    rsbs r2, r2, #0
    rsc r3, r3, #0
    mov r4, #536870912
    mla r5, r14, r3, r4
    mov r6, r3, lsl #10
    mov r5, r5, lsr #7
    mul r14, r5, r14
    orr r6, r6, r2, lsr #22
    mov lr, lr, lsr #13
    mul r5, r14, r6
    mov r6, r1, lsl #10
    orr r6, r6, r0, lsr #22
    mov r5, r5, lsr #16
    mul r5, r14, r5
    mov lr, lr, lsl #14
    add lr, lr, r5, lsr #16
    umull r5, r6, r14, r6
    umull r4, r5, r6, r2
    mla r5, r3, r6, r5
    mov r4, r4, lsr #26
    orr r4, r4, r5, lsl #6
    add r4, r4, r0, lsl #2
    umull r14, r5, r4, r14
    mov r4, #0
    adds r5, r5, r6, lsl #24
    adc r4, r4, r6, lsr #8
    cmp r12, #2048
    bge L_02026784
    add r12, r12, #2032
    adds r12, r12, #12
    bmi L_0202679c
    orr r1, r4, r12, lsl #31
    bic r12, r12, #1
    add r1, r1, r12, lsl #19
    tst lr, #-2147483648
    bne L_02026674
    rsbs r2, r2, #0
    mov r4, r4, lsl #1
    add r4, r4, r5, lsr #31
    mul r14, r2, r4
    mov r6, #0
    mov r4, r5, lsl #1
    orr r4, r4, #1
    umlal r6, r14, r4, r2
    rsc r3, r3, #0
    mla r14, r4, r3, r14
    cmp lr, r0, lsl #21
    bmi L_02026674
    mov r0, r5
    ldmia sp!, {r4, r5, r6, lr}
    bx lr
L_02026674:
    adds r0, r5, #1
    adc r1, r1, #0
    ldmia sp!, {r4, r5, r6, lr}
    bx lr
    dcd 0xfdfeffff
    dcd 0xf9fafbfc
    dcd 0xf5f6f7f8
    dcd 0xf1f2f3f4
    dcd 0xeeeff0f0
    dcd 0xeaebeced
    dcd 0xe7e8e9ea
    dcd 0xe4e5e6e6
    dcd 0xe1e2e2e3
    dcd 0xdedfdfe0
    dcd 0xdbdcdcdd
    dcd 0xd8d9d9da
    dcd 0xd5d6d7d7
    dcd 0xd2d3d4d4
    dcd 0xd0d0d1d2
    dcd 0xcdcececf
    dcd 0xcbcbcccc
    dcd 0xc8c9c9ca
    dcd 0xc6c6c7c8
    dcd 0xc3c4c5c5
    dcd 0xc1c2c2c3
    dcd 0xbfbfc0c0
    dcd 0xbdbdbebe
    dcd 0xbabbbcbc
    dcd 0xb8b9b9ba
    dcd 0xb6b7b7b8
    dcd 0xb4b5b5b6
    dcd 0xb2b3b3b4
    dcd 0xb0b1b1b2
    dcd 0xafafafb0
    dcd 0xadadaeae
    dcd 0xababacac
    dcd 0xa9aaaaaa
    dcd 0xa7a8a8a9
    dcd 0xa6a6a7a7
    dcd 0xa4a4a5a5
    dcd 0xa2a3a3a4
    dcd 0xa1a1a2a2
    dcd 0x9fa0a0a0
    dcd 0x9e9e9e9f
    dcd 0x9c9d9d9d
    dcd 0x9b9b9b9c
    dcd 0x999a9a9a
    dcd 0x98989999
    dcd 0x96979798
    dcd 0x95959696
    dcd 0x94949495
    dcd 0x92939393
    dcd 0x91919292
    dcd 0x90909191
    dcd 0x8f8f8f90
    dcd 0x8d8e8e8e
    dcd 0x8c8c8d8d
    dcd 0x8b8b8c8c
    dcd 0x8a8a8a8b
    dcd 0x8989898a
    dcd 0x88888888
    dcd 0x86878787
    dcd 0x85868686
    dcd 0x84858585
    dcd 0x83838484
    dcd 0x82828383
    dcd 0x81818282
    dcd 0x80808181
L_02026784:
    movs r1, r12, lsl #31
    orr r1, r1, #2130706432
    orr r1, r1, #15728640
    mov r0, #0
    ldmia sp!, {r4, r5, r6, lr}
    bx lr
L_0202679c:
    mvn r6, r12, asr #1
    cmp r6, #52
    bgt L_020268e8
    beq L_020268c4
    cmp r6, #20
    bge L_020267e4
    rsb r6, r6, #19
    mov lr, r0, lsl r6
    rsb r6, r6, #20
    mov r0, r5, lsr r6
    rsb r6, r6, #32
    orr r0, r0, r4, lsl r6
    rsb r6, r6, #32
    mov r4, r4, lsr r6
    orr r1, r4, r12, lsl #31
    mov r12, lr
    mov lr, #0
    b L_02026814
L_020267e4:
    rsb r6, r6, #51
    mov lr, r1, lsl r6
    mov r1, r12, lsl #31
    rsb r6, r6, #32
    orr r12, lr, r0, lsr r6
    rsb r6, r6, #32
    mov lr, r0, lsl r6
    mov r5, r5, lsr #21
    orr r5, r5, r4, lsl #11
    rsb r6, r6, #31
    mov r0, r5, lsr r6
    mov r4, #0
L_02026814:
    rsbs r2, r2, #0
    mul r4, r2, r4
    mov r5, #0
    umlal r5, r4, r2, r0
    rsc r3, r3, #0
    mla r4, r0, r3, r4
    cmp r4, r12
    cmpeq r5, lr
    ldmeqia sp!, {r4, r5, r6, lr}
    bxeq lr
    adds r5, r5, r2
    adc r4, r4, r3
    cmp r4, r12
    bmi L_020268b8
    bne L_0202685c
    cmp r5, lr
    beq L_020268a8
    blo L_020268b8
L_0202685c:
    subs r5, r5, r2
    sbc r4, r4, r3
L_02026864:
    adds r5, r5, r5
    adc r4, r4, r4
    adds r5, r5, r2
    adc r4, r4, r3
    adds lr, lr, lr
    adc r12, r12, r12
    cmp r4, r12
    bmi L_020268a8
    ldmneia sp!, {r4, r5, r6, lr}
    bxne lr
    cmp r5, lr
    blo L_020268a8
    ldmneia sp!, {r4, r5, r6, lr}
    bxne lr
    tst r0, #1
    ldmeqia sp!, {r4, r5, r6, lr}
    bxeq lr
L_020268a8:
    adds r0, r0, #1
    adc r1, r1, #0
    ldmia sp!, {r4, r5, r6, lr}
    bx lr
L_020268b8:
    adds r0, r0, #1
    adc r1, r1, #0
    b L_02026864
L_020268c4:
    rsbs r2, r2, #0
    rsc r3, r3, #0
    cmp r1, r3
    cmpeq r0, r2
    mov r1, r12, lsl #31
    mov r0, #0
    movne r0, #1
    ldmia sp!, {r4, r5, r6, lr}
    bx lr
L_020268e8:
    mov r1, r12, lsl #31
    mov r0, #0
    ldmia sp!, {r4, r5, r6, lr}
    bx lr
L_020268f8:
    orrs r5, r0, r1, lsl #1
    beq L_02026a1c
    cmp r12, lr
    beq L_02026960
    movs r1, r1, lsl #12
    beq L_0202693c
    clz r5, r1
    movs r1, r1, lsl r5
    sub r12, r12, r5
    add r5, r12, #31
    mov r1, r1, lsr #11
    orr r1, r1, r0, lsr r5
    rsb r5, r5, #32
    mov r0, r0, lsl r5
    mov r12, r12, lsl #1
    orr r12, r12, r4, lsr #31
    b L_02026570
L_0202693c:
    mvn r12, #19
    clz r5, r0
    movs r0, r0, lsl r5
    sub r12, r12, r5
    mov r1, r0, lsr #11
    mov r0, r0, lsl #21
    mov r12, r12, lsl #1
    orr r12, r12, r4, lsr #31
    b L_02026570
L_02026960:
    orrs r5, r0, r1, lsl #12
    bne L_02026a44
    bic r5, r3, #-2147483648
    cmp r5, lr, lsl #19
    bhs L_02026984
    and r5, r3, #-2147483648
    eor r1, r5, r1
    ldmia sp!, {r4, r5, r6, lr}
    bx lr
L_02026984:
    orrs r5, r2, r3, lsl #12
    bne L_02026a64
    b L_02026a7c
L_02026990:
    orrs r5, r2, r3, lsl #1
    beq L_02026a08
    cmp r4, lr
    beq L_020269f0
    movs r3, r3, lsl #12
    beq L_020269d0
    clz r5, r3
    movs r3, r3, lsl r5
    sub r4, r4, r5
    add r5, r4, #31
    mov r3, r3, lsr #11
    orr r3, r3, r2, lsr r5
    rsb r5, r5, #32
    mov r2, r2, lsl r5
    mov r4, r4, lsl #1
    b L_02026584
L_020269d0:
    mvn r4, #19
    clz r5, r2
    movs r2, r2, lsl r5
    sub r4, r4, r5
    mov r3, r2, lsr #11
    mov r2, r2, lsl #21
    mov r4, r4, lsl #1
    b L_02026584
L_020269f0:
    orrs r5, r2, r3, lsl #12
    bne L_02026a64
    mov r1, r12, lsl #31
    mov r0, #0
    ldmia sp!, {r4, r5, r6, lr}
    bx lr
L_02026a08:
    mov r1, r12, lsl #31
    orr r1, r1, lr, lsl #19
    mov r0, #0
    ldmia sp!, {r4, r5, r6, lr}
    bx lr
L_02026a1c:
    orrs r5, r2, r3, lsl #1
    beq L_02026a7c
    bic r5, r3, #-2147483648
    cmp r5, lr, lsl #19
    cmpeq r2, #0
    bhi L_02026a64
    eor r1, r1, r3
    and r1, r1, #-2147483648
    ldmia sp!, {r4, r5, r6, lr}
    bx lr
L_02026a44:
    tst r1, #524288
    beq L_02026a7c
    bic r5, r3, #-2147483648
    cmp r5, lr, lsl #19
    cmpeq r2, #0
    bhi L_02026a64
    ldmia sp!, {r4, r5, r6, lr}
    bx lr
L_02026a64:
    tst r3, #524288
    beq L_02026a7c
    mov r1, r3
    mov r0, r2
    ldmia sp!, {r4, r5, r6, lr}
    bx lr
L_02026a7c:
    orr r1, r1, #2130706432
    orr r1, r1, #16252928
    ldmia sp!, {r4, r5, r6, lr}
    bx lr
    dcd 0x00000ffe
}
