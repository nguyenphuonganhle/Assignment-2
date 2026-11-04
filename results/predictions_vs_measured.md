# Predictions vs measured (generated)

Predictions come from PREDICTIONS.md.

| ID | Prediction | Measured | Verdict |
|---|---|---|---|
| P1 | random graphs (largest): EK faster, FF more augmentations, FF paths >= 2x longer | random_sparse: time FF/EK 13.5, augmentations 150 vs 12, avg path 1275.8 vs 7.2; random_dense: time FF/EK 111.7, augmentations 1280 vs 64, avg path 68.7 vs 2.9 | **SUPPORTED** |
| P2 | density sweep: FF path >= 0.3n and EK path <= 5 for p >= 0.12; FF/EK time ratio larger at densest p | FF avg path by p: 0.03: 8, 0.06: 30, 0.12: 43, 0.25: 40, 0.5: 41, 0.9: 37; EK: 5.8, 4.5, 4.0, 3.1, 2.7, 2.6; time ratio 1.5 -> 48.7 | **SUPPORTED** |
| P3 | unit-capacity matching (largest k): augmentations within 10%, FF faster | augmentations 783 vs 783 (gap 0.0%); time FF/EK 0.39 | **SUPPORTED** |
| P4 | capacity growth: FF augmentations grow >= 10x from C=1 to C=10000, EK <= 3x | FF x1480.7 (3 -> 4442); EK x3.0 (3 -> 9) | **SUPPORTED** |
| P5 | crossover: FF faster at C=1, EK faster at C=1000, crossover C* between 5 and 100 | time ratio FF/EK by C: 1: 0.54, 2: 0.52, 5: 0.73, 10: 1.12, 20: 1.61, 50: 2.30, 100: 2.84, 1000: 3.75; first C where EK is faster: 10 | **SUPPORTED** |
| P6 | sign of (FF scans - EK scans) matches sign of (FF time - EK time) on >= 80% of instances | 154 of 170 instances agree (91%) | **SUPPORTED** |
