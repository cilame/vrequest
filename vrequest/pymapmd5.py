import lzma
import base64
import itertools

# 自带的简单的密码表压缩放在脚本里面
# 脚本用起来会更方便。
zpasslist = (
'{Wp48S^xk9=GL@E0stWa761SMbT8$j;nW+8&0PQxkN{#puWwwz&%E^>Ityxm!@0L@CR}h0uY0dA<%-~3yEPJz%uk3Z-q}qm-UHsIyY|Dd>MQjQkYY>V16jKQq>@zfptc$0^bXvph1IXM=iX?;5jSxo^8xJ@Gen87r$6WAfO@I6Rs;$F?4g2&JWPE}1jQb3^YcG=<+SRc'
'^EF<R{g-Veb`iI}X229)dwp`UE(TtshL=CS5Sf;yU_;3ncWH?35*qZsDOSX791lF0n*yA|or!~1*wMXks#=8Iy*q1k*<OpxYb9{<i|oS^1rxniL=9kKws+C(9m$c!PfQYGOv@z4w9@l&3RnHCx6>>l6*MrNdwc(_!CNHy!FI3(D2mPQ(rF79AL5_ky+((#guOS()ts>O'
'b}l<=cCuKdst{n+!SO*el&UAgaj~utOFEspQqs)5))E1-@pG*KQ?tG9ZB!>o3qwr<NBb*Z02z1pQnO>+Lg6kIBRJ{SJ#vaV;gPzer({)z!#*tf6dru>KVIg@LZ9TiM;-sj%I)AR2z-j*$ul%<+8Yk@m6B`t0w<so5N4T@vyJcz=8D)tV2paQfNjJvJ=kb1a9L3PhSOn#'
'f~g!I|BtWGZs5+I38@vF&~-7#_^+yWi78wmc%^K5GSY70d)=T%dJr-penx#6=FXVocSF00W6|0kW)}pZIm&}cFm9MDPGQ(Y$R`%P0QZ?RxNr>K$(X8*`^<YK(v6$9r2_W8Gx-^$f158?tVnv87O9^`I4hFDz#stpgnktJ7BxorN8F?30g&@S7L&dv#t))ka({~BIZfV8'
'Yj4^vFYzx;+c$Yk1CW`o^SFafA3^m=xe*H(A%@!X5H@GAZ79@viDg*;KUyoJ0w(Cf21it++@>)U5F~9rD5Cj+61~Uh8eW$b(q=Xo!4T7-Ct0!sI_ufD_7wDP(``wXwz6tnmaubQ7$;y7I4d!9(uIn%+yV4@HMCikPq2H5PO%pkG#^U~N70^b#qmV4<tx28R)-uJhpGS8'
'!#_vjJkN%!#M)fYcQ2p|VA+`;(dk=jEl?mMjrKSRfpKufwM>{4W4k6A>Ksi*L{3D(Ip3!lE$=d5`$ev=8tWBFF3CEMQ#8UHQS=OE(9pZ6yu(42&rXs;nSDx6ER-%~D}f#U=NV9n<De_ZDip4MmxyK}GE@XhwWaV$#M=3IQC4SSN5vC>;OGEiL!w2LD`~j;WyBNFT<+CR'
'JoLJ#zN%1$Zv`#7?dn-!BRr)-W_&72rGH4kWX^ZrqOo&g4X2*k=;=9g*-~{Y-5%du6Q<5=QQaRq&gYfMKKZq@E47Ai+KF&a0gJ0qHX`x;K|=5(ojstGPB={{B8=cmFG>n%$Ld{AUMy=4JHCpX<GRu=+5oA;iqR=H?{tz=7S#ZwmJs>#8eekt*6v6SF+Z!!jukbXIVHBf'
'MCoH`nm1tgX5`r2t(VU<A69(&MZmGTq%QPQUw=)|>uGW`VYiCGG-%oIb%zx@?dPN-_j46uu7KoG{N3@)>hY&d-a3s$$faF#r|;yPH#OV=hl(TwC#)He4j^N}8v7i>)1({Zb+f|{UZsuRTVzxAF0PLNNy`))?SOslrFw^5n9YbPYWp=bW!1YJiSCJWnQh5d9USyjwzs>V'
';6LK~8)A^H*^2b<XiFeO{g;3C;MpN}|0651vi==2(_AP@zzlI$G@Syg4YmAeWgJ6L!f#LpxSNN!eZ$-5(c`w1T2M;bB$XQUuf@`&3ii*~1QW=IOVcAAJeG!CBMqJ>2f<(oC!dUE_b(G$xR&cy++WNM8n^|1#jC?pA}}DDG0x4b!3v#N5?&e$OZEZm`bk#Bx=bXUo^#xd'
'r2*Vc>io;z8sQ!%v3Q+KJS;C^y>fz(F`9}ITVC$2&3z|iUc!&UF*5fC&^N|gKVzSCj1G6D?&lG~+fchTvlpD^`hW5i?Fl!0QLEfm;}C*EBX9FM)rmCoyy1&soDbuyyJu;?Pajm69}N2?9K4-ItAk!SsW_%m(D=pyYUz0lS&(=@p%~NQBxbHSwdL1e<j#I8+oc`a9!o&`'
'oVS~fqc*N{S(458228!jfG%P8rE$n6z_1iIH5Ln$%6iQO(xQfb9vsal<|5RP&D?7ZNh36SoJ}QCzNT&8uv>h?b_oj%vpL~71|no0buO{t5e(W4P~9^)s}Ku$W9y2`j)Kdxmz_-vSPtUz&XnZNX9_zTCwrU-Tfo&y$1QytRFq)lu6)M)4Lw*&g^FkX=)@mg7KD>0fd-aZ'
'hseLx#lpn=A8j0-q{MZ-i$dt&xlawk9D|;18`wCMuU1!tijBx~162N<lP;rKy|tW{3p&ky+eaWbpA41M8P8Y7ItB(hH508>6WLAPr$@-3+BcY;Xxa}urU0^f7S~SYe5g;csb5cJUhm0v*;`t-MFWij*<8+~H3M6@x{amKOlLXr>rGY3)SCX!k~h+)^h1LSfwFQh_#yO^'
'q1<x(==+`4%!$nmx%$M3NyIK0qW_$HU(nM0qu6}I!}w5<sX;W?nVLTS4!R1g4CJ0y-*DgO=)b99^JLDVJA4sJD@dKjM&0@->j@z8%@H#Foa~_4{HNNo;9;Sn$Gp3YTUrRvQPL0Z2w-AcX{{V`u4=}M5n9l}wDJG+X}05#97xU7jT2tUWzzaIVS4_L_Jx}zj$&jZAh_zL'
'W=-eielikh-g?`MT9nqyvVH5qtP9dI%}$eYt6i_S6I}ox)(J8#Spw?F4UIPi{{uu93Rtb}g4mFaV1tR%g5wE(+efG>gwg!URvPZ!>3x@xqV@yG2)V0mT)5f4bB1Xue2%@YQQL~IvGMxh4jGGl?T^v72--VO55v_c^>*b{yoTQ*NGn__*`wg4VHcvY!yhUJm9hW_$AiZ*'
'r$Y<f^I;nPtzd>H%U>8Q%$@bt7J+wo@q2uMXK?RSK($0dsR&lm%?Zv240T}JP|-B>m9>G^dK?=&%Y6Rg=naVE<@R=o`SEyg(P_{zre+fab0c~7z9N>3#3R7VJ%n_!QZOOf?TcyPshy?>K=?CjD7-cx=vZcw*N16j_`B@n`DMuf%CK+M^<z97SYVjapmag=^XQ*Oq}8Me'
'US)AJLGsFiB$N#@gvD3Y7@5=|@w>x|n`ZeAkDqo*ayc0z@{#}7a(Ngh0=lJn2-yk&VLI|yvVwUSCr93h2PJ%O{vTuv{5Bb&U;BR|GCKjSVULSnJ94H+9kMR|Nx?rlK2w!sh8F25!K?N=OOHHW`F9fsA1*4MoU#C+DyKvbl4TN5N+AFgoWl+0oZMw1_4zv)<E6G$z``LS'
'7STq$|I4MCE}C{H^v;)<53v{zc{2(+eDlEcV2vsL-B<yL0Mzq=lgl*qOWGSUYSWG%Ucen~BJ4LjD_#6DKM%g3T^c04cyskn45tQ~Yx-#7Tb4A>H<7kc0yqTdjPU^p(#X9*2@d1^T^}lN!+5c0yXN4KbGW%GItX0%qxpPoU>0rdj_L@)X(v0cO841mK_xqDUzwYZAdhlt'
'0RY;T)JIXckG6wKv%U8v#iOCwQF<c!gx-%~Rls$%7gcmckXZSNAvfat*TdwDDidJCs*oKJ$SvuYkZ3@Yatc)I=Jp|KWq}}T1Glmc)jH<Ba&dH=Wec6ftO4@J_J?e6Aary{o*p-=shDOY1JH*@a&Li#o#2j0KZpqw(*9QVR7Tn;=~I1Zv8_O;L)xTa_FX`+d*>c@^6_R-'
'CA|?@bc#steJ16TU%NMwg_uUZQN|%Q=#s;a{1p`J8m?(egWoct(>!PiA<;NJ=zR}&kbn7ey8G`9YlMtcY$4k&Gi;*Ij%5=sy$Y&^B~R`Z3$Oq)kiXgD^%i;q#M>IF^(eLWu$I$!GdiFaFyVZAl;jN)Dn?>$Eyx`_7A2ZG=OzYWK8fVJssIWJlr!aVJ-{JZP+Vf~^KpwW'
'K+VCdclS~umNy4z#7n@N*PRR*a`C;SrcA2qo{oA4amPPb(K)F>T)2$Q-7_tX5Y3zi#Ga6l9{o>0sLT0dQx&=U6KYCSHz9{%F;k`0glwa)?qd^p+;eEFHiyJntXop1^~#llYEtT<LJCTMRfvwFD^LK(2#lpT<bI;SofblqT?!lLdzVF+7t=3yX>35uz{hy$ve|?}ypg%e'
'6;uA?nU1DR=Zir<F??uP9}+g%&vvG4%15)<*yJ|iD8@W@<Oe!uAkz|jB^kF!VqnXOPP)`_v&jQpr^xVuU@Xv5=#%XAJGd@{B{~6p<>BKRMJ%8CNoyYKCnb)!ti}qgt-;NzRSOxxS;^&&I+WqHJz=~iEWBLJ#9$s>!a!EUl3St<^ThlhM|fLt8<Wasu5T|Bqt5}n3c0o!'
'DDu4_65TEL@N4Vdpy&+wG><}~tsZ1J;{3=@6M5S)2AEW61!~t(LsfiitxdKP;#@1;8N*=vK`?#?P(5#|4UQEz-76qiJvOajBVwlw71_IhWA(g*!j6CK3;gk`T8C9uPD=baaWZoJrZx^{oQk{cWwdApmM87@gQ4y~%ZBTlAd1A!=4=coL+7BDC8*3nLnH^|JhOjGI#_Y1'
'B#*mo!W-AZ{(aMAS#Q(UGu5vhqe`+`)HajZ)L0CtP1WAGiI5&ban}$qkJokbGoBM_eBj$n)p6Way^&-R>nEWa2a7!{sb9e^-ky=2`?)1J%?_TKe_@E@FsQvCR6Ui9UQ(HXu%G-=XZ@Vw%dB&sAgOVYD*J*FY?}*Ugljw;vTZ>sraq`x@0)!r=fE7U!XC%JXcFDjLYq&N'
'3gE4yM11c06(&Rut}pOd5YDDFAky2yM8uojQO91-e7?F#u?O7J%&bGMEOk#lxG}V2@wWLyc@_eR6#_uLdW!?d>08Cs_$yv1S_lkRLxDLpl|RyIH2qAOE}}hyflP-83}3w6);ywYUF{CsPaU~I3oU?A`@le+(&WCY;ZrxsSD)NZx<@{2k}!)uK}!s~ISyXXbfUiSlE3+C'
'Gdl|~P5pEu^rf`0J+-xgQb|YJj1bc2j@M&n8XRtGNL8CUM>4s_l^bgNR+@V#-KovV>cdwp0bo$6F$KNvcGDyaf^DpOjB?>958EXM*M2pI;XA}OG(%>1aA-5*@!~SgYr7VYyd<btN<EqM@89V%TB4nC?JALOkO)-U5@${{#w}@-6k%Iv7|a<!BhVF$;zZ1J#CZ5E$3e1q'
'3+17l7|(UZK<<=;5!y#JW))vgSmnhm4asnr(!S({03@WSuKWyc#+H9%!WXf?UF<;%f_v@or?3gQc6$6?E{n%Qr_~x369l7aQ(6ZH#T*LYAmQm*kj#EJI(h?vfRnw6i^fLJgrB?)?Ci_iuX;Th&JL2})v+q^W{Av7P`FSPF_1ugg!C4fCCGSXOAUqfxL#4tCehvq4(xyv'
'1igiNPy5R?R<u4E$#qsS@TY|j&ATn)F;3BzprVIv3l|ybh&K6k#E=@u1SQzh$a&Xf(+&I+*kyC540)1W4lc+pS~{{GxqVcVe#xfkcO_l<zrt=T6=e+7Z}qwtbZeVgbl4U-hT{<D-tQ8Whg6G+Y&m1EVCpe}^m&rB5sRd7$v1gg9vT^)k@y}l0?1_t$91xw_YGO}HZ`r7'
'9;3LT$-N@-{No`c+(B5O)p_o?T>@w*HzTp%7gi$f6MCMEJZSU32%o;fH~tqQQi_uEv=0gPs`yRReqye$cxfBY=xy@fsP1E<MhH#aO#>X=UoObX{>+_^>9<g*V&zf5Stx3<c>a-J_z~1~x1ky?QcOtOYw1deM&HTfZ*^d$6cbg(zE*!r!+V{95Os8r)<UiJx)?f;Zt>7u'
'Qr~z-?jhIWxzpS<eD7)HL@6Cev}nb*ChPp&BM?s3frIe9etVlx$bGlbJYXudx!Y#n&fpz^ORi-Xhc77jrv_O{>!O2&EgpYb%}kTAL;>0mwKMe7qpOuk0F@uR{2D`hhz0)oC+keU(J&pxcKET-Z=RG-hX?AeboF#)JIIR$N{y8PR@}&dUHpP9F}j-7B3wf>BnpCc7VnYr'
'w(Ia%Gd7A;a3oye>Zo>QhJA2&D88-+&A$e&J=B*)%x53B!Kd1`Q%V8V6&+5WC!&#&U=`>SOe}oLZ^Nv{+-p8V9#6$xO`!m^sZAeB8ULMQ?&E^_;;0Ndco$2cr$Ke^$!(noo|d9x4gye9ebKfZOrln2C}6!#NBS-H3B_<5XhPm8+GvWg^Bj;(4c%QyuU=&M7T{A-d_>^E'
'iYPe+|KLsne+a!Mu+6+RelJHeB=!FrhecZTzr<>y=(!7)Vx}hQofBN9a#*Nl#r%o~+)<=dzz&gOggGB#EM<9UBr-7Ab1mOLNL5O384Ip3JA}4h0mLXXTLhxae4zwB=kGs9-Ut~i`)8@9j=TArs~gtvlUy@C8|on*hG-ed%H%z~Rw3!G0!9rp>1{KMR{a!l^5|9=6b&7B'
'e~N9CmZpj{ERYnIPTI?adz?M=LWDZp)sS;Az(u(@(Mt7)8Z9Ezjsgmu&R~h3GLxMI;hc-dyN!L5Ib8XA>?{qvixr?U!8V((s;&605$@9u_H|y$QirL0=D^>iFGe!Ttvxj<tiO@FgDu98M_LRZU%?GYa5IcJy>}SB>w#M|TIMoHLbVa7Wp=MUA#lV%AEue7y5e?<<zw%H'
'#U7>w%q3GqjRL1kB1&tf*R;c)<&Flk>jA5iL>ClP_78WQmM1Pb=p}954}!58!jt&PowsRfCO55u6<bwE+PEYzNS-sIsE6~f|3)J-R+2T}%D^Is_Qfm}O%?^0%m*Ma6-&7twV`ht0v^W6LdsyVUiQ@3$zvd)WfV7bM<Or#Szzys0e&CMOYP;G8gUB6a<~L*qwv=q<^)z2'
'o1#D2>MZyi;W?PREkcpjYK4THv!N8A3%U!)k^I9!pX@>Ug6w8yYe@B7*HujoK4S(XF@S?U*E-N7_augRz-K=!J2BX%Tq=FBdSYb{@eAStQ$bMa@l4!Yc;npo<3F@^E>}gHQ#nW<sQf~~X7ws1x%o%Nl6d|}FvlM!PGFEiLX>GU%yXjWzyM~kc?PaC7HHHl$A7pn`?+B^'
'n0C)7^0ENe`R24DJu02-m4nB1G#dsGdew<A{ddHBn1)RhyjK$4rtKWr@>uDX9$WF4HK>g=`6+P(+@=bteC;bYA8C~64G~WDaxPErMj}QR<KX!>-HhWkX1Tt?aD-BrbI(j(jKF7@6NIG3E0b;9=4?PVZ`2!a_mKBER;dCdZB^?AlPRTb7?4DOqqxIUweeyhPT|v525W`u'
'IN{ODDbY<s;g$tm`OSf`Y$gqx-h=cK2I`R*J!(gh1Tb|#Q)NPfv?;KQRsu=83x^fcIysErQMQ&qM`u+LUwC!Bmt%EU-f}?Wm6i+}-Cg}u{7o~4E@6O{SuPSz*Y4+Fahj7@QRtr#%c8tZ+uf`8x?FclSs;ajd$@P!2at`yT&qndNI<RkvF8?-qo@#pE9x#q^$9Ha75S@s'
'I(zeFSLCe=-MNw?DBH6rkO;3`LSLuNfpf4wZ1$}4k6ZySCfiWiIfG+@6<{RIC@P4s#_B`~+4NmX-9|;e(t)naF~ukJz1Bm4GuJc(j{($lcqKqLG61E%DLvUqKt=V@pXyh%ynGT4l^J(*o355T;YyB3zeves#^eg^o@sWwn7yASb6=$SLadAYb9N`rtD6n4rb;;`)l=z`'
'-B{Ut1cIVDd*dS~-PW8q)8d@_<E^4(tbD$b$ynrt*Qd4E`#0+F(bYl?8DIm4Hpo8~?>$1gmxH&<yukP$h9>cKMM((e7(#v?=1Pdo1{j+ng*dquWX^7A#0_x%NkJL00XNc+SwkQ8Dyqq0aK{qm0Dh9dQmb@9k8bW8DQ{<V)G0M&ITPp1D-3DAAEt`4t|Ia4Nw>`P;=1XQ'
'INsJV-u0ynGW=-m@#Jtymsyh$lEm~+ljsDZ%z9$X)_to77u8(gyYDny9s$_x5hlIR5Sz8mm0Q7FO?mf*E%}_($--ll%z&eH*}0Pc>R@8i1{Df3FR_TQ^-OGbUgF;n;W)q^55QO}A?od?H-kMJZ17R>iOdQnzcKBwjzpP*TVAy`7@)}u$V2b2i70(La3oozT$N3;jo&au'
'53OuH^!O@uu=*~_^uC1MK|dgBD2h?F_e{QCSKg=xyy4Z>iA}B|y43?)ATF6H0_h}+jB+niEY-t<OB%LpG6Mpt)-BQwN9(ac8**22*X(<}WS$@w83X4bTjjY1U8Ap_OGmhh!Qb~|Z8e!P_6+i)(q2lTLzURxC>|wmouHKEG_~qw^nH=sUf%qhwa}D?%n%y~-q4OT5ap5`'
'v_N^vCI>W)Y1jA84*TQapbD=H{)ssEKX5s}ONg~av*5b<T`OHhuJl70q${jf$M<JG38ps04_8f*bYl+f*v`ESTcZEDG`~)O9QB;%^OG91l<Dm8^7a83b01y-Gw6SU8F~5YLu7!g@}$5rvz^OAGBrS^%sklKl>v|-bjj;9gxdga5A^1x4!?S*rnL4gp?FIQ-GuK8cv09z'
'lemUy8Y^w%x<>n3734iBCNBzl^V>YaEQ7XhM+XLTDKX#d{QC@Qa5(ewzqUySX$YLpHhAh3f!4i1PLhM`JQ^(pwP_u0C{YH9DkIuEnR`nywtWJ&8bEE$H1<H3c|ID$(rUO1>nwEzTy6nREo30>#-CTRPs0HUNf#QhApQ7XG*A>LZuQCnScF2VFJ|Z^V`OY)-U0i%bjACI'
'{NW`XOa=d6<H>t*f;h>y6QH@P_zIB=0(}dfR9R3aE5>sWWZ9{y@lgreGs^DSce4ypimd#4Yr5PU!-LyWV>>zrxoddc-uS>f>_o9SICw{LJ#}k&&F*~y*O<!s{E`R6iGJuKi890(b}#V%DTrx|+Gm%M$a|2Rz(7iY0|@KiJCuFSZ_-$KKc&b!kA)m7aYG?vT~|au|D;mo'
'_#SZ(joMQK$n0~7Ve|gmM_t4M7p)@DS!fh8Y?5ViRZkAV?5k+n8;?Oo!}2pJ2!`=8!_8g{GzDWhwLcU1em6EBZ?b{5UD*tehWsB}?{foDwvM^7hKmcn`zR?D@KV`6H0|#l+dR|;ifNHCgxoBA?A`t1qR3M3!(j_h0Ry76fNF<-;tKSFLHS2YChfjtL?;3GyMntIzh>B&'
'd<AqTYSb7(E9kg^7A8lWp}e#37)Zh0@l42uk;qP#^A!&lCn?lsd1b80*O8fz6as9lB0t_I6-vrZIG{gO*5;gr6q|p!Yh!DG;to*j0F7KtWQduiOD&iDrI%D_UoMT)v7(2e0}5pY*^x$XlPVr~2|i9@G$D>D!WeGWikxcr#U*dQbUtxE91Z!!X#>)%c<3;{IT-9c?pHVw'
'WtSq@i80*yV_D_ZqO>-Kw-*BDjya;K^Z>#$XNJ|C{JO@m#TNq8#pFQK{<Tf4%mungPJNH@lmf3Q_mywZ*tJq<$5>En@c5-D{@sw*#|_ql628Y7zT1TKn`G@XhwePnw>trKQQ0xe?TSzl7s#q9O|RiLE#$7m876BQxVy!*Oj#}oNv<0-wAN914dSz4mO|LV-uA?YT^{iJ'
'y;-97`JjBsbf~N*$SuFb)vIio!}^e^1qwsryc&?X(8enS8{oD~t#Xe;FY$?9r~3^mG05nQ@fiR(vp~rHKYYLl#Eck)s$gun!IP(T&=D|U>PF9Q#7i-2Hl~+(u-qxD*vW_!<h3OLVi@`JwHv>U_yt2eCw;vq#(?s$qo>VHTV}aj`;B{8TPd)HVyW}IViAvye>elsc$v1I'
'6*T*-M5?flzL_8an>bCfO{)x7-3EENB3{2a*o!hi8Y4pJKtbu>xn?;($$w_Kp`(tl&~C$wH6i`R2JRM0Y9K{bsIlbCqFupY=-d#A_K26|Vb6J!j!82;L<o8m_<#!8{Ieef%YQzaHSW74b~ukjs&UtC(X4Q}eUQHuHjBNFKPh6Ol&s-~2ifMayX#wXihFo^gy$=lBwiLH'
'F0IT$99G4LE#-iGftXWUwWB2x&f-weNa>E>PzaJ+)#H!w&dQ8U80r4p?U}I_F@+q?3IoiIM^nJ(^n|8p?*;bCewK8X`3&t}vQ4&8>+0qj)!tF3)!rb_I5Va0TxIydun^|6N-32|ixuW|-Pw?Qb;AntEwTd)p7*mSm;W^%R8T@;g}18elsxdB-h`>wwX6UZZmsOIBt-Qq'
'0^wOAXTgv2mfb!7)2u;W7YK8Q>>m}5)@7St;D{)M3Y!J;AYW|Y$G+t3#Fncc>cK`*faz`o;Rr>=k&M4_pajB13`*x`g~bmg5Q}aum^D_!39m5g3u2)t$Ee%~!T-=16XiyLW!RZ8E5N^IA$!C>S1>(XoXp&<K;z)5!fVdeSi7J6ixRXZe^usoMoJOVAK~^9NkRSXI@Bah'
'cQn_=XHO?yLS0>LZ#NXQ+<u-)v3dELpjcKS-2-=ylD>a(nU1!8`X}hNx>WHd?L5ju5Y}_~4R`oxA2yt)v8~VQNB^694StC}zI7`}$JoB+dN@SYJ<6wQE+#tp0Zri0iD_#U#$do`mxZKsg&7B~+(wBG0E=v^f4(>v-%#BoU}{1%jV*+h)A+HejBP^bd5PyHAW@Gu6Dm=W'
'lrfI}MKY7)z0S<Tzkj=jL1%7>+w<1SI&>M8B1SXn?6884l62ZEM3X>i=cbzUWYZ3C+mfZ)ymymqxd!Tw{!da(V$%<=)CxH!0c;nBrb~Y4<;3TE?c(cIje1I$HfNL>w-CmI@i>YhPm?i7q22W(yWS(}9hqgEm+Fi=u}q~va$ZuvtD-b=;ttnMFfod|(j(B$<J*>SHXtCd'
'HM1lGGcAQ`oB_kgWV<34*JeDXRH$(EE&B8K&?(a&M#NlY79g??{;DT;ZHdV{B0}1^NQg`$K+weuL)#*|c}+%55L=V@W!w!N+N29%5M8!GZJ+9FuI~;CJRp9HeN-RpTa=nzSy!f^y}mtPDLBPexUb**H1gJR{g$?#Tk>=jEsFWoX{-N^mT)G{iQkrI+woaG4sU~4-j{NP'
'MXxx&f*%`8v5?;}<$E+Yy2yBvvbFu%L1`gOcYLw6Ir1f64^e~&uqS5-LXYoc^;*S#^P8z3qFa{u*HP6dqpUhAgha+f5y&Hgw@&iBHUK&5!>rek9tM^6*JYjJ0s4&F#&dvdrW@O#!uJpMw6N6P%R#_&E>w^AHW;g*NDD|w-tqj}T3gRjjy`E`Z(sjWp7H#?sgfQ6o;aIP'
'P7gx9k{^IL*`eW@Aohkg&(r5DJ;S=cm4CqH7Fz(Xm9>?!Ax#cJZCUZRmMS4{7nC}m&LgtP){1rcsUMk^gb-e+@20rq#l@7k`%Zs`l@Bamz%u>OP^zw8!}HAYrz3dJT?&W*vnkN0gIV=?WrjDMv1-j_CobUd+v4(J#Cxnp2KKEHbozTkzwqTGfT!FN^V4wPOv@=vU7@hV'
'$PGYUP@G<?3h8iw@mEr_o;*_Sxx#&HA<Lf;EB2tSd6Ku7uK)EIxHke%p#q?~l`g&rYNU526%*+<XcDP{075I_)ZEFf5?5?Mqd%$VSDMHMu1jQE_8q|)T(mR&lnPR@LeYyNQ{xsX-?T0eSr>3Tc@tV=ia6PjY8uO}kFmVxD+nnXYR=tPDUU80)@&PaRXy#@vK<1-48l^v'
'wV%0Rc5Vc+GI07c))anmx)rlSjH~gcNqP|7QGH4@7&xRckv$BIl1ly*Aning(aM5PW00*m_!DVXB1$1Kzrj6hS~z}&NoWr)DW<0MDq7&1hS@?sc6zY_4N_}e>RJL1w(rk1fcQs<`^@O1mVO_pV$aBo9*ruY3sOpo)8^{L*};O~cWLb{gU;sM?aSd;h)fX=s`d|z&f!!5'
'4;-a=`1TkGQ}KY^>X^}hBNyGJmGOl=WGLO3(;`k$DE`Vt7PfhKQfmZn2=h`FQ<`soXZq?Z^$snLA74>_m?lK0WF!k-zlkZ5{hKhm5tvQC>~m*<TMyz*HP}wof`DXyEtBLZMJTtMRlTkSkr072WN8&vHvfc4VNkmYJkY32$dCuJ6&d|F2;F2beTpoO=2t)iLfvz(e?m#%'
'(cC4Nw@}dvOa_sqh7wDS_}u2vO0V_CO(jnVAlQ%HO=tAqcOK(rYl(5a(eqv(9w_?)z24}fhH}eYL<T*Vxsb_DrRqa{+R<@?>&d3r^+7z|4viO>Z%B5ixZO*G&LyYmYaT98NNQ;5VZIPqttDjO@(_aij2Yd?;iH#CM-_s6FNUdojFp^b*5U13_41Qe<pVH~&ww<*YNPwV'
';qCgwSvEJee<~dWy9dMA^vxl$PPJ|~Nd9#M74-YQk><w#nwKYs4|mpNX%v;hM9)POynz=Wf)@J<;BR?x+($XbQR^0hxn3N=GytJq-MR9NeS>6%!~xssjZIQKWy8FV?HFo)^Pf-&w25JQlVuLxGo5`bNm{~}cnRZ#h`Ps&{nw|1@J+eWDr}jV=z@p$u(DmJy)|}U1dnjs'
'iV9-L>o~qfAryL*R^y2nT|-mwb!}hN1FfEVBSyd^_YED6KrBp<<RfoMp$}youtq>VF&(CEr*v)j-)g#7F*Z6lFBe}zv9_hzAg-_F?g!JXn19QL@ojIFT6k9jA9a*~5EXrHQ~bxHDP%mw$#=PC4vXiSm-kEGW=``M)0P|{MNMp1XV^3q63@rIcpmM@IM`DkGvZ?;MQ9@F'
'EECDHD?8Z-U8{frePCUI=6hka<@eVA_se=P>)RM{EnBoT=jeJ_MyAWF@j<SnNbE6nC%L~gnkW$o!4ir#vT893OMB&1K>9crxiaGfm-aoiM$6@81|h)UTs@ch6|)Em)}N-o%r@Z2T=toE=XDO4smq_Qp`xWTIHqk-`yRJ@@M{OwkLidWzByP?7q^{yV=QM+-N*%rkiiz|'
'WvkJ?d|p#9<d<I1`h(Jd6MXL7%f~RDoAFNbI?QM7X`TRW?e}WM|FK~S(S}lRp)|X|zSk&#<J!ns%+#1a_4a&uIW&p|bQ21AmdugUH89$|Sh~BNil2+jaIra2oJAGHTG-!D<cxpDhNl{0TOFog1TxS>7~kSi+2GRFwXinNIOXYANe%tz^%16B?);cPsg0)S=2C<FtZF<%'
'iadh&8{{44e$Bdn?QD=2&=1)I5LN8@Ms898Sa&vsd9B%=(0Y?)RFu2CDwiSs(UXj`Yf#c_JT=*c)4*Di$dpZ+cHK7`u{erCP8SN}Bf*Sk)7^-X$ENC2ZiAZEGbp+ff7yNAS}LIDFBW3y8g<|z(j0g5N=;2%8S%*Z$jh`NN&4o`WE3WZ#rHWnFarN8V#q6-MbXD~dxV?c'
'e$b#MHN2!m4dS@<P9^F~Y*HaGGv%EH7%=_F!9dvcax+#si1v#Joa;^NZNKZQm<AV%ZM-NHoiJ(Ju`n8(!YOBL)9S1N+JU|L(XMbEbBhBjeztLjdM!;o+SKxN^Ed(cYFfQ;o!C@tSE<*!uTrzII&>?t^GqEXJOUTm<}Pjn{>R%+pOqqL5Q#1W`ETzCia>q_3bk2!u>o{>'
'54kHXOu&TWr}{G2f0$#GaB-57SG=uE1{|S<%H<I#H*~cjv!teVzzH$m5f3(Rl6KnL>6ZA1&JuzWB_tAH**xs3)W98MZ>upaWlJ`k;IKe;$i~1q{l0<EGa~(M&!U?ChgHdNLoF^!uekxcf@dpLq|`pjEMmL`DSUh|5IqQZ+_O&*)>P62&EL5s4MkC$YKVQ@lnE0FN=tMP'
'!9Kv^dl|5;?>g6rrjA>(1xJ%TM3Qfxhna0@ou%qv&)m`yV$}8PQ=>&VfV=PNbyYhEtq#UyE0)uD@P_v!a2(@*iCDm)!u1qdF1W!?MY#@;IMkxfa{ONm@tlVOr})!EC>)GXT^0O3$n#+=fVBxAJ@B0`6f+Hhg@o*kT%)?yaI7%vLs`VMU%Egulq#Q7bU*``iL?nd*z%A_'
'qS4Q_K%X~5`@4FSvj|8SBRzc)*Z9kMYN}pL5m!u$@X}=(lr$oIj}{^Iw07W-dyEvT8-xt(>cDV=I9{2Tx~34L$HC80+DQ3=T5T_weR^Ep)`^;lOKK7dGPhV5B6`4MBw`f|d-T2PovK45|D)SuI^&X*_}aO@U?FoNF1(1$iC<t}{Qcgty3HU1$0$PDRibPQMy1cr$iD{7'
'%g8h!&?+Mj`iZ?5JGspIsK?`I(wRr&fx=L0NVlZf+qn%`fWMhfgNWMmi_=qTZxHMAR9Le-a>knho!+eeiFb#aT_;nll{elbS-+=7<x5jFQNgidM-hr5qbZN57%^VdEoH_}7G#e!!kM^yXe(1j<bf1}_W2FwKq0%Bk|a5B(oDBh1l^&Ld|d(1EvDZp#cBwmYCovEdP?o&'
'G?ua)&5}!wiiI0NVYUpkXEnE3SfT_S5=ZV89vwncBp3F`VT{u^gb%y#eG1D7{z{s0;o2aJ+Ot>qA7}kSaJ1B^w2x`_Z|$BG?)Ech-!f}QYVP3`QDtg`E_@;l0YoMsetT~MNzyXTyCOxij#v3~nj^%ID92<mH?G(p3}0`1yfkX3uy7HkB$y4>A>afBv&oonW5FQr3DH$?'
'4dSsYLxexfE)(1K6;o6oLMWElOnLtzQPc80HOClCZufek5*o9VpTV$L5%NO>wZm%5BBj#aWpp;fnqBtg5aNen$SGgM+{rZdiBwzrK+BM@ZdD2F^O_VO-3DundKSuyuIO_ty(I0$W%Idw+)XXmsYqt&69_;Yz>44}Y@_1IqaBYlM{&|6wgHty+oIv8kL*Heri7sJedwoV'
'sE)+{&Mz1)L4|=2>dagr6C%~4npk^}IEgA;f>8~R?y^Duu?py+{5fiheZw0~4UhT32&2Y5&nAyO*+^;1kU#HEo_9?}Q`7n9fuPoTvAQ2s4J(eumr{osxJO4aT4QkSO9~NOxhj_Yl5K#z7#6^7`&#)Y0nG+F;o`<S{<N9Cb>XPIvn8Z4@XseB?L{j{Hn1pTmri8k&gS6)'
'12H6LpKI}nqbGhVWDKcI%^P$-+C_hlS9O?{)I<2RJPPhFXl}01l4H0!2r$!h5L;Mr4|(u*@}ul;K-{#TpK@M*9~>>Ha-|^IDT=lS?1Me^cq-Aq=ZzGB!(}-EnU}EKSD=(pDC1;EHy$V*9c$>HKVLX-eO%;Z=#)z!7*jZ?E{dAlsG-*~Zjxo2^0wmEL}R9D*_mjTOp{}n'
'0*xYTIlNR9J;mXf84RCf9}a<pN!UjcJOMLSt*gBH`lG$)TIQtUUe()qsu9QXF^LpBbHBv)eUB2#8cb6`b&C_AB9--`-L9vZL*!i5Z;A{$0V_PG9?@F|TBt)rsAqaST|Gc8c-B`5|I8e1oeQDN`cV^y1O$dG=4vNe`qXcR7uIdrr}-sa%tJ<aQmyr~&b*lu!AN~(v0+bR'
's04A;!1>pq=KATIYxbynKOn#qs&H3sNc?{)3l7YKQx-Tgb`Hg(1BMNVrpLt12hQ4&f<YEdGO<a!!k=d=#K2(q7WHar)ijN62WEz5W8aQ7cAE4&1={oLQ&Y<oDB3YE%wqVH;1_{9z^{@&Glw>kA@0cz<!dF&T&Z}rnOY1X@6$ZGUG|@hcYUZ|j{Iz^3%7Kb*=?cvXp;B#'
'CwhqpB?ys-^7f&W-ZA{kZ_~NJM8}N$B)28W7_8RND_ptwvEUu=9h0|E_MNw?<758Tv7sLY;{2cs6Rm;2Tp-fd<F>9X5kfh@%eY?u2N)M{{70jT1kHE4^Nsj{+n0`X(Q9bfltqzg;A+d^VY!m%d7fQChT<t>sF%1BdX-Nw9+<^AcRKWY`6dz}o{&a=f-<jOX8`?w(EftF'
'*J#6_Mz(v|wAbl0q~_Iee5I${Ii_R7Nv)mJP7p1f?!iije)cRpx{PwfqV%r%EyfBu+SDDBl}%wwO<t)yf@0f4eYY<4^8QL9(;4fzRxNJ4l^P&8bC78jvOh4%Sbfo-sd65OSKHYxHohry3{Tjh@=B9&FWbv_cLEfyf)cVDE$HleeF!V1YXN9%L<70nECL%u$+<eA)U_*n'
'1*E=fU6D!l_Yu(`-tG0!MygRsU%`gRT)M0Sd<{69oDIfyvl7-!x_?v5?B7oWERP-*T5{h<&XoHIin39HSzQ)@>V(5KnvNUJ8kMk|KEb_YrPCV3B*(t1L>%lp2q0PuPzNjmG=8Z0!XB=K$J9zmO*p6Z8T+wET|Gc=&~eH&ajAS;P*)LEsFvC~?BZ$~*N>|yBDe#-P-OP6'
'J=4bLWhXCzP~WUGH0cxc5mOu0CXc;T%?c^jrMpyr&Rqe*K>+R%BLmy5t%Ay-QK4&whQxUW)gBdD{FLs#MN5g_u>Y1EH7JVBEM7a9yW23w!av_ce4rYW-r+`{vd4T^pa$E{VpoPkq`7WG>$1Mdz}alqI#g%|&baFF#OkV{AJ*_6u6$=*z0Tp9=$8jbhVJL|EV9cZ4htwW'
'f5GZgD*`N-$sVRBwOa@j<$5h<nZx`^cz6HS99o2JFZ&Nhu@8qAYx-#d`_8-L;R)L}1mWT3{go34c!KqUGa!Q?6W_8gktPF04ocUEzn*xERTOX|?A^-WiiqSCFLGV)Z;HMS)3$r`VOrJUFgNc0u+J+OOQeXSfj(}43KIf4;mh8E$DU;4vF@ic|FP4ZlvP^?Ep!&cr}O<U'
'=evZbImTjv3sjd}S>ZtBeb2bpkE85U05{QYJYxNX>Giw!o|e@tu3`{X=8!koa=0laoL{@^$rFQcUoM{KAK(8avTN>`!|#Pd_$722AE<)3MISMFl<udRG^NB<vtvILK2`dRt{XIsP5e@8h{u*#OoW_5HyD(#bvnV2=ESN~aQl+pA=CeH*k?GezVO)AcZq)6#t#32MTXNv'
'-QQczv0YV)SHaU_fvlallSDS>MQ}8Rju&PBOdl3@m$~!?KqZNVJcIC-kcTQ9N#i&?7ygUL=sP+`Fw!H766jaeqwy?fD~?}B+JSok@^>jX@2|y+YsFXf@R>JInjC3oYnFF)Hw0NtnE;I^J5*od!#^-{P**p}J<f<L1qqf^FIIO<X*;3|(LrVOo#9DQXD5sKiUj8W+JaWc'
'&j3(9dAtYtGAsy|UD<yDD(VvH=)Q@Cq(WPMw5?@hE5WdQbt5WD0iEP>G9`VBGgezzj9cA!DC2aJDVCBLB_RNV<w}r4^_Z<2+v)fp_nz2Z3V^>lI{{gl38IsLT0m1?%g=k_!+80^bxe3^mK}`w4Sg%nAT}~O!=Y{TnZI3%MNK3bDu}`-_!)<<nx@_CN29vjZb)6${UuKo'
'qmk@`md(qe$juy(J9s}0N_}h{iNV-AQanI!y%v>;1$v*VKdcrHBJ{JW;we4_H5tRwAE3?zIRRl^g?MO6-#Piwh^eP{EX;liFp(D0fp6E%AlRe*20P;`G-`l8>6uvYE4|Bbi^PaJ;}WHI4uuVf@(XJobiw_S&9i{2e>zP=>p*zPGpLOr`PaG1-O=&1Odio)X~PE0>2g6M'
'#%)+7;;SBh{BrNHih{`~^&<5r<YK&1Xc+CFGJFL=8I)kM(UQ`vDE2&|t`gR4og0Ct3kc;CFq(}MhlP4q?@0s%HOP1;n1iJ1SurLkeN07QKNHOkTHmexyQq4c*S5JD0s||bZ@Tx%MY&}rl3n6x>#Iy5(5QLsow4+9=0?Ztijg74f~8A<GaA+kKeiZi=<LK`N~}^O3)WKx'
';$a)<0GiLQS3~{?H<`I@Pmc(e03^Lueo29I=fFx3CJ%qfS|5cPnSO!#Uvyb7F)KACo%T1F&sY+q)e?EO!K1U?W~2-(elci@oss>af@uMgA84sf4bI)BHOMRimZ@|oORa7Els}z>?gOU&CNHvhII(DoU!HRy5W_f9Vv_)4vZIpZF`FO5^%~fKkA<eAs1`w?0GUwkpvZUm'
'Rpsn6&rZ<k`mFstX@mTmxCEcajx6q3BV!P?tLO}bDSkn=(FjAO*@_dlv_sdQJslx-+_s#C^-qdfxjeyvmB0L~&o4}Gy2@=kG~?ao#m^JBVA8*H(!mb-3tic11tU6xuw=EBo`=GK^<jDV_xTC`gaw7xuS4}($j#GG?YEJ-xt17~K`fLhkAeoY-$0NSOJB8rUCm98or2BY'
'<7$0pCQ_FV!19V^z*+97m0G2m!ob|x=y1j6r8=Kni!6$blL~YG;L3RwWBkj3)$$(ZDT<`Bme)Kfc@3S97>UZADV`~01d4z$tPd%yh^`V;F8aq6ZP3Su9G|aLG%J7$AZDc?rsZQ)%+XZ7*3s14DEfFL$W0L`m~V=(>%HepBg^^WZ8pIGlgehdP*a~Bf761hd_<EwEh^S<'
'yeUtPZIW`{?9F7zsv)SH@G9i;MK}|JGZ!Yr@@1zy^FON}0-E6*B)~FvaD?$>aC&Rh6DTv(9A5a6c2wN?P1<H))bOVD)6IFeQA#3qbRI%sC(mAG<yf<wuHTSG&ciaGpmrG#+aDtAjdxq+CD~45Fi*x*`9U}wh@X{1yCOAu^~Jy^SWEe^tK=zu%!Zail1}>Ly7%XF37Ri&'
'b0;orV_7!L>c^D~mzXoUKM|PQ+ZdI6Cq4Yx3sZ$YuZ;|paQn!Y2`Oogi3;!rP#GMUY1=kOy=)1wty+)G2>67%<F1z)(Ahwl%yLWP)xa-P^|e^rb8*UQVH_qG5VY4oiwAVNBiu#p;R&M9AKHKAZ$x*Oi%*ap6?W4JWmONmEosPSk!7TRr+%`|RmS{&Wyl_h;#OffjbcY('
'&VrVz)=0JHvgNe++Sw1tC1S}84WNZB%e|hcK>vv!$P2Bp)`sE+?foPFijJMWa}vmji4)y`Ycht^mGk>`-(iMWyYxCX8(^6hPIj&3#zQ=!bZ{sZlRiSj75)`eKdf^dcK5c5%rtJfXbYl+0r3fAK@2YEs4PIWc5O-$pk=EZ8b34Reu#tPMO<Vq8MQGXu$$<ekIbEx=!>p~'
'!dY_+cy6gq+saXlrSul8y!V%#9PR<d)q>QtF*vZ#5nQQem4XHB{hR6^%ke<fxZy&a#ymid>8dTo3xWl8f+KZ`^S!(uMU~o;#p<L$XW`@+V_IvIqEvFJ9Sek*Snd8WgVsv36NJ^Z?%=~9bo+ZM`8_8#A|<OX@Y<mV3(GSF?1T9Ftti<<@nsG5$T_g#f9pOBERr{=sJMXs'
'mqj7MYa$_5E`dOcC0>;9tYw+@03tv~>9422T>n=o1stF_dfl;mGQe4_cOtbF;Zfvg=5;jz-yYdTHCU}#5)9|^dRQ`1$Nw@<Oe(b2oZ%Q~$c3>+pr#X5(K5~QXXZ0Y^)1)rGJvMx3K%+Kz20f(HZZbPE@YfP@ZrR(VQ$-D%3>$7a$4U@Ue-!To}c={2SNerVtF7kEsx+D'
'w-XIXChJC|4mcpbCv3(ke`Hzg{;I}#x6oZ#mR)wnz<ehdxay)~tEM4YI=c@8^WNaOhAmlfr7L&@ejIO$yV{-s{kxhPaiscDnZVc8b$aDZQXn|&j1U)h>cC&qV0>WcI4wfG|7*sV5I*-izC;mEO#QHe4k2#R;^gNdO9p-~4sLr2j<_GJAkD{Z`;qieFGarLyrH3iF2znG'
'WhV6SUsqo%O6$4KW(GgWY!R{o90p+Iv6GfpH1foZ+AXedBeMYt@tzKCuQPXFv!=u1r?t`W>+(it?dACpp)({q(b}~kgq<NmBb`h9&0kg6uV06?1wO!_GF#_DvU5HHM`TN4)$sSCwwPmR(PS?>13zZReW1m)F_0WarL$^SHOmdnqWE{^(vrR5U-(IV0koyylW_iVR6!TY'
'0E$|tHx2JvcI)r^0@}wa%X}y53yZgMYu`wec!tvSTm-g;CZwgePt`ysjSXTPwbhE{adQE(dujIk{`GGS^^FL{x6`s%6tdqd#zvrDx2i||5wnoT2&7)}3f@Cy1<b>MC&MP4ZEuMHwp<^x)eSr){msJ_?0`-Jq#w83o-g@N?cmqkSx!&}kOUGa1Oq!)bPVk`X67->D&{4y'
'yVGeNwZ3?g*R8S~HYcrb(4xFD^Qb}xNJs-J{icZLn_N62aDT6d-`szHVpXt?Z{nH2tge9(HNk47utk${3A8WhnpgI@PXUP0H+RyhFlEF?ga^~Hz7`rar&1bJqD1Znd<v%cI=$&vF2{aw3TwQ;(;noHqJlC1_(NrUzs5e;{0LDsNwZ5q5AXfOpvdSNfc3J?$%EWRp@DB#'
'MM1;S<E!X7Yid3yekpWxg?X8)6!DA?AvJEe;81akl2(e0@`ZX6+o{Pj;{c3J5YJc`uXS_6F0Sl665irBF__EDjH4=Fe?df+NzqOoX_)vQ{_p)wT;sB6m1Ie|-3kIeu?bb1WiJN8`!DByY1BnodHQr?&aq?PGoef+->f^<IiqZ!7a}>AhBA6+w;VjM9A#ZYk^3Zj{#qh3'
'PPf3URfh36b4mbSxgkhEDUNE<b&TaqqOF#@1j2`|Ik1scNe_L_c*ffTBwoU5wi#9YBTCMGEs*+or@cy}Os>E+p{R2wyE^&1P)q#4g8~PDj$$Qw6bjCW4ZSU$KC0hc_(ZAJrAc%nQTpc3sC#uV)02p_4F2fIecX!8lBOuUY=NvPM}Es8o)PV}krx1-e~o+zIjAp{_{Byc'
'-5gt`SO$&5PdBynqu*-J>aJ!;`CIGSG!bLX=th6J=l7?QF;ymtfmH3GFrT!3=42a#wfkTW{Mta(vnA`mWD4>-%hhAUOzn+ESS2|1YSjHs4(ku5rTwSj^}UlI7bM}44zE{cohro%Y7(!*UdWG+@eZ5LDJP1nD6aaP|JBhL)L)r^xdaDDkXc_yi(_coDB!B8_qFZgdeJV7'
'-{|&}*d_fxlq7PHWd!ht#%a&nRw0uhKqe-5fNEO6)~5;Luo|~o%WXyri9*I}Ok@eYjC7iQwvZi4nA-qO?@11gL@)IT2Mcw9^zmr^%2`zQr?=tpdk_8{XAdQMA^sr-k&rXR7tp=Q-Dlz;xWj<`W-6`!ELReKC^dgo7(iC|XQV*=r5c%yXr*A^vzE9^mfp%5P6B&UtF2kG'
'wRv9hJIA9zm6B~NOF+Th{T>EvatYlo9Kkp7i^#5M3fPz+!*xexhOo(cmZakRUX4}f9)Jfcvn5Z`E0(t=b#jHEk!IhgN%EnSgF)<qXd_~4XvXX|@!!CHasiS1SfdDTuKEdCM1+1((<CqrI9cZ>jRhgyO!zG~M3dqhQGyqjC)|;VtU0?ji-jI+=KRknWunamOz_;ZiaNzl'
'46rXD9mVP05k>W#uWGdi4-;4igc_*Iq4o`y92Nx93h^2glK7Y~Y>Q(f{k<IVtRr4q^P>;F@f})XlA#s>Eq3LTShOx=?WuMGiB2DGjB1QaEab(t?FD}tsSgo}BfE~(s$F1$LYZc0B|p{BCO0_c;kd2KZ-dG9{#V(L)a`rRYpW*$J{yv;_w2hbtaPm8SrXi!)e^;+F+Qf;'
'ZF3myc0Kro@#6X%#sc%}CF<f0!`$n#pqCsM4&_Z!bu_whjTskvZI9*0D!-MH=KQP#C<2b%_nQ51HT_^ZfZAg9>|}MDuWGm3B&SE}uk}=(nA*m^Z<pfUSF<dvu~Iv8gI?+KGP>v^EBFqYvDrf7y~c&YAw`G;1YTX9kBJLg7a#FQ#q?||RI&9!DB@>l-ab{TxL3oZW%K-P'
'eOp84oNh6}fJ(2fkuDp#JhC(lTh=t9@N7S9Ku$oZCqpe&HUTK!QV0u+!i`1d4J3A%NQ+e`MOo4Jbw3irk`c}IPN?N1;8c;$(^iA@zQ04g{Cc^1$!jLkA)X8SGih7TQjOlt1W4fv@Zfqkf7bo`zy7wDUokR;4SS#G&93T!sOe*hsvWtVAiP=)DCKfY^GBY?85nszAP&);'
'R-ic%0SYaIG&UXAydB)j(W$o6<^LCUJp4bvoR!V|6Pw&N8n(U^w&<nz6*_l#hxM7;QN|HB!JP#R`=XerE}u^Ancbp|udW+HM`#FPwOImf;JYogpEyHVJ8S{N?j~ySbRw6ibj4r&eLM<qUgVwap@`TT(<f1AokZaMT`pZIP9l!IO!WHW!7HPH42m%DT~79eK?s2jgBp=M'
'I4Gun$QNaFGH@6z)q5p+7=4DIrDkqIIh=i7z#pbu0`4N(KmFDZnAMO<serPWhQ4<a9{|ne{ekk=&0Xq0zP3_U*w!#HDm$+k=aTm08XQ$rFbzb1?0lWxx<DT*=otTHhjvW?0)m1L+%0pwPt|vBqL^MPHms@JyB#-`(nKGqw#eL3W#)H}-_Cc7l(KGqI)c^|agz@;*TDSu'
'Iy%*CXH;@^vF3QhE?)(+_-il$qA&fMmG4c%v3Kf0$LBvJh<j|_ew_Mo&GR%jpl~S6%K<jo5375amCdBqbrc~8?fI?qhc8&Ly;fxqKd9I<P2?y8sYb-@V&Mc&B>N$K2a@IFXuTLEp20Ug%%kL$NAFio&Gp;G3=1=-HX>Hf*k{x2)l)}eIogaG>DxVb;?7_6A>eUw?p*EX'
'wol8jWiQ=miZOU2crT%<yPF==b{lnsmbt(k2XgC2&7s;PL!#BxKfHJEEV+IDz?xCHQGQDk=_!mXE3U`Yw-4P`H%#-K&&l(nJvUAqauDg_-Y>2LZOSl-3$t+ItiyU-G?fzA5I_BX*ZY?gH6mKyc{&WiVQH0cn#I~URQRf^hiX)}$0qNGkW?BNSasj@r20v$3hJ~Dzl%7|'
'zyCs$(|5?HZ67M%j_7dLHj2y?cG-X1+e}XYEp|uIzO&mXA@ni^E<AQ=HvL=u{RnMD7jQV@pi9oo^y*Yod>4FV$q~~sNH7%2{|iu;@eo<|V@v>3>Y1IvjK$mnAfAiM26T>rU$a=~Y1XGZVBu;#?cKib5g>Dg6?rJ@o6i(Et*Kn?VocwcLtG+<Rwz$+uF@=7wP9e@gbmxo'
'usj1UT}qVYI>kWL8rRaVzpJ{Q<N^#eSudlTaRetaKz!}-4FisetHq-8eC<5lDFzsB7@K7mk6Qka?b20Dx|{X;i}%bqqngXheB3KSXH0}|cik^CD`S+&U1VA?w>_I?IPiLmY{<{ay-gsSvy8awR;E1DdVgM&?`F}05N!xj8qnJIrO`JZA4gNur;Yp#YT1F2-!d#gG9=g5'
'Rjh0JXeP89NtU8OA0oN=St6X0L@d3jZ~dH{RbckJzxwjZNVavEMY8*eVZjguhN(u7_0cTxy?p?z^%J6LIr%7e#gMgEjXs65>cwQcDqC>uu)iLW9(f_={0I%3k8bdE*+KAJrXb3*Ba=D?^Ot8%5S<&)!N+(%@dY0~qivI$Q&%J3HM8@KQ1DYLW}&GtT)omR-v+@^GFh*z'
'Y#}5<X{?>$GgV;R8Cc|r7KtY?7)AQ*GIpep)tmqZsde^`#bdE^K4#gu5d*A~^lleIZbx;1e{fj6CP4sN7LkirY^{=Nz~5|n%75iSU3WLHaQpr(sZ5yizCJP>!144wgqT@ll6A$DR~^te#@Qs$`82Uw3U#`V!4H{UI-e&onFL7aH`4~q@%WSCJD1ZBlGVDo+YHFlepp&n'
'2W&?SQ9Gfef;g*Foh8cAUM7q{b<I!(ayNdlnDmW4m64JT>)-e^N3glR!!B^G&1bZZ&u5_`en~;J%?Aimy()#eKA>w@jf*|?8pX=0$NaJ@s_l?3Jngm;p+kEIpb;!u44M~m`|ISXNgCsL2%|l~_C2zx$}eI-|Dl-t5exZoiNy+cc!KRPO_s>5erwU(z@R(W#ZT)9b+$n}'
'Aqh~?2s~jgo^kM7+{z!NY-s=ijriJpV;c{YRph>QJbQ7+s*`HN|Af29gghG3!X_naNo?mo5InXj37t<6-HP#KL@ItL(bqid?A$x~FP61Z*7y=iYdxFQ2|Znk6valxoQtDc`%VCFP{o_wEqw0N#s4DaC}Z&m^><;d?a62$Rlpvz3|3_fuUqt;J&qxr=n)5FRSHeWFTlw?'
'Zuaa}7Sr9&Z%DuriP&2B+Cmckd`El7JPE*X<dd3u?jT*k(qhf}Q*23XxPTD<?UzBbwB?JV*;1o@UD-uXIQ_w#EK}f;^zqbS>RtPN?exE1uBXoc?%w#ci=I$g*|#?#kj)p8yF(2jG2~)O1oEat_wn2SR569E)HZ(bpMrz$1qIOl&i_Cpr5U}Nn^OvOA+D#gkL4`g+519%'
'{o&Nga})mdn-P_U#1CPr<tL1Ty=M-TC*kt?Id7h5g#qm@zN$wuwGBN~{p-ZzyOAT@1bcMQ8=|Rl_?OGRQWd{_`|u)Emh7|3?xqsIc2nC-F<4$uwFROiAch8tXBw<#j>-mlY_-FCSt*cOXME10UbP`$RxjF1l>`C3(gt~tl!V0BcchySW$sJvp63d&!pB*~aEo9HLuQ_s'
'Dah98&j@*mAe+f@b)hb38Iq+nw<hr?bTl?{Jax;kx6iz3AuxnEx~JKN4<_)17Ah{U-Z5PAk(&z)U4?CwiDubLpR+8$!Yg1=SlcUjRySLccU`P)qeIh5SW6ElvNodYG7S9=a{|CHMhf0uuIpfSoncvV;>L#d4BU@m*<z4&Pm9vb1@yGC8Kc+9j*SkP*^b*{5|A8<fcF^$'
'k{<3!l@$`oHF^v1@7t5OcsK}PaG^_I1?jz%81G*@(l9)Bh|oRe1No)@YvOF0J<VxE&_WfKXHN*OY8(w3D0Ma9SR3F6$Brjd`7e0Fvml|c6$g_|8CAFY!WK^nWyO>>R`hXLBS2I%LEt?`WrK~ojDNq(*X)(l{U?4wn^Uq_jSYTIJh$mj&+FZ08Yz=J*&o-IT#5jDF>yp('
'X!Wmi7Z*}7gnEXCy_$MS&kxOa;%i@Y+CPrP8FI?PBv7H<nh`ZqPa&tWhRiY9JG**Phi@OWmVeec3cqdffOPl|^wLqATZKPw+8G9gzIr)y$W!Z$9{$<#ny1)N!e^^1p&y{Mfg0}@z`h0*1m{4ZsoQm{Cvi8K#)c<SB`_O?aTcp`ju3;2V3DBA?g?FA_I%^6q#A44z@^&>'
'lXk4tFO8KS#Mbq|3{QlDUTl>NGZ!2HGA)@bg-?#6X>guRoO$5r4G^d*Q@~O50xm^;{VAXzxKEczPg{zqv55s$TLcGwJ&hzt)WaKE;EX@9HYp2l-bkz&F5|*2`1_G$0%oV8j8?rW`q!`GOfk%8?JrTBn9XXJBLG#_7_CCZo`B&r|CC`0OPP3`-NxcxDrlIjSqDL5%*m+R'
'Q(}m4i~|~yE=qv0F$mHfF0Wpn))46P@%heR!r}C3&<QIIt^Yp7B7LutMK)rjr*`$f;c=kF?Qw%N@y6UUd^NIAg?XDzhpp5$*FoA(H%Pf58rrm3VeheTEP=AB7d>P>szcHp!2Vraf=tWpJjaWO9-CHH)2_#|^-?cM>O0!M%!acA;6dBiDmu291Eo$>TqSo!HY5Bc4)QRy'
'QRPo8K*^@7A?8_E&?!qyL7c??C0-D{w5oKY8B4cic|~DUBStm3G}gy3o74)A1+C{?De)&@r0-M;L1X)koJEL$QjnYzZ|Hc-d)yEypwVjal7-~8&I2e9wjn7Kj&UD{xRaRO%jV~Jr}#Ie#$CNt5GHnPv?@TFV9=FRr|CNhY7Bt@Of<Rh3}yjp`?4D6`GL<SNVd}ZnQ!?q'
'gBg{dcF!}HU8a3RUvk&0dCk**54o)4KZb8z8^#8rXPV3v#i`6F#Y77o<MT~hbF~aCncd5F%vS&u!B?e>aPkgZ7o1KmdM7L0TU=74_6W!^fXzMsiQ*`%oOmGd!P%P8<*?)Um*%XABeipl&GSLRB*(WN4s~U$=QzvxD;2N$%D5!*3ga+4*eQoVF}Db?Bvi}G27!D6Dl3__'
'b8c|T!0i)Q1A8V>MSxRx`mFEE1NkuB|1FPi<J}B+?4Rg}Tcz8c-ThfUOngxT60+Ibat2G7t{aN=o44`!!xq{~QQY7grLcQV2ihd<YT$GO4sqd94iX)@x|7YK!k{olK26#{EPcIFZXN_~S_5dwSX}7n`V-DA=Joe(CL)#zk%<6aKrfVkS-_XUMTx%DsvRHozv*$m44LNM'
'GWy$sE_^(^PTI*5Kc9x3{3EkF?&x)F#nL}VW}TNt3s9gygQgdV!I8c`-YSHPjEPkX4imVw{C80y6IvU%O%X%q^4U+_VL@zqE)SB_N9tnJzcG7~5jMeTw{ZOc#0p3YS<r{sI$_HgIyqw6J{6_J%6w8WgYk_<S8u>P?Ipz_#^4F$Ug{LrX4SV)-7?lt2L_NcF4mzqxf*GX'
'W_u55h!OJ^)OPkeY3X)OL1}h{%~H#mhakzmFH*_f=)y1Ke1Qgx`w<fanli>aO@{<e(^?xwHchFTs=NQ$ss|ssuxij+NCZ-jk?>-P7@}7G(-p_Slz|)p=64q}zTPV*X>!@gDtnF@-Qt9L0+Bo?Ibr8jP;9}!6lsfJ2;)`*MgQE?{5A5!;mYT0#R3YKHjkn)838ZfX4cg`'
'Yn#qsSG*h;jlwL2dD6+VP7Vbq%9x3qX+@D7nUC*sk7Cct%s$!hU*|jOz<7iC+U(%_%_?nIpU~H}#a!D`t|OtH?;p_PRzBStGh9uOT(ZGiS`$eLFM0Nc!BM1T)k%e#$>yCWGW3=Qa5R=H?Nas$;Q0spP?g+;w@tGv*9TcsWL&2}O8r?C6JB&s=C)o}POF6Y3bQYI3Tz&>'
'6e!ezE##RxvxHjR1!0(T+^2IMnh`~J)@w2qn6vnFxJ2`GCw7=GG18$qs=r3n6W_;ac@oawe~bS2w*CBCvU+lp{@C~vXG|nftm8S#h-*16NzrwLvmm8P@yAgK6T6O$hN5M*ifCA#-vi*XSt}0uK6BjedrI45P10VWj3%n2`Pxs5D0FOLHBwHZ4!Nb!*D(~5G+TyukhIEu'
'Rj|59)or+>AuAbPY$fEl%CzpJVio8J%lEC@lq?2hfo>f{!dBZ<2b79CYW*Fxf|DgzaSX2*5cd<YK=xeu?A3qb&)TkSqv?@`aF#>$18~L<lBU>#u?k#=V3z$%CVcCvFf<sk*BZ=mN8EpDQPCwb=Jfl=j%A(Fr6`VZa3mN_crj$24|Fml>n$6@FF4rVeIj|)n(m^SFzLPV'
'j^hie!k!8I=HE;-pEKufhpi735!xSRw+xt_wN9;7MIh_yh1*i6IBn+e2ixOncJnpK3GwtijDg@P=*UDElSf>A4>$K&)~fD9vEdq_RA`>(aqJd8=34?izVMxpeJ~-oPzQD+m{F67OPm86fkiKlggGau;SKlr>bWtH8@xx)65TMpH8s6qkA<@`*k=q}P#^cfn?wc3s&0!d'
'8^!ixV?-9RD9GKAfKt34;~TLw($iHAR<+zlfaMKdjA+n6v^-M?;{K3<+80l}JIy;mE+)mSMCR3^dwyixk3mf!FvEoDZOdefCb7v2c`qZ&F}Yj?T5l+5S+en7sD@|Wp*;BLZv%1AViIFOejGYVCXh}TV@)Ebfyf1<oP({cU4QNPzR&yiR7>2$az7ICqXxf#66a}`Zv&#o'
'xo};d6NEejG~oO=K<`v#1)<ni358lzV6JLpHi$Si-ik-dvN|j3j!o5xz<bnMf<-J5-dm;$gMp9<Rqmg<2B;|<`mJT>6ox(+RwS078_3=dE`N}l(E<)rg8BkhA9vCdHlsZB^088;(+!Q}WE^3nW9i}q#{PojVZw43Q}cCkj%r1<MB{)-HH#rEV-4$Uvy)#{P%9ik@!n2R'
'&+xAT`%?@3$y#iJVD>FV<i%oBPwLsuu!r;gr*5lP<U<}vYC?{c^7_G(I%ZM-C+@1oFC_V#<IXB3cz`f0hSDu9MTa#W=Y|Xtkcj{9o2=FOAd0J<HSxA6<UZW5RQH<}#{{P!5K%R-fDLX{7F8p-pgE|X#ExX&H3=q(wAc8{L{R2BSz<RkF>pa%Haxnf=V1gFPF5-xbg*Al'
'iV8ia1Pffzi`8#cfYbj4Ww*!~57FyqH00Qft&j_fHfYS0?I(AawnxGY0{LzkpGFwk{n{Hi&5|v6BK!_>aY+t|+_`be{a0KJ9(1*;8WwP2S!uyp<M>eXG!_^4D&FxShELWEk(vG27r&2qnF(BJ+Dmm{w6F@L4vOh>1)2^VY#Sas6paRT1l?<lKBmYa*Za_yJ!9eC(c+Va'
'^N_bx);r1#HAE<!vos*Wa6<d@V@|m?8T1E9lOZdp3B=<>OE67Y#FOI3>Z}ZbaUu@c*UEZIH?!G@4nqEulWCr}lT;2sQEIwNk%76Pl%oz|bHi2G&SL^c-fvwi=Jil35oCusCRfyAn;n8YY~P@A$u5ue&HxNyvku*|v?)?;{v~3;^0U02zyX$Sb5bTrbC<SI_~ca5&xd{-'
'bzq~T10sm0C1BFsf6fEibpF+obV)F*sasuRWjO-!R2_Q0W38&xU2RVDA~8brUZLAlK4a*eP73rHS_7RP>LO7Ka*-m%9elQ-^Z}E}?C4#5xI>iCAUqdGi;jRHLpMH_0tD=a8I|CYP~&IrOp&`M{~FR92Jt4H2diwO$5LWH(p^C6Sk9rgD{-x<mWr5Bj-)R{@waAivIK1d'
'bSR2ZB-A$nkH?}KcB!?s$(WxcXFR`(;NY#+wp9Y0%~RCZYW~PdEndo)h6-7k=eLtwE@J%Z?d(NZJa}<wFYpw;S_D71_DW<#Jf?1D<CnOIq>wnK7zcB7^46i`Z{Fd_hi`_P9<nSVA0J}ZRyX*yC?ed>teQ~X)Zct=h>?G{)Dy5T9^b2cjcRLrddMkFvx96AgC;|t#W^TY'
'C&pIzm1Njt!AK&j8dj|XugU<9#fM&q2LdBBYy2dk9A{gzIm5)T2FOQ>q~e=a)IRvbXS`pedSE&M)_d~HbA3R+HKu$_u?5%@1tg`7s~u_4iMi9^r62Q3KTvDPoI2xfcJf*D2H{S&U!w*_mr7LO13T>d{{F9%r!6>4Xw_e4Iy!K@uXqsF_1;spnRxlh7v7E-P(L#Yd)nC|'
'9#)F@iu&^r>o?#F1up;W%CH6Vn~BRHcH+DZhhTg0{s#+4-wY&nl?Or%tb3_4R|sGl%@#$hr&Erll`x%jPmx5mQ>rZ|2l=&K_E!?baAt363xJyX)}v<&t)<p(DTm96&xrmnh3WUbg}5dk67>l!)~_A<j-=4-8fuVJK6iJik){RQKBaX)iF7FOxKYr{a4@(jA~`mrWan-%'
'mYRuASovetkpkh>f&ytlBA_O8sv_?Ig9e2<P|h;%x<RF?#*o@=j!9%7$=ec|jMjR7;Q;bq9DnE;#;HBHK~rQ%p^S7uN>s^p%wYrwNMSxBFx$4h8|us>b0fi3A>feaGy2?rt?e_|UhcE~H~Dx6`c%M6M$ljYn(Vt2BR6j6gwG!|<U?=qq3BT_B|C$|cZFjA%od?A$!lp?'
'%W&wxI!f^#nNYqf#H=!Q!kKrW1ugu|rzW(6X3k2|TM8QQj6S~VtpJ8dtA3v%8vXcF@HF&gg3~8QFZpw8%kYf76;jdWw`0w3ET7Tgq{rXn>(xs($E%EX<zZ9li5jOpqFx~n@ZfG`B`B+h)c0-$h?)wz(0i9V78^Etop+R=DHp)QL4mfzWp16^%`v~yU4ABJ1JKcWLY_cb'
'_n#%Z7!WFK|3UKe)ftRVP;9wr_Xio`a_jl+Yk5gLi!AIF=SFo1m08*r)^HKY))gHwZ~$U|O67B#9E`PUD$y|zi<O4)S+n#95eEYFLcTtySZSW<_0mTG{{+p1OSYkqSWKY2wM{W})*Ph`<=+QPD?XrlLsww=F~p>h>mf)6C^6W*zC#mew{VXkKG58s8!3vhQyPf2Af@rh'
'&%TTZVlG>u417~Sko=6)&I~l;r}}R#S;?;CZOxW(Js8}{gM`J%(SOk5;+9L<<ZMQ3ws{hN1X8%&BAN!C01_oa|L2=lWLU|$BheNXgfdwVd|G=*i;QeX@g3{?H*;bPX@faH?LP70=~gg&QmQh2z<G*z%}aG3O6A321ctUMU(X&%UEb#o6mNT_5q}>DwIA+n<fTCQwex|k'
'UUWe<z}=syXX&A%iTy*`0~12lr`d`eM%PRu`A*Qw1yE_Ouf6RxIuqVx!S+=M8Ed52R1%NRIh$t{HjtHW{(mx7l^pvrRq#KP_fz0!?}4l4mrlN0iPnd~mcI{}`guB`7WS;4)^jK%qqLP>q9;S`*Z>|lb8W>flSQHGFbr_He_sn&Y~xUKOryW)oO9X$UB<;SXeP;hUJ6jt'
'Rvt)YI={`7G6ciRk?4XIL?SB5D_(uP6^SkdU5n{0kWFxr+dC3@s!TB;54#Hjn!Ph!lX>26-<FjU&?qTLa?$!&G_Z0G<e<^`(A6!W^sFT?12FV5(rvd&(`E|l;!Mk?i2C0fpaH9VSI^M=M<Gb<vbI=Uo1pccf*Z8ydu!o8K?R3>G10fO?c(QmWFpwjzg*cl?~4{OOF*#?'
'+(*S`3W+^fnMf%#T{0R%J4E8vwnGBd>CmENX$4+SGyWDqDP2{>&vmFTEmHjy_=6=9f;sH`IxAJ`jN;7E01m;n|I$>tlPCW6Y!3kQP$*mxXT^N|I?x%YEsr`syCA`{XG@4xEBC)tA9rLm@(NeRua>36;t=y-erEe1GrXUfdi8;TU-K@$q1l09g&~}oG7N=~rsIBf!97P&'
'To)Zd&zQa0&M_bzx>)0>CC{yUv)14N3j~(rM3&>llL-jnFI8@!u6vKOnffa9ID-;cyEOeE@w(ooD^wc8*{S<E9_daXkNSJ?P*LEZ>Jd1!@kZL&kAz8W)X*TlGbQuY2o^U_U_mio-&I{Cbd+0_{VX$4I}VCQIBY+&FTNQ3cbWavi&l<`TJo3*v$o6oVO$&O2qQ6HUhJ7('
'))I&5VHvTcu?Kx<%$bJ^C5N%r2w~=}2<!03lj^W=C2~Ls9+;vU?&JQ{KdRH!u<|}}n)J<aIN1xVs3HbH{pOH^=CZ2qm6V&(@IJGLGD={&3fS)I;VkW<O-<GgpvI%uq<4uc84Xmos5RPJi>4AXGaD*CEbt(7i57mL-0lRQ4wc>Fmj#zS4@y7YDdbsE4Q6E>LWC8JxIR9F'
'P$F8f7G!uI%&Izz?K$LCw}GLT^u={nC>2X44i{~Y&I?#4#UuZ)?nS!Fu7K*Bu1M};y68WO0lTSVedosV=aeq^JjJW-l@Qc1dDk{s%w+S|OEq4wp_-FMGTT}G{;njv`HgkF?>IODZS8a_YJdbiH+sgqGk;R-eFgeOHBCmRDuJk)Wx)_@U!d<xKB~Ol`>M!$$;fAcL>ix>'
'P_9{=jQ&+8Y%-Ulv2bWkT;%I40xcokmDHY1`#P%<ir+##tG-^w7;%q&5^8doqft?}oD+&vEx@7);Higs87=mKW=b|!^oo$z?G#$Sp(V971J=}$6ydJ7lv;@91<)#!v5lsU>w8xsTAVZ@)Z$G<vZ^CRMt}v6<VDXM@WOW^woOL6epp%RIt!vSo$<^)Jmnr?k-R)L!nd(s'
'<Pk9exm^1ErCGh8_?>`@Er0u#kC6>wD6IYvGPk8m=?>5_{0j*HD_*FezJeu5+`mk|4{R-w?>DXB0Xb`HU0cRRatd|A&Vc)a>7&jUb!I0Q54`8#!5P3na!fuuJ2AjO?&h;N`X-qq4+t~<oKOFIcZ%Xzi6?Vgm2pe8_u-2R{H<YT09R}Bri+$DJcldy&6gCZxJm)6ryOBt'
'BevF^TS=(z(SBmk@@xJ_JHkx)KRvpij=xpO>ntEcDnVp0%IN0!{P}#$)Vyjv9&b0a^^~iQ?atQ}r~$<;<<kQ)rRB0678BYfWI|L7{|wtoKAL0{i+sv??<N@Hn>WteWL)f=7L97_uPUN(Q!?N6?7npF-(Udx6|lva{$&gu5+`~tS7XZ*`mHzs0Bx)$@tf9NqnSF4U1&4y'
'ksRbyo#wH}3sDHIbjqj{!rLFHFGnI#i}1BW7bzb<bC&%Tcs{T7>c0HR=l#4gDYk$I*pMOjx3f}n{Dpaky%K{Log={5+8Jqu&zzze#lj$7la`ba_Ft9RK=r{<oKx2mJ=02#hW%o|e<@5xUX%nEImo|WO)Q;Wy%_#s%}%L3u71P@zj$ojrPN#4_`I`xa^_$)Xp9Vd;C-)s'
'S0GO^hke?{D^<u(a(|%WVILTuV*lK;fZgwy?USNb$|!d_ER-8NTk*hjcFSIqo(NX1rKlojFu~47Zm%E#*(uf5`%$|o_;nD+7;zG4d|T8A6XR|VrxrRB8`v>6jLA9!D~^E?5+iW2on`5gq30K4gZn`2#1m+9!gJy-?zSD^1yzDweL(><tFfia@-M}S48Q#_Zu9A0;l#zN'
'fAlKdI?MgWcVmhgXNp#_fT=z=eZ)l}!+XTo;?pM9dwl9`vOVKv$cVl}c{e1({-Cn2OTt$!#OplcvI*U{WNreVq6Fb47fzjWHn9E$>weU93JKXaSZVo;cVq#H+GG6@7sy`G*l+p1CRlj$=*SgV`MB_DEtlUl2I_Q5U=@xmtDCKITc9ANgd@}AyOZXLU@&0|fE%Md9h9dm'
'OpU_j@=3Nh`js#Kllr~-SfsGwg`N11%2>|_iE0Q6r(7sRzO&-EZqmG-oZas!JR$%8cQoQm-)^WcF^mG*gNcR+`9sYFvn!%g$W#DrTo{Dk47ZI{JM)#w3*3l<JsOqJpOR<n>CCi!HDiY&{g3)u#F3sKwFzV2St__omrIiPP9T9MoAPZqci2Rf{Sy2RvEEa5xn(vmGvhLl'
'fRXI>;<IwIsz`06bjUTlr?3v8bX2+RWQOZ%KCupx+ENkQnDbacgSJDYEG36*{KBh;u5)rW1%BSrS0Bg)iIp{#T3eeCvdhr}m&k3n{jF{NM@XGLG;R!Gp_NmQK-D~X5u<B81uDKp%w5x6!FqN?Bh9a{i0Zmj*leV6rz!#V352m2FEp~d8iHU3!c~tITjy)&+X~rbm%mo)'
'B4!`}>`&5C3g`~j{yY4<W0`llWuK(QBfnVH<4OX5(RZ)`$~@`e*Kolmx08GY-8q$l46if*{m(=6SFxK+09K>8y!aH46kn<_{<$9SW)l>0*ZOchaX=jGmJ^3sv4@N7Dsea@w%IUPFRKWbyuW$eySzYDTZU>c#JXuEOzqAW%(<-y1TG^{zE&<0K8wk>{NO8ct-bmL9at}-'
's>$#w&<?^tRjz6zBi?|E)!I}}rWU})G+AaRj}fIM8m_})!g@8$mZJ|Y8>e#!N2^^oo-=x-FIjNaGqC2kqRvhqQYiFI>;JD-U%=0w{b<31kDqdlPgWn(mxcWLtSl*3lHHFvyhGmu0`j69s~^`W{W<z+-sEDUQ4QS~K8&O?_Be=C6zb*K_0;KUthTedTkS%Uo{en43BLxd'
'p(Oc5^ut#I15Tg{f-)X7e>$$HSVGmYp!6r>Z%fy{J<qCRKd+c^IM%#ArZ$74Q>LXHZ%oI4S{oxD!l(1vn07FBGj;m7p%>owrz!f(98dFgA$AlYfeCANg@I$jAn#4ncR?$KG`x6krflA_RY1-CwW-)#1_q;BW#c^G^L``VU^KhCc$B4Q&MM$9VF<sy^cRx4>~8|3fj8Aw'
'@;g0C#%ex07DHG!$C!q@?jiz$NT1e20l!9S*lBI)=b_%yRRCI#QKc(4Z|3I;F4&9p`{4#frJhJ{eYbwG7b+iJK8+FU3j0UwH|P8CGNglqMu@tM>sG3-04mw3LWbq`_NMMs4h@WK5lhwfpLf^?w45}La<9QJ6{<_D8`83orJIBe+cHFbHwv$~Gmow$?5^PWO(M_irOo0}'
'CS_R(f7Z`-AC7}WFQN+-?9JWeR!fPSXO#Yl$aTdFVcHSIu<PVuK=l{S3A*dcifhEf6PLIdlP)=XQ*cFM@FGlH*H7Dspt;j}w~*n|x(>IttaKV_LTtEq(|93|{BzQdCDnN4S<?o<7f>jjq-Y*KS!;|EX%|pKd=BMX47Y&0CCw?I34Iv>D&5OYXM9k1Lc#WH*TvYnxtsF+'
'pm(;xr^i~F>*&j>8J_+qU#DI<R=Khbt*jj>IDADMEqcNRX)%jC;oqvU__gf&6wYn?h3a%js!4%u|ARHxx4jnT0Bww6g|D6ZDSF{Eg<kyv#sck2?0GY=rQb@Vnj}wzjP%uM5s1Z6PRQQcw>CmR$-tG9V-B*!y$RLs0`JLA{@3(l8%z@uI7kvD2aFLiZoC(fAedw=I1}Mz'
')4FArEg^}HrMx#K5Heoql`tzfBEPD3ac~-7>q&0IO&~KzSKcsfXRqji0ky`wOsBmT&`G;5;yrmc0BCOcH6MDRo-M$S@=I-giFIDJZNT4ISHu?D4EI{<&u-HVPRePT_Cz4B70l^f$HI5iaK(GUv9gFKle$UJBQK|#<Iv!KM^@QE@qW#cG3Wq{><9Nd{#{wlyN3}RVs9o|'
'3P&HHv=Sz}Bfe+59X-2H0ypGoqpn4>iVHtM27iz?eWtExsNt)Iii*t6S17F^DE9zh)XhMAYFvJyr+!qPfd@4`{lfvcBldo*F-kPn)JRB9)=T+~kP}msv{W+ZTh2b>P;^E7(=Er$+O1G>JfLGf7zjKQv~+2u`3Xb3xoJH$L0hrsm8T|)D@$5xf>PQ7c8W_=BCD`Herv#J'
'`P)hchJ+MAB&PN<^e6d~r|L2@DJ|OnsA++Y%ZeOj_QI@!pMC&2;a(7XG<CCOLFv!DGnv$A2^$~7L0uil{j!3dn&`DsBfmmiX(Abcg(G19F-d8K^yxh80~@$Dsq(7JIBcR2Bb1SOUuibkLVxSv%cTHGkf;3;KM(`uzPn%zWztZBx_v@)hVwT>0`o(74SHO>(40(lB4YtS'
'a5+UsP-Q%dm*mbhM+<#=FnlzYaF9;DD_&^rgJYyfm_$z0dm}$K(2lqTBIra3K@vy}`dmoi=#Tl49d?k#d|m%buDjG)FZV$@4gLE(;xBcw0;T@#9O~9B_`8P?FDvM<0*EZwtGg$yK|FoyDZqP{78*~dklX*4nzu(X6_ck!zAp;Z`y-QE%AQu|fngR;sAf-Kf*HUBRXm3i'
'-P*Y27t!z_h;vCAn?;Gs8mWoQDSPSr1rRUFOIV5seM>X8f@KydR1Vih%*{7jbtkk*HL<0$7e`s28-c45Wq;~j<h7U(BBs<TB~PTBFL0KBto(gGYP$ZAiG|yfZd<s;^vHG&&5Z^p7~X}yn&<e!4`4fBj~oYuv!Jor!@Ob<SVpBfqD1fJS~!!RU4#C5%s1cs&st@Qa9z-<'
'96No>s~7+aF2A#ACM`)oMSyt2toar`=l`72B>Tg(h+@Tmp7R{q?*0^XHuZ}yNYqa`_LU9^;ll(QcWElXv=e<Wqxj&)_okT54Al8gV1@Re+7>Nu;08BFe`EFp00+ytI%qt|sPKN<8`TVB`&|e94p}vj4H}oA?SNK7QY#p^TYQiQDrcxA<DYu8vU;4shECR}qi);qwKT`9'
'qa8udT-eAwKo60Iub^S1eeguWPnN@OGz+23`j^_@Dtg2gw6*mZo1}PMK;$$p#NlAGHg%)d=_^0STMqvr>enG7>E`?QKv$npFLSLazF3DnM((4B2l)na)l!q`+{%?{sA@_k1l5pW7e$y-$=~|zCFo6I<hps2%-*H^ata&}i)k-k?_!ESuMv|^0fQsslj{QYnxuw~cBM<>'
'5|Tk5fW7XcHUKqynqWQy$hkdSK<d=oE(d{P2C&Rln*KW4N`$-SS|2&5dO83y3Mi=4-1$HbPJdE}=?GjjLxbV+qdlLQ<!6yfh%yx`F5&2v3^F45Gf43gfSD4IG(*~@MCjp9^@lW3i~{k)?k6C=C=yg42$JH?Lm5XHkOvx8Wi9m(b=2Fa=sWchgM(iT4-F;M9^PU0<$;Sm'
'B`L3W0!8cn8q9FS(Q7!&XLYB9aWs{WAX1Hy_*%HA1=?P2TY&%Vn*8TbXZxZW$F5ZHMW1$aig`BY$sgYc(fHbq3{7E)w%q6UQ(t(AoxZ<!VPSfIly@JYLrJ26p%2k9eS)EFR^@O)wN%qM%vEU+EX;yDEz{JkkaN!Zom#p;gKXwYEk&TdZ@h6FtfQp)GfHxPyrrA=ru5ZM'
'8G6C7u#SME{}R3#ayLaOnX{IZo!+%E#b){XW2x=Ivr)6Y9<-0Le?xNki?DjL8@pUBJjnL204am?wgckbxqK#oFUJ2Qa`c|HkO+Q~_D*)((&WK%-!5Bm7W699M6pBkY*(au2DIdKZbm~030~62l!0H6*e7DzJOXMcf@u(j*8i+4)}#BMq-5)qEG*lF<9rM=Un!7^YB<ZO'
'1*U17+`))}H`?weS-ZlI<qKiUFo9W+$f^PET*b}gU(z(0Z%pa35?(xHG3O;;vtWEUGRCzkwJ6mY(lr$(5Gq*N7(~H~nx;VImq{mcScu7Fs|#Kc$Wj|Cye&;OZvd4-v4X4qWb#@HsS>_qhruiWB}M(O`)BHCM;j4v>C=u%Y8lXZl}tVeSO|ET*345IWY{i7xU$_5aR)eO'
'T~cAp_vQM$%GqKfD|m-d7pH&1e0aWd4?A^i`5s$7K}UF9;`c##3adjn>FN&0Ppl6lBi-U|TYQzy%Pj9|q4m0bZYiPvd~(^5RHvUeMcSf3f4o^QjamW|1p&a0?mZew+ZOxxHk^p;7yihGLUKg1z=jp2>(Mu1NBf^IG=v2!J3<)^lQrI*m7+fILKr(t_ZXk*%-^10d{p)x'
'sz%UCdd}MNuNl_-Co-Sj8kAfLq<pRRRr#2fFHv)hT!b&nn`G}4a7`{>*7z31+TTU(@uq^5Yc3}3Kr@)3k+3>jX&<}kcV|Ue_*LtISmF_#@PpX%pnFHHmw9^A#nT!0q#Xmk^drQab4SxquEGR2H9+@59BzNlKZ$L{+-)iQP!6NkmgIh(>hJn_tcY=AOns%7uubEE!T;pF'
'9n7u3Wpi41Z=bP7%tY^&#C?!DZ5`x-f(jwjw!lwK9tn1`vSXJ@b^Pt!%L{K!uYOJP`2&2&rR@D*rV43U;~gr8TGcJrv458*m5Vslx{MBJi6X^`#c+iScUwA+mVgxKq(of)9eb&@9OmQI`Mmt8<8M^W-@#YNqdbZ~Im+9~U^-|4-9A2sIFMhXGgp=2LBdme!G-kaSm?A>'
'VDoA++Cl<RB;ntQ)WU)K9qzNM42OU_|Gs)G8ZOwd<j1%kl)0hQz;hOAl5!3CG623;C<O)NLZ|iHAD97Dk%>NW+)#w05$82$HuMjEXGf417)(tq{`DUI7LKtXI?v_Ol991Ze>WQjady5okv}!?ycRk(orvHTCE)urJg{x|1=6GctoG04$o;>xqaM}8Zf`MN)g~)~MACDC'
'^RZC~-e?_?n+oA$r@6@w98H9#E2Q^iXaGK#4uth!$>{Ap@>n(Z%#qG=RUs%0B)^vF{(c&fMOcRJK`DYOxq+kC^;iCDiY^R4i|DVoKQ@SJ%3=+6{}NBtL?q9@kkzzLjilF-W?RR~J}z*xPK{s}f+t7aIQc*8!iU!-nGc-6IGu1K?T#Uw2Y7-l%x`%wM%$mw{tFXcATUz('
'Q*zB>^`B^ktbdRhs<F``Pzx;=h%b!pj@vc?oULz6JWW)1;Id9`<?GQ`i1zSIh)t~!NwFx<5zzab68e42WR)-KTyz$79Qc4(eh3;ExGST!`5jolDZ41%$13dCk<cW16LbujL{~`23RfhOPrJ&em+}5XJ#jwJY4;ijoSjd{|5_{(pzx6V;9C{%e-1{N1pw5+t5cRvVr|D7'
';&<3zz<@ZFmnRAWLpiUJAuz=9ANRGXGYCvQ_Jj`Mt|JBj1ZZ@_=Gc~;6c<OWcY-h@5aGqVCLDBio150F7~}&Od(%n!JoXz;<NP-i1S?N<+C(V+G!&OCyhnOPH{h|nHYSIfKhXKUtNc573o(`Z)@+S23Q0rCjtj7o5*T!|TtP?U_Sp`Y{K8N;%!1reB3^=D7?Sbo2|aDf'
'vKMFVK%F;t7ItisL55oT7b<m$q<=Wo_Fx5<X=N=R8cKcA<gL|6Uvn2gp9*G0zR?#QOS_L*J|l=^&WMji4hi8VNY3txelQh{{vn_(e=yOCA$ombUOt325=oTRSB5^M(7>FjM8dZ<`^byGHUyDZw3Ivz5qBj{0<yKv>R0o;ItyUf?2$&rwF<RyXj0?gZAXF1jaF7NSu<-6'
'$7I<e9Eh}x6XgcaUB39(f3vE*Mki{In%IpP>xp+|UuvUoO^}<ps|nHXuJ@tt;yCtNgAuSf^85MH%-K-#L%kZxmUV`Zd+|N1!%*VOo|T@GinO5Bj955|tGItrq>7MN0)oj(m#uNd{hqfue}ly%?-O3Wm#Kw3<`9BclbEwAuQ=qLc1^Y`l{5t~R;E@jJ&m3J9~VPmz>M{i'
'&FzooI1~3Q6A<2}W0Ygb#i<>WAS0KWbQ0y&<fQu$8YA1b``Sl!phWQ1(1TxOW!>jQv1pH6%iC%`?GoYtasI22eqHWlAQ9yuy>`cR8o;8g2uXdBWcVc|kk%2eN()u=kCn>OW88D0(Q>&8kpfVl3r15Ji#c_FlnG^zL@3u}+&f&%T~(LRNv8#^0Hl7YkB`Fmw(umFvQ0Mf'
'(4cm}zcCy$gi*o)IYt;qS{H#AG)qG<)!`JsVOtp0#!_RzJq5**YRG^5%z1JetWTu9j7^kk8A(^X(64?xqKOteK)mrlnXvet0%ABp;ftUZEHn?c8whL{@d~2mruJPUDi-+ba?B<lOc+*CEEbI|7(XO>L>e+j;ZJ-%qwK*vB-K<K{>}}e{BaXk3_E>PPwMV66;~0A82zz@'
'JhY=`3}i%7ob$z6Jnh}6{X{0y2(;*zr6C}3yJ;R*I3;F@$(UKj&LRP5bxQ=PDJ7~p3ehd=!7y{coO@w^obQ+TURjRdeKc2ivPR?T^`Gbq)lptn=wHR+Og&9V9kXg-3&l=tSSo?%Z-Zmfq5<;pRN+qht)fNdwJt8`%Xsbthg{-cnigw=OkTU6D=Y{wpUeyX`63=jUNo$&'
'm2*IMq~YyVCAauDP@J^y@FM~9!9(kh=m41<N$Xp5GU4r^>>ubHz^?q0*KQN||0SfmN@bT=V)lZ%sLB7C9}@VH#aaInp-uclD?ec5xB}p0O-^poRuR3`$6yhR3bC?zO3Mp8mC@C~5!TS*Twld3-NSAr5FQe!Otbr&%;PyDK#+`)x5m`PAbFSa;5M-4I5?>j7W`3+u9E6i'
'v>M~si+21F1&zI<W&E&%{TNkZ)?6!*JTBow<ozE&4cj9E)B>HoAJ_<0NVVFw4urXvVhar*TXf5a4<|-f7TsdPrPHi_d!gO{Yl10h9rWEYG5gbJ``370V*MY6VN6b+b2G%->?$x=UZzeE`BLhrF0OUmvF3eOU2*QEjeQK)g5n)6iYh&%b@Q`JHug9PpCcL3?n~<U=ibg$'
'#7cB)ehI!nBB7m-Zo)M+66X_Zim)PRp2EwUcMlYn?jHi;(9154qsp=jZgkT6bFa!Au99LNU@Zu9+g1k-`-zWi0A0@`?x4%Pf<frMH)<ABN6gPhft7xQ^B{un4ebh+_40~ZaF2t15k_pXlghFgZJY6SbB&lv0UTKXd%~GD!Y389kfnL7U9$8dboF~7t|NgEIJ1#(kxMrK'
'qQaG<5els43oTpz=8qlPh3yL;g-A`)yD5rZ&n&x6G3pVG?uVHcVzv2^b^{8MbugdRHeaEf3<F`cmd>sOcg&XkJv7W*VA59KQ2iHHO*E9plbx+uzoc{*YZ3%Z`!l#Q;GN9S4N^ATdxC#d1>Pnz-clrYPe$nW9i}n!+14A4-nHZP!LXZ3DU1I~#rdk?>86RJvL@}jw#WrZ'
')f+uZvlcXrW?^qBrfoC%g0qVS8=&mUI_}<#6%B7zeE;xWda-`tKVj*ph{QC(Bes^o)VYaxhwkzhXt}Pn$b>BH`i4*EurPSL)bvxX$1QUQW-TlPl0Qi&bfx%#zO5Y`=0Oa1(;PGweeI)_ZJ-1ciKT@zy;ftkHK5_~=Nl>>oKS1T-&Nb^a7T^bJwA1wh$m;|Jt8;gNA>GW'
'SDFUMi!7MDYwX+&_?b8+vaYe@cIKNLOD#oVI`P;AyUsmL$(AjW%H>K>`;Ob=C8|!u-b;6ll%xyqOUlF6$sJdpPSxsXugeE9;XAiX?ocDpR6&m-N3oWS<5qHG4-AA%9Q;bxkG%CT--+M1$SYrDF-aAN3L7efo`=qZxI;4|B(fGA*e(UQJ=@Lys|9@Qs#Jf-<6^>{-x5C;'
't}EL@by&r#TZA-#-1e&LSUp-9;A@$Urqt>LF|F40eVF8oLF{Zv-UI_{qyDuE{)s^TfOGw@vA%sDwBec!v`#9(PvUL933K}kR0!+8Z8I+XRh5SS5{t13a2}nLOpWOZwkyRrw{9PpMrrqT|4Iw`1uink3qzHnrFpYhT%ALafT}!?6W%z_L-_<X<7_T!)Ov^EIsyUVVk3+S'
'M}I!ysLVoaF<(r#G*&aXtRNFOIzct&od=%XGwJvU^(gU>RMMJ1O2vEe5a<#**gm<T?lrL2Fz5eJ{)bn1DICIR`;wpYtne=2RpHz+74^yCbhzvkxV%p?GkF#3f}w(MJ|!<MuAbl4v%1K4^)$nqDs_Q#OfAFlVX~vUjGr)Z4TpbEJDC`vER@WtWiWL$f$Luhwh@0)3fAx#'
';ovf7nigh_pK_3lzb(qm-Ltzay?2E=LZZbe*{Va=!&D;t)#{j+VGPApq%~AgScY%l%vi}2cRG{qw(jC>gtJ^#L5|g*M!2?AZyvz3p^wT!5WiFy52$0#dOU{yZ>x5<KD=0%>R0PQBn9u(sDg^jKz@MRr4nR_1&av+6{S7KM0vP2@g%z87=d;s49*6&B?hlB0%+d4<h;*N'
'#vto3WXJkt9Kle6#Rv!PFBONFb2%B|#a67BVjRY|l1R2^RJGil`aUB4%BRJa49u}l#__w5Woo<EA9KQTE}JkA>9P`tOt~je=K0DPw5MXP8Hc&g!{Bl(^J0iwe&3dvrrg@S5MNivSGAF0mKVq9yyt=-9wV#^3L>M);$ieQ_q6<6Oa(ojpSd4Xx3ou-3_;Zr9des<lh%e<'
'IZ#)s2)zK*S{a~|$=moQ^g1c2XiZ!bYA%$qNw;yVzsTDX;#c2J+2k1TMeGKPd`>8e7N8Jc3hIF^KH#4*V|CLnKryPtIa6_PdynuY&xGxeMYwvObpnVx*j*AXCo;&8d*EM6$52m0|9ovCpS9Ws#3~M<OowKOZDkeyDjMnLS3^_Lx{QWmY6iVXZTUa%1*O}6vDyYYd3@($'
'5V9E57?~a$7`lR`p78{2gR%qeAJr<7V9ez$%rBo<8A^`P=Hx*b<n6W)ZD+AMY{NyV2tLwD%(}A_##`l5udQyk7=SoEEBu@9YM__9SqraukH-7Djx@KApo+MnyTxn1$mrPdt|&8gMor_TiXFw-`aau*Ei1(}nO7_hnK?xlt^qk&znUZHE#qRTo2R|k9{6~_La5V$**QAK'
'4LjwQ8g7;2nnBaEemi$V$51AWszu#)C9(8EXvrS;EZglq8h>y;M{kkjjPoK_c%(IksJ7|6*@e#U@L7nU1CA1RPW^Ki@1nS__m1$7W?=KAIN<*1YI+N#SICN3Nipfyb|@G{lmnhiIUL0CIXux*yoHR>pO}Hk%r%UfWmRQHL6KTyIWlq2!b?nI1m{18EyDY0@cQ-+JKIWW'
'hwkd&f9(92oSnVys!(o1hCmwz#C=X4+$y*@V-$e8#=38Krmj5ojrtPmJp|ntz!PW>-L&nWMIxZP3X--%-Bdw=-8<XoG>ml*#%7be^eD%>Zv!=mvPeHmif=7`8=e1kBvLC*4}G<eb1<Z@saQT`{0b@?qbFWO<?Ug65r6fGPEG0uj-`=+lUx4U!0y_oz?1|@!E34;dUG=n'
'oc_I7bp1JE_j_jpPkd3Yt8*mtgBp3Q@ko%`f2B|$I2N5>Lu(X5SBHs|5gAd*S;F`<xs$+IstV4<w8=bUKopJRpl9^TQ7)IF*!J#fXtL>ZZCI5CFT~DxvmGZ}v2HGMrNf_whU(1dL(=1h4+I*p^tka>hcfr>-UZt8zhMwW=-5H8>3;8ZREUBDBepWR6F3n9c2-hq7;7!i'
'K^f!JY&hkhyq!e>OsX7wd4QDT3jz<$P!gawBpTX=+mHOYd@}WMt}X}4U>TM#bVs%-mR?6g7xhK{jS82!l)&o%u)Xl1541Da4L~P)55az%*fd(5mueG}Ul7!`Y@C|TrUqsJyr5<+O)m@l)C4ag9nZzCjA4vT8U!f4vXP7h2lKQveKHmO>DLgovgY&m-aWEhIJ@VZc1U(u'
'HW0~$UdU61WBn@7M|9hgI+C*?))&4mb8_A^zVPiZY=?VDOsv`Sl0o>HPt8U0II=ibMNmhR#6iXe6S7ENUKb@s|Lk4ZfV0yVl?<6)m|*Jf+(xX4YM-?OiHTn0j#$N}8Ei}oi5)g3!MmpA=*MJbGH1Xm76p5l33-l&Qp<bIH!8MHg2Ahv7{EynH3B#8oa7%SrN4D<$*);^'
'N0@*{_imqPIk=&s;cJNTEYbJDJ3`V_VCMqcb=;}Wla_n%rJl+RR!6>Hdpq6JbFEZmSz~*N!0dHzO<Zx}rxrK0C(TvGhXCWF9oz7id%+pS=>}?xS@(XD3U5IS-7xvvb21Z6QTz#xGHb^L{>FGFab=Upp!Hodt_*I#i^~gt(gL}`FvNACpVKRh3Bor}#i)cD2-mLtO_Zj+'
'E{6olnhK52;7zn%GIe@<3RRc-tfDuLBZ0g}zC7G+AUm-EqH<uo7Doj@G_p4Hp1#YNR2x^)-Q=*%`d@s2dI3_jcEdjRgAnK7&n_T?82|0{A12&AK`KYB`fv{y>e!T*%Q`ahQIP@ALH`>dk&OV;`tfsMsZ~Hp`+!d}=o&KMA_zTp&LCu`dLvsivvh^B9~r!m@B&XKkWcUF'
'BC=J97NHkz=NN<lpaR`fo;###Z9bxRVjx0R4P8w%RHCSgpxxXR=`(hyS{1XTh6e^=L}hBE4bV5dUgV3A=m$6d@ysIg+uOko1A@g){!tVsG=kivyTp2<qevCb_Tivc@Fc_Er+nVaY1fGqe#9Um4%-{tNTOJUC>_S33~yZ|^b`bss$T!AYAMYKNAld@HmJ{mzgeuWK!&Oj'
')vYbRWMCiu-{*^{F8y5eVq_OQ<Pm$OI$F?To5c9#d7cR>r4y&98?J&GIIKsw?6ZAZ>@;ur`{juO2{V+O55E&f!j%$eL;Y19e26&fCu;_3c7m-5e^BqhW+e5)SqtwxJ=@)9=SMsPx+5cqd}|JNA_lwpOFkO>@XctoigCH%#<`MKS8d+S#P0e{ERAC|bG{C~dyfoip$2##'
'p@8D5us6bhANB*8XGlGY_R+}2gWs&C3&mx+0nK9hz-}PY>|sbU33flZx67w}Vl(yWQ$e;1KkCArx(;pvbZO)hsiHcjyiKJH#A=+B_!wS?(K}y<T(YEbKSQ;mD#A$M`-e!rgs|bkt|;#A@bt0r&fyoiCn1YHaAs*nG6Qz=XajtK^FeCxmg(J1)Q>kDyl7&vI9IN++n%al'
'PPZJsS{d}UnGBsH#u_02hH%w|AM13nnqmJO^BQQ|dbJhqq|0=|BOB(m>r}^@zS^;*DUTDf;>hcOJ{XoXhZ*N?VZWOC3hSmS2n*^X3HhL=aJ3UooQoaXbV~gX(e^i*j(d>r(JtVN#B?4PUvfYzr}dl`B)onhEdep2F8(KyQKy2D#h}n)X#hEepKiD&28Ad~5=*$;Iz#;j'
'bGRHC2`rgYC}Zl8pxGg#RDlc3%DhQ|zKkg*w2V7mcF<YUw2$Q6?JaOQTr51a$$%IuDKu-huRnb$YDL+WuY8f4)IizUFIilnwmh#`=`Kxvnaoh5#tb_TSWEmKM?W<~$LI2d^Ti`51YLs8fDi*I0hd{aIz_>h0eZ^T^h-{CjYJ{8Y5L?0POQS4QDr`+^FF^bYfLvnSmNG)'
'pYAHHo*a&zJE?TZ>?o^iU+?ND_7%NXe<-i<tqdMKe6#+6z`mW4B)%KU56`>raCw2e7KvyyW~kRH4$hgL)O~cyNF}K6SyA1SHhV*~-F8<-2SD#WEE8MCePS_E@$L3PNMH5pBGh1~Xxf-_feFl^z`ZTXZ7|j#Sz=wXMNz2H<DSp9HpQ*A9!PwQt*;s%pYD!{2S9GS>yumy'
'T%bUT(*fs=`)~4R7#tSw+kWh&@zF^Ktl!fjPQ(zydcIs$=T>zu$WVk3`Fc-$1P8e(kM0i=o>S(eD<UXd>a5oZc##FiE{7+5{C3#fa#Qz}+-p)R$fo(mhC4AeFssV8gzg6W#MI$xm}!zlF+Px~RUp)_GbSMB<O38GjJp+m{cAb8P$nrZBx#PI;X)FxaMf+olmV|o24+x#'
'c4)CT>d3FqNA45oj7Y4pMWbHFs{{#)Zn2#)C)MF=ct96*pL(Y_O|zSfB4ri#w7w!V<A#qOv^lJ>&H#u)UKJ%-A)XsnYB;6%es$3V8#>{W<;^;256l%$=Y#}B=l)SkhDDU~o*4eZ&g~8bh?rIUmdjQen#@!y9gRY%$Y|b(23w2a9BiJ@K`rMO*>|QkbE!TcD15M;rOug}'
'!`V?9#1tKIkA!j9rHqRUMqKKft!e)p!N-alAOWNI`z>bejpdUD*w7*YB8(-u$LOW#p0v=qrt2!#e*O}VC`J@dV4cRm{b*f6BokoK3<j?1|NOjBt%W@%D!gc!0pnp6xcu%bxd2%ah4m?Y@ZulhC}2}RSMi{7eyGDWuO=0j4<!KmXwy4!_<r>&cE*a`{3+5~5&xb@QQie0'
'M<1ZAn_z|AnTgr|swCRjUe8;oRyJ8u==)bQS?H`lW9QTjm$lfP9<}HxZani6y*-qhBK2}zJD$1PQH|d8XGXc0KGb3cj!w^p>%L}p{G1)w+%ILR^P8a-$3QtX=6ezDA&v{DQsbH6+FS(>1^LhXrRt;0YQl53!ud}u_wyn+&GR><qInKYltEIDKdX#l=n{^70Qyk0F8H^*'
'-&@vbPyj3q)-GK>L`9ahqnjG6?q7Dyld6j3u!rCrly+`vobBBe$W1=hnVVjFqx6%RSv-V=v^o!{cbh^v4zmpUP#78BPtsc5>;2BLef~F|)6l@7Z`~zFi&>4<)htm@OUv(O8EsRfDWh7{Xufu9ThxP%WSN{xxa`o^c`|_68sGzuB-Yg4)FBm50nWpQOP(9=(s^_0JM2`}'
'?1O`<W+iC+)vVmpCJnTT;b`L~4_t-)czS!B#%p80xZ!$$Zm2zKFh(<jsWSL%s1{WDfWrZtO(kD`>q1WEj^`LwB2f=KsXy1PkIO_<Ma$VyUEh+KZ6nYY3eJ5f3sO&UM+QV9fG!^u3RqV&r@W|}T!Sl#&Xaip^9gEY<XiSSVD1*CeA`5KBDj~y6Ld1CWcA-`bK^hhC<x=i'
's7RlvumKPIwW}Ks!}s_CK4Z55`qBgX56~<DZv9fM#!F)Q5}d_MA^-76=LW-D9XN$X91}%O7)vtF9RbYIqmRYnQ&7eGuDpR&EKTBUL3>Vnuc6VJuS^##mbb5%WP+Q?q>xxk#nb0()JeBSGGm(?k?eh)U{r`j0nMYqWe>2rW)f`yS|cG%L?C2O+1)sz{}ON3KkL69V=Udu'
'x)UXBDho%-7;2d(TFyq5XaGulF<fI>TdNARSGU#8`8c|5M@7FxGQV&;jnW;sI5K|S)iSf}^UW{3hqRkE(>$*&51(Jaw=1LQcm%r%WzXoX)cQjr+-xM-dec$RCCdzM9FC?lq;$sJ7DDg6OMtY}nZ=zTnjLxUG9`^{+*+b+P<AypmVDzhKu~3o;HSj{NAut_e12eX3K5@d'
'_a|&@MES&LT%7kM+Rw(W#=dcxKQZt6O9kIU&*KlV^i^#YWf*_v3Hew;9p#+vjpuK(=Z3uY&2Fmt9_g_;z=wEc79l@dunOPBal>~vvg%BkBGuEg{<>5%5=`$UMk{UOenC08G^+h>(%w?<1dimkAFW{^w`-8_o<X+lOT)@Vv1aG-by7=|UYbZ#xgsAJDgDtoyL%vj!A_tk'
'hoRM-=~GWnwKT0sTLLn*suTKk;evGAnR0#v;uAD(8q!nc=5YOrB-XI0m9Vdrg~Efef!xqzo3ZCi*BCfv%Q0~_$h1d2^P~n{s99{tC<01}(+w#|k{7GGkaU!50rAl_rKxOFI%@_VDpF_v4^0Hd>Tf9JYMlsd>Uh%AE55$-RxwGxw=hm#?^@^P<N3wGu20LHG0`<0<R+`g'
'pAkAEm?VfRK?t_dsqHh~om$P@;dQcHG0G%1*H89Ud*Q+jvzv%FUXdg)QS{mIUJfyMAq2#cyPLot)^6@P5Cd6%Rl}m`^~?wXw8R%gQi6152d`MZrdVuB`MzXK+I(saS4`ZPGl8$d&-k`5b<hCRngh)0WK{0SW}CBjVyduYuo-vvvqC2ZKvYn86cq^7P3o<&ns&g#hSU|q'
'YDY&Cd4m$@(<mdu<)mx|1k4oJj*>xv)>zZyirFnDnWWcThe}z;(WlrRGea3;`@2w0bN;S3oTu6JaZg5oZ!w90Qesoe_!*b|%=$=NXvbD&>_nM=IXGBT>XX>R>A2ErN*$>Xm>!L;svpEAJfaNjpK1Kx)>m(wAeGdxhRhIB<JnYDlOO;900000rE173IirIh00HTj0-UG^'
'%1?qfvBYQl0ssI200dcD'
)

def map_pass_leet(string, mode='hard'):
    def create_leet(string, mode='hard'):
        '''
        这里即便是 hard 模式也没有使用遍历处理方式，
        因为那样对数据的膨胀过大，所以这里暂时就选择了一个更加折中的办法进行处理
        '''
        easy = dict(
            A = ['4'],
            B = ['8'],
            C = [],
            D = [],
            E = ['3'],
            F = [],
            G = ['6'],
            H = [],
            I = [],
            J = [],
            K = [],
            L = ['1'],
            M = [],
            N = [],
            O = ['0'],
            P = [],
            Q = [],
            R = ['2'],
            S = ['5'],
            T = ['7'],
            U = ['v'],
            V = [],
            W = [],
            X = [],
            Y = [],
            Z = ['2'],
        )
        hard = dict(
            A = ['4', '@'],
            B = ['8'],
            C = ['('],
            D = [')'],
            E = ['3'],
            F = [],
            G = ['6'],
            H = ['#'],
            I = ['!'],
            J = [],
            K = [],
            L = ['1', '|'],
            M = [],
            N = [],
            O = ['0'],
            P = ['9'],
            Q = ['&'],
            R = ['2'],
            S = ['5', '$'],
            T = [],
            U = ['v'],
            V = [],
            W = [],
            X = [],
            Y = [],
            Z = ['2', '%'],
        )
        if mode == 'easy': _mode = easy
        if mode == 'hard': _mode = hard
        yield []
        r = []
        q = []
        for i in string:
            if i.upper() in _mode and i.upper() not in q and _mode[i.upper()]:
                q.append(i.upper())
                r.append([i.upper(), _mode[i.upper()][0]])
        for l in range(1, len(r)+1):
            for i in itertools.combinations(r,l):
                yield i
        e = []
        q = []
        if ('A' in string.upper() or \
            'L' in string.upper() or \
            'S' in string.upper()) and \
            mode == 'hard':
            for i in string:
                if i.upper() in _mode and i.upper() not in q and _mode[i.upper()]:
                    q.append(i.upper())
                    e.append([i.upper(), _mode[i.upper()][-1]])
        for l in range(1, len(e)+1):
            for i in itertools.combinations(e, l):
                if any([i[0].upper() in 'ALS' for i in i]):
                    yield i
    for i in create_leet(string, mode):
        s = string
        i = dict(i)
        for j in string:
            if j.upper() in i:
                s = s.replace(j, i[j.upper()])
        yield s

def mk_map_passleet(passlist, lenlimit=range(0,300), mode='hard'):
    if not isinstance(lenlimit, (list, tuple, range)):
        raise TypeError('lenlimit type must be list,tuple,range')
    l = list(lenlimit)
    for i in passlist:
        if len(i) not in l:
            continue
        for j in map_pass_leet(i, mode):
            yield j

zpasslist = base64.b85decode(zpasslist.encode())
zpasslist = lzma.decompress(zpasslist).decode().splitlines()

# 目前压缩率比较高的自带算法是 lzma
# # 字符串的压缩以及解压处理
# import lzma
# import base64
# _encode = base64.b64encode
# _decode = base64.b64decode
# _encode = base64.b85encode
# _decode = base64.b85decode
# # 将字符串压缩后进行base编码
# string = lzma.compress(string.encode())
# string = _encode(string).decode()
# # 格式化输出
# for idx,i in enumerate(string,1):
#     print(i,end='')
#     if idx % 200 == 0:
#         print("'\n'",end='')
# print('\n',len(string))
# # 将字符串解码后解压
# string = _decode(string.encode())
# string = lzma.decompress(string).decode()



# 普通单字母 + 常见中文名拼音简写
zh_name_heads = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 
    'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
    'cb',  'cbo', 'cc',  'cf',  'cg',  'cgl', 'cgy', 'ch',  'cj',  'cjh', 'cl',  'cli', 'cm',  'cp',  'cq',  
    'ct',  'cw',  'cx',  'cxk', 'cxl', 'cxy', 'cxz', 'cy',  'cyl', 'cyy', 'gf',  'hm',  'hw',  'hxy', 'hy',  'lb',  
    'lbo', 'lc',  'lcm', 'ld',  'ldd', 'ldm', 'lf',  'lfy', 'lg',  'lgf', 'lgh', 'lgl', 'lgr', 'lgx', 'lgy', 
    'lgz', 'lh',  'lhm', 'lhx', 'lhy', 'lj',  'ljg', 'ljh', 'ljj', 'lk',  'll',  
    'lli', 'lly', 'lm',  'ln',  'lna', 'lp',  'lq',  'lr',  'ls',  'lsh', 'lsl', 'lsy', 'lsz', 'lt',  'ltt', 
    'lw',  'lx',  'lxf', 'lxh', 'lxl', 'lxm', 'lxr', 'lxy', 'lxz', 'ly',  'lyh', 'lyf', 'lyl', 'lym', 'lyy', 
    'lyz', 'lzq', 'mac', 'mal', 'mc',  'ml',  'mli', 'mxy', 'sw',  'sxy', 'wb',  'wbo', 'wc',  'wcm', 'wd',  
    'wdd', 'wdm', 'wf',  'wfl', 'wfy', 'wg',  'wgf', 'wgh', 'wgl', 'wgr', 'wgx', 'wgy', 'wgz', 'wh',  'whm', 
    'why', 'wj',  'wjf', 'wjg', 'wjh', 'wjj', 'wjp', 'wk',  'wl',  'wlh', 'wli', 'wlj', 'wll', 'wlu', 'wly', 
    'wm',  'wn',  'wna', 'wp',  'wq',  'wr',  'ws',  'wsh', 'wsl', 'wsy', 'wsz', 'wt',  'wtt', 'ww',  'wx',  
    'wxf', 'wxh', 'wxl', 'wxm', 'wxr', 'wxu', 'wxy', 'wxz', 'wy',  'wyh', 'wyl', 'wym', 'wyu', 'wyy', 'wyz', 
    'wzq', 'xj',  'xm',  'xuj', 'xum', 'xuw', 'xw',  'yb',  'ybo', 'yc',  'yf',  'ygy', 'yh',  'yj',  'yl',  
    'yli', 'ym',  'yp',  'yt',  'yw',  'yx',  'yxl', 'yxy', 'yxz', 'yy',  'zb',  'zbo', 'zc',  'zcm', 'zd',  
    'zf',  'zfy', 'zgf', 'zgl', 'zgr', 'zgy', 'zgz', 'zh',  'zhm', 'zhy', 'zj',  'zjg', 'zjh', 'zjj', 'zjl', 'zk',  
    'zl',  'zlh', 'zli', 'zlj', 'zll', 'zly', 'zm',  'zn',  'zna', 'zp',  'zq',  'zr',  'zs',  'zsl', 'zsy', 
    'zsz', 'zt',  'ztt', 'zw',  'zx',  'zxf', 'zxh', 'zxl', 'zxm', 'zxr', 'zxu', 'zxy', 'zxz', 'zy',  'zyh', 
    'zyl', 'zym', 'zyu', 'zyy', 'zyz', 'zzq',
]

# 时间遍历 # 247138 条
# 如果过滤掉 /, - 这种类型的处理，则只有 99854 条
import datetime
import itertools
gstart = datetime.datetime(1970,1,1,0,0,0)
gend   = datetime.datetime(2020,1,2,0,0,0)

def map_date(
    start   = gstart,
    end     = gend,
    ):
    def date_range(start_date,end_date):
        for n in range(int((end_date-start_date).days)):
            yield start_date+datetime.timedelta(n)
    
    q = []
    for i in date_range(start, end):
        i = (i.year, i.month, i.day)
        q.append(i)
    return q

def map_year_month_day(onlynumber=False):
    a,b,c = '%Y','%m','%d'
    fmts = ['{}{}{}',] if onlynumber == True else [
        '{}{}{}',
        '{}/{}/{}',
        '{}-{}-{}',
    ]
    q = []
    for i in map_date():
        year, month, day = i
        year  = '{:>02}'.format(year)
        month = '{:>02}'.format(month)
        day   = '{:>02}'.format(day)
        for fmt in fmts:
            q1 = fmt.format(year, month, day)
            qq = fmt.format(year[2:], month, day)
            q.append(q1)
            q.append(qq)
            if month.startswith('0') or day.startswith('0'):
                month, day = month.lstrip('0'), day.lstrip('0')
                q1 = fmt.format(year, month, day)
                qq = fmt.format(year[2:], month, day)
                q.append(q1)
                q.append(qq)
    for i in map_date():
        year, month, day = i
        year  = '{:>02}'.format(year)
        month = '{:>02}'.format(month)
        day   = '{:>02}'.format(day)
        for fmt in fmts:
            q2 = fmt.format(day, month, year)
            qq = fmt.format(day, month, year[2:])
            q.append(q2)
            q.append(qq)
            if month.startswith('0') or day.startswith('0'):
                month, day = month.lstrip('0'), day.lstrip('0')
                q2 = fmt.format(day, month, year)
                qq = fmt.format(day, month, year[2:])
                q.append(q2)
                q.append(qq)
    for i in sorted(set(q)):
        yield i

def map_year_month(onlynumber=False):
    a,b,c = '%Y','%m','%d'
    fmts = ['{}{}',] if onlynumber == True else [
        '{}{}',
        '{}/{}',
        '{}-{}',
    ]
    q = []
    for i in map_date():
        year, month, day = i
        year  = '{:>02}'.format(year)
        month = '{:>02}'.format(month)
        for fmt in fmts:
            q1 = fmt.format(year, month)
            qq = fmt.format(year[2:], month)
            q.append(q1)
            q.append(qq)
            if month.startswith('0'):
                month = month.lstrip('0')
                q1 = fmt.format(year, month)
                qq = fmt.format(year[2:], month)
                q.append(q1)
                q.append(qq)
    for i in map_date():
        year, month, day = i
        year  = '{:>02}'.format(year)
        month = '{:>02}'.format(month)
        for fmt in fmts:
            q2 = fmt.format(month, year)
            qq = fmt.format(month, year[2:])
            q.append(q2)
            q.append(qq)
            if month.startswith('0'):
                month = month.lstrip('0')
                q2 = fmt.format(month, year)
                qq = fmt.format(year[2:], month)
                q.append(q1)
                q.append(qq)
    for i in sorted(set(q)):
        yield i

def map_month_day(onlynumber=False):
    a,b,c = '%Y','%m','%d'
    fmts = ['{}{}',] if onlynumber == True else [
        '{}{}',
        '{}/{}',
        '{}-{}',
    ]
    q = []
    for i in map_date(
            start   = datetime.datetime(2020,1,1,0,0,0),
            end     = datetime.datetime(2021,1,2,0,0,0),
        ):
        year, month, day = i
        month = '{:>02}'.format(month)
        day   = '{:>02}'.format(day)
        for fmt in fmts:
            q1 = fmt.format(month, day)
            q.append(q1)
            if month.startswith('0') or day.startswith('0'):
                month = month.lstrip('0')
                day   = day.lstrip('0')
                q1 = fmt.format(month, day)
                q.append(q1)
    for i in map_date(
            start   = datetime.datetime(2020,1,1,0,0,0),
            end     = datetime.datetime(2021,1,2,0,0,0),
        ):
        year, month, day = i
        month = '{:>02}'.format(month)
        day   = '{:>02}'.format(day)
        for fmt in fmts:
            q2 = fmt.format(day, month)
            q.append(q2)
            if month.startswith('0') or day.startswith('0'):
                month = month.lstrip('0')
                day   = day.lstrip('0')
                q1 = fmt.format(day, month)
                q.append(q1)
    for i in sorted(set(q)):
        yield i

def map_namehead_times(
        prefixlist=None,
        onlynumber=True, 
        plusfunc=lambda a, b: a + b  # 名字缩写与时间的加和方式，可以考虑增加下划线之类的
    ):
    # 拼音加日期组合
    prefixlist = [''] if prefixlist is None else prefixlist
    a = list(map(str, range(1970, 2020)))
    b = map_month_day(onlynumber)
    c = map_year_month(onlynumber)
    d = map_year_month_day(onlynumber)
    for times in [a,b,c,d]:
        for nhead,ttime in itertools.product(prefixlist, times):
            yield plusfunc(nhead, ttime)




if __name__ == '__main__':
    # 这里解压出的 zpasslist 是从 sqlmap 中获取到的密码字典 + 自己在别处收集的一些密码
    # 大约 15000+ 条密码数据。
    # 通过 map_pass_leet 函数将每个密码的常见的黑客语的各种可能组合的映射遍历出来，让字典更具备鲁棒性
    # 经过测试发现，黑客语 easy 模式膨胀度约 15 倍，hard 模式膨胀度大约为 30 倍。在较大的字典内慎用。
    import time
    import hashlib

    # 检查简单的密码字典表，有尝试使用简单的黑客语遍历一般密码的异化密码的可能，最长花两秒时间
    k = 'p4ssw0rd'  # ~1.4s
    k = '4dmin'     # ~0.1s
    w = hashlib.md5(k.encode()).hexdigest()
    ctime = time.time()
    for i in itertools.chain(mk_map_passleet(zpasslist), map_namehead_times()):
        v = hashlib.md5(i.encode()).hexdigest()
        if v == w:
            print(v, i)
            break
    print(time.time()-ctime)

    # 通过姓名首字母拼接日期(日期包括月份日期中有零和没有零两种情况)进行密码遍历，最长会花大约一分钟
    k = 'mxy201611' # ~20s
    k = 'z2018123'  # ~4.2s
    k = 'a20189'    # ~0.5s
    w = hashlib.md5(k.encode()).hexdigest()
    ctime = time.time()
    for i in map_namehead_times(zh_name_heads):
        v = hashlib.md5(i.encode()).hexdigest()
        if v == w:
            print(v, i)
            break
    print(time.time()-ctime)