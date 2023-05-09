// Verilog
// 4 inputs
// 1 outputs
// 3 D-type flipflops
// 2 inverters
// 8 gates (1 ANDs + 1 NANDs + 2 ORs + 4 NORs)


module s27(CK,G0,G1,G17,G2,G3);
input CK,G0,G1,G2,G3;
output G17;

  wire G5,G10,G6,G11,G7,G13,G14,G8,G15,G12,G16,G9,G17_i;

  wire out_trigger, out_trigger_2;
  wire wc;

  dff DFF_0(.CK(CK),.Q(G5),.D(G10));
  dff DFF_1(.CK(CK),.Q(G6),.D(G11));
  dff DFF_2(.CK(CK),.Q(G7),.D(G13));
  not NOT_0(G14,G0);
  not NOT_1(G17_i,G11);
  and AND2_0(G8,G14,G6);
  or OR2_0(G15,G12,G8);
  or OR2_1(G16,G3,G8);
  nand NAND2_0(G9,G16,G15);
  nor NOR2_0(G10,G14,G11);
  nor NOR2_1(G11,G5,G9);
  nor NOR2_2(G12,G1,G7);
  nor NOR2_3(G13,G2,G12);
  //Trojan_2
  not gc (wc, G16);
  and g19 (out_trigger_2, wc, G9);
  xor xor2(G17,out_trigger_2,G17_i);

endmodule
