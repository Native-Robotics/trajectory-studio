# cuRobo improvement replay

135 / 135 processed · 135 recorded passes · 0 failed · 0 not measured

| Measured change | Result | New vs historical GPU median |
|---|---|---|
| Fresh-process planning | 22% less | 9.715 s vs 12.524 s |
| Retained-worker request | 44% less | 7.048 s vs 12.524 s |
| Motion duration | 21% less | 6.662 s vs 8.438 s |
| Jerk worse | Higher jerk | RMS 4.975 vs 1.482 rad/s³; normalized 330575 vs 58574 |
| GPU memory tradeoff | Higher memory | 968 MiB fresh vs 376 MiB before; 1374 MiB retained worker |

Fixed-ten medians; retained-worker requests use second observations and include reuse. Historical GPU checks were looser and develop exceeded recorded TCP acceleration limits, so these are not equal-validity comparisons.

<details><summary>Measurement method and limitations</summary>

Original replay: 46 / 135 historical passes under earlier checks, not strict original-constraint parity. Coverage above reflects only this measured replay.

Manifest records strict-original-v1: recorded passes use the strict original-constraint validator. This identifies saved evidence; it is not a new re-audit.

Historical original GPU and intermediate results were evaluated with earlier, looser wrist-down, endpoint and linear checks, not strict original-constraint parity. Their historical passes are retained as recorded outcomes, not retroactively certified against the corrected strict validator. Historical develop also failed recorded TCP acceleration checks; performance comparisons do not establish constraint parity.

Previous develop and cuRobo measurements used separate fresh production Planner processes. New replay uses one persistent Planner with sequential requests and one worker. Old planning_s excludes imports and Planner initialization; new elapsed_s is measured request latency including polling and any child startup. These are different execution methods, not a controlled isolated algorithm speedup. Cache labels count actual recorded lookup hits, not request order. One observation per replay task; optional warm repeats are separate. SOLVED is the production result; constraints_valid is recorded independent qualification. TCP, dynamics and collision validation are sampled, not continuous-time proofs. Motion metrics are exact on saved cubic coefficients. Jerk integrals omit impulses at acceleration jumps, which are reported separately. No overall quality score is assigned. Resource sampling can miss peaks and summed RSS can double-count shared pages.

Final frozen-source replay: all 135 Barilla requests passed strict original-constraint qualification and original FCL collision validation. The fixed ten-task fresh-process and retained-worker comparisons are complete. Historical cuRobo passes used looser checks; original develop outputs violate the recorded TCP acceleration limit.

Measured requests: 135; summed request latency 1785.781 s; median 11.182 s. The sum excludes time between requests and is not total process wall time.

</details>

| Metric | develop fresh | old cuRobo fresh | improved persistent |
|---|---:|---:|---:|
| Latency s (different methods) | 9.012 | 12.524 | 7.398 |
| Motion duration s | 1.919 | 8.438 | 6.662 |
| Joint mileage rad | 5.616 | 5.357 | 5.002 |
| RMS jerk rad/s³ (excludes jumps) | 41.065 | 1.482 | 4.975 |
| Normalized jerk (excludes jumps) | 9909.695 | 58574.346 | 330575.152 |
| Maximum acceleration jump rad/s² | 4.523 | 0.000 | 0.000 |

| Task | Status | Request latency s | Motion s | Cache | Error | Studio |
|---|---|---:|---:|---|---|---|
| 0 | SOLVED | 14.336 | 8.800 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#8a8ddaf4df6b649825207c045607280d71738a46f2bdc784808b276156181a29-curobo) |
| 1 | SOLVED | 11.214 | 8.642 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#5ec0425abcfd1ddbba907989465fdeea37351a3c928d1fbc0f0688efdb2dc6e7-curobo) |
| 2 | SOLVED | 11.188 | 9.018 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#236e7d6c7f2343a27196c7806774659f42f95dbe607e08c39d807c06659060f3-curobo) |
| 3 | SOLVED | 5.164 | 6.308 | cold cache (0/2) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#d11f7e3674a194e159d178dfd86113da494021a409ab52062aca88a210751222-curobo) |
| 4 | SOLVED | 6.745 | 7.578 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#1fe518293663051f682bc433aef49c035880ad988e21871c1aed491a99642815-curobo) |
| 5 | SOLVED | 13.276 | 8.956 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#d34f5d1a676ed74000aeb376421dcab2c4210a7746df4028cac938720c422a19-curobo) |
| 6 | SOLVED | 5.081 | 6.448 | cold cache (0/2) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#14dad0b1314d843887dfb27099e2ef3b4551d27e37832ddba80830b607eed6f7-curobo) |
| 7 | SOLVED | 11.528 | 8.590 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#874c2ff6ed99371f56f5534b0e5647f78ecd31e1f64bfb060ac54a5272ed5767-curobo) |
| 8 | SOLVED | 13.651 | 11.617 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#157778044707b6b38066ec220a68d9041ce05269962daec3475b8396422ab85a-curobo) |
| 9 | SOLVED | 10.918 | 8.224 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#990b4a17e4bbe938fc45f65f5c5906b48b80d60a977651ab4cca93918db60460-curobo) |
| 10 | SOLVED | 7.694 | 7.498 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#4669b0add291cb1840e127a15e95ac71c69d31ae66310e3febbf98ef128e2a05-curobo) |
| 11 | SOLVED | 12.592 | 9.140 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#f7fe241f51ceed34d82d9905d0a026a00956115d82779a7777ca72f95d870e95-curobo) |
| 12 | SOLVED | 5.717 | 6.313 | cold cache (0/2) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#67fd7e6ecb9b1d55bbc1a6f5884b05b950b490367c6e46425db4fcb5da887f43-curobo) |
| 13 | SOLVED | 8.753 | 7.487 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#65ae9262939ee84049590871f8f39c96dc6e8dfa537644b01aeb4f5f9a7989bf-curobo) |
| 14 | SOLVED | 14.806 | 11.717 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#783a0b36e747e15823b50bb53e6ed467e361112a23fcb9e4a898883b6785c838-curobo) |
| 15 | SOLVED | 6.316 | 6.703 | cold cache (0/2) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#c82ec835fe944eff30aab8917fa1906c8ec0b2b2169bf51f4a4b036eb089e240-curobo) |
| 16 | SOLVED | 8.291 | 7.360 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#ff51eac0fb305749a0b576535bfcc5646e4198417271fb7acc213d73d7790f7b-curobo) |
| 17 | SOLVED | 13.571 | 9.363 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#e2e58e342e85c79a2dd921678efc9adbc8318d0750c58d7c1fdad071cb3ffc06-curobo) |
| 18 | SOLVED | 6.199 | 6.173 | cold cache (0/2) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#1327e2bffb12a417a7bf56f44d3865dc9518fd7535c9d700682d477c6f789d4b-curobo) |
| 19 | SOLVED | 9.295 | 8.341 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#cdfe50e6501abd720ddab2d018f396d281c935a71283ff7ee0b2958ac2128473-curobo) |
| 20 | SOLVED | 17.396 | 13.813 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#b1b1ac1cca245324e658d7a0088299f8cc568d71cbb75469e533c4c3bd002857-curobo) |
| 21 | SOLVED | 6.689 | 7.015 | cold cache (0/2) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#4534dd005e414e88e712d5e26835809ae2cb800719088e89652d6c51665b090b-curobo) |
| 22 | SOLVED | 9.316 | 9.741 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#0c734fba9f3ac973cef401117d12dba0fb92e1dfd0141e1f8950b84834a5b583-curobo) |
| 23 | SOLVED | 17.582 | 11.382 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#4420c1ba15a9f9f4647aee9b87f9cea70aa69c39c555fde596e9e879b8949b6e-curobo) |
| 24 | SOLVED | 7.625 | 8.251 | cold cache (0/2) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#7733d0fe0777e8be858249b95aea32045ca4c9027dd26a1d6d40d633de3e73b2-curobo) |
| 25 | SOLVED | 10.789 | 10.476 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#5e7e6dc69fed087aa0561b802e4856b091b494602708f6bc5a86ad9667b78018-curobo) |
| 26 | SOLVED | 46.690 | 12.640 | cold cache (0/7); 1 recoveries / 30.167 s |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#30530dc6123a455aee737bac0143d5fbdcd3af27041b0faf47fddb64f9f67c74-curobo) |
| 27 | SOLVED | 8.785 | 11.900 | cold cache (0/2) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#09ace9b8946c23d6a961a3b2cf747c6b961b6ed5a3a1dec045300f2843c0b665-curobo) |
| 28 | SOLVED | 10.899 | 10.364 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#e704290c065a7a6f906d1e1712005222e139a9d452c5fe6cb1089d6443636c6c-curobo) |
| 29 | SOLVED | 37.595 | 19.924 | cold cache (0/6); 1 recoveries / 18.082 s |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#aa329637486d5889d002b13a941467b9323ef35664410d5e7884091b3447de8c-curobo) |
| 30 | SOLVED | 8.211 | 10.598 | cold cache (0/2) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#637b8daa125b4be9dd797ab6a17346b58f42fcddb325a3348d90ce6c8ab954e7-curobo) |
| 31 | SOLVED | 12.253 | 11.161 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#8985758efd9744de84c67f0ac421aa8d8c511a6a65e420311f880b35354a6368-curobo) |
| 32 | SOLVED | 36.620 | 15.734 | cold cache (0/6); 1 recoveries / 17.366 s |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#4dd61fe30a89a5ed02fd537e7dcb2dd66fc4463ebe132868fbc4f727a1e382c4-curobo) |
| 33 | SOLVED | 9.575 | 10.131 | cold cache (0/2) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#c3c0bcb6e33ecfb2112015a8d37c42dce013894f0690e884ca64936b48927d24-curobo) |
| 34 | SOLVED | 11.795 | 10.395 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#8141b5e91d8cb3c68e51899df31a9c9d80809e7ed2dd1b89bc54b619b1f587e7-curobo) |
| 35 | SOLVED | 25.498 | 15.690 | partial / unknown (0/4); 1 recoveries / 15.578 s |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#d069b37b66b1d41c81251cfea60d3b252cee286101bf5df09953410f12ab6be1-curobo) |
| 36 | SOLVED | 8.613 | 8.323 | cold cache (0/2) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#763c16198f2fb926e8935cb1ce0a07d5b7e5336a3f019b72358302b0700e31f7-curobo) |
| 37 | SOLVED | 8.272 | 12.132 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#24b002cf8d129dd361c832e6778abace2907e3117f9b4e32cf43fc536599b1d0-curobo) |
| 38 | SOLVED | 11.182 | 8.014 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#9ad11ec668c886435ff5dd801c01b54942626ab51dd4ab144d28e47c660208e7-curobo) |
| 39 | SOLVED | 12.293 | 8.578 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#33e4a6207e3dab0b3fc8109aae69ee9bdddd9bce057f63f9dc7c27fb6ef5fa0e-curobo) |
| 40 | SOLVED | 29.822 | 8.686 | partial / unknown (0/5); 1 recoveries / 25.155 s |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#0e7ffe1a4f7b5ff1b5c177f7922a9771761ae07a91671f301a4e4d4823c54aea-curobo) |
| 41 | SOLVED | 6.975 | 6.795 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#cbe58dce5dfe7225b68f50dd900f0d153dc97de450baf96eb68534e9b503a76e-curobo) |
| 42 | SOLVED | 11.340 | 8.666 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#e7cedb57a03526cdc098d5be05f441367847a971c057f0cf37576c6415b961d1-curobo) |
| 43 | SOLVED | 5.187 | 5.604 | cold cache (0/2) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#8f4a1848561c6b0481d0aabfd7a1f571c5c22973d2215c770cb59ea8754c7e94-curobo) |
| 44 | SOLVED | 7.080 | 6.719 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#b3e3aa9d895fdfda3efdefd2ae590d75c2ececcf14c1e186c1d88a847eae5352-curobo) |
| 45 | SOLVED | 10.903 | 9.242 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#da8fd8fb136d8413134c46b398ef9ca69ab9075d6d46c84390c641c0c72951af-curobo) |
| 46 | SOLVED | 5.152 | 5.580 | cold cache (0/2) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#8ab37c289d3653f6f35f1555b43212e7de6a53004f746ad426ed6c7a365ed18f-curobo) |
| 47 | SOLVED | 7.383 | 6.770 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#4d081814e8fc880ebdce04406d4e0196f0241b0d95f738533a44afd0e5217f5f-curobo) |
| 48 | SOLVED | 13.598 | 8.901 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#e240fbe29a5ce182ccb8795707b119ea851f496f35bf07ab43a65644ead6d7e7-curobo) |
| 49 | SOLVED | 5.672 | 5.699 | cold cache (0/2) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#e5dd98e0d6bb34a919f64a2d32db4c71b928c217f9055d563b302dd6d51ad328-curobo) |
| 50 | SOLVED | 7.529 | 7.231 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#1b35f6b527105f98c7e206def5bec2869b3e84fb5fa8ae765f71ce8c2d88365a-curobo) |
| 51 | SOLVED | 19.099 | 17.560 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#cca725669f41282089b22f19a06dcd7048473b791c898f66ae55c9fb2ef90752-curobo) |
| 52 | SOLVED | 5.570 | 5.848 | cold cache (0/2) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#112d53ea58de51f07ed99c0721ee21b9b8475bb0a7123a7f9926f8d4d6c61e0b-curobo) |
| 53 | SOLVED | 11.992 | 8.430 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#982c6c56f60923b151ff2a7c2d07e0a811815ec4ef46470e921f62a5cfc4c0e8-curobo) |
| 54 | SOLVED | 7.444 | 11.459 | cold cache (0/2) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#fe9d57153f6c5b7fd2f6e245232fbf45e7ed69464f192a8375112aee4c5c94df-curobo) |
| 55 | SOLVED | 16.409 | 9.261 | partial / unknown (0/4); 1 recoveries / 10.503 s |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#888c893a10c23064efa0fabd5e4cc73ed77fa082e38f4bdb17a3456b5616d852-curobo) |
| 56 | SOLVED | 5.816 | 5.815 | cold cache (0/2) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#227de82358a9d408c4fc0b353a4179d8a7bc7ea7c3d2397bc278456ffa7b0856-curobo) |
| 57 | SOLVED | 31.809 | 15.027 | cold cache (0/4) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#31c6b4c06c35d130d20be9c68f41fa77efb1847edfa7324187a25b50d04480e2-curobo) |
| 58 | SOLVED | 5.969 | 5.808 | cold cache (0/2) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#d6936b0636d7dcebbcf939eb6c69a902513bb3f35c34c2b3274c65b189483e7c-curobo) |
| 59 | SOLVED | 10.759 | 13.663 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#3b7198671eafb52f81108f96154f8560cf6498efbf86e16a87078e1d77de5f22-curobo) |
| 60 | SOLVED | 34.614 | 13.101 | cold cache (0/6); 1 recoveries / 13.460 s |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#9822f921fa845c3bfd710ad59557848746e0a6dfbab3f68a86c1c57a34856874-curobo) |
| 61 | SOLVED | 8.058 | 9.399 | cold cache (0/2) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#804dee9f7056c1d029d0b79fbe6d907db91799b2305c88a7dd3c7b4b0a06d610-curobo) |
| 62 | SOLVED | 19.390 | 14.602 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#431c3a24cce6527a75f725f7b271417a0aa92f31ec83b8a652ea4e540702771e-curobo) |
| 63 | SOLVED | 7.778 | 9.499 | cold cache (0/2) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#dd9aacd13c2ade6745669747cbc76894ee5d2a9d9d9b4ee06d2efbb8c5ccabd4-curobo) |
| 64 | SOLVED | 10.420 | 9.370 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#66258ebd02eb8021eb5f8971fead92e9836612b16d5f71d3ad3adecd4696aeae-curobo) |
| 65 | SOLVED | 22.259 | 13.805 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#b7e09cccb0e65e05310addb02ff898db0211cc43157f6441779a744e7a0fb18b-curobo) |
| 66 | SOLVED | 7.779 | 7.726 | cold cache (0/2) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#e96ea26bd2338ec705f4db36f41d1bd8b30ca40b8fdc542ab7087195afdf8793-curobo) |
| 67 | SOLVED | 11.482 | 11.412 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#1b93f5804a233180e209a9010892362fa3b2b92ade5cba3b65f5eb6a549bd377-curobo) |
| 68 | SOLVED | 28.931 | 9.757 | cold cache (0/6); 1 recoveries / 10.207 s |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#742b222cac1e5779c87c9bd6a4f9234ed0a02d6b12f533c21e4def9230b18743-curobo) |
| 69 | SOLVED | 9.484 | 9.166 | cold cache (0/2) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#345d876fd0fc95ac0151fef0b9c6c7c74798e233d1d35a9dbeaac76c8aaed43a-curobo) |
| 70 | SOLVED | 10.775 | 7.201 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#2a2d5e19cd08f574edf0847e5d4c397f30429bd3ea6db9b0af7298726524d6ae-curobo) |
| 71 | SOLVED | 35.096 | 9.403 | cold cache (0/6); 1 recoveries / 15.660 s |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#6e59033d1635a3b2f095bc3263efb3ec16914e0f90e5e4f7d6a930480bf69669-curobo) |
| 72 | SOLVED | 8.505 | 6.332 | cold cache (0/2) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#5e499e311cb80fb23e8b193d31110e52e896705d19074e81108d151dabd27627-curobo) |
| 73 | SOLVED | 13.156 | 9.796 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#2ec4c9744327816ea59c42d226461c14d56405b4e55e09b6f7d39e45e32e8743-curobo) |
| 74 | SOLVED | 32.398 | 10.852 | cold cache (0/4) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#f445e97f46fb9f916c2a6eb460df8cdacf57c383fe6b01f0f051557d47f7769b-curobo) |
| 75 | SOLVED | 21.288 | 8.358 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#71837a5cb15736f75cdb9a5bd2374ba46d1b8216c673734312ef5990baf123f1-curobo) |
| 76 | SOLVED | 10.025 | 8.620 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#a26127aac6e378746ea0c47fede339653070bb00409548511632d36b122a8a1c-curobo) |
| 77 | SOLVED | 26.751 | 13.949 | cold cache (0/4) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#6a5f8ea3118c31d3f60930a7df7f0a6f03d38eff661bd1d13f4b76aca4e7a406-curobo) |
| 78 | SOLVED | 14.397 | 11.729 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#869f070423e3d0c736ba34d7938a41a3feaf98227446fdb769369c8052d0e9e2-curobo) |
| 79 | SOLVED | 11.199 | 7.755 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#7b1a482499831cda3e71671cf062709e725e411fb942c312434d6f05cac139ef-curobo) |
| 80 | SOLVED | 14.061 | 11.669 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#958b253c80f575b409bd9a458acc6a04c6c76150efcb43904629d7adda7ab6d5-curobo) |
| 81 | SOLVED | 15.713 | 11.192 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#01bda9f1433078562e2b0cb88ad5b4b737423629eff3f8591e2e8706920e46cf-curobo) |
| 82 | SOLVED | 13.992 | 10.025 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#3d33ebd8a3b7f79918b1372c6daf6331c357edf50d8cef40a0550eadf11ecfe9-curobo) |
| 83 | SOLVED | 11.566 | 7.795 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#28086cf6c71a1f3dfc8a729bed8bbd960203ef7512ab7f0e12eec65ca8c4a101-curobo) |
| 84 | SOLVED | 34.590 | 14.760 | cold cache (0/6); 1 recoveries / 23.753 s |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#87392729615302071d9a74394a89b77557d3c0b0dd0be9cf5008072c501908f6-curobo) |
| 85 | SOLVED | 11.454 | 7.548 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#96f708147d9d95c483b26113d4a9d87211f67c14a3bcfc906c688efc3653c3ce-curobo) |
| 86 | SOLVED | 12.621 | 7.909 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#bc9d3ba210e336b7b6661afe1715d9879379c0ab95c97c7d210f87c15b3d79a1-curobo) |
| 87 | SOLVED | 8.655 | 6.726 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#db4b62f1e13011124c31100513dd79570a9612c6e783634cd58dc25fa9721c65-curobo) |
| 88 | SOLVED | 20.378 | 7.875 | cold cache (0/6); 1 recoveries / 7.813 s |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#21ebe498a10bb43332e4188d2b0de486a0aae0ef3e8482acde8b8efcbae8d123-curobo) |
| 89 | SOLVED | 6.468 | 5.587 | cold cache (0/2) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#c5a4aa5303d5f84eff8f62f04e0deabdb2ccc4cd7ee1cf7a5469669c91f8d47d-curobo) |
| 90 | SOLVED | 9.813 | 6.422 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#40fe3beaa86a5f79013c8edb66f0262d1ce6bd41c438f0901df481964e8999b3-curobo) |
| 91 | SOLVED | 14.292 | 8.094 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#9d630805839dec2bece9888927e7a9445f3269813c426929ccd8e7459512e8a1-curobo) |
| 92 | SOLVED | 7.233 | 5.181 | cold cache (0/2) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#b49321899a1b75128020909ec14d74ec2568acaafbed07d999094e99dbf6e1ec-curobo) |
| 93 | SOLVED | 9.718 | 6.795 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#f8b38d7e79e2041a5125528c4d185971d6d2addca8dbe7161273b72313694a52-curobo) |
| 94 | SOLVED | 13.990 | 7.722 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#7ef9efcad87480f35d34fcdc0ce90aea09149214e6e81f95baaab1541851d716-curobo) |
| 95 | SOLVED | 7.353 | 5.824 | cold cache (0/2) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#a85c9e41ad745c26160fe19eddca1667a4adad081f37815ae0188254f8a8154f-curobo) |
| 96 | SOLVED | 10.491 | 5.965 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#456c57de38c1cc4d36022e8d157e7a81ca4c2173e8d0ae99351a1e31b60ba13e-curobo) |
| 97 | SOLVED | 18.976 | 8.810 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#b4de76070055fbdc047e75e28a625b59dd4d74d5d97410fde4c9bb1cce87601e-curobo) |
| 98 | SOLVED | 7.449 | 4.766 | cold cache (0/2) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#6a437fb05c6357c93e10def63301fc07b8fb83885217794b825a843bb0e76e45-curobo) |
| 99 | SOLVED | 11.301 | 6.421 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#dcbcfaebb091b3d7bdffcedc7f396fc50637d574f2f53b23c820175e9904bb79-curobo) |
| 100 | SOLVED | 24.018 | 7.989 | cold cache (0/6); 1 recoveries / 7.599 s |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#05f86a85796b4f5b28b612a3d0d87b73e2e972a470c1dfc2ba503b8561cfcfb9-curobo) |
| 101 | SOLVED | 7.854 | 5.576 | cold cache (0/2) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#5001f06ef9cb8af38b6e8cb6c75c44537203883ba12e69613260b8ff5eb58a0b-curobo) |
| 102 | SOLVED | 21.597 | 9.182 | cold cache (0/4) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#83187667e10a3759711f81492f1e4cb77b6d8867970e0207d53cd72d7b73b32a-curobo) |
| 103 | SOLVED | 14.271 | 13.041 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#f1d6937ee124a9cc2fc3733dc7934568b463bdf0d2bca0c790029fc1cf2dcd92-curobo) |
| 104 | SOLVED | 16.994 | 16.266 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#4cefdaeac1aadee6f95cdb7597284083e9835942447325445efea0185556dea2-curobo) |
| 105 | SOLVED | 14.854 | 14.391 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#c6665a00526d4df2164127857e4add75bdec6bd6b71ef802dce6c19df2b70d9e-curobo) |
| 106 | SOLVED | 9.582 | 8.990 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#3d1d09a173c1f703cbdca8f1496694443b355ef36faef7947eeed082411fc3f9-curobo) |
| 107 | SOLVED | 13.959 | 10.234 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#ca5b5bb5875c40b466aec21cb14a23657496bb0a935f240a822dd5220e9032e3-curobo) |
| 108 | SOLVED | 11.393 | 7.691 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#d535f91b6132185bce5be948e9c7dc76c214a7cb86e36f9d7eed65fd6a052af3-curobo) |
| 109 | SOLVED | 16.186 | 13.199 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#1b303e154306ba795ffa12b17b1e33b491ddccdc3bab93bd1c6970cb9dec4b40-curobo) |
| 110 | SOLVED | 9.864 | 8.486 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#e470ca2078a3a5d3f316378826cbeb090ede1a237da9fade3d7e1a045c072f7a-curobo) |
| 111 | SOLVED | 11.006 | 8.425 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#0912a6a491d9518d6c6c61229155c9f3a5cd6dea50074c4e320502cc4a0a2c13-curobo) |
| 112 | SOLVED | 7.834 | 9.067 | cold cache (0/2) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#cce28b55970f688433ae3270f54f9e0036432a0cdc6b20e64bc4bdecf001eb42-curobo) |
| 113 | SOLVED | 9.506 | 7.050 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#238f10b4362ebbb9db94e56412c673f51bc404d976e263d886e30f2577811432-curobo) |
| 114 | SOLVED | 11.743 | 7.176 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#ed9a42ca2340e12556739855c8703760405b075336604457a3e83174e23d9a52-curobo) |
| 115 | SOLVED | 7.176 | 6.252 | cold cache (0/2) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#ad3d5831de3a7b166ebeba9722dcdb98326608b562e9782a3b55f9fc734b0274-curobo) |
| 116 | SOLVED | 9.482 | 6.019 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#ddef37c608ea11aa2258d1fe80b7ca7840b359a894d4b367bfb2fdfabcf7f4f8-curobo) |
| 117 | SOLVED | 11.895 | 6.821 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#7fe4d262bbe946f86d8647f445d7532834cbb2b01e39d61dfc51050b07b9f91c-curobo) |
| 118 | SOLVED | 6.858 | 4.995 | cold cache (0/2) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#2002018bb663a96dd8b345964ad7cd86d97dac28e575a7cc3253674e0d0bab63-curobo) |
| 119 | SOLVED | 9.681 | 5.406 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#91d725b4fecb997ee58578a303f680b527cffc7bcb9411b22d9a74298a3b6c3b-curobo) |
| 120 | SOLVED | 18.763 | 8.326 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#1f84dfac252acd51f09607023f7f39d4d3c835dadc88e06cd9df2b4903cbd974-curobo) |
| 121 | SOLVED | 7.384 | 4.509 | cold cache (0/2) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#44f8fe25625bbebe24cf4181a004e924ab3a4a6a5ed6d630ab9f66b6218e78b7-curobo) |
| 122 | SOLVED | 10.774 | 6.731 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#ae52343668153759404058ccd22e337e87743b963fba0f00d5e408decb9798df-curobo) |
| 123 | SOLVED | 16.665 | 8.218 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#5cafdab26d209f9d7becea720347933dce38179df82b759cf8af5ab2fcab693e-curobo) |
| 124 | SOLVED | 8.192 | 5.595 | cold cache (0/2) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#780c535cd4277c9dea97ed39f857d97f5d75a1951ad924bf14109cd8621b9a23-curobo) |
| 125 | SOLVED | 11.840 | 6.306 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#00db71c591a1cdbe9b19ecb437c6f3ad850e04fd35888f16474a7a15f73a7294-curobo) |
| 126 | SOLVED | 18.205 | 8.583 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#5184a18819f4000d819bf18c25df9c6dc2c824f2fdf78256f539f57f29b64d6e-curobo) |
| 127 | SOLVED | 8.481 | 5.204 | cold cache (0/2) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#499c03a3f09689faf199cae6f47938020231026e4a317d093135cc22e06095d4-curobo) |
| 128 | SOLVED | 12.796 | 6.527 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#7271cc305a51225178b98efa70c2bcd8667175ae778b673099c6acab72084326-curobo) |
| 129 | SOLVED | 16.827 | 7.504 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#a7a1b9e090dd9a95aeafcea70476149acbfb714fdf217964c85833775c60f04b-curobo) |
| 130 | SOLVED | 9.216 | 5.692 | cold cache (0/2) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#04de589e9bf012919e80ad690762d2ef652697b36f8cfece0b58e3c1570339c8-curobo) |
| 131 | SOLVED | 12.936 | 5.699 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#fe639e5939c63f39a020645344669bf4b4b74716f3243b4b90dd78d8f8dcc09d-curobo) |
| 132 | SOLVED | 30.929 | 10.728 | cold cache (0/6); 1 recoveries / 12.094 s |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#b8566bd8bebdd6dd62770b473a4135d9929b4afbc0301eff08c7b223081f8c7d-curobo) |
| 133 | SOLVED | 9.258 | 4.817 | cold cache (0/2) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#67745ceb8883e3de2624686a280a5dcfc89d8f3ff7586a9634d8d1dca9307d9b-curobo) |
| 134 | SOLVED | 4.351 | 2.552 | cold cache (0/2) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-improved-20260913/index.html#650d86a604f523befc71a7c1d1c1a7eb438b6485b8d544b601405f3f69004418-curobo) |

## Separate repeat observations

| Iteration | Task | Status | Request latency s | Cache | CPU-s sampled | RSS MiB sampled | GPU MiB sampled | Recoveries | Recovery s |
|---|---|---|---:|---|---:|---:|---:|---:|---:|
| 0 | 3 | SOLVED | 7.633 | cold cache (0/2) | 8.110 | 1583.371 | 968.000 | 0 | 0.000 |
| 1 | 3 | SOLVED | 3.890 | warm cache (2/2) | 4.080 | 1586.539 | 1068.000 | 0 | 0.000 |
| 2 | 4 | SOLVED | 6.803 | cold cache (0/3) | 7.340 | 1602.484 | 1392.000 | 0 | 0.000 |
| 3 | 4 | SOLVED | 6.701 | cold cache (0/3) | 7.220 | 1604.945 | 1546.000 | 0 | 0.000 |
| 4 | 21 | SOLVED | 6.704 | cold cache (0/2) | 7.190 | 1606.379 | 1546.000 | 0 | 0.000 |
| 5 | 21 | SOLVED | 5.763 | warm cache (2/2) | 6.200 | 1606.531 | 1332.000 | 0 | 0.000 |
| 6 | 54 | SOLVED | 11.820 | mixed cache (1/4) | 12.850 | 1610.711 | 1352.000 | 1 | 5.386 |
| 7 | 54 | SOLVED | 7.395 | cold cache (0/2) | 7.960 | 1614.156 | 1338.000 | 0 | 0.000 |
| 8 | 59 | SOLVED | 10.720 | cold cache (0/3) | 11.570 | 1618.395 | 1368.000 | 0 | 0.000 |
| 9 | 59 | SOLVED | 10.777 | cold cache (0/3) | 11.660 | 1621.594 | 1560.000 | 0 | 0.000 |
| 10 | 69 | SOLVED | 9.361 | cold cache (0/2) | 10.140 | 1624.066 | 1594.000 | 0 | 0.000 |
| 11 | 69 | SOLVED | 11.922 | mixed cache (2/4) | 12.880 | 1627.562 | 1422.000 | 1 | 5.681 |
| 12 | 95 | SOLVED | 7.390 | cold cache (0/2) | 7.910 | 1630.074 | 1422.000 | 0 | 0.000 |
| 13 | 95 | SOLVED | 5.912 | warm cache (2/2) | 6.350 | 1630.285 | 1300.000 | 0 | 0.000 |
| 14 | 118 | SOLVED | 6.794 | cold cache (0/2) | 7.290 | 1632.992 | 1472.000 | 0 | 0.000 |
| 15 | 118 | SOLVED | 5.776 | warm cache (2/2) | 6.220 | 1633.215 | 1258.000 | 0 | 0.000 |
| 16 | 119 | SOLVED | 9.772 | cold cache (0/3) | 10.590 | 1637.023 | 1494.000 | 0 | 0.000 |
| 17 | 119 | SOLVED | 9.693 | cold cache (0/3) | 10.480 | 1639.148 | 1622.000 | 0 | 0.000 |
| 18 | 133 | SOLVED | 9.382 | cold cache (0/2) | 10.080 | 1639.477 | 1642.000 | 0 | 0.000 |
| 19 | 133 | SOLVED | 7.998 | warm cache (2/2) | 8.580 | 1639.699 | 1410.000 | 0 | 0.000 |

## Separate fresh-worker comparison

Same fresh Python parent/worker and 20 ms planning-clock procedure as the historical benchmark. Runs occur on different dates, so machine load may differ. Historical develop paths failed recorded TCP acceleration checks; resource and smoothness numbers do not imply validity.

| Task | Old cuRobo planning s | New planning s | Old motion s | New motion s | New status | Cache hits/lookups |
|---|---:|---:|---:|---:|---|---|
| 3 | 13.125 | 7.612 | 10.125 | 6.308 | SOLVED | cold cache (0/2) |
| 4 | 11.922 | 9.012 | 10.125 | 7.578 | SOLVED | cold cache (0/3) |
| 21 | 11.320 | 9.011 | 6.750 | 7.015 | SOLVED | cold cache (0/2) |
| 54 | 11.725 | 9.716 | 8.438 | 11.459 | SOLVED | cold cache (0/2) |
| 59 | 16.515 | 12.928 | 11.813 | 13.663 | SOLVED | cold cache (0/3) |
| 69 | 13.729 | 11.826 | 8.438 | 9.166 | SOLVED | cold cache (0/2) |
| 95 | 11.619 | 9.714 | 6.750 | 5.824 | SOLVED | cold cache (0/2) |
| 118 | 11.922 | 9.111 | 6.750 | 4.995 | SOLVED | cold cache (0/2) |
| 119 | 14.511 | 12.022 | 10.125 | 5.406 | SOLVED | cold cache (0/3) |
| 133 | 14.412 | 11.625 | 6.750 | 4.817 | SOLVED | cold cache (0/2) |

### Paired fresh-process medians

| Metric | Paired tasks | DEV fresh | Old GPU fresh | New GPU fresh |
|---|---:|---:|---:|---:|
| Planning latency s | 10 | 9.012 | 12.524 | 9.715 |
| Whole-process CPU-s (GNU time) | 10 | 9.150 | 12.225 | 9.985 |
| Peak summed RSS MiB (sampled) | 10 | 319.693 | 1580.477 | 1573.314 |
| Peak GPU compute MiB (sampled) | 10 | 0.000 | 376.000 | 968.000 |
| Motion duration s | 10 | 1.919 | 8.438 | 6.662 |
| Joint mileage rad | 10 | 5.616 | 5.357 | 5.002 |
| RMS jerk rad/s³ (excludes jumps) | 10 | 41.065 | 1.482 | 4.975 |
| Normalized jerk (excludes jumps) | 10 | 9909.695 | 58574.346 | 330575.152 |
| Maximum acceleration jump rad/s² | 10 | 4.523 | 0.000 | 0.000 |

## Second-observation warm summary

Second observation per fixed task ID: 10 / 10 complete consecutive pairs. Statuses: {'SOLVED': 10}. Retained child PID in 10 / 10 pairs with PID evidence. Actual cache labels: {'warm cache': 5, 'cold cache': 4, 'mixed cache': 1}. Medians select the second iteration even if it failed; unmatched or nonconsecutive pairs are excluded. Process reuse and actual cache hits are separate measurements. CPU is sampled, not GNU time; RSS can double-count shared pages and sampled peaks may be missed.

| Metric | Observations | Median |
|---|---:|---:|
| Request latency s | 10 | 7.048 |
| CPU-s sampled | 10 | 7.590 |
| Peak summed RSS MiB sampled | 10 | 1624.578 |
| Peak GPU compute MiB sampled | 10 | 1374.000 |

## Recorded planner stage costs

Per-request recorded stage totals include all saved planner/part attempts and timed refinement failures. Construction includes cache lookup; native planning includes its retries. Qualification timing covers its retiming retry phase. Core preacceptance FCL is included as its own stage and sums saved retry attempts; the separate worker-final FCL collision check, queueing, imports and IPC are excluded. Some recovery records omit earlier stage timings: partial-coverage totals are lower bounds, not complete costs; missing stages may also have been skipped. These stage medians must not be added to infer total latency.

| Stage | Median recorded s | Requests with timing | Partial attempt coverage |
|---|---:|---:|---:|
| Construction / cache lookup | 0.239 | 135 | 3 |
| Native planning | 3.142 | 135 | 3 |
| Cartesian refinement | 0.571 | 135 | 0 |
| Timing prepass | 0.397 | 135 | 13 |
| Qualification / retiming retry phase | 1.144 | 135 | 13 |
| Core preacceptance FCL collision check | 0.792 | 135 | 4 |
