OPENQASM 2.0;
include "qelib1.inc";
qreg qregless[27];
u3(pi,-pi,-pi/2) qregless[0];
u3(pi/2,pi/2,pi/2) qregless[1];
u3(pi/2,0,-0.5282754135632297) qregless[2];
swap qregless[1],qregless[2];
u3(pi/2,-pi/2,-pi) qregless[3];
u3(pi,pi/2,-pi) qregless[4];
swap qregless[4],qregless[1];
y qregless[5];
u3(pi,0,pi/2) qregless[6];
u3(pi/2,-pi,0) qregless[7];
u3(pi/2,pi/2,-pi/2) qregless[9];
cx qregless[10],qregless[7];
u3(pi/2,-pi,-pi) qregless[10];
rz(2.3007525789727232) qregless[11];
cx qregless[8],qregless[11];
cx qregless[8],qregless[9];
u3(pi/2,0,-pi/2) qregless[8];
swap qregless[5],qregless[8];
u3(pi/2,-2.674469109947498,pi/2) qregless[11];
cx qregless[11],qregless[8];
swap qregless[9],qregless[8];
ry(0.13090551648021426) qregless[12];
u3(pi/2,0,pi/2) qregless[13];
cx qregless[12],qregless[13];
s qregless[14];
cx qregless[14],qregless[13];
cx qregless[11],qregless[14];
swap qregless[8],qregless[11];
s qregless[13];
u3(pi/2,-pi,-pi/2) qregless[15];
swap qregless[12],qregless[15];
cx qregless[12],qregless[13];
u3(pi,0,0) qregless[12];
x qregless[13];
u3(1.4576609265440963,0,pi/2) qregless[17];
u3(pi/2,0,-pi/2) qregless[18];
cx qregless[17],qregless[18];
y qregless[18];
ry(1.6044830613285317) qregless[19];
cx qregless[19],qregless[16];
rz(1.9981457047103641) qregless[16];
swap qregless[16],qregless[14];
cx qregless[11],qregless[14];
x qregless[14];
swap qregless[11],qregless[14];
swap qregless[11],qregless[8];
cx qregless[9],qregless[8];
y qregless[8];
u3(pi,-pi,-pi/2) qregless[9];
swap qregless[14],qregless[16];
swap qregless[14],qregless[11];
cx qregless[8],qregless[11];
u3(pi/2,-pi/2,-pi) qregless[8];
swap qregless[5],qregless[8];
cx qregless[5],qregless[3];
swap qregless[2],qregless[3];
swap qregless[1],qregless[2];
swap qregless[0],qregless[1];
swap qregless[1],qregless[4];
u3(pi/2,-pi,pi/2) qregless[5];
cx qregless[7],qregless[4];
u3(pi,0,pi/2) qregless[4];
swap qregless[1],qregless[4];
cx qregless[6],qregless[7];
u3(0,-3*pi/4,pi/4) qregless[6];
u3(0,pi/2,-pi) qregless[7];
cx qregless[14],qregless[11];
u3(pi/2,-pi,-pi) qregless[11];
y qregless[19];
u3(2.556178486463051,-pi/2,2.2619257108135216) qregless[20];
swap qregless[20],qregless[19];
cx qregless[19],qregless[16];
y qregless[21];
u3(pi,-pi/2,-pi) qregless[22];
swap qregless[22],qregless[19];
swap qregless[16],qregless[19];
cx qregless[19],qregless[20];
u3(pi/2,pi/2,0) qregless[20];
u3(1.5756894568848911,-pi,0) qregless[23];
cx qregless[21],qregless[23];
swap qregless[21],qregless[18];
cx qregless[18],qregless[15];
swap qregless[12],qregless[15];
swap qregless[12],qregless[13];
swap qregless[13],qregless[14];
swap qregless[11],qregless[14];
cx qregless[8],qregless[11];
sx qregless[8];
swap qregless[8],qregless[5];
cx qregless[5],qregless[3];
u3(pi/2,pi/2,pi/2) qregless[3];
swap qregless[2],qregless[3];
swap qregless[1],qregless[2];
swap qregless[0],qregless[1];
u3(pi/2,-pi,pi/2) qregless[5];
swap qregless[3],qregless[5];
swap qregless[9],qregless[8];
cx qregless[5],qregless[8];
u3(pi,-pi/2,-pi) qregless[5];
sx qregless[8];
u3(pi/2,-pi,-pi) qregless[11];
swap qregless[11],qregless[8];
cx qregless[5],qregless[8];
sx qregless[5];
cx qregless[5],qregless[3];
u3(pi,-pi,-pi/2) qregless[3];
swap qregless[2],qregless[3];
swap qregless[3],qregless[5];
swap qregless[14],qregless[16];
swap qregless[16],qregless[19];
u3(pi,-pi,pi/2) qregless[18];
cx qregless[15],qregless[18];
swap qregless[12],qregless[15];
swap qregless[10],qregless[12];
swap qregless[12],qregless[13];
cx qregless[14],qregless[13];
s qregless[13];
u3(pi/2,-pi,pi/2) qregless[14];
swap qregless[14],qregless[16];
cx qregless[14],qregless[13];
u3(pi/2,-pi/2,pi/2) qregless[13];
u3(pi/2,0,0) qregless[14];
swap qregless[11],qregless[14];
s qregless[18];
swap qregless[15],qregless[18];
swap qregless[12],qregless[15];
swap qregless[12],qregless[10];
cx qregless[10],qregless[7];
u3(pi/2,0,0) qregless[7];
swap qregless[4],qregless[7];
swap qregless[1],qregless[4];
swap qregless[18],qregless[21];
swap qregless[19],qregless[22];
swap qregless[16],qregless[19];
cx qregless[19],qregless[20];
u3(0,-pi,pi/2) qregless[20];
u3(pi/2,-pi,0) qregless[23];
cx qregless[21],qregless[23];
u3(pi,0,0) qregless[23];
u3(0,0,-pi) qregless[24];
swap qregless[24],qregless[23];
swap qregless[23],qregless[21];
swap qregless[21],qregless[18];
cx qregless[17],qregless[18];
u3(pi/2,pi/2,-pi) qregless[17];
swap qregless[21],qregless[18];
cx qregless[15],qregless[18];
y qregless[15];
swap qregless[15],qregless[12];
swap qregless[12],qregless[10];
cx qregless[7],qregless[10];
u3(pi,0,0) qregless[7];
swap qregless[4],qregless[7];
sx qregless[10];
cx qregless[7],qregless[10];
swap qregless[15],qregless[12];
swap qregless[10],qregless[12];
cx qregless[10],qregless[7];
u3(0,-pi,-pi/2) qregless[7];
swap qregless[6],qregless[7];
cx qregless[12],qregless[13];
u3(pi/2,0,0) qregless[13];
swap qregless[12],qregless[13];
swap qregless[10],qregless[12];
swap qregless[7],qregless[10];
u3(pi/2,0,pi/2) qregless[18];
swap qregless[18],qregless[21];
swap qregless[17],qregless[18];
swap qregless[18],qregless[15];
swap qregless[17],qregless[18];
cx qregless[21],qregless[23];
u3(pi/2,-pi/2,-pi) qregless[21];
u3(0,pi/2,pi/2) qregless[23];
u3(pi/2,-pi/2,-pi) qregless[25];
cx qregless[22],qregless[25];
u3(pi/2,0,pi/2) qregless[22];
swap qregless[19],qregless[22];
u3(pi/2,0,-pi) qregless[25];
swap qregless[22],qregless[25];
cx qregless[24],qregless[25];
x qregless[24];
swap qregless[23],qregless[24];
cx qregless[23],qregless[21];
y qregless[23];
u3(pi/2,-pi,0) qregless[25];
swap qregless[24],qregless[25];
swap qregless[25],qregless[22];
swap qregless[22],qregless[19];
cx qregless[19],qregless[16];
sx qregless[16];
swap qregless[14],qregless[16];
swap qregless[13],qregless[14];
cx qregless[12],qregless[13];
cx qregless[12],qregless[15];
x qregless[13];
swap qregless[14],qregless[11];
cx qregless[8],qregless[11];
u3(pi/2,0,0) qregless[8];
u3(pi,pi/2,-pi) qregless[11];
swap qregless[8],qregless[11];
swap qregless[5],qregless[8];
cx qregless[14],qregless[11];
s qregless[11];
s qregless[14];
cx qregless[13],qregless[14];
u3(0,-pi/2,-pi/2) qregless[14];
s qregless[15];
cx qregless[15],qregless[18];
u3(pi/2,-pi/2,-pi/2) qregless[15];
y qregless[19];
cx qregless[16],qregless[19];
u3(pi/2,pi/2,-pi) qregless[16];
swap qregless[19],qregless[16];
swap qregless[14],qregless[16];
swap qregless[14],qregless[11];
cx qregless[11],qregless[8];
u3(pi,-pi/2,-pi) qregless[8];
swap qregless[9],qregless[8];
u3(pi/2,-pi,0) qregless[11];
swap qregless[11],qregless[14];
swap qregless[14],qregless[13];
swap qregless[12],qregless[13];
cx qregless[10],qregless[12];
sx qregless[10];
swap qregless[10],qregless[7];
cx qregless[4],qregless[7];
cx qregless[1],qregless[4];
u3(pi/2,-pi/2,-pi/2) qregless[4];
h qregless[7];
swap qregless[13],qregless[14];
swap qregless[13],qregless[12];
swap qregless[12],qregless[15];
cx qregless[14],qregless[11];
u3(pi/2,pi/2,pi/2) qregless[11];
swap qregless[8],qregless[11];
u3(pi/2,-pi,-pi) qregless[14];
cx qregless[14],qregless[11];
swap qregless[16],qregless[19];
cx qregless[16],qregless[14];
cx qregless[18],qregless[15];
y qregless[15];
swap qregless[18],qregless[21];
cx qregless[19],qregless[20];
swap qregless[25],qregless[24];
swap qregless[24],qregless[23];
cx qregless[21],qregless[23];
u3(pi,-pi,-pi/2) qregless[21];
x qregless[23];
u3(pi,-pi,-pi) qregless[26];