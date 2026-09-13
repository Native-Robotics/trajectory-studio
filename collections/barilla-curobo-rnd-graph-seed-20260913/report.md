# cuRobo improvement replay

135 / 135 processed · 135 recorded passes · 0 failed · 0 not measured

Private graph-choice RNG; original constraints and FCL remain enforced. Task 0 repeats exactly in the pilot. Some cached-planner variability remains; general numerical determinism is not claimed. Full replay is coverage/quality evidence, not an isolated speed comparison.

Measured requests: 135; summed request latency 873.893 s; median 5.115 s. The sum excludes time between requests and is not total process wall time.

Snapshot: 2026-09-13T04:15:43.580568+00:00

Original replay: 46 / 135 historical passes under earlier checks, not strict original-constraint parity. Coverage above reflects only this measured replay.

Manifest records strict-original-v1: recorded passes use the strict original-constraint validator. This identifies saved evidence; it is not a new re-audit.

Historical original GPU and intermediate results were evaluated with earlier, looser wrist-down, endpoint and linear checks, not strict original-constraint parity. Their historical passes are retained as recorded outcomes, not retroactively certified against the corrected strict validator. Historical develop also failed recorded TCP acceleration checks; performance comparisons do not establish constraint parity.

Old timings use fresh Planner processes; new timings use sequential requests in one persistent Planner. Exact motion metrics and recorded validation are shown separately; latency differences include both planner changes and process reuse.

Previous develop and cuRobo measurements used separate fresh production Planner processes. New replay uses one persistent Planner with sequential requests and one worker. Old planning_s excludes imports and Planner initialization; new elapsed_s is measured request latency including polling and any child startup. These are different execution methods, not a controlled isolated algorithm speedup. Cache labels count actual recorded lookup hits, not request order. One observation per replay task; optional warm repeats are separate. SOLVED is the production result; constraints_valid is recorded independent qualification. TCP, dynamics and collision validation are sampled, not continuous-time proofs. Motion metrics are exact on saved cubic coefficients. Jerk integrals omit impulses at acceleration jumps, which are reported separately. No overall quality score is assigned. Resource sampling can miss peaks and summed RSS can double-count shared pages.

Fixed ten-task comparison: 10 / 10 measured. Medians use only this matched subset.

| Metric | develop fresh | old cuRobo fresh | improved persistent |
|---|---:|---:|---:|
| Latency s (different methods) | 9.012 | 12.524 | 3.526 |
| Motion duration s | 1.919 | 8.438 | 5.573 |
| Joint mileage rad | 5.616 | 5.357 | 5.013 |
| RMS jerk rad/s³ (excludes jumps) | 41.065 | 1.482 | 4.537 |
| Normalized jerk (excludes jumps) | 9909.695 | 58574.346 | 64086.849 |
| Maximum acceleration jump rad/s² | 4.523 | 0.000 | 0.000 |

| Task | Status | Request latency s | Motion s | Cache | Error | Studio |
|---|---|---:|---:|---|---|---|
| 0 | SOLVED | 11.537 | 7.119 | partial / unknown (0/4); 1 recoveries / 6.230 s |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#8a8ddaf4df6b649825207c045607280d71738a46f2bdc784808b276156181a29-curobo) |
| 1 | SOLVED | 5.887 | 8.192 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#5ec0425abcfd1ddbba907989465fdeea37351a3c928d1fbc0f0688efdb2dc6e7-curobo) |
| 2 | SOLVED | 7.003 | 7.523 | mixed cache (1/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#236e7d6c7f2343a27196c7806774659f42f95dbe607e08c39d807c06659060f3-curobo) |
| 3 | SOLVED | 3.311 | 5.344 | cold cache (0/2) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#d11f7e3674a194e159d178dfd86113da494021a409ab52062aca88a210751222-curobo) |
| 4 | SOLVED | 4.191 | 6.170 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#1fe518293663051f682bc433aef49c035880ad988e21871c1aed491a99642815-curobo) |
| 5 | SOLVED | 7.190 | 7.621 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#d34f5d1a676ed74000aeb376421dcab2c4210a7746df4028cac938720c422a19-curobo) |
| 6 | SOLVED | 3.084 | 5.476 | cold cache (0/2) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#14dad0b1314d843887dfb27099e2ef3b4551d27e37832ddba80830b607eed6f7-curobo) |
| 7 | SOLVED | 6.603 | 7.329 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#874c2ff6ed99371f56f5534b0e5647f78ecd31e1f64bfb060ac54a5272ed5767-curobo) |
| 8 | SOLVED | 4.897 | 7.357 | mixed cache (1/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#157778044707b6b38066ec220a68d9041ce05269962daec3475b8396422ab85a-curobo) |
| 9 | SOLVED | 5.657 | 7.419 | mixed cache (1/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#990b4a17e4bbe938fc45f65f5c5906b48b80d60a977651ab4cca93918db60460-curobo) |
| 10 | SOLVED | 4.234 | 6.074 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#4669b0add291cb1840e127a15e95ac71c69d31ae66310e3febbf98ef128e2a05-curobo) |
| 11 | SOLVED | 5.670 | 7.843 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#f7fe241f51ceed34d82d9905d0a026a00956115d82779a7777ca72f95d870e95-curobo) |
| 12 | SOLVED | 3.410 | 5.341 | cold cache (0/2) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#67fd7e6ecb9b1d55bbc1a6f5884b05b950b490367c6e46425db4fcb5da887f43-curobo) |
| 13 | SOLVED | 4.361 | 6.278 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#65ae9262939ee84049590871f8f39c96dc6e8dfa537644b01aeb4f5f9a7989bf-curobo) |
| 14 | SOLVED | 6.279 | 7.248 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#783a0b36e747e15823b50bb53e6ed467e361112a23fcb9e4a898883b6785c838-curobo) |
| 15 | SOLVED | 3.439 | 5.602 | cold cache (0/2) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#c82ec835fe944eff30aab8917fa1906c8ec0b2b2169bf51f4a4b036eb089e240-curobo) |
| 16 | SOLVED | 3.870 | 6.108 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#ff51eac0fb305749a0b576535bfcc5646e4198417271fb7acc213d73d7790f7b-curobo) |
| 17 | SOLVED | 6.092 | 7.908 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#e2e58e342e85c79a2dd921678efc9adbc8318d0750c58d7c1fdad071cb3ffc06-curobo) |
| 18 | SOLVED | 3.304 | 5.323 | cold cache (0/2) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#1327e2bffb12a417a7bf56f44d3865dc9518fd7535c9d700682d477c6f789d4b-curobo) |
| 19 | SOLVED | 4.474 | 6.536 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#cdfe50e6501abd720ddab2d018f396d281c935a71283ff7ee0b2958ac2128473-curobo) |
| 20 | SOLVED | 13.875 | 11.954 | cold cache (0/6); 1 recoveries / 6.968 s |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#b1b1ac1cca245324e658d7a0088299f8cc568d71cbb75469e533c4c3bd002857-curobo) |
| 21 | SOLVED | 3.484 | 5.803 | cold cache (0/2) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#4534dd005e414e88e712d5e26835809ae2cb800719088e89652d6c51665b090b-curobo) |
| 22 | SOLVED | 4.519 | 8.017 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#0c734fba9f3ac973cef401117d12dba0fb92e1dfd0141e1f8950b84834a5b583-curobo) |
| 23 | SOLVED | 7.969 | 10.615 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#4420c1ba15a9f9f4647aee9b87f9cea70aa69c39c555fde596e9e879b8949b6e-curobo) |
| 24 | SOLVED | 3.683 | 9.079 | cold cache (0/2) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#7733d0fe0777e8be858249b95aea32045ca4c9027dd26a1d6d40d633de3e73b2-curobo) |
| 25 | SOLVED | 5.222 | 10.580 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#5e7e6dc69fed087aa0561b802e4856b091b494602708f6bc5a86ad9667b78018-curobo) |
| 26 | SOLVED | 18.884 | 10.843 | cold cache (0/4) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#30530dc6123a455aee737bac0143d5fbdcd3af27041b0faf47fddb64f9f67c74-curobo) |
| 27 | SOLVED | 3.590 | 6.695 | cold cache (0/2) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#09ace9b8946c23d6a961a3b2cf747c6b961b6ed5a3a1dec045300f2843c0b665-curobo) |
| 28 | SOLVED | 4.686 | 8.537 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#e704290c065a7a6f906d1e1712005222e139a9d452c5fe6cb1089d6443636c6c-curobo) |
| 29 | SOLVED | 14.586 | 10.765 | cold cache (0/6); 1 recoveries / 8.145 s |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#aa329637486d5889d002b13a941467b9323ef35664410d5e7884091b3447de8c-curobo) |
| 30 | SOLVED | 3.462 | 6.854 | cold cache (0/2) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#637b8daa125b4be9dd797ab6a17346b58f42fcddb325a3348d90ce6c8ab954e7-curobo) |
| 31 | SOLVED | 5.610 | 8.303 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#8985758efd9744de84c67f0ac421aa8d8c511a6a65e420311f880b35354a6368-curobo) |
| 32 | SOLVED | 7.884 | 11.748 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#4dd61fe30a89a5ed02fd537e7dcb2dd66fc4463ebe132868fbc4f727a1e382c4-curobo) |
| 33 | SOLVED | 4.405 | 7.520 | cold cache (0/2) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#c3c0bcb6e33ecfb2112015a8d37c42dce013894f0690e884ca64936b48927d24-curobo) |
| 34 | SOLVED | 5.277 | 6.788 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#8141b5e91d8cb3c68e51899df31a9c9d80809e7ed2dd1b89bc54b619b1f587e7-curobo) |
| 35 | SOLVED | 41.024 | 13.531 | cold cache (0/7); 1 recoveries / 8.552 s |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#d069b37b66b1d41c81251cfea60d3b252cee286101bf5df09953410f12ab6be1-curobo) |
| 36 | SOLVED | 4.561 | 7.863 | cold cache (0/2) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#763c16198f2fb926e8935cb1ce0a07d5b7e5336a3f019b72358302b0700e31f7-curobo) |
| 37 | SOLVED | 4.905 | 8.629 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#24b002cf8d129dd361c832e6778abace2907e3117f9b4e32cf43fc536599b1d0-curobo) |
| 38 | SOLVED | 6.084 | 6.698 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#9ad11ec668c886435ff5dd801c01b54942626ab51dd4ab144d28e47c660208e7-curobo) |
| 39 | SOLVED | 5.284 | 6.933 | mixed cache (1/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#33e4a6207e3dab0b3fc8109aae69ee9bdddd9bce057f63f9dc7c27fb6ef5fa0e-curobo) |
| 40 | SOLVED | 6.798 | 9.962 | mixed cache (1/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#0e7ffe1a4f7b5ff1b5c177f7922a9771761ae07a91671f301a4e4d4823c54aea-curobo) |
| 41 | SOLVED | 3.684 | 5.542 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#cbe58dce5dfe7225b68f50dd900f0d153dc97de450baf96eb68534e9b503a76e-curobo) |
| 42 | SOLVED | 5.764 | 7.031 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#e7cedb57a03526cdc098d5be05f441367847a971c057f0cf37576c6415b961d1-curobo) |
| 43 | SOLVED | 3.183 | 4.741 | cold cache (0/2) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#8f4a1848561c6b0481d0aabfd7a1f571c5c22973d2215c770cb59ea8754c7e94-curobo) |
| 44 | SOLVED | 3.822 | 5.684 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#b3e3aa9d895fdfda3efdefd2ae590d75c2ececcf14c1e186c1d88a847eae5352-curobo) |
| 45 | SOLVED | 5.449 | 6.961 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#da8fd8fb136d8413134c46b398ef9ca69ab9075d6d46c84390c641c0c72951af-curobo) |
| 46 | SOLVED | 2.802 | 4.864 | cold cache (0/2) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#8ab37c289d3653f6f35f1555b43212e7de6a53004f746ad426ed6c7a365ed18f-curobo) |
| 47 | SOLVED | 3.896 | 5.815 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#4d081814e8fc880ebdce04406d4e0196f0241b0d95f738533a44afd0e5217f5f-curobo) |
| 48 | SOLVED | 5.593 | 7.462 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#e240fbe29a5ce182ccb8795707b119ea851f496f35bf07ab43a65644ead6d7e7-curobo) |
| 49 | SOLVED | 3.184 | 5.013 | cold cache (0/2) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#e5dd98e0d6bb34a919f64a2d32db4c71b928c217f9055d563b302dd6d51ad328-curobo) |
| 50 | SOLVED | 3.852 | 5.868 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#1b35f6b527105f98c7e206def5bec2869b3e84fb5fa8ae765f71ce8c2d88365a-curobo) |
| 51 | SOLVED | 13.480 | 11.868 | cold cache (0/6); 1 recoveries / 5.575 s |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#cca725669f41282089b22f19a06dcd7048473b791c898f66ae55c9fb2ef90752-curobo) |
| 52 | SOLVED | 3.298 | 5.013 | cold cache (0/2) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#112d53ea58de51f07ed99c0721ee21b9b8475bb0a7123a7f9926f8d4d6c61e0b-curobo) |
| 53 | SOLVED | 5.705 | 7.115 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#982c6c56f60923b151ff2a7c2d07e0a811815ec4ef46470e921f62a5cfc4c0e8-curobo) |
| 54 | SOLVED | 3.568 | 6.821 | cold cache (0/2) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#fe9d57153f6c5b7fd2f6e245232fbf45e7ed69464f192a8375112aee4c5c94df-curobo) |
| 55 | SOLVED | 6.369 | 7.330 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#888c893a10c23064efa0fabd5e4cc73ed77fa082e38f4bdb17a3456b5616d852-curobo) |
| 56 | SOLVED | 3.305 | 4.905 | cold cache (0/2) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#227de82358a9d408c4fc0b353a4179d8a7bc7ea7c3d2397bc278456ffa7b0856-curobo) |
| 57 | SOLVED | 16.770 | 13.703 | cold cache (0/6); 1 recoveries / 8.675 s |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#31c6b4c06c35d130d20be9c68f41fa77efb1847edfa7324187a25b50d04480e2-curobo) |
| 58 | SOLVED | 3.212 | 4.997 | cold cache (0/2) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#d6936b0636d7dcebbcf939eb6c69a902513bb3f35c34c2b3274c65b189483e7c-curobo) |
| 59 | SOLVED | 4.765 | 7.709 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#3b7198671eafb52f81108f96154f8560cf6498efbf86e16a87078e1d77de5f22-curobo) |
| 60 | SOLVED | 19.179 | 10.718 | cold cache (0/9); 2 recoveries / 12.799 s |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#9822f921fa845c3bfd710ad59557848746e0a6dfbab3f68a86c1c57a34856874-curobo) |
| 61 | SOLVED | 3.793 | 7.661 | cold cache (0/2) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#804dee9f7056c1d029d0b79fbe6d907db91799b2305c88a7dd3c7b4b0a06d610-curobo) |
| 62 | SOLVED | 17.254 | 12.760 | cold cache (0/6); 1 recoveries / 8.955 s |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#431c3a24cce6527a75f725f7b271417a0aa92f31ec83b8a652ea4e540702771e-curobo) |
| 63 | SOLVED | 3.514 | 6.000 | cold cache (0/2) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#dd9aacd13c2ade6745669747cbc76894ee5d2a9d9d9b4ee06d2efbb8c5ccabd4-curobo) |
| 64 | SOLVED | 4.281 | 6.449 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#66258ebd02eb8021eb5f8971fead92e9836612b16d5f71d3ad3adecd4696aeae-curobo) |
| 65 | SOLVED | 10.363 | 13.517 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#b7e09cccb0e65e05310addb02ff898db0211cc43157f6441779a744e7a0fb18b-curobo) |
| 66 | SOLVED | 3.413 | 5.803 | cold cache (0/2) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#e96ea26bd2338ec705f4db36f41d1bd8b30ca40b8fdc542ab7087195afdf8793-curobo) |
| 67 | SOLVED | 5.238 | 6.849 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#1b93f5804a233180e209a9010892362fa3b2b92ade5cba3b65f5eb6a549bd377-curobo) |
| 68 | SOLVED | 16.822 | 8.548 | cold cache (0/6); 1 recoveries / 7.779 s |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#742b222cac1e5779c87c9bd6a4f9234ed0a02d6b12f533c21e4def9230b18743-curobo) |
| 69 | SOLVED | 4.065 | 6.144 | cold cache (0/2) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#345d876fd0fc95ac0151fef0b9c6c7c74798e233d1d35a9dbeaac76c8aaed43a-curobo) |
| 70 | SOLVED | 4.664 | 6.005 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#2a2d5e19cd08f574edf0847e5d4c397f30429bd3ea6db9b0af7298726524d6ae-curobo) |
| 71 | SOLVED | 16.782 | 12.045 | cold cache (0/6); 1 recoveries / 7.585 s |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#6e59033d1635a3b2f095bc3263efb3ec16914e0f90e5e4f7d6a930480bf69669-curobo) |
| 72 | SOLVED | 3.412 | 5.421 | cold cache (0/2) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#5e499e311cb80fb23e8b193d31110e52e896705d19074e81108d151dabd27627-curobo) |
| 73 | SOLVED | 5.444 | 7.930 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#2ec4c9744327816ea59c42d226461c14d56405b4e55e09b6f7d39e45e32e8743-curobo) |
| 74 | SOLVED | 26.995 | 7.965 | cold cache (0/7); 1 recoveries / 7.429 s |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#f445e97f46fb9f916c2a6eb460df8cdacf57c383fe6b01f0f051557d47f7769b-curobo) |
| 75 | SOLVED | 4.074 | 7.494 | cold cache (0/2) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#71837a5cb15736f75cdb9a5bd2374ba46d1b8216c673734312ef5990baf123f1-curobo) |
| 76 | SOLVED | 5.601 | 7.309 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#a26127aac6e378746ea0c47fede339653070bb00409548511632d36b122a8a1c-curobo) |
| 77 | SOLVED | 6.481 | 10.037 | mixed cache (1/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#6a5f8ea3118c31d3f60930a7df7f0a6f03d38eff661bd1d13f4b76aca4e7a406-curobo) |
| 78 | SOLVED | 5.466 | 8.146 | mixed cache (1/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#869f070423e3d0c736ba34d7938a41a3feaf98227446fdb769369c8052d0e9e2-curobo) |
| 79 | SOLVED | 5.387 | 7.036 | mixed cache (1/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#7b1a482499831cda3e71671cf062709e725e411fb942c312434d6f05cac139ef-curobo) |
| 80 | SOLVED | 6.894 | 10.514 | mixed cache (1/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#958b253c80f575b409bd9a458acc6a04c6c76150efcb43904629d7adda7ab6d5-curobo) |
| 81 | SOLVED | 5.781 | 6.787 | mixed cache (1/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#01bda9f1433078562e2b0cb88ad5b4b737423629eff3f8591e2e8706920e46cf-curobo) |
| 82 | SOLVED | 6.568 | 9.841 | mixed cache (1/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#3d33ebd8a3b7f79918b1372c6daf6331c357edf50d8cef40a0550eadf11ecfe9-curobo) |
| 83 | SOLVED | 5.164 | 6.636 | mixed cache (1/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#28086cf6c71a1f3dfc8a729bed8bbd960203ef7512ab7f0e12eec65ca8c4a101-curobo) |
| 84 | SOLVED | 13.811 | 17.473 | mixed cache (1/6); 1 recoveries / 7.031 s |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#87392729615302071d9a74394a89b77557d3c0b0dd0be9cf5008072c501908f6-curobo) |
| 85 | SOLVED | 5.281 | 6.134 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#96f708147d9d95c483b26113d4a9d87211f67c14a3bcfc906c688efc3653c3ce-curobo) |
| 86 | SOLVED | 5.983 | 7.386 | mixed cache (1/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#bc9d3ba210e336b7b6661afe1715d9879379c0ab95c97c7d210f87c15b3d79a1-curobo) |
| 87 | SOLVED | 3.733 | 5.667 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#db4b62f1e13011124c31100513dd79570a9612c6e783634cd58dc25fa9721c65-curobo) |
| 88 | SOLVED | 6.595 | 6.375 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#21ebe498a10bb43332e4188d2b0de486a0aae0ef3e8482acde8b8efcbae8d123-curobo) |
| 89 | SOLVED | 2.994 | 4.752 | cold cache (0/2) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#c5a4aa5303d5f84eff8f62f04e0deabdb2ccc4cd7ee1cf7a5469669c91f8d47d-curobo) |
| 90 | SOLVED | 4.136 | 5.418 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#40fe3beaa86a5f79013c8edb66f0262d1ce6bd41c438f0901df481964e8999b3-curobo) |
| 91 | SOLVED | 6.687 | 6.784 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#9d630805839dec2bece9888927e7a9445f3269813c426929ccd8e7459512e8a1-curobo) |
| 92 | SOLVED | 3.194 | 4.516 | cold cache (0/2) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#b49321899a1b75128020909ec14d74ec2568acaafbed07d999094e99dbf6e1ec-curobo) |
| 93 | SOLVED | 4.697 | 5.586 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#f8b38d7e79e2041a5125528c4d185971d6d2addca8dbe7161273b72313694a52-curobo) |
| 94 | SOLVED | 7.256 | 6.048 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#7ef9efcad87480f35d34fcdc0ce90aea09149214e6e81f95baaab1541851d716-curobo) |
| 95 | SOLVED | 3.298 | 4.871 | cold cache (0/2) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#a85c9e41ad745c26160fe19eddca1667a4adad081f37815ae0188254f8a8154f-curobo) |
| 96 | SOLVED | 4.421 | 4.995 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#456c57de38c1cc4d36022e8d157e7a81ca4c2173e8d0ae99351a1e31b60ba13e-curobo) |
| 97 | SOLVED | 8.380 | 6.459 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#b4de76070055fbdc047e75e28a625b59dd4d74d5d97410fde4c9bb1cce87601e-curobo) |
| 98 | SOLVED | 3.404 | 4.184 | cold cache (0/2) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#6a437fb05c6357c93e10def63301fc07b8fb83885217794b825a843bb0e76e45-curobo) |
| 99 | SOLVED | 4.289 | 5.500 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#dcbcfaebb091b3d7bdffcedc7f396fc50637d574f2f53b23c820175e9904bb79-curobo) |
| 100 | SOLVED | 12.134 | 6.814 | cold cache (0/6); 1 recoveries / 5.750 s |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#05f86a85796b4f5b28b612a3d0d87b73e2e972a470c1dfc2ba503b8561cfcfb9-curobo) |
| 101 | SOLVED | 3.516 | 4.594 | cold cache (0/2) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#5001f06ef9cb8af38b6e8cb6c75c44537203883ba12e69613260b8ff5eb58a0b-curobo) |
| 102 | SOLVED | 6.143 | 7.181 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#83187667e10a3759711f81492f1e4cb77b6d8867970e0207d53cd72d7b73b32a-curobo) |
| 103 | SOLVED | 6.009 | 6.842 | mixed cache (1/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#f1d6937ee124a9cc2fc3733dc7934568b463bdf0d2bca0c790029fc1cf2dcd92-curobo) |
| 104 | SOLVED | 5.956 | 10.030 | mixed cache (1/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#4cefdaeac1aadee6f95cdb7597284083e9835942447325445efea0185556dea2-curobo) |
| 105 | SOLVED | 5.760 | 6.930 | mixed cache (1/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#c6665a00526d4df2164127857e4add75bdec6bd6b71ef802dce6c19df2b70d9e-curobo) |
| 106 | SOLVED | 6.366 | 7.825 | mixed cache (1/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#3d1d09a173c1f703cbdca8f1496694443b355ef36faef7947eeed082411fc3f9-curobo) |
| 107 | SOLVED | 18.677 | 9.943 | mixed cache (1/4) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#ca5b5bb5875c40b466aec21cb14a23657496bb0a935f240a822dd5220e9032e3-curobo) |
| 108 | SOLVED | 5.406 | 6.148 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#d535f91b6132185bce5be948e9c7dc76c214a7cb86e36f9d7eed65fd6a052af3-curobo) |
| 109 | SOLVED | 5.787 | 10.391 | mixed cache (1/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#1b303e154306ba795ffa12b17b1e33b491ddccdc3bab93bd1c6970cb9dec4b40-curobo) |
| 110 | SOLVED | 4.443 | 6.472 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#e470ca2078a3a5d3f316378826cbeb090ede1a237da9fade3d7e1a045c072f7a-curobo) |
| 111 | SOLVED | 6.258 | 7.107 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#0912a6a491d9518d6c6c61229155c9f3a5cd6dea50074c4e320502cc4a0a2c13-curobo) |
| 112 | SOLVED | 3.019 | 5.655 | cold cache (0/2) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#cce28b55970f688433ae3270f54f9e0036432a0cdc6b20e64bc4bdecf001eb42-curobo) |
| 113 | SOLVED | 4.468 | 6.108 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#238f10b4362ebbb9db94e56412c673f51bc404d976e263d886e30f2577811432-curobo) |
| 114 | SOLVED | 5.165 | 5.871 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#ed9a42ca2340e12556739855c8703760405b075336604457a3e83174e23d9a52-curobo) |
| 115 | SOLVED | 2.975 | 5.125 | cold cache (0/2) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#ad3d5831de3a7b166ebeba9722dcdb98326608b562e9782a3b55f9fc734b0274-curobo) |
| 116 | SOLVED | 3.733 | 4.909 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#ddef37c608ea11aa2258d1fe80b7ca7840b359a894d4b367bfb2fdfabcf7f4f8-curobo) |
| 117 | SOLVED | 5.115 | 5.598 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#7fe4d262bbe946f86d8647f445d7532834cbb2b01e39d61dfc51050b07b9f91c-curobo) |
| 118 | SOLVED | 3.140 | 4.190 | cold cache (0/2) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#2002018bb663a96dd8b345964ad7cd86d97dac28e575a7cc3253674e0d0bab63-curobo) |
| 119 | SOLVED | 4.072 | 4.796 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#91d725b4fecb997ee58578a303f680b527cffc7bcb9411b22d9a74298a3b6c3b-curobo) |
| 120 | SOLVED | 7.889 | 6.890 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#1f84dfac252acd51f09607023f7f39d4d3c835dadc88e06cd9df2b4903cbd974-curobo) |
| 121 | SOLVED | 3.365 | 3.860 | cold cache (0/2) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#44f8fe25625bbebe24cf4181a004e924ab3a4a6a5ed6d630ab9f66b6218e78b7-curobo) |
| 122 | SOLVED | 4.683 | 5.455 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#ae52343668153759404058ccd22e337e87743b963fba0f00d5e408decb9798df-curobo) |
| 123 | SOLVED | 6.959 | 6.759 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#5cafdab26d209f9d7becea720347933dce38179df82b759cf8af5ab2fcab693e-curobo) |
| 124 | SOLVED | 3.570 | 4.777 | cold cache (0/2) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#780c535cd4277c9dea97ed39f857d97f5d75a1951ad924bf14109cd8621b9a23-curobo) |
| 125 | SOLVED | 4.288 | 5.130 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#00db71c591a1cdbe9b19ecb437c6f3ad850e04fd35888f16474a7a15f73a7294-curobo) |
| 126 | SOLVED | 14.973 | 8.726 | cold cache (0/6); 1 recoveries / 7.963 s |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#5184a18819f4000d819bf18c25df9c6dc2c824f2fdf78256f539f57f29b64d6e-curobo) |
| 127 | SOLVED | 3.350 | 4.461 | cold cache (0/2) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#499c03a3f09689faf199cae6f47938020231026e4a317d093135cc22e06095d4-curobo) |
| 128 | SOLVED | 4.346 | 5.761 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#7271cc305a51225178b98efa70c2bcd8667175ae778b673099c6acab72084326-curobo) |
| 129 | SOLVED | 6.374 | 6.269 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#a7a1b9e090dd9a95aeafcea70476149acbfb714fdf217964c85833775c60f04b-curobo) |
| 130 | SOLVED | 3.659 | 4.754 | cold cache (0/2) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#04de589e9bf012919e80ad690762d2ef652697b36f8cfece0b58e3c1570339c8-curobo) |
| 131 | SOLVED | 4.180 | 5.088 | cold cache (0/3) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#fe639e5939c63f39a020645344669bf4b4b74716f3243b4b90dd78d8f8dcc09d-curobo) |
| 132 | SOLVED | 15.502 | 6.513 | cold cache (0/6); 1 recoveries / 7.276 s |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#b8566bd8bebdd6dd62770b473a4135d9929b4afbc0301eff08c7b223081f8c7d-curobo) |
| 133 | SOLVED | 3.442 | 4.136 | cold cache (0/2) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#67745ceb8883e3de2624686a280a5dcfc89d8f3ff7586a9634d8d1dca9307d9b-curobo) |
| 134 | SOLVED | 2.392 | 1.417 | cold cache (0/2) |  | [Inspect](http://localhost:8001/collections/barilla-curobo-rnd-graph-seed-20260913/index.html#650d86a604f523befc71a7c1d1c1a7eb438b6485b8d544b601405f3f69004418-curobo) |

## Recorded planner stage costs

Per-request recorded stage totals include all saved planner/part attempts and timed refinement failures. Construction includes cache lookup; native planning includes its retries. Qualification timing covers its retiming retry phase. Core preacceptance FCL is included as its own stage and sums saved retry attempts; the separate worker-final FCL collision check, queueing, imports and IPC are excluded. Some recovery records omit earlier stage timings: partial-coverage totals are lower bounds, not complete costs; missing stages may also have been skipped. These stage medians must not be added to infer total latency.

| Stage | Median recorded s | Requests with timing | Partial attempt coverage |
|---|---:|---:|---:|
| Construction / cache lookup | 0.236 | 135 | 1 |
| Native planning | 2.816 | 135 | 1 |
| Cartesian refinement | 0.112 | 135 | 0 |
| Timing prepass | 0.013 | 135 | 15 |
| Qualification / retiming retry phase | 0.271 | 135 | 15 |
| Core preacceptance FCL collision check | 0.626 | 135 | 1 |
