::: {.p3}

## [3.4]{.sec}IPv4 addressing, subnetting, VLSM and CIDR [Must · ■■□]{.tag} {#s3-4}

An IPv4 address is a 32-bit number that identifies a network interface and tells a router where to send packets for it. It is written as four decimal numbers, one per byte (an *octet*), separated by dots: 172.16.45.200. Subnetting, the art of dividing an address block into smaller networks, is the most frequently examined skill in this book, and it is a mechanical one that anybody can perform in under a minute after a short drill.

::: bigidea
The mask splits a 32-bit address into a network part and a host part, and subnetting is nothing more than moving that split to fit the number of hosts needed.
:::

### Network part, host part, mask

Every address has two parts: the *network* part, shared by all devices in the same subnet, and the *host* part, which distinguishes devices inside it. The *subnet mask* marks the split with ones over the network bits and zeros over the host bits. The *prefix length* is the count of ones, so 255.255.248.0 is written /21 (eight plus eight plus five ones). Two addresses are on the same subnet exactly when they agree on all network bits, which a host tests by bitwise AND with its own mask. In every subnet two addresses are special: the *network address* (host bits all zero) names the subnet itself, and the *broadcast address* (host bits all one) reaches every host in it. Hence a subnet with h host bits holds 2<sup>h</sup> addresses and 2<sup>h</sup> − 2 usable hosts.

<figure>
<svg viewBox="0 0 480 144" width="480">
<text class="sm" x="118" y="12" text-anchor="start" >Octet 1</text>
<text class="sm" x="160.0" y="12" text-anchor="middle" >octet 1</text>
<text class="sm" x="249.0" y="12" text-anchor="middle" >octet 2</text>
<text class="sm" x="338.0" y="12" text-anchor="middle" >octet 3</text>
<text class="sm" x="427.0" y="12" text-anchor="middle" >octet 4</text>
<text class="lbl" x="14" y="33" text-anchor="start" >Address</text>
<rect class="fill" x="118.0" y="20" width="10.5" height="18" rx="0" />
<text class="mono" x="123.2" y="33" text-anchor="middle" style="font-size:8px">1</text>
<rect class="fill" x="128.5" y="20" width="10.5" height="18" rx="0" />
<text class="mono" x="133.8" y="33" text-anchor="middle" style="font-size:8px">0</text>
<rect class="fill" x="139.0" y="20" width="10.5" height="18" rx="0" />
<text class="mono" x="144.2" y="33" text-anchor="middle" style="font-size:8px">1</text>
<rect class="fill" x="149.5" y="20" width="10.5" height="18" rx="0" />
<text class="mono" x="154.8" y="33" text-anchor="middle" style="font-size:8px">0</text>
<rect class="fill" x="160.0" y="20" width="10.5" height="18" rx="0" />
<text class="mono" x="165.2" y="33" text-anchor="middle" style="font-size:8px">1</text>
<rect class="fill" x="170.5" y="20" width="10.5" height="18" rx="0" />
<text class="mono" x="175.8" y="33" text-anchor="middle" style="font-size:8px">1</text>
<rect class="fill" x="181.0" y="20" width="10.5" height="18" rx="0" />
<text class="mono" x="186.2" y="33" text-anchor="middle" style="font-size:8px">0</text>
<rect class="fill" x="191.5" y="20" width="10.5" height="18" rx="0" />
<text class="mono" x="196.8" y="33" text-anchor="middle" style="font-size:8px">0</text>
<rect class="fill" x="207.0" y="20" width="10.5" height="18" rx="0" />
<text class="mono" x="212.2" y="33" text-anchor="middle" style="font-size:8px">0</text>
<rect class="fill" x="217.5" y="20" width="10.5" height="18" rx="0" />
<text class="mono" x="222.8" y="33" text-anchor="middle" style="font-size:8px">0</text>
<rect class="fill" x="228.0" y="20" width="10.5" height="18" rx="0" />
<text class="mono" x="233.2" y="33" text-anchor="middle" style="font-size:8px">0</text>
<rect class="fill" x="238.5" y="20" width="10.5" height="18" rx="0" />
<text class="mono" x="243.8" y="33" text-anchor="middle" style="font-size:8px">1</text>
<rect class="fill" x="249.0" y="20" width="10.5" height="18" rx="0" />
<text class="mono" x="254.2" y="33" text-anchor="middle" style="font-size:8px">0</text>
<rect class="fill" x="259.5" y="20" width="10.5" height="18" rx="0" />
<text class="mono" x="264.8" y="33" text-anchor="middle" style="font-size:8px">0</text>
<rect class="fill" x="270.0" y="20" width="10.5" height="18" rx="0" />
<text class="mono" x="275.2" y="33" text-anchor="middle" style="font-size:8px">0</text>
<rect class="fill" x="280.5" y="20" width="10.5" height="18" rx="0" />
<text class="mono" x="285.8" y="33" text-anchor="middle" style="font-size:8px">0</text>
<rect class="fill" x="296.0" y="20" width="10.5" height="18" rx="0" />
<text class="mono" x="301.2" y="33" text-anchor="middle" style="font-size:8px">0</text>
<rect class="fill" x="306.5" y="20" width="10.5" height="18" rx="0" />
<text class="mono" x="311.8" y="33" text-anchor="middle" style="font-size:8px">0</text>
<rect class="fill" x="317.0" y="20" width="10.5" height="18" rx="0" />
<text class="mono" x="322.2" y="33" text-anchor="middle" style="font-size:8px">1</text>
<rect class="fill" x="327.5" y="20" width="10.5" height="18" rx="0" />
<text class="mono" x="332.8" y="33" text-anchor="middle" style="font-size:8px">0</text>
<rect class="fill" x="338.0" y="20" width="10.5" height="18" rx="0" />
<text class="mono" x="343.2" y="33" text-anchor="middle" style="font-size:8px">1</text>
<rect class="box" x="348.5" y="20" width="10.5" height="18" rx="0" />
<text class="mono" x="353.8" y="33" text-anchor="middle" style="font-size:8px">1</text>
<rect class="box" x="359.0" y="20" width="10.5" height="18" rx="0" />
<text class="mono" x="364.2" y="33" text-anchor="middle" style="font-size:8px">0</text>
<rect class="box" x="369.5" y="20" width="10.5" height="18" rx="0" />
<text class="mono" x="374.8" y="33" text-anchor="middle" style="font-size:8px">1</text>
<rect class="box" x="385.0" y="20" width="10.5" height="18" rx="0" />
<text class="mono" x="390.2" y="33" text-anchor="middle" style="font-size:8px">1</text>
<rect class="box" x="395.5" y="20" width="10.5" height="18" rx="0" />
<text class="mono" x="400.8" y="33" text-anchor="middle" style="font-size:8px">1</text>
<rect class="box" x="406.0" y="20" width="10.5" height="18" rx="0" />
<text class="mono" x="411.2" y="33" text-anchor="middle" style="font-size:8px">0</text>
<rect class="box" x="416.5" y="20" width="10.5" height="18" rx="0" />
<text class="mono" x="421.8" y="33" text-anchor="middle" style="font-size:8px">0</text>
<rect class="box" x="427.0" y="20" width="10.5" height="18" rx="0" />
<text class="mono" x="432.2" y="33" text-anchor="middle" style="font-size:8px">1</text>
<rect class="box" x="437.5" y="20" width="10.5" height="18" rx="0" />
<text class="mono" x="442.8" y="33" text-anchor="middle" style="font-size:8px">0</text>
<rect class="box" x="448.0" y="20" width="10.5" height="18" rx="0" />
<text class="mono" x="453.2" y="33" text-anchor="middle" style="font-size:8px">0</text>
<rect class="box" x="458.5" y="20" width="10.5" height="18" rx="0" />
<text class="mono" x="463.8" y="33" text-anchor="middle" style="font-size:8px">0</text>
<text class="lbl" x="477.0" y="33" text-anchor="start" >172.16.45.200</text>
<text class="lbl" x="14" y="59" text-anchor="start" >Mask /21</text>
<rect class="fill" x="118.0" y="46" width="10.5" height="18" rx="0" />
<text class="mono" x="123.2" y="59" text-anchor="middle" style="font-size:8px">1</text>
<rect class="fill" x="128.5" y="46" width="10.5" height="18" rx="0" />
<text class="mono" x="133.8" y="59" text-anchor="middle" style="font-size:8px">1</text>
<rect class="fill" x="139.0" y="46" width="10.5" height="18" rx="0" />
<text class="mono" x="144.2" y="59" text-anchor="middle" style="font-size:8px">1</text>
<rect class="fill" x="149.5" y="46" width="10.5" height="18" rx="0" />
<text class="mono" x="154.8" y="59" text-anchor="middle" style="font-size:8px">1</text>
<rect class="fill" x="160.0" y="46" width="10.5" height="18" rx="0" />
<text class="mono" x="165.2" y="59" text-anchor="middle" style="font-size:8px">1</text>
<rect class="fill" x="170.5" y="46" width="10.5" height="18" rx="0" />
<text class="mono" x="175.8" y="59" text-anchor="middle" style="font-size:8px">1</text>
<rect class="fill" x="181.0" y="46" width="10.5" height="18" rx="0" />
<text class="mono" x="186.2" y="59" text-anchor="middle" style="font-size:8px">1</text>
<rect class="fill" x="191.5" y="46" width="10.5" height="18" rx="0" />
<text class="mono" x="196.8" y="59" text-anchor="middle" style="font-size:8px">1</text>
<rect class="fill" x="207.0" y="46" width="10.5" height="18" rx="0" />
<text class="mono" x="212.2" y="59" text-anchor="middle" style="font-size:8px">1</text>
<rect class="fill" x="217.5" y="46" width="10.5" height="18" rx="0" />
<text class="mono" x="222.8" y="59" text-anchor="middle" style="font-size:8px">1</text>
<rect class="fill" x="228.0" y="46" width="10.5" height="18" rx="0" />
<text class="mono" x="233.2" y="59" text-anchor="middle" style="font-size:8px">1</text>
<rect class="fill" x="238.5" y="46" width="10.5" height="18" rx="0" />
<text class="mono" x="243.8" y="59" text-anchor="middle" style="font-size:8px">1</text>
<rect class="fill" x="249.0" y="46" width="10.5" height="18" rx="0" />
<text class="mono" x="254.2" y="59" text-anchor="middle" style="font-size:8px">1</text>
<rect class="fill" x="259.5" y="46" width="10.5" height="18" rx="0" />
<text class="mono" x="264.8" y="59" text-anchor="middle" style="font-size:8px">1</text>
<rect class="fill" x="270.0" y="46" width="10.5" height="18" rx="0" />
<text class="mono" x="275.2" y="59" text-anchor="middle" style="font-size:8px">1</text>
<rect class="fill" x="280.5" y="46" width="10.5" height="18" rx="0" />
<text class="mono" x="285.8" y="59" text-anchor="middle" style="font-size:8px">1</text>
<rect class="fill" x="296.0" y="46" width="10.5" height="18" rx="0" />
<text class="mono" x="301.2" y="59" text-anchor="middle" style="font-size:8px">1</text>
<rect class="fill" x="306.5" y="46" width="10.5" height="18" rx="0" />
<text class="mono" x="311.8" y="59" text-anchor="middle" style="font-size:8px">1</text>
<rect class="fill" x="317.0" y="46" width="10.5" height="18" rx="0" />
<text class="mono" x="322.2" y="59" text-anchor="middle" style="font-size:8px">1</text>
<rect class="fill" x="327.5" y="46" width="10.5" height="18" rx="0" />
<text class="mono" x="332.8" y="59" text-anchor="middle" style="font-size:8px">1</text>
<rect class="fill" x="338.0" y="46" width="10.5" height="18" rx="0" />
<text class="mono" x="343.2" y="59" text-anchor="middle" style="font-size:8px">1</text>
<rect class="box" x="348.5" y="46" width="10.5" height="18" rx="0" />
<text class="mono" x="353.8" y="59" text-anchor="middle" style="font-size:8px">0</text>
<rect class="box" x="359.0" y="46" width="10.5" height="18" rx="0" />
<text class="mono" x="364.2" y="59" text-anchor="middle" style="font-size:8px">0</text>
<rect class="box" x="369.5" y="46" width="10.5" height="18" rx="0" />
<text class="mono" x="374.8" y="59" text-anchor="middle" style="font-size:8px">0</text>
<rect class="box" x="385.0" y="46" width="10.5" height="18" rx="0" />
<text class="mono" x="390.2" y="59" text-anchor="middle" style="font-size:8px">0</text>
<rect class="box" x="395.5" y="46" width="10.5" height="18" rx="0" />
<text class="mono" x="400.8" y="59" text-anchor="middle" style="font-size:8px">0</text>
<rect class="box" x="406.0" y="46" width="10.5" height="18" rx="0" />
<text class="mono" x="411.2" y="59" text-anchor="middle" style="font-size:8px">0</text>
<rect class="box" x="416.5" y="46" width="10.5" height="18" rx="0" />
<text class="mono" x="421.8" y="59" text-anchor="middle" style="font-size:8px">0</text>
<rect class="box" x="427.0" y="46" width="10.5" height="18" rx="0" />
<text class="mono" x="432.2" y="59" text-anchor="middle" style="font-size:8px">0</text>
<rect class="box" x="437.5" y="46" width="10.5" height="18" rx="0" />
<text class="mono" x="442.8" y="59" text-anchor="middle" style="font-size:8px">0</text>
<rect class="box" x="448.0" y="46" width="10.5" height="18" rx="0" />
<text class="mono" x="453.2" y="59" text-anchor="middle" style="font-size:8px">0</text>
<rect class="box" x="458.5" y="46" width="10.5" height="18" rx="0" />
<text class="mono" x="463.8" y="59" text-anchor="middle" style="font-size:8px">0</text>
<text class="lbl" x="477.0" y="59" text-anchor="start" >255.255.248.0</text>
<text class="lbl" x="14" y="85" text-anchor="start" >Network = addr AND mask</text>
<rect class="fill" x="118.0" y="72" width="10.5" height="18" rx="0" />
<text class="mono" x="123.2" y="85" text-anchor="middle" style="font-size:8px">1</text>
<rect class="fill" x="128.5" y="72" width="10.5" height="18" rx="0" />
<text class="mono" x="133.8" y="85" text-anchor="middle" style="font-size:8px">0</text>
<rect class="fill" x="139.0" y="72" width="10.5" height="18" rx="0" />
<text class="mono" x="144.2" y="85" text-anchor="middle" style="font-size:8px">1</text>
<rect class="fill" x="149.5" y="72" width="10.5" height="18" rx="0" />
<text class="mono" x="154.8" y="85" text-anchor="middle" style="font-size:8px">0</text>
<rect class="fill" x="160.0" y="72" width="10.5" height="18" rx="0" />
<text class="mono" x="165.2" y="85" text-anchor="middle" style="font-size:8px">1</text>
<rect class="fill" x="170.5" y="72" width="10.5" height="18" rx="0" />
<text class="mono" x="175.8" y="85" text-anchor="middle" style="font-size:8px">1</text>
<rect class="fill" x="181.0" y="72" width="10.5" height="18" rx="0" />
<text class="mono" x="186.2" y="85" text-anchor="middle" style="font-size:8px">0</text>
<rect class="fill" x="191.5" y="72" width="10.5" height="18" rx="0" />
<text class="mono" x="196.8" y="85" text-anchor="middle" style="font-size:8px">0</text>
<rect class="fill" x="207.0" y="72" width="10.5" height="18" rx="0" />
<text class="mono" x="212.2" y="85" text-anchor="middle" style="font-size:8px">0</text>
<rect class="fill" x="217.5" y="72" width="10.5" height="18" rx="0" />
<text class="mono" x="222.8" y="85" text-anchor="middle" style="font-size:8px">0</text>
<rect class="fill" x="228.0" y="72" width="10.5" height="18" rx="0" />
<text class="mono" x="233.2" y="85" text-anchor="middle" style="font-size:8px">0</text>
<rect class="fill" x="238.5" y="72" width="10.5" height="18" rx="0" />
<text class="mono" x="243.8" y="85" text-anchor="middle" style="font-size:8px">1</text>
<rect class="fill" x="249.0" y="72" width="10.5" height="18" rx="0" />
<text class="mono" x="254.2" y="85" text-anchor="middle" style="font-size:8px">0</text>
<rect class="fill" x="259.5" y="72" width="10.5" height="18" rx="0" />
<text class="mono" x="264.8" y="85" text-anchor="middle" style="font-size:8px">0</text>
<rect class="fill" x="270.0" y="72" width="10.5" height="18" rx="0" />
<text class="mono" x="275.2" y="85" text-anchor="middle" style="font-size:8px">0</text>
<rect class="fill" x="280.5" y="72" width="10.5" height="18" rx="0" />
<text class="mono" x="285.8" y="85" text-anchor="middle" style="font-size:8px">0</text>
<rect class="fill" x="296.0" y="72" width="10.5" height="18" rx="0" />
<text class="mono" x="301.2" y="85" text-anchor="middle" style="font-size:8px">0</text>
<rect class="fill" x="306.5" y="72" width="10.5" height="18" rx="0" />
<text class="mono" x="311.8" y="85" text-anchor="middle" style="font-size:8px">0</text>
<rect class="fill" x="317.0" y="72" width="10.5" height="18" rx="0" />
<text class="mono" x="322.2" y="85" text-anchor="middle" style="font-size:8px">1</text>
<rect class="fill" x="327.5" y="72" width="10.5" height="18" rx="0" />
<text class="mono" x="332.8" y="85" text-anchor="middle" style="font-size:8px">0</text>
<rect class="fill" x="338.0" y="72" width="10.5" height="18" rx="0" />
<text class="mono" x="343.2" y="85" text-anchor="middle" style="font-size:8px">1</text>
<rect class="box" x="348.5" y="72" width="10.5" height="18" rx="0" />
<text class="mono" x="353.8" y="85" text-anchor="middle" style="font-size:8px">0</text>
<rect class="box" x="359.0" y="72" width="10.5" height="18" rx="0" />
<text class="mono" x="364.2" y="85" text-anchor="middle" style="font-size:8px">0</text>
<rect class="box" x="369.5" y="72" width="10.5" height="18" rx="0" />
<text class="mono" x="374.8" y="85" text-anchor="middle" style="font-size:8px">0</text>
<rect class="box" x="385.0" y="72" width="10.5" height="18" rx="0" />
<text class="mono" x="390.2" y="85" text-anchor="middle" style="font-size:8px">0</text>
<rect class="box" x="395.5" y="72" width="10.5" height="18" rx="0" />
<text class="mono" x="400.8" y="85" text-anchor="middle" style="font-size:8px">0</text>
<rect class="box" x="406.0" y="72" width="10.5" height="18" rx="0" />
<text class="mono" x="411.2" y="85" text-anchor="middle" style="font-size:8px">0</text>
<rect class="box" x="416.5" y="72" width="10.5" height="18" rx="0" />
<text class="mono" x="421.8" y="85" text-anchor="middle" style="font-size:8px">0</text>
<rect class="box" x="427.0" y="72" width="10.5" height="18" rx="0" />
<text class="mono" x="432.2" y="85" text-anchor="middle" style="font-size:8px">0</text>
<rect class="box" x="437.5" y="72" width="10.5" height="18" rx="0" />
<text class="mono" x="442.8" y="85" text-anchor="middle" style="font-size:8px">0</text>
<rect class="box" x="448.0" y="72" width="10.5" height="18" rx="0" />
<text class="mono" x="453.2" y="85" text-anchor="middle" style="font-size:8px">0</text>
<rect class="box" x="458.5" y="72" width="10.5" height="18" rx="0" />
<text class="mono" x="463.8" y="85" text-anchor="middle" style="font-size:8px">0</text>
<text class="lbl" x="477.0" y="85" text-anchor="start" >172.16.40.0</text>
<text class="lbl" x="14" y="111" text-anchor="start" >Broadcast = net OR wildcard</text>
<rect class="fill" x="118.0" y="98" width="10.5" height="18" rx="0" />
<text class="mono" x="123.2" y="111" text-anchor="middle" style="font-size:8px">1</text>
<rect class="fill" x="128.5" y="98" width="10.5" height="18" rx="0" />
<text class="mono" x="133.8" y="111" text-anchor="middle" style="font-size:8px">0</text>
<rect class="fill" x="139.0" y="98" width="10.5" height="18" rx="0" />
<text class="mono" x="144.2" y="111" text-anchor="middle" style="font-size:8px">1</text>
<rect class="fill" x="149.5" y="98" width="10.5" height="18" rx="0" />
<text class="mono" x="154.8" y="111" text-anchor="middle" style="font-size:8px">0</text>
<rect class="fill" x="160.0" y="98" width="10.5" height="18" rx="0" />
<text class="mono" x="165.2" y="111" text-anchor="middle" style="font-size:8px">1</text>
<rect class="fill" x="170.5" y="98" width="10.5" height="18" rx="0" />
<text class="mono" x="175.8" y="111" text-anchor="middle" style="font-size:8px">1</text>
<rect class="fill" x="181.0" y="98" width="10.5" height="18" rx="0" />
<text class="mono" x="186.2" y="111" text-anchor="middle" style="font-size:8px">0</text>
<rect class="fill" x="191.5" y="98" width="10.5" height="18" rx="0" />
<text class="mono" x="196.8" y="111" text-anchor="middle" style="font-size:8px">0</text>
<rect class="fill" x="207.0" y="98" width="10.5" height="18" rx="0" />
<text class="mono" x="212.2" y="111" text-anchor="middle" style="font-size:8px">0</text>
<rect class="fill" x="217.5" y="98" width="10.5" height="18" rx="0" />
<text class="mono" x="222.8" y="111" text-anchor="middle" style="font-size:8px">0</text>
<rect class="fill" x="228.0" y="98" width="10.5" height="18" rx="0" />
<text class="mono" x="233.2" y="111" text-anchor="middle" style="font-size:8px">0</text>
<rect class="fill" x="238.5" y="98" width="10.5" height="18" rx="0" />
<text class="mono" x="243.8" y="111" text-anchor="middle" style="font-size:8px">1</text>
<rect class="fill" x="249.0" y="98" width="10.5" height="18" rx="0" />
<text class="mono" x="254.2" y="111" text-anchor="middle" style="font-size:8px">0</text>
<rect class="fill" x="259.5" y="98" width="10.5" height="18" rx="0" />
<text class="mono" x="264.8" y="111" text-anchor="middle" style="font-size:8px">0</text>
<rect class="fill" x="270.0" y="98" width="10.5" height="18" rx="0" />
<text class="mono" x="275.2" y="111" text-anchor="middle" style="font-size:8px">0</text>
<rect class="fill" x="280.5" y="98" width="10.5" height="18" rx="0" />
<text class="mono" x="285.8" y="111" text-anchor="middle" style="font-size:8px">0</text>
<rect class="fill" x="296.0" y="98" width="10.5" height="18" rx="0" />
<text class="mono" x="301.2" y="111" text-anchor="middle" style="font-size:8px">0</text>
<rect class="fill" x="306.5" y="98" width="10.5" height="18" rx="0" />
<text class="mono" x="311.8" y="111" text-anchor="middle" style="font-size:8px">0</text>
<rect class="fill" x="317.0" y="98" width="10.5" height="18" rx="0" />
<text class="mono" x="322.2" y="111" text-anchor="middle" style="font-size:8px">1</text>
<rect class="fill" x="327.5" y="98" width="10.5" height="18" rx="0" />
<text class="mono" x="332.8" y="111" text-anchor="middle" style="font-size:8px">0</text>
<rect class="fill" x="338.0" y="98" width="10.5" height="18" rx="0" />
<text class="mono" x="343.2" y="111" text-anchor="middle" style="font-size:8px">1</text>
<rect class="box" x="348.5" y="98" width="10.5" height="18" rx="0" />
<text class="mono" x="353.8" y="111" text-anchor="middle" style="font-size:8px">1</text>
<rect class="box" x="359.0" y="98" width="10.5" height="18" rx="0" />
<text class="mono" x="364.2" y="111" text-anchor="middle" style="font-size:8px">1</text>
<rect class="box" x="369.5" y="98" width="10.5" height="18" rx="0" />
<text class="mono" x="374.8" y="111" text-anchor="middle" style="font-size:8px">1</text>
<rect class="box" x="385.0" y="98" width="10.5" height="18" rx="0" />
<text class="mono" x="390.2" y="111" text-anchor="middle" style="font-size:8px">1</text>
<rect class="box" x="395.5" y="98" width="10.5" height="18" rx="0" />
<text class="mono" x="400.8" y="111" text-anchor="middle" style="font-size:8px">1</text>
<rect class="box" x="406.0" y="98" width="10.5" height="18" rx="0" />
<text class="mono" x="411.2" y="111" text-anchor="middle" style="font-size:8px">1</text>
<rect class="box" x="416.5" y="98" width="10.5" height="18" rx="0" />
<text class="mono" x="421.8" y="111" text-anchor="middle" style="font-size:8px">1</text>
<rect class="box" x="427.0" y="98" width="10.5" height="18" rx="0" />
<text class="mono" x="432.2" y="111" text-anchor="middle" style="font-size:8px">1</text>
<rect class="box" x="437.5" y="98" width="10.5" height="18" rx="0" />
<text class="mono" x="442.8" y="111" text-anchor="middle" style="font-size:8px">1</text>
<rect class="box" x="448.0" y="98" width="10.5" height="18" rx="0" />
<text class="mono" x="453.2" y="111" text-anchor="middle" style="font-size:8px">1</text>
<rect class="box" x="458.5" y="98" width="10.5" height="18" rx="0" />
<text class="mono" x="463.8" y="111" text-anchor="middle" style="font-size:8px">1</text>
<text class="lbl" x="477.0" y="111" text-anchor="start" >172.16.47.255</text>
<line class="acc" x1="348.0" y1="16" x2="348.0" y2="124"/>
<text class="acct" x="348.0" y="135" text-anchor="middle" >21 network bits | 11 host bits</text>
<text class="sm" x="14" y="135" text-anchor="start" >shaded = network bits</text>
</svg>
<figcaption><b>Figure 3.10</b> The 32-bit ruler for 172.16.45.200/21. The mask line falls inside the third octet, between bit 21 and bit 22; everything left of it is the network, everything right of it is the host.</figcaption>
</figure>

::: example
**Network, broadcast, range and hosts for 172.16.45.200/21, by the block-size method.**

1. Mask: 21 ones is 255.255.248.0. The interesting octet is the third, where the mask is 248.
2. Block size = 256 − 248 = 8. Subnets in the third octet start at multiples of 8: 0, 8, … 40, 48.
3. The address has 45 in the third octet, and 40 ≤ 45 < 48, so the network address is 172.16.40.0.
4. The broadcast address is one below the next network: 172.16.47.255.
5. Usable range: 172.16.40.1 to 172.16.47.254. Host bits = 32 − 21 = 11, so hosts = 2¹¹ − 2 = 2,046.
6. Wildcard mask (the mask inverted, used in OSPF and ACLs) = 0.0.7.255.

[Result: network 172.16.40.0, broadcast 172.16.47.255, 2,046 usable hosts, wildcard 0.0.7.255.]{.result}
:::

[**Block-size trick** — in the interesting octet, block = 256 − mask octet. List the multiples of the block; the address sits in one of them. Prefix /25 to /30 gives blocks 128, 64, 32, 16, 8, 4 in the fourth octet, and /17 to /23 gives the same series in the third.]{.margin}The master table below is worth memorising for the rows from /24 to /30, and the rest follow by the doubling rule: each bit added to the prefix halves the block.

| Prefix | Mask | Wildcard | Block size (octet) | Addresses | Usable hosts |
|---|---|---|---|---|---|
| /8 | 255.0.0.0 | 0.255.255.255 | 1 (octet 1) | 16,777,216 | 16,777,214 |
| /12 | 255.240.0.0 | 0.15.255.255 | 16 (octet 2) | 1,048,576 | 1,048,574 |
| /16 | 255.255.0.0 | 0.0.255.255 | 1 (octet 2) | 65,536 | 65,534 |
| /17 | 255.255.128.0 | 0.0.127.255 | 128 (octet 3) | 32,768 | 32,766 |
| /18 | 255.255.192.0 | 0.0.63.255 | 64 (octet 3) | 16,384 | 16,382 |
| /19 | 255.255.224.0 | 0.0.31.255 | 32 (octet 3) | 8,192 | 8,190 |
| /20 | 255.255.240.0 | 0.0.15.255 | 16 (octet 3) | 4,096 | 4,094 |
| /21 | 255.255.248.0 | 0.0.7.255 | 8 (octet 3) | 2,048 | 2,046 |
| /22 | 255.255.252.0 | 0.0.3.255 | 4 (octet 3) | 1,024 | 1,022 |
| /23 | 255.255.254.0 | 0.0.1.255 | 2 (octet 3) | 512 | 510 |
| /24 | 255.255.255.0 | 0.0.0.255 | 1 (octet 3) | 256 | 254 |
| /25 | 255.255.255.128 | 0.0.0.127 | 128 (octet 4) | 128 | 126 |
| /26 | 255.255.255.192 | 0.0.0.63 | 64 (octet 4) | 64 | 62 |
| /27 | 255.255.255.224 | 0.0.0.31 | 32 (octet 4) | 32 | 30 |
| /28 | 255.255.255.240 | 0.0.0.15 | 16 (octet 4) | 16 | 14 |
| /29 | 255.255.255.248 | 0.0.0.7 | 8 (octet 4) | 8 | 6 |
| /30 | 255.255.255.252 | 0.0.0.3 | 4 (octet 4) | 4 | 2 |
| /31 | 255.255.255.254 | 0.0.0.1 | 2 (octet 4) | 2 | 2 (RFC 3021) |
| /32 | 255.255.255.255 | 0.0.0.0 | 1 (octet 4) | 1 | 1 (host route) |

### Classes, private ranges and special addresses

Originally the first bits of an address fixed its size: class A (first octet 1 to 126, /8), class B (128 to 191, /16), class C (192 to 223, /24), class D (224 to 239, multicast) and class E (240 to 255, reserved). The scheme wasted addresses, because an organisation needing 300 hosts had to take a class B with 65,534, and it bloated the routing tables. It was replaced in 1993 by *CIDR* (classless inter-domain routing), in which the prefix length is carried with the address and may be any value. The classes survive only in vocabulary and in some default behaviour of old protocols.

The special ranges below appear in many interview questions.

| Range | Meaning |
|---|---|
| 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16 | Private addresses (RFC 1918): not routed on the Internet, reused in every home and company |
| 127.0.0.0/8 | Loopback; 127.0.0.1 is the machine itself |
| 169.254.0.0/16 | Link-local (APIPA): self-assigned when DHCP fails |
| 100.64.0.0/10 | Carrier-grade NAT (shared address space) |
| 0.0.0.0 | "This host" at start-up, and the default route as 0.0.0.0/0 |
| 255.255.255.255 | Limited broadcast, never forwarded by a router |
| 224.0.0.0/4 | Multicast |
| 192.0.2.0/24, 198.51.100.0/24, 203.0.113.0/24 | Reserved for documentation; used in this book's examples |

Two prefixes break the rule "usable hosts = 2<sup>h</sup> − 2". A /31 has two addresses and, by RFC 3021, both are usable on a point-to-point link, because such a link has no need of a network or broadcast address; this saves half of the addresses on every router-to-router link. A /32 names a single host or interface, and appears as a loopback address or a *host route*.

### Splitting and VLSM

*Fixed-length* subnetting cuts a block into equal subnets. To obtain at least s subnets, borrow b host bits with 2<sup>b</sup> ≥ s; the prefix grows by b.

::: example
**Divide 192.168.10.0/24 into six subnets.**

1. Six subnets need 2<sup>b</sup> ≥ 6, so b = 3 (eight subnets). New prefix: 24 + 3 = /27, mask 255.255.255.224.
2. Block size = 256 − 224 = 32. Host bits = 5, so 2⁵ − 2 = 30 hosts per subnet.
3. The subnets start at .0, .32, .64, .96, .128, .160, .192, .224. For the second, network 192.168.10.32, usable .33 to .62, broadcast .63.

[Result: eight /27 subnets of 30 hosts, block size 32; two are left over for growth.]{.result}
:::

Equal subnets waste addresses when the needs differ. *Variable-length subnet masking* (VLSM) gives each subnet the prefix it needs. The rule is to sort requirements from largest to smallest, allocate the largest first, and place each subnet on a multiple of its own block size so that blocks never straddle.

::: example
**VLSM from 192.168.10.0/24 for LANs of 100, 50 and 25 hosts and two point-to-point WAN links.**

1. 100 hosts: 2⁷ − 2 = 126 ≥ 100, so /25. Allocate 192.168.10.0/25: usable .1 to .126, broadcast .127.
2. 50 hosts: 2⁶ − 2 = 62 ≥ 50, so /26. Next free address .128: 192.168.10.128/26, usable .129 to .190, broadcast .191.
3. 25 hosts: 2⁵ − 2 = 30 ≥ 25, so /27. Next free .192: 192.168.10.192/27, usable .193 to .222, broadcast .223.
4. Each WAN needs 2 addresses: /30. 192.168.10.224/30 (usable .225, .226) and 192.168.10.228/30 (usable .229, .230).
5. What remains is .232 to .255, which is 192.168.10.232/29 and 192.168.10.240/28, both spare.

[Result: /25, /26, /27, /30, /30 with 24 addresses spare; allocating the small ones first would have forced the /25 to start at .128 and the plan would not fit.]{.result}
:::

<figure>
<svg viewBox="0 0 480 126" width="480">
<rect class="fill" x="20.0" y="50" width="209.9" height="30" rx="0" />
<text class="lbl" x="125.0" y="63" text-anchor="middle" >/25</text>
<text class="sm" x="125.0" y="74" text-anchor="middle" >LAN 100 hosts</text>
<rect class="fill" x="229.9" y="50" width="105.0" height="30" rx="0" />
<text class="lbl" x="282.4" y="63" text-anchor="middle" >/26</text>
<text class="sm" x="282.4" y="74" text-anchor="middle" >LAN 50</text>
<rect class="fill" x="334.9" y="50" width="52.5" height="30" rx="0" />
<text class="lbl" x="361.1" y="63" text-anchor="middle" >/27</text>
<text class="sm" x="361.1" y="74" text-anchor="middle" >LAN 25</text>
<rect class="hl" x="387.4" y="50" width="6.6" height="30" rx="0" />
<rect class="hl" x="393.9" y="50" width="6.6" height="30" rx="0" />
<rect class="box" x="400.5" y="50" width="13.1" height="30" rx="0" />
<rect class="box" x="413.6" y="50" width="26.2" height="30" rx="0" />
<text class="sm" x="124.96" y="26" text-anchor="middle" >192.168.10.0</text>
<line class="lg" x1="20.0" y1="80" x2="20.0" y2="86" />
<line class="lg" x1="229.9" y1="80" x2="229.9" y2="86" />
<line class="lg" x1="334.9" y1="80" x2="334.9" y2="86" />
<line class="lg" x1="387.4" y1="80" x2="387.4" y2="86" />
<line class="lg" x1="400.5" y1="80" x2="400.5" y2="86" />
<line class="lg" x1="413.6" y1="80" x2="413.6" y2="86" />
<line class="lg" x1="438.2" y1="80" x2="438.2" y2="86" />
<text class="sm" x="20.0" y="96" text-anchor="middle" >.0</text>
<text class="sm" x="229.9" y="96" text-anchor="middle" >.128</text>
<text class="sm" x="334.9" y="96" text-anchor="middle" >.192</text>
<text class="sm" x="387.4" y="96" text-anchor="middle" >.224</text>
<text class="sm" x="413.6" y="96" text-anchor="middle" >.240</text>
<text class="sm" x="439.8" y="96" text-anchor="middle" >.255</text>
<text class="acct" x="390.64" y="44" text-anchor="middle" >two /30 WANs</text>
<line class="acc" x1="390.6" y1="48" x2="390.6" y2="50" />
<text class="sm" x="407.03999999999996" y="112" text-anchor="middle" >.232/29 + .240/28 spare</text>
<text class="sm" x="20" y="14" text-anchor="start" >Last octet 0 to 255, one cell = 1.64 px per address</text>
</svg>
<figcaption><b>Figure 3.11</b> The VLSM plan as an address-space bar. The largest subnet is placed first, and each later one starts on a multiple of its own block size; what remains at the top is spare.</figcaption>
</figure>

### Summarisation and the same-subnet test

A router can announce one *summary* (supernet) instead of many routes when the subnets are contiguous and aligned. The method is to write the networks in binary, and find the longest common prefix.

::: example
**Summarise 10.1.4.0/24 to 10.1.7.0/24, and test 10.1.5.0 to 10.1.8.0.**

1. The third octets 4, 5, 6, 7 are 00000100, 00000101, 00000110, 00000111. They share the first six bits, 000001.
2. The prefix is 16 + 6 = 22: the summary is 10.1.4.0/22, which covers exactly 4 × 256 addresses and nothing else.
3. For 10.1.5.0 to 10.1.8.0 the third octets 5, 6, 7, 8 are 00000101 … 00001000, which share only the first four bits, 0000. The smallest single prefix is 10.1.0.0/20, which also claims 10.1.0.0 to 10.1.3.255 and 10.1.9.0 to 10.1.15.255. That over-claims addresses the router does not have.

[Result: 10.1.4.0/22 summarises the first set exactly; the second cannot be summarised without over-claiming, and must be advertised as three routes: 10.1.5.0/24, 10.1.6.0/23 and 10.1.8.0/24.]{.result}
:::

The same-subnet test is a cousin of this: two hosts are on one subnet if their addresses agree on the mask's network bits. For 10.10.10.130/26 and 10.10.10.190/26, the block size is 64 and both fall in 128 to 191, so they share a subnet; 10.10.10.193 falls in 192 to 255, so it does not. Interviewers at Cisco and Arista sometimes ask for this as code (Q3.14).

Finally, a word on how routers use all of these prefixes: when several routes match a destination, the router chooses the one with the *longest prefix*, the most specific. The algorithm and its data structure are treated in Pillar 1 (the trie), and the idea is applied in Section 3.8.

::: trap
*Claim:* "Every subnet has 2<sup>n</sup> − 2 usable hosts, so a /31 has none and a /32 has none." *Why it is wrong:* the "minus two" removes the network and broadcast addresses, which a /31 point-to-point link does not need (RFC 3021). *Correct statement:* a /31 gives two usable addresses on a point-to-point link, a /32 identifies one host, and 2<sup>h</sup> − 2 applies from /30 downwards.
:::

::: lens
[CISCO · AMAZON · JUNIPER · ARISTA · NOKIA]{.co}

The question is "network, broadcast and range for X/Y without a calculator" (Q3.10), or a VLSM design (Q3.12). The examiner watches the method: state the block size first, then the multiples, then the answer. A strong candidate also mentions /31 and checks that the VLSM plan fits before presenting it.
:::

::: lab
`LAB 3.4 · 30 MIN` (i) On paper, solve the five drills below against a stopwatch; the target is 45 seconds each. (ii) In Python, check your answers with the standard library.

```python
import ipaddress
n = ipaddress.ip_network("172.16.45.200/21", strict=False)
print(n.network_address, n.broadcast_address, n.num_addresses - 2, n.hostmask)
```

```
172.16.40.0 172.16.47.255 2046 0.0.7.255
```

**What you should notice:** the library agrees with the block-size method. Then rewrite the same calculator with only integer shifts and masks (`mask = (0xFFFFFFFF << (32 - p)) & 0xFFFFFFFF`) and compare; that version is the one to write in an interview.
:::

::: check
1. Network and broadcast of 10.20.30.77/26. [^c3-10]
2. Usable range of 192.168.5.130/25. [^c3-11]
3. How many usable hosts in 172.20.0.0/19? [^c3-12]
4. Are 200.1.1.65/27 and 200.1.1.95/27 on the same subnet? Is the second a valid host address? [^c3-13]
5. The smallest prefix that holds 500 hosts. [^c3-14]
:::

[^c3-10]: Block 64, 77 lies in 64 to 127: network 10.20.30.64, broadcast 10.20.30.127.
[^c3-11]: Block 128: network .128, broadcast .255, usable 192.168.5.129 to 192.168.5.254.
[^c3-12]: 13 host bits, so 2¹³ − 2 = 8,190.
[^c3-13]: Block 32, both lie in 64 to 95, so they share a subnet, but .95 is its broadcast address and is not a valid host address.
[^c3-14]: 2⁹ − 2 = 510 ≥ 500 and 2⁸ − 2 = 254 is too few, so 9 host bits: /23.

:::
