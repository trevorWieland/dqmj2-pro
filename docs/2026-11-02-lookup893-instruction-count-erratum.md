# Lookup893 instruction-count correction

The frozen893 writeup contains the sentence “All60 instructions are observed.” It should read “All 60 code bytes, comprising 15 ARM instructions, are observed.”

The source, compiler/linker comparison, VM coverage set and match report already use the correct60-byte extent. This corrects the prose only and adds no function or byte credit. The hashed frozen packet remains intact; this erratum accompanies the following evidence handoff.
